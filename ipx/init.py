#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import cgi
import cgitb
import json
import os
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
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

# Ajout ou suppression du relay si POST
topic = form.getvalue("topic")
idRelay = form.getvalue("idRelay")
nameRelay = form.getvalue("nameRelay")
brightness = form.getvalue("brightness")

if topic:
	print("Suppression du topic: "+topic)
elif idRelay and nameRelay:
	if re.match(r"^r[0-9]{2}$", idRelay) and not brightness or re.match(r"^d[0-9]c[0-9]$", idRelay) and brightness:
		topic = mqttTopic + "/light/" + idRelay + "/config"
		payload = "{ \"~\": \"" + mqttTopic + "/light/" + idRelay + "\"" # TODO
		payload += ", \"name\": \"" + str(nameRelay) + "\""
		payload += ", \"unique_id\": \"" + idRelay + "_light\""
		payload += ", \"command_topic\": \"~/set\""
		payload += ", \"state_topic\": \"~/state\""
		payload += ", \"schema\": \"json\""
		if brightness:
			payload += ", \"brightness\": true"
		payload += " }"
		print("topic: "+topic+"<br /> payload: "+payload+"<br />")
		#publish(topic, payload)
	else:
		print("Erreur: l'id doit être de forme r01 pour les relais de l'IPX et X8R et d1c1 pour le XDimmer")

# Récupération des messages MQTT
messages = subscribe.simple(mqttTopic + "/light/+/config", hostname=mqttHost, port=mqttPort, msg_count=2)
# for msg in messages:
# 	print("%s %s" % (msg.topic, msg.payload))

html = """<!DOCTYPE html>
<head>
	<title>Config MQTT pour Home-Assistant</title>
</head>
<body>
	<br />Configuration d'une entité :<br /><br />
	<form action="/init.py" method="post">
		<table>
			<tr><td>Id: </td><td><input type="text" name="idRelay" value="Id relay" title="L'id doit être de forme r01 pour les relais de l'IPX et X8R et d1c1 pour le XDimmer" /></td></tr>
			<tr><td>Nom: </td><td><input type="text" name="nameRelay" value="Nom du relay" /></td></tr>
			<tr><td>Dimmable: </td><td><input type="checkbox" name="brightness" value="Dimmable" /></td></tr>
			<tr><td>Configurer MQTT: </td><td><input type="submit" name="send" value="Envoyer" /></td></tr>
		</table>
	</form>
	<br />
	<hr>
	<br />
	Liste des entités configurées :<br /><br />
	<table>
	"""
for msg in messages:
	payload = json.loads(str(msg.payload, encoding="utf-8"))
	html += "<tr>"
	html += "<td>" + str(msg.topic) + "</td><td>" + json.dumps(payload, indent=4).replace(" ", "&nbsp;").replace("\n", "<br />") + "</td>"
	html += '<td><form action="/init.py" method="post">'
	html += '<input type="hidden" name="topic" value="' + str(msg.topic) + '" />'
	html += '<input type="submit" name="suppr" value="Supprimer" />'
	html += "</form>"
	html += "</td>"
	html += "</tr>"
html += """
	</table>
</body>
</html>
"""

print(html)