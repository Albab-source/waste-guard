#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------


import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

#====================================================
# MQTT Settings 
MQTT_Broker = "192.168.100.220"
MQTT_Port = 8883
Keep_Alive_Interval = 45
MQTT_Topic_Humidity = "sensorpcn/ruang1/humidity"
MQTT_Topic_Temperature = "sensor/limbah/tower1"

#====================================================
 


def on_connect(client, userdata, rc):
	if rc != 0:
		pass
		print ("Unable to connect to MQTT Broker...")
	else:
		print ("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
	pass
		
def on_disconnect(client, userdata, rc):
	if rc !=0:
		pass
		
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish

##pw set di tambahkan untuk auth
mqttc.username_pw_set("PCNTest1","PCNTest1@")

mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

##in paho documentation at the end of description for tls_set() you can see "Must be called before connect*()."
mqttc.tls_set()

		
def publish_To_Topic(topic, message):
	mqttc.publish(topic,message)
	print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	


#====================================================
# FAKE SENSOR 
# Dummy code used as Fake Sensor to publish some random values
# to MQTT Broker

# Daftar topik dan range random sesuai rules.json
SENSOR_TOPICS = [
    {
        "topic": "sensor/limbah/temperature/device-001",
        "range": (50, 60)
    },
    {
        "topic": "sensor/limbah/temperature/device-002",
        "range": (35, 45)
    },
    {
        "topic": "sensor/limbah/ph/device-001",
        "range": (10, 11)
    },
    {
        "topic": "sensor/limbah/ph/device-002",
        "range": (4, 8)
    },
    {
        "topic": "sensor/limbah/volume/device-001",
        "range": (800, 850)
    },
    {
        "topic": "sensor/limbah/volume/device-002",
        "range": (900, 1100)
    },
    {
        "topic": "sensor/limbah/cod/device-001",
        "range": (10, 15)
    },
    {
        "topic": "sensor/limbah/cod/device-002",
        "range": (15, 20)
    },
]

def publish_Fake_Sensor_Values_to_MQTT():
    threading.Timer(15.0, publish_Fake_Sensor_Values_to_MQTT).start()
    for sensor in SENSOR_TOPICS:
        value = round(random.uniform(*sensor["range"]), 2)
        print(f"Publishing to {sensor['topic']}: {value}")
        publish_To_Topic(sensor["topic"], value)

publish_Fake_Sensor_Values_to_MQTT()

#====================================================
#  python publisher_dummy.py
#  python main.py