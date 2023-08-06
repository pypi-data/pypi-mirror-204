from datetime import datetime

from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
from materialize import materialize

mongo_connection = {
    'uri': "mongodb+srv://admin:6lHqq9LqgwDlninK@cluster0.aqtcyq2.mongodb.net/?retryWrites=true&w=majority",
    'database': 'kafkastream',
    'rawdata': 'rawdata',
    'collection': 'sparkaggregate'
}

mongo_client = MongoClient(mongo_connection['uri'], server_api=ServerApi('1'), tlsCAFile=certifi.where())

aggregation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
device_id = 56
hours = []
days = [1, 5, 7, 10, 15]

m = materialize(mongo_connection, aggregation_date, device_id, hours, days)
raw_data_collection = mongo_client[mongo_connection['database']][mongo_connection['rawdata']]
m.read_data_and_aggregate(raw_data_collection)

