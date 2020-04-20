#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import os

class Constantes():
    
    # Recuperation des variables d'environnement
    httpPort = int(os.getenv('HTTP_PORT', 8080))
    mqttPort = int(os.getenv('MQTT_PORT', 1883))
    mqttHost = os.getenv('MQTT_HOST', "localhost")
    mqttTopic = os.getenv('MQTT_TOPIC', "ipx")
    mqttUser = os.getenv('MQTT_USER')
    mqttPassword = os.getenv('MQTT_PASSWORD')
    ipxHost = os.getenv("IPX_HOST", "192.168.1.1")
    ipxApiKey = os.getenv("IPX_API_KEY", "apikey")
    ipxLogin = os.getenv("IPX_LOGIN", "admin")
    ipxPassword = os.getenv("IPX_PASSWORD", "password")
    ipxPullStatus = int(os.getenv("IPX_PULL_STATUS", 0))
    ipxDimmerLightStatus = os.getenv("IPX_DIMMER")
    ipxRelayLightStatus = os.getenv("IPX_RELAY_LIGHT")
    ipxRelaySwitchStatus = os.getenv("IPX_RELAY_SWITCH")
