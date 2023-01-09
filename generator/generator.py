import json
from urllib.parse import urljoin
from datetime import datetime
import paho.mqtt.client as mqtt
import random
import time

N = 10
ENDPOINT = "mqtt"
QOS = 2
topics = ['UPB/RPi_1', 'Dorinel/Zeus']

def on_connect(client, args, flags, rc):
	print(f"IOT device Connected with result code {rc}")

def on_message(client, args, msg):
	return

def main():
	client = mqtt.Client("CLIENTI_NEBUNI")
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(ENDPOINT, 1883)
	client.loop_start()

	for i in range(N):
		topic_number = random.randint(0,len(topics) - 1)
		payload = {}
		if (topic_number % 2 == 0):
			payload['BAT'] = random.randint(0, 100)
			payload['HUMID'] = random.randint(0, 100)		
			payload['PRJ'] = "SPRC"		
			payload['IMP'] = random.randint(0, 100)		
			payload['status'] = "OK"
			payload['timestamp'] = datetime.now()	
		else:
			payload['Alarm'] = random.randint(0, 1)
			payload['AQI'] = "OK"
			payload['RSSI'] = random.randint(10, 3000)
		broker_payload = json.dumps(payload,default=str)
		client.publish(topics[topic_number],broker_payload)
		time.sleep(3)

	client.disconnect()
	client.loop_stop()


if __name__ == "__main__":
	main()
