#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import http.server
import json
import os
import paho.mqtt.client as mqtt
import requests
from threading import Thread

# Recuperation des variebles d'environnement
httpPort = int(os.getenv('HTTP_PORT', 8080))
mqttPort = int(os.getenv('MQTT_PORT', 1883))
mqttHost = os.getenv('MQTT_HOST', "localhost")
mqttTopic = os.getenv('MQTT_TOPIC', "ipx")
ipxHost = os.getenv("IPX_HOST", "192.168.1.1")
ipxApiKey = os.getenv("IPX_API_KEY", "apikey")
ipxLogin = os.getenv("IPX_LOGIN", "admin")
ipxPassword = os.getenv("IPX_PASSWORD", "password")

# MQTT
class Mqtt(Thread):
    """ Thread chargé de la connexion au broker MQTT """
    def __init__(self, mqttHost, mqttPort, mqttTopic, ipxHost, ipxApiKey, ipxLogin, ipxPassword):
        Thread.__init__(self)
        self.mqttHost = mqttHost
        self.mqttPort = mqttPort
        self.mqttTopic = mqttTopic
        self.ipxHost = ipxHost
        self.ipxApiKey = ipxApiKey
        self.ipxLogin = ipxLogin
        self.ipxPassword = ipxPassword

    def on_connect(self, client, userdata, flags, rc):
        """ Abonnement aux topics souhaités """
        affichage = "Connected to MQTT with result code " + str(rc)
        print(affichage)
        topic = self.mqttTopic + "/light/+/set"
        client.subscribe(topic)
        topic = self.mqttTopic + "/switch/+/set"
        client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        """ Traitement du message recu """
        urlIpx = 'http://' + self.ipxHost
        payload = str(msg.payload)
        payload = payload[2:-1]
        relay = msg.topic.replace(self.mqttTopic, '').replace('/light/', '').replace('/switch/', '').replace('/set', '')
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
                    req = requests.get("http://" + self.ipxHost + "/api/xdevices.json?key=" + self.ipxApiKey + "&Get=G")
                    jsonStatus = json.loads(req.text)
                    numStatus = int(dimmer)*int(channel)
                    brightness = str(jsonStatus['G' + str(numStatus)]['Valeur'])
                urlIpx += brightness
        else:
            # Gestion des relais IPX et X8R
            urlIpx += '/api/xdevices.json?key=' + self.ipxApiKey + '&'
            if "ON" == json_data['state']:
                urlIpx += 'SetR='
            elif "OFF" == json_data['state']:
                urlIpx += 'ClearR='
            urlIpx += relay.replace('r', '')
        # Reqete de commande à l'IPX
        requests.get(urlIpx, auth=(self.ipxLogin, self.ipxPassword))

    def run(self):
        """ Démarrage du service MQTT """
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(self.mqttHost, self.mqttPort, 60)
        client.loop_forever()
    
# Serveur HTTP
class Http(Thread):
    """ Thread chargé de distribuer des pages web """
    def __init__(self, httpPort):
        Thread.__init__(self)
        self.httpPort = httpPort

    def run(self):
        """ Démarrage du service web """
        server_address = ("", self.httpPort)

        server = http.server.HTTPServer
        handler = http.server.CGIHTTPRequestHandler
        handler.cgi_directories = ["/"]
        affichage = "Server up on port : ", self.httpPort
        print(affichage)

        httpd = server(server_address, handler)
        httpd.serve_forever()

# Création des threads
mqttd = Mqtt(mqttHost, mqttPort, mqttTopic, ipxHost, ipxApiKey, ipxLogin, ipxPassword)
httpd = Http(httpPort)

# Lancement des threads
mqttd.start()
httpd.start()
