#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import cgi
import json
import os
import paho.mqtt.client as mqtt
import requests
from const import Constantes
from mqtt import Mqtt

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
if uid.lower().startswith("d"):
  if not brightness:
    dimmer = uid[1:2]
    channel = uid[3:]
    # Si la valeur n'est pas renseignée on prend la dernière en statut
    req = requests.get("http://" + Constantes.ipxHost + "/api/xdevices.json?key=" + Constantes.ipxApiKey + "&Get=G")
    jsonStatus = json.loads(req.text)
    numStatus = (int(dimmer)-1)*4+int(channel)
    brightness = str(jsonStatus['G' + str(numStatus)]['Valeur'])
  payload += ', "brightness": ' + str(int(int(brightness)*2.55))
payload += ' }'

print("type: ")
print(change)
print("\ntopic: ")
print(topic)
print("\npayload: ")
print(payload)

Mqtt.publish(topic, payload, True)
