Gestion de Tâches - Lancement Rapide

Ce projet permet de gérer des tâches via un serveur Python et plusieurs clients interactifs.

1️⃣ Sans Docker

Pour exécuter le projet directement sur votre machine :
Aller dans votre directore en utilisant cd + nom directoire
remplacer dans client.py le ligne 8
de def __init__(self, host="host.docker.internal", port=5000): en def __init__(self, host="127.0.0.1", port=5000):
et dans menu.py le ligne 4
de cli = ClientTaches(host="host.docker.internal", port=5000)   en cli = ClientTaches(host="172.0.0.1", port=5000)  

Lancer le serveur

Ouvrir un terminal dans le dossier du projet :

python serveur.py


Lancer le client/menu interactif

Dans un autre terminal :

python menu.py


Le menu client permet d’ajouter, lister, supprimer et changer le statut des tâches.
Vous pouvez lancer plusieurs clients sur votre machine pour simuler plusieurs utilisateurs.

2️⃣ Avec Docker (sans Compose)

Assurez-vous que le client se connecte au serveur via host.docker.internal dans client.py.

Construire les images
docker build -t serveur_taches -f Dockerfile.serveur .
docker build -t client_taches -f Dockerfile.client .

Lancer le serveur
docker run -it -p 5000:5000 --name serveur_taches serveur_taches

Lancer plusieurs clients interactifs
docker run -it --rm --name client1 client_taches
docker run -it --rm --name client2 client_taches
docker run -it --rm --name client3 client_taches


Les clients se connectent automatiquement au serveur.
Les conteneurs clients sont supprimés automatiquement à la fermeture grâce à --rm.

Arrêter et supprimer le serveur
docker stop serveur_taches
docker rm serveur_taches

3️⃣ Avec Docker Compose

Construire et lancer tous les services (serveur + plusieurs clients) :

docker compose up --build


Attacher à un client interactif :

docker attach client1
docker attach client2
docker attach client3


Détacher sans arrêter : CTRL + P → CTRL + Q

Arrêter et supprimer tous les services :

docker compose down

Notes importantes

Serveur : écoute toutes les interfaces (0.0.0.0) sur le port 5000.

Client :

host="127.0.0.1" pour exécution sans Docker

host="serveur" pour Docker Compose

host="host.docker.internal" pour Docker sans Compose

Tous les clients partagent la même liste de tâches sur le serveur.
# Workflow Git du projet

- Création des branches : main, dev, feature/serveur, feature/client, feature/docker
- Développement isolé sur les branches feature/*
- Pull Requests ouvertes vers dev
- Fusion de dev vers main
- Tag v1.0.0 pour version stable
