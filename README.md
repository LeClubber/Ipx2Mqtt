# Ipx2Mqtt

Outil de conversion de l'API de l'IPX800 V4 vers MQTT et inversement pour Home Assistant. Permet d'utiliser les éléments de type 'light' et 'switch' à partir des relais de l'IPX ou des modules X8R ainsi que des modules XDimmer.

## Configuration

Pour chaque relai et dimmer, il faut configurer un push sur chaque entité de l'IPX avec l'URL de ce type :

- <http://ip_serveur:8080/light.py?uid=r17&etat=1> pour les lumières
- <http://ip_serveur:8080/switch.py?uid=r17&etat=1> pour les switch (prises commandées)

Le paramètre uid correspond à l'id donné au relai. Il correspont de r01 à r56 aux 56 relais possible de l'IPX, et de d1c1 à d4c4 pour les XDimmer (dimmer n°1 et channel n°1 au dimmer n°4 et channel n°4). L'état est à 0 pour éteint et 1 pour allumé.

La configuration des entités peut se faire de 2 façons :

- Par le fichier de configuration [configuration.yaml](configuration.yaml) (voir exemple light)
- Par l'URL <http://ip_serveur:8080/init.py> qui va enregistrer dans MQTT la configuration

## Déploiement

Il vous faut :

- Home-Assistant (en même temps, vous êtes surtout là pour lui non?)
- Un brocker (serveur) MQTT (non sécurisé, sans login/mot de passe pour l'instant)
- Le service Ipx2Mqtt

Il y a deux solutions pour déployer ce cervice :

- Docker (recommandé)
- Exécuter le script python directement

### Docker

Je préfère cette solution car elle encapsule le processus, contient toutes les dépendances  et facilite le déploiement.

Le service peut être démarré grâce à la commande suivante :

``` sh
docker run -d --name ipx -p 8080:8080 \
    -e IPX_HOST=192.168.1.1 \
    -e IPX_API_KEY=apikey \
    -e IPX_LOGIN=admin \
    -e IPX_PASSWORD=password \
    leclubber/ipx2mqtt
```

Ou en docker-compose (recommandé) :

``` sh
version: '3'
services:
  ipx:
    container_name: ipx
    image: leclubber/ipx2mqtt
    ports:
      - 8080:8080
    environment:
      - IPX_HOST=192.168.1.1
      - IPX_API_KEY=apikey
      - IPX_LOGIN=admin
      - IPX_PASSWORD=password
```

Les variables d'environnement sont optionnelles, elles possèdent une valeur par défaut. Ces variables d'environnement sont les suivantes :

- HTTP_PORT (8080 par défaut)
- MQTT_PORT (1883 par défaut)
- MQTT_HOST (localhost par défaut)
- MQTT_TOPIC (ipx par défaut)
- IPX_HOST (192.168.1.1 par défaut)
- IPX_API_KEY (apikey par défaut)
- IPX_LOGIN (admin par défaut)
- IPX_PASSWORD (password par défaut)

Un fichier [docker-compose.yml](docker-compose.yml) est disponible pour exemple, avec toutes les variables d'environnement ainsi que les services homeassistant et mqtt.

Une fois votre fichier docker-compose.yml réalisé, il faut lancer la commande suivante pour démarrer le ou les services configurés :

``` sh
docker-compose up -d
```

### Python

Il faut récupérer le contenu du dossier [ipx](ipx) et le mettre sur votre futur serveur.

Les variables d'environnement sont optionnelles, elles possèdent une valeur par défaut (voir section Docker).
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
- [ ] Update le statut de l'IPX dans MQTT par requête toutes les x secondes (optionnel)
- [ ] Gestion des volets roulant
- [ ] Utilisation d'un login/mot de passe pour le broker MQTT
