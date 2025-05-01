# MBA Global Insights - Application d'Analyse Interactive

## Description
Application d'analyse interactive des MBA mondiaux permettant d'explorer les classements, les motivations des candidats, les tendances mondiales et de simuler des scores de classement.

## Fonctionnalités
- Visualisation du classement Financial Times et de sa méthodologie
- Analyse des motivations des candidats MBA
- Exploration des tendances mondiales par région
- Simulateur de classement interactif

## Prérequis
- Python 3.11+ (via Homebrew)
- Environnement virtuel (.venv)

## Installation

### 1. Cloner le dépôt
```bash
git clone [URL_DU_DEPOT]
cd [NOM_DU_DOSSIER]
```

### 2. Créer et activer l'environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -e .
```

## Utilisation
Exécutez l'application avec la commande suivante :
```bash
python mba_insights_app.py
```

## Structure du projet
```
projet/
├── mba_insights_app.py  # Application principale
├── pyproject.toml       # Configuration du projet
└── README.md            # Documentation
```

## Développement
Ce projet suit les règles de développement définies dans le document "Règles Globales de Développement 2025 0101", notamment :
- Code et documentation en français
- Type hints partout
- Tests unitaires avec pytest
- Formatage avec Black
- Vérification statique avec MyPy

## Licence
© 2025 MBA Global Insights - Tous droits réservés
