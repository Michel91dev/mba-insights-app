# -*- coding: utf-8 -*-
"""
MBA Global Insights - Application Web
Version Streamlit de l'application d'analyse interactive des MBA
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import base64
from typing import List, Dict, Tuple, Optional, Union, Any, Callable
import matplotlib
matplotlib.use('Agg')  # Nécessaire pour l'utilisation sans interface graphique

# -----------------------------------------------------------------------------
# Configuration de la page et constantes
# -----------------------------------------------------------------------------

# Couleurs
COULEUR_PRINCIPALE = "#1a5276"    # Bleu foncé professionnel
COULEUR_SECONDAIRE = "#2980b9"    # Bleu plus clair
COULEUR_ACCENT = "#f39c12"        # Orange pour l'accent
COULEUR_TECHNO = "#27ae60"        # Vert pour la technologie
COULEUR_FOND = "#f0f0f0"          # Fond gris clair

# Configuration pour la traduction
if 'langue' not in st.session_state:
    st.session_state.langue = 'fr'  # Par défaut en français

# Configuration de la page
st.set_page_config(
    page_title="MBA Global Insights - Analyse Interactive",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Personnalisation du style CSS
def appliquer_style() -> None:
    """Applique le style CSS personnalisé à l'application."""
    st.markdown(f"""
    <style>
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        h1, h2, h3 {{
            color: {COULEUR_PRINCIPALE};
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 24px;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 16px;
            background-color: #f0f0f0;
            font-weight: 600;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COULEUR_PRINCIPALE} !important;
            color: white !important;
        }}
        .stTabs [data-baseweb="tab-highlight"] {{
            background-color: {COULEUR_PRINCIPALE};
        }}
        div[data-testid="stExpander"] details summary p {{
            font-size: 1.1rem;
            font-weight: 600;
        }}
        div.stButton > button:first-child {{
            background-color: {COULEUR_PRINCIPALE};
            color: white;
            font-weight: 600;
        }}
        div.stButton > button:hover {{
            background-color: {COULEUR_SECONDAIRE};
            color: white;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            color: {COULEUR_PRINCIPALE};
        }}
        .footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: {COULEUR_PRINCIPALE};
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 0.8rem;
        }}
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Fonctions utilitaires
# -----------------------------------------------------------------------------

def creer_graphique_camembert(categories: List[str], valeurs: List[float],
                           couleurs: List[str], titre: str = "") -> plt.Figure:
    """
    Crée un graphique en camembert avec matplotlib.

    Args:
        categories: Liste des noms de catégories
        valeurs: Liste des valeurs correspondantes
        couleurs: Liste des couleurs pour chaque catégorie
        titre: Titre optionnel du graphique

    Returns:
        Figure matplotlib
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(COULEUR_FOND)

    # Créer le graphique
    wedges, texts, autotexts = ax.pie(valeurs, labels=categories, autopct='%1.1f%%',
                                    startangle=90, colors=couleurs)

    # Configurer les polices
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=12)

    # Égaliser l'aspect du graphique
    ax.axis('equal')

    # Ajouter le titre si spécifié
    if titre:
        ax.set_title(titre, fontsize=14, pad=20)

    # Appliquer tight_layout pour ajuster les marges
    fig.tight_layout()

    return fig

