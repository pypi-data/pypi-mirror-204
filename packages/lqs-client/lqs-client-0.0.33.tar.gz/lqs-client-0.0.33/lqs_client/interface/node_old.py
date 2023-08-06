import os
import time
import logging
import threading

import requests
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image, CompressedImage, CameraInfo

logging.basicConfig(
    level=os.getenv("LQS_LOG_LEVEL") or logging.INFO,
    format="%(asctime)s  (%(levelname)s - %(name)s): %(message)s",
)
logger = logging.getLogger(__name__)

# http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29


class Node:
    def __init__(self, getter, lister, utils, config):
        self._get = getter
        self._list = lister
        self._utils = utils
        self._config = config

        self._log = None
        self._start_time = None
        self._end_time = None

        self._publishers = {}
        self._subscriptions = {}
        self._remaps = {}

        self._use_s3_directly = True
        # self._use_s3_directly = False

        if self._config.get("verbose"):
            logger.setLevel(logging.DEBUG)

    def get_message_class(self, message_type_name):
        if message_type_name == "sensor_msgs/Image":
            return Image
        elif message_type_name == "sensor_msgs/CompressedImage":
            return CompressedImage
        elif message_type_name == "sensor_msgs/CameraInfo":
            return CameraInfo
        else:
            logger.info(
                "Currently only supports Image, CompressedImage, and CameraInfo message types."
            )
            raise Exception(f"Unsupported message type: {message_type_name}")

    def subscribe(self, log_id, topic_names, rel_start_time, rel_end_time, remaps={}):
        rospy.init_node("lqs_client", anonymous=True)

        self._log = self._get.log(log_id=log_id)["data"]

        self._start_time = self._log["start_time"] + rel_start_time
        self._end_time = self._log["start_time"] + rel_end_time

        topics_all = self._list.topics(log_id=log_id, limit=100)["data"]
        self._remaps = remaps
        self._subscriptions = {}
        for topic in topics_all:
            if topic["name"] in topic_names:
                message_class = self.get_message_class(topic["message_type_name"])
                self._publishers[topic["name"]] = rospy.Publisher(
                    remaps.get(topic["name"], topic["name"]),
                    message_class,
                    queue_size=10,
                )
                thread = threading.Thread(
                    target=self.load_records, args=(topic["name"],)
                )
                thread.start()
                self._subscriptions[topic["name"]] = {
                    "topic": topic,
                    "thread": thread,
                    "has_data": True,  # assume there is data to start
                    "next_message_timestamp": None,
                    "records": [],
                }

    def fetch_record_bytes(self, record):
        start_time = time.time()
        if self._use_s3_directly:
            mode = "direct"
            record["bytes"] = self._utils.get_message_data_from_record(record)
        else:
            mode = "presgined"
            record["bytes"] = requests.get(record["bytes_url"]).content
        end_time = time.time()
        print(
            f"({mode}) fetched bytes for {record['timestamp']} in {end_time - start_time}"
        )

    def load_records_old(self, topic_name):
        # limit = 100 if self._use_s3_directly else 10
        limit = 10
        offset = 0
        while True:
            if topic_name not in self._subscriptions:
                continue
            sub = self._subscriptions[topic_name]
            records = sub["records"]
            if len(records) >= limit:
                continue
            topic = sub["topic"]
            records_response = self._list.records(
                log_id=self._log["id"],
                topic_id=topic["id"],
                timestamp_gte=self._start_time,
                timestamp_lt=self._end_time,
                limit=limit,
                offset=offset,
                include_bytes=False if self._use_s3_directly else True,
            )
            records = records_response["data"]
            print(f"loaded {len(records)} records for {topic_name}")
            if len(records) == 0:
                self._subscriptions[topic_name]["has_data"] = False
                break
            offset += limit
            # fetch message data
            for record in records:
                # print(f"fetching bytes for {topic_name} ({record['timestamp']})")
                record[
                    "bytes"
                ] = None  # init to none to avoid race condition in publish check
                # threading.Thread(target=self.fetch_record_bytes, args=(record,)).start()
                self.fetch_record_bytes(record)
            # combine records, sort by timestamp
            self._subscriptions[topic_name]["records"] += records
            self._subscriptions[topic_name]["records"].sort(
                key=lambda x: x["timestamp"]
            )
            next_record = self._subscriptions[topic_name]["records"][0]
            self._subscriptions[topic_name]["next_message_timestamp"] = next_record[
                "timestamp"
            ]

    def load_records(self, topic_name):
        # limit = 100 if self._use_s3_directly else 10
        limit = 100
        offset = 0
        while True:
            if topic_name not in self._subscriptions:
                continue
            sub = self._subscriptions[topic_name]
            records = sub["records"]
            # if len(records) > limit:
            #     continue
            topic = sub["topic"]
            records_response = self._list.records(
                log_id=self._log["id"],
                topic_id=topic["id"],
                timestamp_gte=self._start_time,
                timestamp_lt=self._end_time,
                limit=limit,
                offset=offset,
                include_bytes=False if self._use_s3_directly else True,
            )
            records = records_response["data"]
            print(f"loaded {len(records)} records for {topic_name}")
            if len(records) == 0:
                # self._subscriptions[topic_name]["has_data"] = False
                break
            offset += limit
            # fetch message data
            # for record in records:
            #     record["bytes"] = self._utils.get_message_data_from_record(record)
            #     self._subscriptions[topic_name]["records"].append(record)
            self._subscriptions[topic_name]["records"] += records
            next_record = self._subscriptions[topic_name]["records"][0]
            self._subscriptions[topic_name]["next_message_timestamp"] = next_record[
                "timestamp"
            ]

    def publish_next_message(self):
        # look through our records and publish the next message based on timestamp
        next_message_time = None
        next_message_topic = None
        for topic_name in self._subscriptions:
            sub = self._subscriptions[topic_name]
            if sub["next_message_timestamp"] is None:
                if sub["has_data"]:
                    # we haven't loaded data for this topic yet, so we can't publish anything
                    return
                else:
                    # we've loaded all the data for this topic, so we can skip it
                    continue
            if (
                next_message_time is None
                or sub["next_message_timestamp"] < next_message_time
            ):
                # this topic may have the next message to publish
                next_message_time = sub["next_message_timestamp"]
                next_message_topic = topic_name

        if next_message_topic is not None:
            self.publish(next_message_topic)
            return True
        else:
            return False

    def publish(self, topic_name):
        sub = self._subscriptions[topic_name]
        topic = sub["topic"]
        records = sub["records"]
        if len(records) == 0:
            self._subscriptions[topic_name]["has_data"] = False
            return
        record = records.pop(0)
        # TODO: prefetch bytes for next record

        # message_data = requests.get(record["bytes_url"]).content
        # while record["bytes"] is None:
        #     time.sleep(0.01)
        # message_data = record["bytes"]
        message_data = self._utils.get_message_data_from_record(record)
        message_class = self.get_message_class(topic["message_type_name"])
        message = message_class()
        message.deserialize(message_data)
        publisher = self._publishers[topic_name]
        # print(f"publishing {topic_name} ({record['timestamp']}) {len(message_data)} bytes")
        publisher.publish(message)
        if len(self._subscriptions[topic_name]["records"]) == 0:
            print(f"no more records for {topic_name}")
            self._subscriptions[topic_name]["has_data"] = False
            return
        next_record = self._subscriptions[topic_name]["records"][0]
        self._subscriptions[topic_name]["next_message_timestamp"] = next_record[
            "timestamp"
        ]

    def play_old(self, rate=10):
        rate = rospy.Rate(rate)
        while not rospy.is_shutdown():
            self.publish_next_message()
            data_remaining = False
            for topic_name in self._subscriptions:
                if self._subscriptions[topic_name]["has_data"]:
                    data_remaining = True
                    break
            if not data_remaining:
                logger.info("No more data to publish.")
                print("No more data to publish.")
                break
            rate.sleep()

    def play(self, rate=10):
        rate = rospy.Rate(rate)
        while not rospy.is_shutdown():
            self.publish_next_message()
            data_remaining = False
            for topic_name in self._subscriptions:
                if self._subscriptions[topic_name]["has_data"]:
                    data_remaining = True
                    break
            if not data_remaining:
                logger.info("No more data to publish.")
                print("No more data to publish.")
                break
            rate.sleep()
