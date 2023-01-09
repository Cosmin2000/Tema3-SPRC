import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
from sys import stdout
import os


bucket="influxdb"
token='token123'
org="my-org"
url="http://influxdb:8086"
broker_port=1883
broker="mqtt"
database="influxdb"

db_client = InfluxDBClient(url=url,token=token , org=org, debug=True)
write_api = db_client.write_api(write_options=SYNCHRONOUS)
# db_client.switch_database(database)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc), flush=True)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

def on_publish(client,userdata,result):
    print("Device 1 : Data published.", flush=True)
    pass

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    


    # DB Business
    tokens = msg.topic.split("/")
    location = tokens[0]
    station = tokens[1]
    
    print(location + "." + station, flush = True)
    payload = eval(msg.payload)
    # Log
    logger.info("Received a message by topic |{topic}|".format(topic=msg.topic))
    timestamp=''


    fields = {}
    # print(type(eval(msg.payload)))
    for key, value in payload.items():
        if key == 'timestamp':
            timestamp = payload['timestamp']
            logger.info("Data timestamp is : {timestamp}".format(timestamp=timestamp))

        # print(type(value))
        if (type(value) == int or type(value) == float):
            fields[key] = value
            logger.info("{location}.{station}.{field} {value}".format(location=location,station=station,field=key,value=value))
            
    db_insert(location, station, timestamp, fields)


def db_insert(location, station, timestamp, fields):
    for key, value in fields.items():
        p = Point("my_measurement").tag("location",location).field(key, value)
        
        write_api.write(bucket=bucket,org=org, record=p)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(broker, broker_port)


logger = None
if (os.getenv("DEBUG_DATA_FLOW") == 'true'):
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG) 
    logFormatter = logging.Formatter\
    ("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    consoleHandler = logging.StreamHandler(stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
