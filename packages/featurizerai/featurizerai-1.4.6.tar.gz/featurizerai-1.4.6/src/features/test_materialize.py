from flask import Flask, request, jsonify, json
from materialize import materialize
from custom_schema import custom_schema

app = Flask(__name__)

mongo_connection = {
    'uri': "mongodb+srv://admin:6lHqq9LqgwDlninK@cluster0.aqtcyq2.mongodb.net/?retryWrites=true&w=majority",
    'database': 'kafkastream',
    'rawdata': 'rawdata',
    'collection': 'sparkaggregate'
}

schema_fields = [
    {"name": "timestamp", "type": "integer"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "deviceid", "type": "integer"}
]

custom_schema = custom_schema(schema_fields)

@app.route('/aggregate', methods=['POST'])
def aggregate():
    # Define the dynamic Spark SQL queries to be executed
    sparksql = [
        "SELECT COUNT(email) AS email_count_last_24_hours, COUNT(name) AS name_count_last_24_hours, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 86400 and timestamp_unix < {timestamp_base} GROUP BY deviceid",
        "SELECT COUNT(email) AS email_count_last_7_days, COUNT(name) AS name_count_last_7_days, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 604800 and timestamp_unix < {timestamp_base} GROUP BY deviceid",
        "SELECT COUNT(email) AS email_count_last_15_days, COUNT(name) AS name_count_last_15_days, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 1296000 and timestamp_unix < {timestamp_base} GROUP BY deviceid",
        "SELECT COUNT(email) AS email_count_last_30_days, COUNT(name) AS name_count_last_30_days, deviceid FROM temp_table WHERE deviceid={deviceid} AND timestamp_unix > {timestamp} - 2.592e+6 and timestamp_unix < {timestamp_base} GROUP BY deviceid",
    ]
    json_data = request.get_json()
    timestamp = json_data.get('timestamp')
    deviceid = json_data.get('deviceid')
    token = json_data.get('token')

    materialize_instance = materialize(mongo_connection, timestamp, "deviceid", deviceid, token, custom_schema.schema, sparksql, partition_column="deviceid")

    aggregated_data_str = materialize_instance.read_data_and_aggregate()
    aggregated_data = json.loads(aggregated_data_str)

    return jsonify(aggregated_data)

if __name__ == '__main__':
    app.run(debug=True)
