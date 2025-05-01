# DEVBOOK - Conversion de MBA Global Insights en application web

## Objectif
Convertir l'application MBA Global Insights de Tkinter vers Streamlit pour faciliter le partage, tout en gardant une structure compacte et lisible.

## Architecture simplifiée
- **Un seul fichier principal** : `mba_insights_web.py` contenant toute la logique
- **Pas de structure complexe** ni de multiples fichiers
- **Organisation par sections fonctionnelles** dans le code

## Avantages de cette approche
- **Simplicité de déploiement** : un seul fichier à exécuter
- **Facilité de maintenance** : tout le code au même endroit
- **Clarté pour les utilisateurs** : structure simple à comprendre

## Comment lancer l'application
```bash
# Dans l'environnement virtuel
streamlit run mba_insights_web.py
```

## Organisation du code (dans un seul fichier)
1. Configuration de l'application
2. Fonctions utilitaires
3. Sections pour chaque onglet :
   - Classement FT
   - Motivations des Candidats
   - Tendances Mondiales
   - Simulateur de Classement

## Migration des données
Toutes les données et visualisations du projet original sont conservées avec une mise en forme adaptée à Streamlit.
