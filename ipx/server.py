#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import os
from httpd import Http
from mqttd import Mqtt
from time import sleep

# Recuperation des variebles d'environnement
httpPort = int(os.getenv('HTTP_PORT', 8080))
mqttPort = int(os.getenv('MQTT_PORT', 1883))
mqttHost = os.getenv('MQTT_HOST', "localhost")
mqttTopic = os.getenv('MQTT_TOPIC', "ipx")
ipxHost = os.getenv("IPX_HOST", "192.168.1.1")
ipxApiKey = os.getenv("IPX_API_KEY", "apikey")
ipxLogin = os.getenv("IPX_LOGIN", "admin")
ipxPassword = os.getenv("IPX_PASSWORD", "password")

# Création des threads
mqttd = Mqtt(mqttHost, mqttPort, mqttTopic, ipxHost, ipxApiKey, ipxLogin, ipxPassword)
httpd = Http(httpPort)

# Lancement des threads
mqttd.start()
httpd.start()
