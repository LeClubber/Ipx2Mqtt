#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import cgi
import cgitb
import json
import os
import paho.mqtt.client as mqtt
import re
from time import sleep

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

listConfig = dict()
def on_message(client, userdata, msg):
	listConfig[msg.topic] = str(msg.payload, encoding="utf-8")

def loadConfig():
	client = mqtt.Client()
	client.on_message = on_message
	client.connect(mqttHost, mqttPort)
	client.subscribe(mqttTopic + "/light/+/config")
	client.subscribe(mqttTopic + "/switch/+/config")
	client.loop_start()
	# Attente de reception des messages
	sleep(2)
	client.loop_stop()

print("Content-type: text/html; charset=utf-8\n")

# Ajout ou suppression du relay si POST
confirm = form.getvalue("confirm")
topic = form.getvalue("topic")
idRelay = form.getvalue("idRelay")
nameRelay = form.getvalue("nameRelay")
brightness = form.getvalue("brightness")

html = """<!DOCTYPE html>
<head>
	<title>Config MQTT pour Home-Assistant</title>
</head>
<body>
"""

if confirm:
	publish(confirm, None)
elif topic:
	html += '<br /><form action="/init.py" method="post">'
	html += "Confirmez-vous la suppression du topic: " + topic + " ?"
	html += '<input type="hidden" name="confirm" value="' + topic + '" />'
	html += '<input type="submit" name="suppr" value="Supprimer" />'
	html += "</form><br /><br /><hr>"
elif idRelay and nameRelay:
	if re.match(r"^r[0-9]{2}$", idRelay) and not brightness or re.match(r"^d[0-9]c[0-9]$", idRelay) and brightness:
		topic = mqttTopic + "/light/" + idRelay + "/config"
		payload = "{ \"~\": \"" + mqttTopic + "/light/" + idRelay + "\"" # TODO
		payload += ", \"name\": \"" + nameRelay + "\""
		payload += ", \"unique_id\": \"" + idRelay + "_light\""
		payload += ", \"command_topic\": \"~/set\""
		payload += ", \"state_topic\": \"~/state\""
		payload += ", \"schema\": \"json\""
		if brightness:
			payload += ", \"brightness\": true"
		payload += " }"
		#print("topic: "+topic+"<br /> payload: "+payload+"<br />")
		publish(topic, payload)
	else:
		html += "<br />Erreur: l'id doit être de forme r01 pour les relais de l'IPX et X8R et d1c1 pour le XDimmer<br /><br /><hr>"

# Récupération des messages MQTT
loadConfig()

html += """
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
	<br />"""
if not listConfig:
	html += "Aucune entité configurée"
else:
	html += """
	Liste des entités configurées :<br /><br />
	<table>
		<thead>
			<tr>
				<th>Topic</th>
				<th>Payload</th>
			</tr>
		</thead>
		<tbody>
	"""
	for topic in listConfig:
		payload = json.loads(listConfig[topic])
		html += "<tr>"
		html += "<td>" + topic + "</td>"
		html += "<td>" + json.dumps(payload, indent=4).replace(" ", "&nbsp;").replace("\n", "<br />") + "</td>"
		html += '<td><form action="/init.py" method="post">'
		html += '<input type="hidden" name="topic" value="' + str(topic) + '" />'
		html += '<input type="submit" name="suppr" value="Supprimer" />'
		html += "</form>"
		html += "</td>"
		html += "</tr>"
	html += """
		</tbody>
	</table>"""
html += """
</body>
</html>
"""

print(html)