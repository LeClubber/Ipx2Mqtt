#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import json
import paho.mqtt.client as mqtt
import requests
from const import Constantes
from threading import Thread

# MQTT
class Mqtt(Thread):
    """ Thread chargé de la connexion au broker MQTT """

    def __init__(self):
        Thread.__init__(self)

    def on_connect(self, client, userdata, flags, rc):
        """ Abonnement aux topics souhaités """
        affichage = "Connected to MQTT with result code " + str(rc)
        print(affichage)
        topic = Constantes.mqttTopic + "/light/+/set"
        client.subscribe(topic)
        topic = Constantes.mqttTopic + "/switch/+/set"
        client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        """ Traitement du message recu """
        urlIpx = 'http://' + Constantes.ipxHost
        topic = str(msg.topic)
        payload = str(msg.payload, encoding="utf-8")

        relay = topic.replace(Constantes.mqttTopic, '').replace('/light/', '').replace('/switch/', '').replace('/set', '')
        json_data = json.loads(payload)
        if relay.lower().startswith("d"):
            # Gestion des XDimmer
            dimmer = relay[1:2]
            channel = relay[3:]
            urlIpx += "/user/api.cgi?SetDim=" + dimmer + "&DimCha=" + channel + "&DimValue="
            if "OFF" == json_data['state']:
                urlIpx += "0"
            elif "ON" == json_data['state']:
                brightness = ""
                if "brightness" in json_data:
                    # On change d'échelle de 255 à 100
                    brightness = str(int(int(json_data['brightness'])/2.55))
                else:
                    # Si la valeur n'est pas renseignée on prend la dernière en statut
                    req = requests.get("http://" + Constantes.ipxHost + "/api/xdevices.json?key=" + Constantes.ipxApiKey + "&Get=G")
                    jsonStatus = json.loads(req.text)
                    numStatus = int(dimmer)*int(channel)
                    brightness = str(jsonStatus['G' + str(numStatus)]['Valeur'])
                urlIpx += brightness
        else:
            # Gestion des relais IPX et X8R
            urlIpx += '/api/xdevices.json?key=' + Constantes.ipxApiKey + '&'
            if "ON" == json_data['state']:
                urlIpx += 'SetR='
            elif "OFF" == json_data['state']:
                urlIpx += 'ClearR='
            urlIpx += relay.replace('r', '')
        # Reqete de commande à l'IPX
        requests.get(urlIpx, auth=(Constantes.ipxLogin, Constantes.ipxPassword))

    def run(self):
        """ Démarrage du service MQTT """
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(Constantes.mqttHost, Constantes.mqttPort, 60)
        client.loop_forever()
    
    def publish(cls, topic, playload, retain=True):
        """ Publication des messages MQTT """
        client = mqtt.Client()
        client.connect(Constantes.mqttHost, Constantes.mqttPort, 60)
        client.publish(topic, playload, retain=retain)
        client.disconnect()
    publish = classmethod(publish)