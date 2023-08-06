import os
import logging
from uuid import UUID
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    level=os.getenv("LQS_LOG_LEVEL") or logging.INFO,
    format="%(asctime)s  (%(levelname)s - %(name)s): %(message)s",
)
logger = logging.getLogger(__name__)


class S3Resource(str, Enum):
    extraction = "extraction"
    ingestion = "ingestion"
    log = "log"
    record = "record"
    topic = "topic"


class Utils:
    def __init__(self, getter, s3, gen, config):
        self._getter = getter
        self._s3 = s3
        self._gen = gen
        self._config = config
        self._cached_ingestions = {}
        self._cached_message_types = {}

        if self._config.get("verbose"):
            logger.setLevel(logging.DEBUG)

    def upload_part(
        self,
        resource: S3Resource,
        resource_id: UUID,
        file_path: str,
        upload_id: str,
        part_number: int,
        key: str = None,
        part_size: int = 5 * 1024 * 1024,
    ):
        file = open(file_path, "rb")
        file.seek((part_number - 1) * part_size)
        part_data = file.read(part_size)

        logger.debug(f"Uploading part {part_number} ({len(part_data)} bytes)")

        if key is None:
            key = file_path.split("/")[-1]

        r_headers, r_params, r_body = self._s3.upload_part(
            resource=resource,
            resource_id=resource_id,
            key=key,
            part_number=part_number,
            upload_id=upload_id,
            body=part_data,
        )
        e_tag = r_headers["ETag"]
        return {"PartNumber": part_number, "ETag": e_tag}

    def upload(
        self,
        resource: S3Resource,
        resource_id: UUID,
        file_path: str,
        key: str = None,
        part_size: int = 5 * 1024 * 1024,
        max_workers: int = 8,
        exist_ok: bool = False,
    ):
        if key is None:
            key = file_path.split("/")[-1]

        if not exist_ok:
            r_headers, r_params, r_body = self._s3.head_object(
                resource=resource, resource_id=resource_id, key=key
            )
            logger.debug(f"HEAD {resource} ({resource_id}): {key} - {r_body}")
            if r_body["exists"]:
                raise FileExistsError(f"File already exists in S3: {key}")

        logger.debug("Uploading %s to %s", file_path, key)
        logger.debug("Creating multipart upload for %s %s", resource, resource_id)
        (
            _create_mpu_headers,
            _create_mpu_params,
            create_mpu_body,
        ) = self._s3.create_multipart_upload(
            resource=resource, resource_id=resource_id, key=key
        )
        try:
            upload_id = create_mpu_body["InitiateMultipartUploadResult"]["UploadId"]
            logger.debug("Upload ID: %s", upload_id)
        except KeyError as e:
            logger.error("Error creating multipart upload: %s", create_mpu_body)
            raise e

        file = open(file_path, "rb")
        file_size = os.fstat(file.fileno()).st_size
        part_count = (file_size // part_size) + 1
        logger.debug("File size: %s", file_size)
        logger.debug("Part size: %s", part_size)

        parts = []
        futures = []
        logger.debug("Uploading parts with %s workers", max_workers)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(part_count):
                part_number = i + 1
                future = executor.submit(
                    self.upload_part,
                    resource=resource,
                    resource_id=resource_id,
                    file_path=file_path,
                    upload_id=upload_id,
                    part_number=part_number,
                    key=key,
                    part_size=part_size,
                )
                futures.append(future)

        for future in futures:
            parts.append(future.result())
            logger.debug("Uploaded part %s of %s", len(parts), part_count)

        logger.debug("Completing multipart upload")
        (
            _complete_mpu_headers,
            _complete_mpu_params,
            complete_mpu_body,
        ) = self._s3.complete_multipart_upload(
            resource=resource,
            resource_id=resource_id,
            key=key,
            upload_id=upload_id,
            parts=parts,
        )
        logger.debug("Completed multipart upload %s", complete_mpu_body)

    def get_message_data_from_record(
        self, record, s3_bucket=None, s3_key=None, ingestion_id=None
    ):
        format = record["format"]
        if format != "ros":
            raise NotImplementedError(f"Format {format} not supported")

        if ingestion_id is None:
            ingestion_id = record["ingestion_id"]
            if ingestion_id in self._cached_ingestions:
                ingestion = self._cached_ingestions[ingestion_id]
            elif ingestion_id is not None:
                ingestion = self._getter.ingestion(ingestion_id)["data"]
                self._cached_ingestions[ingestion_id] = ingestion

        if s3_bucket is None:
            s3_bucket = record["s3_bucket"]
            if s3_bucket is None:
                s3_bucket = ingestion["s3_bucket"]
                if s3_bucket is None:
                    raise ValueError("No S3 bucket specified")

        if s3_key is None:
            s3_key = record["s3_key"]
            if s3_key is None:
                s3_key = ingestion["s3_key"]
                if s3_key is None:
                    raise ValueError("No S3 key specified")

        message_data = self._s3.get_message_data_from_record(
            record=record, s3_bucket=s3_bucket, s3_key=s3_key, ingestion_id=ingestion_id
        )

        return message_data

    def get_ros_message_from_record(
        self,
        record,
        s3_bucket=None,
        s3_key=None,
        ingestion_id=None,
        message_type_name=None,
        message_type_id=None,
    ):
        message_data = self.get_message_data_from_record(
            record=record,
            s3_bucket=s3_bucket,
            s3_key=s3_key,
            ingestion_id=ingestion_id,
        )

        # TODO: this can certainly be condensed
        if message_type_name is None:
            message_type = self._getter.message_type(message_type_id)["data"]
            message_type_name = message_type["name"]
            self._cached_message_types[message_type_id] = message_type_name
        elif message_type_id is not None:
            if message_type_id in self._cached_message_types:
                message_type_name = self._cached_message_types[message_type_id]
            else:
                message_type = self._getter.message_type(message_type_id)["data"]
                message_type_name = message_type["name"]
                self._cached_message_types[message_type_id] = message_type_name
        else:
            message_type_id = record["message_type_id"]
            if message_type_id in self._cached_message_types:
                message_type_name = self._cached_message_types[message_type_id]
            else:
                message_type = self._getter.message_type(message_type_id)["data"]
                message_type_name = message_type["name"]
                self._cached_message_types[message_type_id] = message_type_name

        message_class = self._gen.get_message_class(message_type_name)
        message = message_class()
        message.deserialize(message_data)
        return message
