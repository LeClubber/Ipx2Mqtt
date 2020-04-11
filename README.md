# Ipx2Mqtt

Outil de conversion de l'API de l'IPX800 V4 vers MQTT et inversement pour Home Assistant. Permet d'utiliser les éléments de type 'light' et 'switch' à partir des relais de l'IPX ou des modules X8R ainsi que des modules XDimmer.

Pour chaque relai et dimmer, il faut configurer un push sur chaque entité de l'IPX avec l'URL de ce type :

- <http://ip_serveur:8080/light.py?uid=r17&etat=1> pour les lumières
- <http://ip_serveur:8080/switch.py?uid=r17&etat=1> pour les switch (prises commandées)

La configuration des entités peut se faire de 2 façons :

- Par le fichier de configuration (voir exemple)
- Par l'URL <http://ip_serveur:8080/init.py> qui va enregistrer dans MQTT la configuration

RAF:

- [x] Set brightness des XDimmer
- [x] Refactoring en classe Python
- [x] Initialisation des config dans MQTT
- [ ] Documentation - En cours
- [ ] Gestion des volets roulant
- [ ] Utilisation d'un login/mot de passe pour le broker MQTT