def creer_graphique_barres(categories: List[str], valeurs: List[float],
                         couleur: str, titre: str, axe_y: str) -> plt.Figure:
    """
    Crée un graphique à barres avec matplotlib.

    Args:
        categories: Liste des noms de catégories
        valeurs: Liste des valeurs correspondantes
        couleur: Couleur des barres
        titre: Titre du graphique
        axe_y: Libellé de l'axe Y

    Returns:
        Figure matplotlib
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(COULEUR_FOND)

    # Créer le graphique à barres
    bars = ax.bar(categories, valeurs, color=couleur)

    # Ajouter les valeurs au-dessus des barres
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
               f'{int(height)}%', ha='center', va='bottom',
               fontweight='bold', fontsize=10)

    # Configurer le graphique
    ax.set_ylim(0, 100)
    ax.set_ylabel(axe_y, fontsize=12)
    ax.set_title(titre, fontsize=14, pad=15)
    ax.tick_params(axis='both', labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Ajuster l'espacement du graphique
    fig.tight_layout()

    return fig

def creer_graphique_radar(categories: List[str], valeurs: List[float],
                        couleur: str) -> plt.Figure:
    """
    Crée un graphique radar (ou "toile d'araignée") avec matplotlib.

    Args:
        categories: Liste des noms de catégories
        valeurs: Liste des valeurs correspondantes
        couleur: Couleur de remplissage du radar

    Returns:
        Figure matplotlib
    """
    # Calculer le nombre d'angles égaux pour notre graphique
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Fermer le graphique en revenant au premier point

    # Normaliser les valeurs entre 0 et 1 pour un radar uniforme
    valeurs_normalisees = [v / 100 for v in valeurs]
    valeurs_normalisees += valeurs_normalisees[:1]  # Fermer le graphique

    # Créer la figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(COULEUR_FOND)

    # Tracer les polygones
    ax.fill(angles, valeurs_normalisees, color=couleur, alpha=0.25)
    ax.plot(angles, valeurs_normalisees, color=couleur, linewidth=2, linestyle='solid')

    # Ajouter les étiquettes
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)

    # Configurer le graphique
    ax.set_yticklabels([])  # Cacher les étiquettes d'échelle
    ax.grid(True)

    return fig

# -----------------------------------------------------------------------------
# Gestion de la traduction
# -----------------------------------------------------------------------------

# Dictionnaire de traductions
translations = {
    'fr': {
        # Titres et descriptions générales
        'titre_app': "MBA GLOBAL INSIGHTS",
        'description_app': "Explorez les tendances et classements des MBA internationaux à travers des visualisations interactives.",
        
        # Onglets
        'tab_classement': "Classement FT",
        'tab_motivations': "Motivations des Candidats",
        'tab_tendances': "Tendances Mondiales",
        'tab_simulateur': "Simulateur de Classement",
        'tab_references': "Références & Explications",
        
        # Technologie
        'tech_impact_titre': "Impact de la Technologie sur les MBA",
        'tech_impact_desc': "Analyse de l'évolution de la composante technologique dans les programmes MBA internationaux.",
        'tech_tendances': "Tendances Tech & IA dans les MBA en 2025",
        'tech_curriculum': "La technologie devient un élément central des programmes MBA",
        'tech_specialisation': "Spécialisations Tech & IA en forte croissance",
        'tech_competences': "Compétences technologiques recherchées",
        'tech_carriere': "Nouvelles opportunités de carrière",
        'tech_detail_1': "Les programmes MBA intègrent l'IA et la technologie au cœur du curriculum",
        'tech_detail_2': "Les écoles de commerce développent des spécialisations en IA pour répondre aux besoins du marché",
        'tech_detail_3': "La maîtrise des données et de l'IA devient essentielle pour les diplômés MBA",
        'tech_detail_4': "Les carrières tech post-MBA offrent des rémunérations 25% supérieures à la moyenne",
        
        # Pied de page
        'copyright': "© 2025 Michel Safars",
    },
    'en': {
        # General titles and descriptions
        'titre_app': "MBA GLOBAL INSIGHTS",
        'description_app': "Explore international MBA trends and rankings through interactive visualizations.",
        
        # Tabs
        'tab_classement': "FT Ranking",
        'tab_motivations': "Candidate Motivations",
        'tab_tendances': "Global Trends",
        'tab_simulateur': "Ranking Simulator",
        'tab_references': "References & Explanations",
        
        # Technology
        'tech_impact_titre': "Technology Impact on MBA Programs",
        'tech_impact_desc': "Analysis of technological component evolution in international MBA programs.",
        'tech_tendances': "Tech & AI Trends in MBA Programs in 2025",
        'tech_curriculum': "Technology becomes a core element of MBA curricula",
        'tech_specialisation': "Tech & AI specializations growing rapidly",
        'tech_competences': "In-demand technological skills",
        'tech_carriere': "New career opportunities",
        'tech_detail_1': "MBA programs integrate AI and technology at the heart of the curriculum",
        'tech_detail_2': "Business schools are developing AI specializations to meet market needs",
        'tech_detail_3': "Data and AI proficiency becomes essential for MBA graduates",
        'tech_detail_4': "Post-MBA tech careers offer salaries 25% higher than average",
        
        # Footer
        'copyright': "© 2025 Michel Safars",
    }
}

def traduire(cle: str) -> str:
    """Traduit une clé selon la langue sélectionnée."""
    langue = st.session_state.langue
    if cle in translations[langue]:
        return translations[langue][cle]
    return cle  # Retourne la clé si aucune traduction n'est trouvée

def image_drapeau(code_pays: str) -> str:
    """Génère une image en base64 du drapeau pour l'affichage dans Streamlit."""
    if code_pays == 'fr':
        # Drapeau français
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAALCAYAAAB24g05AAAABmJLR0QA/wD/AP+gvaeTAAAAPElEQVQokWNgGAXEAEYGBob/FBj0H10TIwMDwwlSDQAZgmIIKS6gKQATiBKEJkm0AcRGI9EGoAcn9QAAoBQJ/wWt7D0AAAAASUVORK5CYII="
    else:
        # Drapeau anglais
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAALCAYAAAB24g05AAAABmJLR0QA/wD/AP+gvaeTAAAApElEQVQokcWQsQrCQBBEZ79ASBG0URtB8H9S28XGzsbKxsLCX0gC32UdmBDk9BK0cJrdu7c7bEgA4IgORZyQCeV1y0rDlS2vJkhcOJCjB/uVs3J7NltRBjNgEtFLWYE5MAOsAF9IKXXgR1BAU4I/GMOyuCWoA2YxCmyBfdxlHVgCU8k3yTtGI8ldnQQkh4hOJUfJZ8lB9jP2MzBBZB/R/Qdo4feDG1iWOvKxkn5wAAAAAElFTkSuQmCC"

