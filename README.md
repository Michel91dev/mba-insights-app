# MBA Global Insights - Application d'Analyse Interactive

## Description
Application d'analyse interactive des MBA mondiaux permettant d'explorer les classements, les motivations des candidats, les tendances mondiales et de simuler des scores de classement.

L'application est disponible en deux versions :
- **Version Desktop** : Interface graphique avec Tkinter
- **Version Web** : Application web avec Streamlit pour un partage facilité

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
pip install -r requirements.txt
```

## Utilisation

### Version Desktop
```bash
python mba_insights_app.py
```

### Version Web
```bash
streamlit run mba_insights_web.py
```

## Déploiement Web
L'application web peut être facilement déployée sur Streamlit Cloud :

1. Créez un compte sur [Streamlit Cloud](https://streamlit.io/cloud)
2. Connectez votre compte GitHub
3. Sélectionnez ce dépôt et le fichier `mba_insights_web.py`
4. Votre application sera automatiquement déployée et accessible publiquement

## Auteur
Michel S.

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
© 2025 Michel Safars ©
