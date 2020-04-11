#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import cgi
import os
import paho.mqtt.client as mqtt

mqttPort = int(os.getenv('MQTT_PORT', 1883))
mqttHost = os.getenv('MQTT_HOST', "localhost")
mqttTopic = os.getenv('MQTT_TOPIC', "ipx")

form = cgi.FieldStorage()
print("Content-type: text/plain; charset=utf-8\n")

uid = form.getvalue("uid")
etat = form.getvalue("etat")
brightness = form.getvalue("brightness")

topic = mqttTopic + "/switch/" + uid + "/state"
payload = '{ ' + '"state": "'
if etat == "0":
  payload += 'OFF'
else:
  payload += 'ON'
payload += '" }'

print("topic: ")
print(topic)
print("\npayload: ")
print(payload)

client = mqtt.Client()
client.connect(mqttHost, mqttPort, 60)
client.publish(topic, payload, retain=True)
client.disconnect()
