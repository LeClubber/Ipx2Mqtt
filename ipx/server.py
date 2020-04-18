#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

from httpd import Http
from mqttd import Mqtt

# Création des threads
mqttd = Mqtt()
httpd = Http()

# Lancement des threads
mqttd.start()
httpd.start()
