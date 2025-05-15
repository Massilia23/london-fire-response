#!/bin/bash

# Définir le chemin d'installation de Miniconda
CONDA_DIR="$HOME/miniconda"

# Télécharger Miniconda automatiquement
echo "🔽 Téléchargement de Miniconda..."
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh

# Installer silencieusement
echo "⚙️ Installation de Miniconda dans $CONDA_DIR..."
bash /tmp/miniconda.sh -b -p "$CONDA_DIR"

# Initialiser conda
eval "$($CONDA_DIR/bin/conda shell.bash hook)"

# Ajouter conda au PATH
export PATH="$CONDA_DIR/bin:$PATH"

# Mettre à jour conda
echo "🔄 Mise à jour de conda..."
conda update -y -n base -c defaults conda

# Créer l’environnement conda à partir du fichier YAML
echo "📦 Création de l'environnement conda depuis environment.yml..."
conda env create -f environment.yml

echo "✅ Installation terminée ! Activez l'environnement avec :"
echo "   conda activate london-fire-response"
