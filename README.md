# Bienvenue dans le Projet

## Suivez les étapes ci-dessous pour cloner le dépôt, construire et exécuter l'application à l'aide de Docker Compose.

## Étapes d'Installation

### Cloner le dépôt

Ouvrez votre terminal et exécutez la commande suivante pour cloner le dépôt :

```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_REPERTOIRE>
```

### Construire et lancer les conteneurs avec Docker Compose

Exécutez la commande suivante pour construire les images et démarrer les conteneurs :

```bash
docker compose up --build
```

### Modifier le port (si nécessaire)

Si vous souhaitez utiliser un port différent, ouvrez le fichier .env et modifiez la variable PORT :

```env
PORT=Votre_Port_Souhaité
```

### Accéder à l'application

Une fois les conteneurs démarrés, ouvrez votre navigateur et allez à l'adresse suivante :

```
http://localhost:{port}
```

Remplacez {port} par le numéro de port que vous avez défini dans le fichier .env.

### Accéder à Swagger

Pour consulter la documentation Swagger de l'API, rendez-vous à l'adresse suivante :

```
http://localhost:{port}/swagger
```

## Remarques

- Assurez-vous d'avoir Docker installé sur votre machine.
- Si vous rencontrez des problèmes lors du démarrage des conteneurs, vérifiez que le port choisi n'est pas déjà utilisé par une autre application.
