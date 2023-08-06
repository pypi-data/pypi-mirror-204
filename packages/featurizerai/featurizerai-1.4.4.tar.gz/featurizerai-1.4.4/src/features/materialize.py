import json
import logging
from datetime import datetime, timedelta

import jwt
from pymongo import MongoClient
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count
from pyspark.sql.types import StringType, StructType, StructField, TimestampType, IntegerType
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import certifi
from pymongo.server_api import ServerApi

class materialize:
    def __init__(self, mongo_connection, aggregation_date, device_id, hours, days, token):
        self.mongo_connection = mongo_connection
        self.aggregation_date = datetime.strptime(aggregation_date, "%Y-%m-%d %H:%M:%S")
        self.device_id = device_id
        self.token = token
        self.hours = hours
        self.days = days
        self.schema = StructType([
            StructField("timestamp", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("email", StringType(), True),
            StructField("deviceid", IntegerType(), True)
        ])

        self.spark = SparkSession.builder \
            .appName("IncrementalAggregation") \
            .master("local[*]") \
            .getOrCreate()

    def read_data_and_aggregate(self, raw_data_collection):

        # authenicate token
        mongo_client = MongoClient(self.mongo_connection['uri'], server_api=ServerApi('1'), tlsCAFile=certifi.where())
        mongo_db = mongo_client[self.mongo_connection['database']]
        mongo_db_featurizer = mongo_client['featurizer']
        users_collection = mongo_db_featurizer["users"]
        SECRET_KEY = "features"  # Change this to your desired secret key
        TOKEN_EXPIRATION = 3600  # Token expiration in seconds (1 hour)

        try:
            payload = jwt.decode(self.token, SECRET_KEY, algorithms=["HS256"])
            user_id: str = payload.get("user_id")
            if user_id is None:
                print("User not found")
                return ("Invalid token")
            print(user_id)
            user = users_collection.find_one({"userid": user_id})
            if user is None:
                print("User not found")
                return ("Invalid token")
        except Exception as e:
            print(e)
            return ("Invalid token")


        mongo_client = MongoClient(self.mongo_connection['uri'], server_api=ServerApi('1'), tlsCAFile=certifi.where())
        mongo_db = mongo_client[self.mongo_connection['database']]
        aggregated_data_collection = mongo_db[self.mongo_connection['collection']]

        raw_data = raw_data_collection.find()
        raw_data_list = [doc for doc in raw_data]
        df = self.spark.createDataFrame(raw_data_list, self.schema)

        # Filter the DataFrame based on the given device_id
        df = df.filter(col("deviceid") == self.device_id)
        start_time = self.aggregation_date
        df = df.filter((col("deviceid") == self.device_id) & (col("timestamp") < start_time.timestamp()))
        df = df.withColumn("timestamp_unix", F.col("timestamp").cast("bigint"))
        df.createOrReplaceTempView("temp_table")

        # Create columns for each hour and day passed using Spark SQL
        for hour in self.hours:
            hour_timestamp = int((self.aggregation_date - timedelta(hours=hour)).timestamp())
            hourly_count = self.spark.sql(
                f"SELECT COUNT(email) AS email_count_last_{hour}_hours, COUNT(name) AS name_count_last_{hour}_hours, deviceid FROM temp_table WHERE deviceid={self.device_id} AND timestamp_unix > {hour_timestamp} GROUP BY deviceid")
            df = df.join(hourly_count, on=["deviceid"], how="left")
            df = df.withColumn(f"email_count_last_{hour}_hours",
                               F.col(f"email_count_last_{hour}_hours").cast(IntegerType()))
            df = df.withColumn(f"name_count_last_{hour}_hours",
                               F.col(f"name_count_last_{hour}_hours").cast(IntegerType()))

        for day in self.days:
            day_timestamp = int((self.aggregation_date - timedelta(days=day)).timestamp())
            daily_count = self.spark.sql(
                f"SELECT COUNT(email) AS email_count_last_{day}_days, COUNT(name) AS name_count_last_{day}_days, deviceid FROM temp_table WHERE deviceid={self.device_id} AND timestamp_unix > {day_timestamp} GROUP BY deviceid")
            df = df.join(daily_count, on=["deviceid"], how="left")
            df = df.withColumn(f"email_count_last_{day}_days",
                               F.col(f"email_count_last_{day}_days").cast(IntegerType()))
            df = df.withColumn(f"name_count_last_{day}_days", F.col(f"name_count_last_{day}_days").cast(IntegerType()))

        aggregated_data = df \
            .withColumn("date", F.lit(start_time.strftime("%Y-%m-%d"))) \
            .drop("name", "email", "timestamp", "timestamp_unix") \
            .dropDuplicates(["deviceid", "date"])

        # Print the results
        aggregated_data.show()

        aggregated_data_dict = aggregated_data.collect()[0].asDict()
        json_aggregated_data = json.dumps(aggregated_data_dict)
        print(json_aggregated_data)

        if json_aggregated_data is not None:
            aggregated_data_collection.update_one(
                {"date": aggregated_data_dict["date"], "deviceid": aggregated_data_dict["deviceid"]},
                {"$set": {"aggregated_data": json_aggregated_data}},
                upsert=True
            )
        else:
            logging.error("Serialized aggregated data is None, skipping update")

        return aggregated_data_dict
