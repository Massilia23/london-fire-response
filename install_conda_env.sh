#!/bin/bash

# Script pour créer l'environnement conda london-fire-response

# Affichage du nom du script
echo "📦 Installation de l'environnement conda 'london-fire-response'..."

# Vérifie si conda est installé
if ! command -v conda &> /dev/null
then
    echo "❌ Conda n'est pas installé. Installe Miniconda ou Anaconda d'abord."
    exit 1
fi

# Création de l'environnement
conda env create -f environment.yml

# Initialisation conda pour bash (utile si 'conda activate' ne fonctionne pas)
echo "🔧 Initialisation de conda pour bash..."
conda init bash

echo "✅ Environnement créé. Redémarre ton terminal ou exécute : 'source ~/.bashrc'"
echo "➡️ Ensuite active l'environnement avec : conda activate london-fire-response"