def selecteur_langue() -> None:
    """Affiche un sélecteur de langue avec des drapeaux."""
    col1, col2, col3 = st.columns([0.89, 0.055, 0.055])
    
    with col2:
        fr_img = image_drapeau('fr')
        if st.image(fr_img, width=30, output_format="AUTO"):
            st.session_state.langue = 'fr'
    
    with col3:
        en_img = image_drapeau('en')
        if st.image(en_img, width=30, output_format="AUTO"):
            st.session_state.langue = 'en'

# -----------------------------------------------------------------------------
# Interface principale
# -----------------------------------------------------------------------------

def afficher_entete() -> None:
    """Affiche l'en-tête de l'application avec le titre principal et le sélecteur de langue."""
    # Afficher le sélecteur de langue
    selecteur_langue()
    
    # Afficher le titre principal
    st.markdown(f"""
    <div style="background-color: {COULEUR_PRINCIPALE}; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center; margin: 0;">{traduire('titre_app')}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher la description
    st.markdown(traduire('description_app'))

def afficher_pied_de_page() -> None:
    """Affiche le pied de page de l'application."""
    st.markdown(f"""
    <div class="footer">
        {traduire('copyright')}
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Contenu des onglets
# -----------------------------------------------------------------------------

def onglet_classement_ft() -> None:
    """Affiche le contenu de l'onglet Classement FT."""
    st.header("Classement Financial Times des MBA")

    st.markdown("""
    Découvrez comment le prestigieux classement du Financial Times évalue les programmes MBA dans le monde.
    Le classement FT est l'un des plus respectés et se base sur une combinaison de critères.
    """)

    # Créer des colonnes pour la mise en page
    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("Composition du classement")

        # Données pour le graphique
        categories = ['Critères Alumni', 'Données Écoles', 'Recherche']
        valeurs = [56, 34, 10]
        couleurs = [COULEUR_SECONDAIRE, COULEUR_ACCENT, '#27ae60']

        # Créer et afficher le graphique
        fig = creer_graphique_camembert(categories, valeurs, couleurs)
        st.pyplot(fig)

    with col2:
        # Afficher les détails des critères dans des expandeurs
        with st.expander("Critères Alumni (56%)", expanded=True):
            alumni_criteria = [
                "Salaire moyen pondéré (16%)",
                "Augmentation de salaire (16%)",
                "Rapport qualité-prix (5%)",
                "Progression de carrière (3%)",
                "Réalisation des objectifs (4%)",
                "Réseau d'anciens élèves (4%)"
            ]
            for criterion in alumni_criteria:
                st.markdown(f"• {criterion}")

        with st.expander("Critères Écoles (34%)", expanded=True):
            school_criteria = [
                "Diversité de genre",
                "Diversité internationale",
                "Mobilité internationale",
                "Expérience internationale",
                "Professeurs avec doctorat",
                "Critères ESG"
            ]
            for criterion in school_criteria:
                st.markdown(f"• {criterion}")

        with st.expander("Recherche (10%)", expanded=True):
            research_criteria = [
                "Articles publiés par les professeurs",
                "Qualité de la recherche",
                "Impact des publications"
            ]
            for criterion in research_criteria:
                st.markdown(f"• {criterion}")

    # Ajouter un tableau des 10 meilleures écoles
    st.subheader("Top 10 des MBA mondiaux (2025)")

    top_schools = {
        "Rang": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "École": ["Harvard Business School", "INSEAD", "Stanford GSB", "Wharton", "London Business School",
                "Columbia Business School", "MIT Sloan", "HEC Paris", "Booth (Chicago)", "IESE Business School"],
        "Pays": ["États-Unis", "France/Singapour", "États-Unis", "États-Unis", "Royaume-Uni",
                "États-Unis", "États-Unis", "France", "États-Unis", "Espagne"],
        "Score": [100, 98, 96, 94, 92, 90, 89, 87, 86, 85]
    }

    st.dataframe(top_schools, use_container_width=True)

def onglet_motivations_candidats() -> None:
    """Affiche le contenu de l'onglet Motivations des Candidats."""
    st.header("Principales Motivations des Candidats MBA")

    st.markdown("""
    Découvrez pourquoi les étudiants du monde entier choisissent de poursuivre un MBA.
    Les données montrent que les motivations varient mais se concentrent autour de quelques thèmes clés.
    """)

    # Créer le graphique des motivations
    motivations = ['Progression\nde carrière', 'Augmentation\nsalariale',
                  'Réseau\nprofessionnel', 'Compétences\nmanagériales',
                  'Changement\nde secteur', 'Entrepreneuriat']
    percentages = [85, 70, 65, 60, 45, 30]

    fig = creer_graphique_barres(
        motivations,
        percentages,
        COULEUR_SECONDAIRE,
        'Principales motivations pour faire un MBA',
        'Pourcentage de candidats (%)'
    )
    st.pyplot(fig)

    # Détails des motivations
    st.subheader("Détails des motivations")

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Développement Professionnel", expanded=True):
            st.markdown("""
            • Progression vers des postes de direction
            • Acquisition de compétences stratégiques
            • Préparation au leadership global
            • Développement de la pensée critique
            """)

        with st.expander("Développement Personnel", expanded=True):
            st.markdown("""
            • Construction d'un réseau international
            • Développement de la confiance en soi
            • Exposition à de nouvelles cultures
            • Acquisition de compétences relationnelles
            """)

    with col2:
        with st.expander("Changement de Carrière", expanded=True):
            st.markdown("""
            • Transition vers un nouveau secteur
            • Préparation à l'entrepreneuriat
            • Accès à de nouvelles opportunités
            • Positionnement pour les rôles internationaux
            """)

        with st.expander("Retour sur Investissement", expanded=True):
            st.markdown("""
            • Augmentation du potentiel de revenu
            • Accélération de la progression de carrière
            • Accès aux meilleures entreprises
            • Sécurisation des postes de direction
            """)

    # Témoignages
    st.subheader("Témoignages d'Anciens Étudiants")

    testimonials = [
        {
            "name": "Sophie Moreau",
            "school": "HEC Paris",
            "quote": "Mon MBA m'a permis de passer du conseil à la direction stratégique dans la tech, doublant mon salaire en deux ans."
        },
        {
            "name": "Thomas Leroy",
            "school": "INSEAD",
            "quote": "Le réseau international que j'ai développé pendant mon MBA a été crucial pour lancer ma startup avec des partenaires de trois continents."
        },
        {
            "name": "Emma Chen",
            "school": "London Business School",
            "quote": "Les compétences en leadership acquises pendant mon MBA m'ont préparée à gérer des équipes multiculturelles dans un contexte international."
        }
    ]

    cols = st.columns(len(testimonials))
    for i, (col, testimonial) in enumerate(zip(cols, testimonials)):
        with col:
            st.markdown(f"""
            <div style="background-color: white; padding: 15px; border-radius: 5px; height: 200px; border-left: 5px solid {COULEUR_PRINCIPALE};">
                <p style="font-style: italic;">"{testimonial['quote']}"</p>
                <p style="text-align: right; font-weight: bold; margin-bottom: 0;">{testimonial['name']}</p>
                <p style="text-align: right; font-size: 0.8rem; margin-top: 0;">{testimonial['school']}</p>
            </div>
            """, unsafe_allow_html=True)

def onglet_tendances_mondiales() -> None:
    """Affiche le contenu de l'onglet Tendances Mondiales."""
    st.header("Tendances Mondiales des MBA")
    st.markdown("Analyse des tendances actuelles dans les programmes MBA par région du monde et leur évolution au fil du temps.")
    
    # Mise en valeur de la composante technologique
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 5px solid {COULEUR_TECHNO}; margin: 20px 0;">
        <h3 style="color: {COULEUR_TECHNO}; margin-top: 0;">L'IA et les technologies transforment les MBA</h3>
        <p>Les écoles de commerce du monde entier intègrent de plus en plus les technologies de pointe dans leurs programmes MBA. Wharton, Harvard, INSEAD, HEC Paris et LBS sont en tête de cette transformation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Créer des onglets pour les régions
    region_tabs = st.tabs(["Amérique du Nord", "Europe", "Asie", "Reste du monde"])

    with region_tabs[0]:  # Amérique du Nord
        st.subheader("Tendances en Amérique du Nord")

        st.markdown("""
        **Tendances principales :**

        • Intégration de l'IA et de l'analytique dans les programmes
        • Programmes spécialisés en technologie et innovation
        • Accent accru sur l'entrepreneuriat et les startups
        • Flexibilité des formats d'apprentissage (hybride, en ligne, à temps partiel)
        • Initiatives renforcées pour la diversité et l'inclusion
        """)

        # Statistiques pour l'Amérique du Nord
        col1, col2, col3 = st.columns(3)
        col1.metric("Durée moyenne MBA", "20 mois", "-2 mois vs 2020")
        col2.metric("Coût moyen", "$150,000", "+12% vs 2020")
        col3.metric("ROI médian", "4.2 ans", "-0.5 an vs 2020")

    with region_tabs[1]:  # Europe
        st.subheader("Tendances en Europe")

        st.markdown("""
        **Tendances principales :**

        • Leadership en durabilité et critères ESG
        • Programmes plus courts (12-15 mois) et plus intensifs
        • Internationalisation accrue des promotions
        • Développement de partenariats inter-écoles européennes
        • Focus croissant sur l'impact social et sociétal
        """)

        # Statistiques pour l'Europe
        col1, col2, col3 = st.columns(3)
        col1.metric("Durée moyenne MBA", "12 mois", "-1 mois vs 2020")
        col2.metric("Coût moyen", "€80,000", "+8% vs 2020")
        col3.metric("ROI médian", "3.8 ans", "-0.3 an vs 2020")

    with region_tabs[2]:  # Asie
        st.subheader("Tendances en Asie")

        st.markdown("""
        **Tendances principales :**

        • Croissance rapide des programmes locaux de haute qualité
        • Partenariats stratégiques avec les entreprises technologiques
        • Accent sur l'innovation et l'application pratique
        • Développement de modèles de leadership spécifiquement asiatiques
        • Expansion des campus satellites d'écoles occidentales
        """)

        # Statistiques pour l'Asie
        col1, col2, col3 = st.columns(3)
        col1.metric("Durée moyenne MBA", "16 mois", "-1 mois vs 2020")
        col2.metric("Coût moyen", "$90,000", "+20% vs 2020")
        col3.metric("ROI médian", "3.2 ans", "-0.7 an vs 2020")

    with region_tabs[3]:  # Reste du monde
        st.subheader("Tendances dans le reste du monde")

        st.markdown("""
        **Tendances principales :**

        • Développement de programmes adaptés aux besoins des marchés locaux
        • Croissance des MBA en ligne pour plus d'accessibilité
        • Focus sur les problématiques propres aux économies émergentes
        • Partenariats public-privé pour le financement des études
        • Montée de l'entrepreneuriat social et de l'innovation à impact
        """)

        # Statistiques pour le reste du monde
        col1, col2, col3 = st.columns(3)
        col1.metric("Durée moyenne MBA", "18 mois", "-1 mois vs 2020")
        col2.metric("Coût moyen", "$60,000", "+15% vs 2020")
        col3.metric("ROI médian", "3.5 ans", "-0.2 an vs 2020")

    # Tendances générales
    st.subheader("Tendances Générales 2025")

    with st.expander("Évolutions post-pandémie", expanded=True):
        st.markdown("""
        • Retour à la préférence pour les formats en présentiel après la période COVID
        • Intérêt croissant pour l'intelligence artificielle et les compétences numériques
        • Évolution des modes de financement (plus d'aide financière, moins de soutien parental)
        • Légère baisse d'intérêt pour le secteur technologique au profit de la finance durable
        • Importance accrue des compétences en gestion de crise et résilience
        """)

def onglet_simulateur_classement() -> None:
    """Affiche le contenu de l'onglet Simulateur de Classement."""
    st.header("Simulateur de Classement MBA")

    st.markdown("""
    Explorez l'impact des différents critères sur le classement d'une école de commerce.
    Ajustez les curseurs pour voir comment les changements dans chaque domaine affectent le score global.
    """)

    # Colonnes pour le simulateur et le résultat
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Ajustez les paramètres")

        # Variables pour les sliders
        salaire = st.slider("Salaire moyen (pondéré)", 0, 100, 70, help="Influence sur le classement: 16%")
        carriere = st.slider("Progression de carrière", 0, 100, 65, help="Influence sur le classement: 3%")
        reseau = st.slider("Réseau d'anciens élèves", 0, 100, 60, help="Influence sur le classement: 4%")
        diversite = st.slider("Diversité (genre et internationale)", 0, 100, 50, help="Part des critères École")
        recherche = st.slider("Qualité de la recherche", 0, 100, 55, help="Influence sur le classement: 10%")
        esg = st.slider("Critères ESG", 0, 100, 45, help="Part croissante des critères École")

        # Bouton pour calculer le score
        if st.button("Calculer le score"):
            # Informations sur le calcul
            st.info("""
            Le calcul prend en compte la pondération des différents critères
            selon la méthodologie du Financial Times.
            """)

    with col2:
        # Calculer le score en tenant compte de la pondération
        score_salaire = salaire * 0.16
        score_carriere = carriere * 0.03
        score_reseau = reseau * 0.04
        score_diversite = diversite * 0.1
        score_recherche = recherche * 0.1
        score_esg = esg * 0.07

        # Score total (normalisé sur 100)
        score_total = (score_salaire + score_carriere + score_reseau +
                     score_diversite + score_recherche + score_esg) * 2
        score_total = min(100, score_total)  # Plafonner à 100

        # Afficher le score avec une jauge
        st.subheader("Résultat de la simulation")

        # Définir la couleur en fonction du score
        if score_total >= 80:
            couleur_score = "green"
            niveau = "Excellent"
        elif score_total >= 65:
            couleur_score = "orange"
            niveau = "Bon"
        else:
            couleur_score = "red"
            niveau = "À améliorer"

        # Afficher le score sous forme de métrique
        st.metric("Score global", f"{score_total:.1f}/100", niveau)

        # Créer un graphique radar pour visualiser les différentes dimensions
        categories = ['Salaire', 'Carrière', 'Réseau', 'Diversité', 'Recherche', 'ESG']
        valeurs = [salaire, carriere, reseau, diversite, recherche, esg]

        fig = creer_graphique_radar(categories, valeurs, COULEUR_SECONDAIRE)
        st.pyplot(fig)

        # Comparaison avec les meilleures écoles
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <p style="font-weight: 600; margin-bottom: 5px;">Comparaison indicative:</p>
            <ul style="margin: 0; padding-left: 20px;">
                <li>Harvard/Stanford: 95-100</li>
                <li>Top 10 mondial: 85-95</li>
                <li>Top 30 mondial: 75-85</li>
                <li>Top 50 mondial: 65-75</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Application principale
# -----------------------------------------------------------------------------

def onglet_references() -> None:
    """Affiche le contenu de l'onglet Références & Explications."""
    st.header(traduire('tech_impact_titre'))
    st.markdown(traduire('tech_impact_desc'))
    
    st.subheader(traduire('tech_tendances'))
    
    # Afficher l'information sur l'impact de la technologie avec un style distinctif
    st.markdown(f"""
    <div style="background-color: {COULEUR_FOND}; padding: 20px; border-radius: 5px; border-left: 5px solid {COULEUR_TECHNO}; margin-bottom: 20px;">
        <h3 style="color: {COULEUR_TECHNO}; margin-top: 0;">{traduire('tech_curriculum')}</h3>
        <p>{traduire('tech_detail_1')}</p>
        
        <h3 style="color: {COULEUR_TECHNO}; margin-top: 15px;">{traduire('tech_specialisation')}</h3>
        <p>{traduire('tech_detail_2')}</p>
        
        <h3 style="color: {COULEUR_TECHNO}; margin-top: 15px;">{traduire('tech_competences')}</h3>
        <p>{traduire('tech_detail_3')}</p>
        
        <h3 style="color: {COULEUR_TECHNO}; margin-top: 15px;">{traduire('tech_carriere')}</h3>
        <p>{traduire('tech_detail_4')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Références des sources d'information
    st.subheader("Sources")
    st.markdown("""
    - Financial Times Global MBA Ranking 2025 
    - Wharton School of Business: New MBA Major in Artificial Intelligence for Business (Avril 2025)
    - Harvard Business School: Technology Integration Report (2025)
    - INSEAD: Digital Transformation in Business Education (2025)
    - HEC Paris: Programme MBA Tech & Digital (2025)
    - London Business School: Future of Business Education Survey (2025)
    """)
    
    # Méthodologie
    st.subheader("Méthodologie")
    st.markdown("""
    L'analyse de l'impact de la technologie sur les programmes MBA s'appuie sur:
    1. L'examen des curricula des 25 meilleurs MBA mondiaux
    2. L'analyse des tendances d'insertion professionnelle des diplômés
    3. Les entretiens avec des responsables de programmes
    4. Les enquêtes auprès des étudiants et alumni
    """)

def main() -> None:
    """Fonction principale qui exécute l'application Streamlit."""
    # Appliquer le style CSS personnalisé
    appliquer_style()

    # Afficher l'en-tête
    afficher_entete()

    # Créer les onglets avec traduction des noms
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        traduire('tab_classement'),
        traduire('tab_motivations'),
        traduire('tab_tendances'),
        traduire('tab_simulateur'),
        traduire('tab_references')
    ])

    # Remplir chaque onglet avec son contenu
    with tab1:
        onglet_classement_ft()

    with tab2:
        onglet_motivations_candidats()

    with tab3:
        onglet_tendances_mondiales()

    with tab4:
        onglet_simulateur_classement()
        
    with tab5:
        onglet_references()

    # Afficher le pied de page
    afficher_pied_de_page()

# Point d'entrée de l'application
if __name__ == "__main__":
    main()
