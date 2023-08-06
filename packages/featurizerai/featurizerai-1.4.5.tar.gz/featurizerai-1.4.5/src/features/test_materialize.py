from materialize import materialize
from custom_schema import custom_schema

mongo_connection = {
    'uri': "mongodb+srv://admin:6lHqq9LqgwDlninK@cluster0.aqtcyq2.mongodb.net/?retryWrites=true&w=majority",
    'database': 'kafkastream',
    'rawdata': 'rawdata',
    'collection': 'sparkaggregate'
}

# Define schema fields as a list of dictionaries
schema_fields = [
    {"name": "timestamp", "type": "integer"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "deviceid", "type": "integer"}
]

# Create an instance of CustomSchema with the defined schema fields
custom_schema = custom_schema(schema_fields)

# Define the dynamic Spark SQL queries to be executed
sparksql = [
    "SELECT COUNT(email) AS email_count_last_24_hours, COUNT(name) AS name_count_last_24_hours, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 86400 and timestamp_unix < {timestamp_base} GROUP BY deviceid",
    "SELECT COUNT(email) AS email_count_last_7_days, COUNT(name) AS name_count_last_7_days, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 604800 and timestamp_unix < {timestamp_base} GROUP BY deviceid",
    "SELECT COUNT(email) AS email_count_last_15_days, COUNT(name) AS name_count_last_15_days, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 1296000 and timestamp_unix < {timestamp_base} GROUP BY deviceid",
    "SELECT COUNT(email) AS email_count_last_30_days, COUNT(name) AS name_count_last_30_days, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 2.592e+6 and timestamp_unix < {timestamp_base} GROUP BY deviceid",
    "SELECT COUNT(email) AS email_count_last_45_days, COUNT(name) AS name_count_last_45_days, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 3.888e+6 and timestamp_unix < {timestamp_base} GROUP BY deviceid",
    "SELECT COUNT(email) AS email_count_last_60_days, COUNT(name) AS name_count_last_60_days, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 5.184e+6 and timestamp_unix < {timestamp_base} GROUP BY deviceid"
]

# Create an instance of the materialize class
materialize_instance = materialize(mongo_connection, "2023-04-23 00:00:00", "deviceid", 56, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYnVyYWsiLCJleHAiOjE2ODIyNjIxNDB9.1w7INo6iAbglYuniYl-HJATTqbK6sOdu9JuyIEnXJ-M", custom_schema.schema, sparksql)

# Read the raw data from MongoDB
aggregated_data = materialize_instance.read_data_and_aggregate()
print(aggregated_data)
