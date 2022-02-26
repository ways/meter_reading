# Read HAN data from mqtt

# GPL3+ <dev@falkp.no>

# Requirements:
# pip install paho-mqtt

import time
import os
import sys
import json
import paho.mqtt.client as mqtt
from aidon_obis import *
import mqttconfig

tempfile="/run/meter_" + mqttconfig.mqtt_client
exit=False

def on_message(client, userdata, message):
    global client2
    # Split bytes
    split = [message.payload[i] for i in range (0, len(message.payload))]

    # Iterate and remove start byte, end byte
    for key, value in enumerate(split):
        # print(value, hex(value))
        if value == 126: # 0x7e
            del(split[key])

    result = None
    try:
        result = a.parse(bytes(split), mqttconfig.verbose)
    except (struct.error, IndexError, TypeError):
        #pass
        if mqttconfig.verbose:
            print("on_message: Unable to parse %s" % a)

    if result:
        # type1: {"p_act_in": 1756}
        # type2: {"version_id": b"AIDON_V0001", "meter_id": b"7XXXXXXXXXXXXXX1", "meter_type": b"6525", "p_act_in": 1756, "p_act_out": 0, "p_react_in": 0, "p_react_out": 299, "il1": 2.8, "il2": 1.3, "ul1": 237.4, "ul2": 236.3, "ul3": 235.5}
        if mqttconfig.verbose:
            print("on_message:", str(result).replace("'", '"').replace('b"', '"'))
        # Write out result to temp-file incase one wants to use it locally
        if mqttconfig.store_local:
            with open(tempfile, 'w', encoding = 'utf-8') as f:
                f.write(str(result).replace("'", '"').replace('b"', '"'))

        for key, value in result.items():
            topic=mqttconfig.broker2_topic + "/" + key
            payload=str(value).replace("b'", '')

            # print(topic, payload)
            try:
                client2.publish(topic, payload=payload)
            except TimeoutError():
                print("on_message: Error, publish timepout")


def aidon_callback(fields):
    """ Print result from parsing """
    if mqttconfig.verbose:
        print("aidon_callback", fields)


def on_disconnect(client, userdata, rc):
    global exit

    print("Disconnect reason  "  +str(rc))
    print("Client %s, userdata %s" % (client, userdata))
    #sys.exit(1)
    #raise SystemExit()
    exit=True



a = aidon(aidon_callback)

client = mqtt.Client(mqttconfig.mqtt_client)     #create new instance
client.on_message=on_message   #attach function to callback
client.connect(mqttconfig.broker_address, keepalive=60) #connect to broker
client.on_disconnect=on_disconnect
client.loop_start()

client2 = mqtt.Client(mqttconfig.mqtt_client)     #create new instance
client2.username_pw_set(username=mqttconfig.broker2_user,password=mqttconfig.broker2_password)
client2.connect(mqttconfig.broker2_address, keepalive=60) #connect to broker
client2.on_disconnect=on_disconnect

time.sleep(1)

#print("Subscribing to topic","tibber")
client.subscribe("tibber")

try:
    while not exit:
        time.sleep(1)
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
