# État d’avancement du projet « Temps de Réponse Brigade des Pompiers de Londres »
## 1. Mise en place du projet

- Création du dépôt GitHub dédié au projet : `london-fire-response`.
- Initialisation de la structure de dossiers locale sur la VM :
  - `data/raw/incidents/` : pour les fichiers bruts incidents.
  - `data/raw/mobilisations/CSV_files` : pour les fichiers bruts mobilisations.
  - `data/raw/cleaned_data/` : pour les fichiers des données incidents et mobilisations nettoyés.
  - `notebooks/` : pour les notebooks Jupyter.
  - Téléchargement et placement des fichiers de données fournis par la Brigade des Pompiers de Londres dans les dossiers appropriés (incidents, mobilisations).
  - les fichiers xlsx ont été convertis en CSV pour une meilleure ingestion 

## 2. Gestion du versionnement avec Git et GitHub

- Initialisation du dépôt Git local.
- Connexion du dépôt local à GitHub via SSH.
- Installation et configuration de Git LFS (Large File Storage) pour gérer les fichiers volumineux (plus de 100 Mo).
- Push des fichiers volumineux vers GitHub via Git LFS avec succès.

## 3. Environnement de travail

 Option 1:
  - Tentative de création d’un environnement Conda pour gérer les dépendances Python.
  - Correction des erreurs liées à l’activation de l’environnement Conda (`conda init` ajouté dans `.bashrc`).
  - Recommandation et préparation à la création d’un environnement isolé nommé `london-fire-response` via un fichier `environment.yml`.
  - Les instrution de lancement de conda sont dans le fichier : `install_conda_env.sh`
Option 2:
  - Tentative de création d’un environnement virtuel venv pour gérer les dépendances Python.
  - Recommandation et préparation à la création d’un environnement isolé nommé via les instructions dans le ` requirements.txt`

## 4. Prochaines étapes prévues

- Réalisé : Création d’un notebook Jupyter (`notebooks/data_exploration.ipynb`) pour réaliser l’exploration initiale des données.
- réalisé : Installation et configuration de VSCode sur la VM pour travailler confortablement sur les notebooks et scripts.
- Lancement de l’exploration des données : import, visualisation, nettoyage, analyse descriptive.
=> Réalisé: chargement et nettoyage des données incidents et mobilisations via : notebooks\Ingestion
