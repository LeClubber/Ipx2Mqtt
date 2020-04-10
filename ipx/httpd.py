#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jérémy BRAUD

import http.server
from threading import Thread

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
