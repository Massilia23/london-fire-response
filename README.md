# 🔥 London Fire Brigade 

## 🎯 Objectif
Le projet porte sur l’analyse des incidents et mobilisations des services de la brigade des pompiers de Londres.
L’idée est de comprendre comment ces interventions sont gérées, d’identifier des schémas de mobilisation (temps de réponse, distribution géographique, nature des incidents...) et éventuellement prédire ou améliorer l’efficacité opérationnelle.

Ce projet s’inscrit dans le cadre du cursus Data Scientist et a pour but de produire :
- Un rapport d'exploration et de visualisation des données ' pas sur de ça'
- Un rapport de modélisation
- Un rapport final accompagné du code
- Un streamlit de présentation 

## 📁 Arborescence actuelle du projet

LONDON-FIRE-RESPONSE/
├── .venv/
├── data/
│   ├── raw/
│   └── Cleaned_data/
│       ├── InUSE/
│       └── OLD/
├── incidents/
├── mobilisations/
│   ├── CSV_files/
│   └── xlsx_files/
├── docs/
│   └── README_progress.md
├── notebooks/
│   ├── exploration/
│   │   └── data-exploration_initiale.ipynb
│   └── Ingestion/
│       ├── chargement_incidents.ipynb
│       └── chargement_mobilisations.ipynb
├── models/
├── .gitattributes
├── .gitignore
├── environment.yml
├── install_conda_env.sh
├── README.md
└── requirements.txt

## 📊 Données

Les données utilisées sont fournies par la ville de Londres :

- **Incidents** :  
  https://data.london.gov.uk/dataset/london-fire-brigade-incident-records

- **Mobilisations** :  
  https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records

## 🛠 Technologies utilisées

- Python 3.x
- Git / GitHub
- Git LFS (pour les fichiers volumineux)
- Pandas, NumPy, Matplotlib, Seaborn 
- Jupyter Notebook 

## 🚧 État d’avancement

- [x] Création du dépôt et initialisation Git
- [x] Téléchargement des fichiers incidents et mobilisations
- [x] Mise en place de Git LFS pour gérer les fichiers > 100 Mo
- [x] Prétraitement des données
- [x] Analyse exploratoire
- [ ] Visualisations
- [ ] Modélisation et prédictions
- [ ] Rédaction des rapports

## 📌 Auteur

Massilia BAKHOUCHE 
