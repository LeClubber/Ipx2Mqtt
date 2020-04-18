#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import cgi
import os
import paho.mqtt.client as mqtt
from const import Constantes
from mqttd import Mqtt

form = cgi.FieldStorage()
print("Content-type: text/plain; charset=utf-8\n")

change = form.getvalue("type")
uid = form.getvalue("uid")
etat = form.getvalue("etat")
brightness = form.getvalue("brightness")

topic = Constantes.mqttTopic + "/" + change + "/" + uid + "/state"
payload = '{ ' + '"state": "'
if etat == "0":
  payload += 'OFF'
else:
  payload += 'ON'
payload += '"'
if brightness:
  payload += ', "brightness": ' + int(int(brightness)*2.55)
payload += ' }'

print("type: ")
print(change)
print("\ntopic: ")
print(topic)
print("\npayload: ")
print(payload)

Mqtt.publish(topic, payload, True)
