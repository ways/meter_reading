# Read HAN data from mqtt

# GPL3+ <dev@falkp.no>

# Requirements:
# pip install paho-mqtt

import time
import sys
import json
import paho.mqtt.client as mqtt
from aidon_obis import *
import mqttconfig


def on_message(client, userdata, message):
    global client2
    # Split bytes
    split = [message.payload[i] for i in range (0, len(message.payload))]

    # Iterate and remove start byte, end byte
    for key, value in enumerate(split):
        # print(value, hex(value))
        if value == 126: # 0x7e
            del(split[key])

    result = a.parse(bytes(split))

    if result:
        print(mqttconfig.broker2_topic, result)
        client2.publish(mqttconfig.broker2_topic, payload=str(result))


def aidon_callback(fields):
    """ Print result from parsing """
    print(fields)


a = aidon(aidon_callback)

client = mqtt.Client(mqttconfig.mqtt_client)     #create new instance
client.on_message=on_message   #attach function to callback
client.connect(mqttconfig.broker_address) #connect to broker
client.loop_start()

client2 = mqtt.Client(mqttconfig.mqtt_client)     #create new instance
client2.username_pw_set(username=mqttconfig.broker2_user,password=mqttconfig.broker2_password)
client2.connect(mqttconfig.broker2_address) #connect to broker

time.sleep(1)

#print("Subscribing to topic","tibber")
client.subscribe("tibber")

try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
