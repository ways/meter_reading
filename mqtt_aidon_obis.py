# Read HAN data from mqtt

# GPL3+ <dev@falkp.no>

# Requirements:
# pip install paho-mqtt

# Change to your broker
broker_address="192.168.1.34" 

import time
import paho.mqtt.client as mqtt
from aidon_obis import *


def on_message(client, userdata, message):
    # print(message.payload.hex())

    # Split bytes
    split = [message.payload[i] for i in range (0, len(message.payload))]

    # Iterate and remove start byte, end byte
    for key, value in enumerate(split):
        # print(value, hex(value))
        if value == 126: # 0x7e
            del(split[key])

    a.parse(bytes(split))


def aidon_callback(fields):
    """ Print result from parsing """
    print(fields)


a = aidon(aidon_callback)

client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
client.connect(broker_address) #connect to broker
client.loop_start()

time.sleep(1)

print("Subscribing to topic","tibber")
client.subscribe("tibber")

try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
