import time

import features
from features.create_stream import create_stream
from features.authenticate import authenticate
from features.materialize import materialize
from features.custom_schema import custom_schema

def authenticate_user():
    sdk = authenticate()
    access_token, token_type = sdk.authenticate('burak', 'burak')
    return access_token

def stream(token):
    kafka_connection = {
        "bootstrap.servers": "buraks-air.lan:9092",
        "group.id": "your-group-id",
        "auto.offset.reset": "earliest"
    }

    # Optional: Provide custom MongoDB connection settings
    mongo_connection = {
        'uri': "mongodb+srv://admin:6lHqq9LqgwDlninK@cluster0.aqtcyq2.mongodb.net/?retryWrites=true&w=majority",
        'database': 'kafkastream',
        'rawcollection': 'rawdata',
        'collection': 'sparkaggregate'
    }

    # Create a new instance of the create_stream class
    featurizerai = create_stream(kafka_connection, mongo_connection, "fake-data_test5", "timestamp")

    # Start the Kafka consumer in a separate thread
    featurizerai.start(token)

    # # Run the consumer for 60 seconds
    # time.sleep(60)
    #
    # # Stop the consumer and wait for the thread to finish
    # featurizerai.stop()
def main():
    token = authenticate_user()
    stream(token)

if __name__ == "__main__":
    main()
