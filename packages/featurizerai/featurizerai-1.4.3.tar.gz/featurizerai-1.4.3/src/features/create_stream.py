import json
import ast
import logging
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from confluent_kafka import Consumer, KafkaError
import certifi
import os
import threading

class create_stream:
    def __init__(self, kafka_connection, mongo_connection=None, topicname=""):
        self.topicname = topicname
        self.kafka_connection = kafka_connection
        self.mongo_connection = mongo_connection or {
            'uri': "mongodb+srv://admin:6lHqq9LqgwDlninK@cluster0.aqtcyq2.mongodb.net/?retryWrites=true&w=majority",
            'database': 'kafkastream',
            'rawcollection': 'rawdata',
            'collection': 'sparkaggregate'
        }
        self._stop_event = threading.Event()

    os.environ['HADOOP_OPTS'] = f"{os.environ.get('HADOOP_OPTS', '')} -Djava.library.path=/Library/hadoop/lib/native"

    def is_epoch(self, timestamp):
        try:
            datetime.fromtimestamp(int(timestamp))
            return True
        except ValueError:
            return False

    def _run(self):
        mongo_client = MongoClient(self.mongo_connection['uri'], server_api=ServerApi('1'), tlsCAFile=certifi.where())
        mongo_db = mongo_client[self.mongo_connection['database']]
        raw_data_collection = mongo_db[self.mongo_connection['rawcollection']]

        consumer = Consumer(self.kafka_connection)
        print(self.topicname)
        consumer.subscribe([self.topicname])

        while not self._stop_event.is_set():
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
            else:
                message_value = ast.literal_eval(msg.value().decode("utf-8"))
                if self.is_epoch(message_value.get("timestamp")):
                    if self.is_epoch(message_value.get("timestamp")):
                        message_value["timestamp"] = int(message_value["timestamp"])
                    else:
                        message_value["timestamp"] = datetime.now().timestamp()

                    raw_data_collection.insert_one(message_value)
                    print("Message received: {}".format(message_value))
        consumer.close()

    def start(self):
        if not hasattr(self, '_consumer_thread') or not self._consumer_thread.is_alive():
            self._stop_event.clear()
            self._consumer_thread = threading.Thread(target=self._run)
            self._consumer_thread.start()
            print('featurizerai: Started consumer thread.')
        else:
            print("Thread is already running. Cannot start it again.")

    def stop(self):
        if hasattr(self, '_consumer_thread') and self._consumer_thread.is_alive():
            self._stop_event.set()
            self._consumer_thread.join()
            print('featurizerai: Stopped consumer thread.')
        else:
            print("Thread is not running. Cannot stop it.")
