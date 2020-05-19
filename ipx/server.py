#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

from const import Constantes
from httpd import Httpd
from mqtt import Mqtt2Ipx
from mqtt import Mqtt

# Création des threads
httpd = Httpd()
mqtt2ipx = Mqtt2Ipx()

# Lancement des threads
httpd.start()
mqtt2ipx.start()
Mqtt.ipxPullStatus()

