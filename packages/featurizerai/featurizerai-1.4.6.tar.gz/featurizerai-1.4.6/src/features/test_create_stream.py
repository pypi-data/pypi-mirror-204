import time

from create_stream import create_stream

def main():
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
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYnVyYWsiLCJleHAiOjE2ODIzMzg3OTN9.VutSPOtM4aRgyEBwdoNh-89jdCfcfC9eDe1D8UU3tAs"
    featurizerai.start(jwt)

    # Run the consumer for 60 seconds
    time.sleep(60)

    # Stop the consumer and wait for the thread to finish
    featurizerai.stop()

if __name__ == "__main__":
    main()
