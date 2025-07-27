import paho.mqtt.client as mqtt
import json, string, random, mysql.connector, requests
import asyncio
import websockets
from datetime import datetime

#===============================================================
# Database Manager Class

class DatabaseManager():
	def __init__(self):
		self.conn = mysql.connector.connect(
            host="localhost", 
            user="root",       
            password="",  
            database="dbpcn"  
        )
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# Functions to push Sensor Data into Database

# Function to save Data Sensor to DB Table
def store_data(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	sensorId = json_Dict['sensorId']
	timestamp = json_Dict['date']
	value = json_Dict['value']
	topic = json_Dict['topic']
	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record(f"insert into data_{topic} (sensorId, {topic}) values (%s,%s)",[sensorId, value])
	dbObj.add_del_update_db_record(f"update devices set last_seen = %s where deviceId = %s",[timestamp, sensorId])
	del dbObj
	print (f"Inserted {topic} Data into Database.")
	print ("")
	print (f"upadate last seen to {timestamp}")
	print ("")

#===============================================================

# MQTT Settings 
MQTT_Broker = "192.168.100.220"
MQTT_Port = 8883
Keep_Alive_Interval = 45
MQTT_Topic = "sensor/limbah/#"

WEBHOOK_URL = "http://localhost:9000/webhook"
WS_SERVER_URI = "ws://localhost:8080" 

# Fungsi async untuk kirim data ke WebSocket
async def send_to_websocket(data):
    try:
        async with websockets.connect(WS_SERVER_URI) as websocket:
            await websocket.send(json.dumps(data))
    except Exception as e:
        print(f"[WS ERROR] {e}")

# ----------- KIRIM WEBHOOK -----------
def send_webhook(payload):
    headers = {
    'Content-Type': 'application/json',
    'authorization': 'Bearer your-secret-token'
    }
    data = {
        "sensorId": payload['sensorId'], 
        "topic": payload['topic'],
        "value": payload['value'],
        "status": payload['status']
    }
    try:
        r = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(data))
        print(f"[WEBHOOK] {r.status_code} - {r.text}")
    except Exception as e:
        print("[WEBHOOK ERROR]", e)

# Load rules dari file JSON
# with open("rules.json", "r") as f:
#     rules = json.load(f)
rules = {
     "sensor/limbah/temperature": {
        "conditions": [
        {"operator": ">", "value": 40}
        ],
        "action": {
            "topic": "alert/limbah/temperature",
            "message": "⚠️ : Temperature Limbah melebihi batas ambang!"
        }
    },
    "sensor/limbah/ph": {
        "conditions": [
            {"operator": "<", "value": 6}
        ],
        "action": {
            "topic": "alert/limbah/ph",
            "message": "⚠️ : ph Limbah kurang dari batas ambang!"
        }
    },
    "sensor/limbah/volume": {
        "conditions": [
          {"operator": ">", "value": 1000}
        ],
        "action": {
            "topic": "alert/limbah/volume",
            "message": "⚠️ : volume Limbah melebihi batas ambang!"
        }
    },
    "sensor/limbah/cod": {
        "conditions": [
          {"operator": ">", "value": 20}
        ],
        "action": {
            "topic": "alert/limbah/cod",
            "message": "⚠️ : volume Limbah melebihi batas ambang!"
        }
    }
}
	
# ----------- COCOKKAN RULE -----------
def evaluate_conditions(data, conditions):
    try:
        results = []
        for cond in conditions:
            sValue = data
            operator = cond['operator']
            value = cond['value']

            if operator == ">":
                results.append(sValue > value)
            elif operator == "<":
                results.append(sValue < value)
            elif operator == "==":
                results.append(sValue == value)
            elif operator == ">=":
                results.append(sValue >= value)
            elif operator == "<=":
                results.append(sValue <= value)
            else:
                results.append(False)

        return all(results)
    except Exception as e:
        print("[ERR]", e)

# QoS Configuration
QOS_LEVEL = 1 

#Subscribe to all Sensors at Base Topic
def on_connect(mosq, obj, flags, rc):
	print(f"Connected to MQTT Broker with QoS:{QOS_LEVEL}")
	mqttc.subscribe(MQTT_Topic, QOS_LEVEL)

#Save Data into DB Table
def on_message(mosq, obj, msg):
    try:
        topic = msg.topic
        payload = float(msg.payload.decode())
        print(f"[MQTT] {msg.topic} => {payload}")

        partOfTopic = topic.split("/")
        sensorPath = "/".join(partOfTopic[:3])
        kindOfSensor = partOfTopic[2]
        device = partOfTopic[3]
        
        dateTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        dataSensor = {
            "sensorId": device,
            "topic" : kindOfSensor,
            "value": payload,
            "date": dateTime
        }
        jsonData = json.dumps(dataSensor)

        if sensorPath in rules:
            try:
                rule = rules.get(sensorPath)
                passed = evaluate_conditions(payload, rule['conditions'])
                if passed:
                    alert_msg = f"{kindOfSensor}{rule['action']['message']}"
                    mqttc.publish(f"{rule['action']['topic']}/{device}", alert_msg) 

                    # Kirim webhook
                    send_webhook({**dataSensor, "status": alert_msg})
            except Exception as e:
                print(f"Error parsing message: {e}")

        print ("MQTT Data Received...")
        print ("MQTT Topic: " + topic)
        print ("QoS:" + str(msg.qos))  # Menampilkan QoS dari pesan yang diterima
        print ("ID: " + str(dataSensor['sensorId']))
        print (kindOfSensor + ": " + str(payload))
        jsonD = json.loads(jsonData)
        print ("Date: " + str(jsonD['date']))
        # print ("Date: " + str(dateTime))

        store_data(jsonData)
        asyncio.run(send_to_websocket(jsonData))
    
    except Exception as e:
        print("[ERROR]", e)

def on_subscribe(mosq, obj, mid, granted_qos):
	print(f"Subscribed to topic with QoS: {granted_qos}")
	# Bisa berbeda dari yang diminta jika broker tidak mendukung QoS yang diminta

mqttc = mqtt.Client(protocol=mqtt.MQTTv311)

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Subscribe ke semua topik dalam rules
for topic in rules:
    mqttc.subscribe(topic)

##pw set di tambahkan untuk auth
mqttc.username_pw_set("client1","client1@")

# Connect
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop
mqttc.loop_forever()
#===============================================================
