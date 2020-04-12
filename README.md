# Ipx2Mqtt

Outil de conversion de l'API de l'IPX800 V4 vers MQTT et inversement pour Home Assistant. Permet d'utiliser les éléments de type 'light' et 'switch' à partir des relais de l'IPX ou des modules X8R ainsi que des modules XDimmer.

## Configuration

Pour chaque relai et dimmer, il faut configurer un push sur chaque entité de l'IPX avec l'URL de ce type :

- <http://ip_serveur:8080/light.py?uid=r17&etat=1> pour les lumières
- <http://ip_serveur:8080/switch.py?uid=r17&etat=1> pour les switch (prises commandées)

La configuration des entités peut se faire de 2 façons :

- Par le fichier de configuration (voir exemple)
- Par l'URL <http://ip_serveur:8080/init.py> qui va enregistrer dans MQTT la configuration

## Déploiement

Il y a deux solutions pour déployer la solution :

- Docker
- Exécuter le script python directement

### Docker

Je préfère cette solution car elle encapsule le processus et facilite le déploiemet.

### Python

Il faut récupérer le contenu du dossier [ipx](ipx) et le mettre sur votre futur serveur.

Les variables d'environnement sont optionnelles, elles possèdent une valeur par défaut. Ces variables d'environnement sont les suivantes :

- HTTP_PORT (8080 par défaut)
- MQTT_PORT (1883 par défaut)
- MQTT_HOST (localhost par défaut)
- MQTT_TOPIC (ipx par défaut)
- IPX_HOST (192.168.1.1 par défaut)
- IPX_API_KEY (apikey par défaut)
- IPX_LOGIN (admin par défaut)
- IPX_PASSWORD (password par défaut)

Chaque variable sera définie de cette manière :

``` sh
export ENV_VAR=valeur
```

Exécuter ensuite les lignes suivantes :

``` sh
pip install -r requirements.txt
chmod +x *.py
./server.py
```

## Todo list

- [x] Set brightness des XDimmer
- [x] Refactoring en classe Python
- [x] Initialisation des config dans MQTT
- [ ] Documentation - En cours
- [ ] Update le statut de l'IPX dans MQTT par reqête toutes les x secondes (optionnel)
- [ ] Gestion des volets roulant
- [ ] Utilisation d'un login/mot de passe pour le broker MQTT
