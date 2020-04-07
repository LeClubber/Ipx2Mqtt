#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import cgi
import cgitb
import os
import paho.mqtt.client as mqtt
import re

cgitb.enable()

mqttPort = int(os.getenv('MQTT_PORT', 1883))
mqttHost = os.getenv('MQTT_HOST', "localhost")
mqttTopic = os.getenv('MQTT_TOPIC', "ipx")

form = cgi.FieldStorage()

def publish(topic, playload):
	client = mqtt.Client()
	client.connect(mqttHost, mqttPort, 60)
	client.publish(topic, playload, retain=True)
	client.disconnect()


print("Content-type: text/html; charset=utf-8\n")

idRelay = form.getvalue("idRelay")
nameRelay = form.getvalue("nameRelay")
brightness = form.getvalue("brightness")
brightnessStr=""
if brightness:
	brightnessStr=str(brightness)
if idRelay and nameRelay:
	if re.match(r"^r[0-9]{2}$", idRelay) and not brightness or re.match(r"^d[0-9]c[0-9]$", idRelay) and brightness:
		#print("Id: "+str(idRelay)+" Nom: "+str(nameRelay)+" Dim: "+str(brightnessStr))
		topic = mqttTopic + "/light/" + idRelay + "/config"
		playload = "{ \"~\": \"" + mqttTopic + "/light/" + idRelay + "\"" # TODO
		playload += ", \"name\": \"" + str(nameRelay) + "\""
		playload += ", \"unique_id\": \"" + idRelay + "_light\""
		playload += ", \"command_topic\": \"~/set\""
		playload += ", \"state_topic\": \"~/state\""
		playload += ", \"schema\": \"json\""
		if brightness:
			playload += ", \"brightness\": true"
		playload += " }"
		print("topic: "+topic+"<br /> playload: "+playload+"<br />")
		#publish(topic, playload)
	else:
		print("Erreur: l'id doit être de forme r01 pour les relais de l'IPX et X8R et d1c1 pour le XDimmer")

html = """<!DOCTYPE html>
<head>
	<title>Config MQTT pour Home-Assistant</title>
</head>
<body>
	<form action="/init.py" method="post">
		<table>
			<tr><td>Id: </td><td><input type="text" name="idRelay" value="Id relay" title="L'id doit être de forme r01 pour les relais de l'IPX et X8R et d1c1 pour le XDimmer" /></td></tr>
			<tr><td>Nom: </td><td><input type="text" name="nameRelay" value="Nom du relay" /></td></tr>
			<tr><td>Dimmable: </td><td><input type="checkbox" name="brightness" value="Dimmable" /></td></tr>
			<tr><td>Configurer MQTT: </td><td><input type="submit" name="send" value="Envoyer"></td></tr>
		</table>
	</form> 
</body>
</html>
"""

print(html)