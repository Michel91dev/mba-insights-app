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
COULEUR_IA = "#c0392b"           # Rouge pour l'IA et nouveaux éléments
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
        'tab_ia_techno': "IA & Technologie",
        'tab_references': "Références & Explications",
        
        # IA et Technologie
        'ia_techno_titre': "Intelligence Artificielle & Technologie dans les MBA",
        'ia_techno_desc': "Analyse et outil d'aide à la décision pour l'intégration de l'IA et des technologies dans les programmes MBA.",
        'ia_techno_intro': "Cet outil vous permet d'analyser et de visualiser l'impact des différentes composantes technologiques dans les programmes MBA.",
        
        # Catégories IA et Tech
        'cat_sans_prog': "Sans programmation",
        'cat_avec_prog': "Avec programmation",
        'cat_ia_ml': "IA & Machine Learning",
        'cat_deep_tech': "Deep Tech",
        'cat_techno_gen': "Technologies générales",
        
        # Types de cours
        'cours_common': "Cours obligatoires",
        'cours_electifs': "Cours électifs",
        'cours_projets': "Projets et ateliers",
        
        # Descriptions des catégories
        'desc_sans_prog': "Cours d'initiation à la tech et l'IA sans exigence de programmation (sensibilisation, concepts, stratégie).",
        'desc_avec_prog': "Cours incluant des éléments de code, algorithmes ou programmation de base (Python, R, SQL).",
        'desc_ia_ml': "Cours spécialisés en intelligence artificielle, machine learning et applications métier de l'IA.",
        'desc_deep_tech': "Cours avancés sur les technologies émergentes (blockchain, IoT, robotique, VR/AR).",
        'desc_techno_gen': "Technologies générales appliquées au business (transformation digitale, e-commerce, etc.).",
        
        # Interface utilisateur pour l'outil d'analyse
        'ui_ecole': "École de référence",
        'ui_simuler': "Simuler l'impact",
        'ui_resultats': "Résultats de la simulation",
        'ui_benchmark': "Comparaison avec les meilleures écoles",
        'ui_recommandations': "Recommandations personnalisées",
        'ui_dosage': "Dosage recommandé (% du programme)",
        'ui_impact': "Impact sur la valorisation du MBA",
        
        # Motivations des candidats - textes pour l'onglet en français
        'motivations_titre': "Principales Motivations des Candidats MBA",
        'motivations_intro': "Découvrez pourquoi les étudiants du monde entier choisissent de poursuivre un MBA. Les données montrent que les motivations varient mais se concentrent autour de quelques thèmes clés.",
        'motivations_details': "Détails des motivations",
        'motivations_graphique': "Principales motivations pour faire un MBA",
        'motivations_pourcentage': "Pourcentage de candidats (%)",
        'carrieres': "Progression\nde carrière", 
        'salaires': "Augmentation\nsalariale",
        'reseaux': "Réseau\nprofessionnel", 
        'competences': "Compétences\nmanagériales",
        'secteur': "Changement\nde secteur", 
        'entrepreneuriat': "Entrepreneuriat",
        'motivation_carriere': "Progression de carrière",
        'motivation_salaire': "Augmentation salariale",
        'motivation_reseau': "Réseau professionnel",
        'motivation_competence': "Compétences managériales",
        'motivation_secteur': "Changement de secteur",
        'motivation_entrepreneuriat': "Entrepreneuriat",
        'developpement_professionnel': "Développement Professionnel",
        'opportunites_financieres': "Opportunités Financières",
        'reseau_global': "Réseau Global",
        'reconversion': "Reconversion Professionnelle",
        
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
        'tab_ia_techno': "AI & Technology",
        'tab_references': "References & Explanations",
        
        # Motivations des candidats - textes pour l'onglet en anglais
        'motivations_titre': "Main MBA Candidate Motivations",
        'motivations_intro': "Discover why students worldwide choose to pursue an MBA. Data shows that motivations vary but focus around a few key themes.",
        'motivations_details': "Motivation Details",
        'motivations_graphique': "Main motivations for pursuing an MBA",
        'motivations_pourcentage': "Percentage of candidates (%)",
        'carrieres': "Career\nAdvancement", 
        'salaires': "Salary\nIncrease",
        'reseaux': "Professional\nNetwork", 
        'competences': "Management\nSkills",
        'secteur': "Industry\nChange", 
        'entrepreneuriat': "Entrepreneurship",
        'motivation_carriere': "Career Advancement",
        'motivation_salaire': "Salary Increase",
        'motivation_reseau': "Professional Network",
        'motivation_competence': "Management Skills",
        'motivation_secteur': "Industry Change",
        'motivation_entrepreneuriat': "Entrepreneurship",
        'developpement_professionnel': "Professional Development",
        'opportunites_financieres': "Financial Opportunities",
        'reseau_global': "Global Network",
        'reconversion': "Career Change",
        
        # AI and Technology
        'ia_techno_titre': "Artificial Intelligence & Technology in MBA Programs",
        'ia_techno_desc': "Analysis and decision-making tool for integrating AI and technology into MBA programs.",
        'ia_techno_intro': "This tool allows you to analyze and visualize the impact of various technological components in MBA programs.",
        
        # IA and Tech Categories
        'cat_sans_prog': "No Programming",
        'cat_avec_prog': "With Programming",
        'cat_ia_ml': "AI & Machine Learning",
        'cat_deep_tech': "Deep Tech",
        'cat_techno_gen': "General Technologies",
        
        # Course Types
        'cours_common': "Core Courses",
        'cours_electifs': "Elective Courses",
        'cours_projets': "Projects and Workshops",
        
        # Category Descriptions
        'desc_sans_prog': "Introduction to tech and AI without programming requirements (awareness, concepts, strategy).",
        'desc_avec_prog': "Courses including code elements, algorithms or basic programming (Python, R, SQL).",
        'desc_ia_ml': "Specialized courses in artificial intelligence, machine learning and business applications of AI.",
        'desc_deep_tech': "Advanced courses on emerging technologies (blockchain, IoT, robotics, VR/AR).",
        'desc_techno_gen': "General technologies applied to business (digital transformation, e-commerce, etc.).",
        
        # User Interface for Analysis Tool
        'ui_ecole': "Reference School",
        'ui_simuler': "Simulate Impact",
        'ui_resultats': "Simulation Results",
        'ui_benchmark': "Comparison with Top Schools",
        'ui_recommandations': "Personalized Recommendations",
        'ui_dosage': "Recommended Dosage (% of program)",
        'ui_impact': "Impact on MBA Valuation",
        
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

def selecteur_langue() -> None:
    """Affiche un sélecteur de langue avec des boutons texte."""
    # Créer une ligne avec 3 colonnes, une grande pour l'espacement et deux pour les boutons
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    
    # Style pour afficher le bouton actif avec une couleur de fond
    style_actif = "background-color: #1a5276; color: white; font-weight: bold;"
    style_inactif = "background-color: #f0f0f0; color: black;"
    
    # Déterminer quel bouton est actif en fonction de la langue sélectionnée
    style_fr = style_actif if st.session_state.langue == 'fr' else style_inactif
    style_en = style_actif if st.session_state.langue == 'en' else style_inactif
    
    with col2:
        # Bouton pour la langue française
        if st.button("FR", key="fr_button", help="Passer en français", use_container_width=True):
            st.session_state.langue = 'fr'
            st.rerun()
    
    with col3:
        # Bouton pour la langue anglaise
        if st.button("EN", key="en_button", help="Switch to English", use_container_width=True):
            st.session_state.langue = 'en'
            st.rerun()

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
    st.header(traduire('motivations_titre'))

    st.markdown(traduire('motivations_intro'))

    # Créer le graphique des motivations - utiliser les traductions
    if st.session_state.langue == 'fr':
        motivations = ['Progression\nde carrière', 'Augmentation\nsalariale',
                       'Réseau\nprofessionnel', 'Compétences\nmanagériales',
                       'Changement\nde secteur', 'Entrepreneuriat']
    else:
        motivations = [traduire('carrieres'), traduire('salaires'),
                       traduire('reseaux'), traduire('competences'),
                       traduire('secteur'), traduire('entrepreneuriat')]
    
    percentages = [85, 70, 65, 60, 45, 30]

    fig = creer_graphique_barres(
        motivations,
        percentages,
        COULEUR_SECONDAIRE,
        traduire('motivations_graphique'),
        traduire('motivations_pourcentage')
    )
    st.pyplot(fig)

    # Détails des motivations
    st.subheader(traduire('motivations_details'))

    col1, col2 = st.columns(2)

    with col1:
        with st.expander(traduire('developpement_professionnel'), expanded=True):
            st.markdown("""
            • Progression vers des postes de direction
            • Acquisition de compétences stratégiques
            • Accélération de l'évolution de carrière
            • Visibilité accrue dans l'entreprise
            """)
        
        with st.expander(traduire('opportunites_financieres')):
            st.markdown("""
            • Salaire initial post-MBA supérieur (+50-90% en moyenne)
            • Accès à des industries mieux rémunérées
            • Augmentation des primes et avantages
            • Meilleur pouvoir de négociation salariale
            """)

    with col2:
        with st.expander(traduire('reseau_global')):
            st.markdown("""
            • Connexions avec des étudiants internationaux
            • Réseau d'anciens élèves mondial
            • Accès à des recruteurs internationaux
            • Opportunités d'emploi à l'échelle mondiale
            """)
        
        with st.expander(traduire('reconversion')):
            st.markdown("""
            • Changement de carrière vers un nouveau secteur
            • Accès à des fonctions différentes
            • Possibilité de créer sa propre entreprise
            • Développement d'expertise dans un domaine spécifique
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

def onglet_ia_et_technologie() -> None:
    """Affiche le contenu de l'onglet Intelligence Artificielle & Technologie dans les MBA."""
    st.header(traduire('ia_techno_titre'))
    st.markdown(traduire('ia_techno_desc'))
    
    # Introduction et explication de l'outil
    st.markdown(f"""
    <div style="background-color: {COULEUR_FOND}; padding: 15px; border-radius: 5px; border-left: 5px solid {COULEUR_IA}; margin: 20px 0;">
        <p>{traduire('ia_techno_intro')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Création de 3 colonnes principales
    col_gauche, col_centre, col_droite = st.columns([1, 2, 1])
    
    # Colonne de gauche - Paramètres et configuration
    with col_gauche:
        st.subheader(traduire('ui_ecole'))
        
        # Sélection de l'école de référence
        ecoles_references = {
            "Wharton (Rank #1 Tech)": 42,
            "MIT Sloan (Rank #2 Tech)": 38,
            "Stanford GSB (Rank #3 Tech)": 32,
            "INSEAD (Rank #4 Tech)": 28,
            "Harvard Business School (Rank #5 Tech)": 25,
            "London Business School (Rank #7 Tech)": 24,
            "HEC Paris (Rank #8 Tech)": 22,
            "IE Business School (Rank #10 Tech)": 20,
            "IESE Business School (Rank #12 Tech)": 19,
            "Cambridge Judge (Rank #14 Tech)": 18,
            "Oxford Saïd (Rank #15 Tech)": 17,
            "ESADE (Rank #18 Tech)": 16,
            "RSM Erasmus (Rank #20 Tech)": 15
        }
        
        # Sélection de l'école avec affichage du ranking
        ecole_reference = st.selectbox(
            "Sélectionnez un MBA de référence",
            list(ecoles_references.keys()),
            index=6  # HEC Paris par défaut
        )
        
        # Afficher le pourcentage IA & Tech de l'école sélectionnée
        pourcentage_ecole = ecoles_references[ecole_reference]
        st.info(f"Cette école consacre environ **{pourcentage_ecole}%** de son curriculum à l'IA & aux technologies.")
        
        st.markdown("---")
        
        # Catégories d'IA et technologies
        st.subheader("Catégories d'analyse")
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-size: 0.9em;">
        <p><strong>Note sur la pondération :</strong> Chaque curseur représente le <strong>pourcentage du curriculum MBA</strong> 
        que vous souhaitez consacrer à cette catégorie spécifique de contenu technologique. 
        La somme de tous les curseurs vous donne le pourcentage total du programme dédié à l'IA et aux technologies.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**{traduire('cat_sans_prog')}**")
        st.caption(traduire('desc_sans_prog'))
        sans_prog = st.slider(
            "% du curriculum",
            min_value=0, max_value=25, value=10, step=1,
            key="sans_prog",
            help="Pourcentage du curriculum MBA consacré aux cours de sensibilisation à l'IA et à la tech sans programmation"
        )
        
        st.markdown(f"**{traduire('cat_avec_prog')}**")
        st.caption(traduire('desc_avec_prog'))
        avec_prog = st.slider(
            "% du curriculum",
            min_value=0, max_value=25, value=5, step=1,
            key="avec_prog",
            help="Pourcentage du curriculum MBA consacré aux cours incluant des éléments de programmation"
        )
        
        st.markdown(f"**{traduire('cat_ia_ml')}**")
        st.caption(traduire('desc_ia_ml'))
        ia_ml = st.slider(
            "% du curriculum",
            min_value=0, max_value=25, value=8, step=1,
            key="ia_ml",
            help="Pourcentage du curriculum MBA consacré aux cours spécialisés en IA et machine learning"
        )
        
        st.markdown(f"**{traduire('cat_deep_tech')}**")
        st.caption(traduire('desc_deep_tech'))
        deep_tech = st.slider(
            "% du curriculum",
            min_value=0, max_value=25, value=3, step=1,
            key="deep_tech",
            help="Pourcentage du curriculum MBA consacré aux technologies émergentes avancées (blockchain, IoT, etc.)"
        )
        
        st.markdown(f"**{traduire('cat_techno_gen')}**")
        st.caption(traduire('desc_techno_gen'))
        tech_gen = st.slider(
            "% du curriculum",
            min_value=0, max_value=25, value=7, step=1,
            key="tech_gen",
            help="Pourcentage du curriculum MBA consacré aux technologies générales appliquées au business"
        )
        
        # Afficher le total
        total_poids = sans_prog + avec_prog + ia_ml + deep_tech + tech_gen
        st.success(f"**Total: {total_poids}%** du curriculum dédié à l'IA & tech")
        
        # Bouton pour simuler
        st.markdown("---")
        simuler = st.button(traduire('ui_simuler'))
    
    # Colonne centrale - Résultats et visualisations
    with col_centre:
        # Si le bouton simuler est cliqué
        if simuler or 'simulation_effectuee' in st.session_state:
            st.session_state.simulation_effectuee = True
            st.subheader(traduire('ui_resultats'))
            
            # Sous-colonnes pour différentes visualisations
            viz_col1, viz_col2 = st.columns(2)
            
            # Répartition par type de cours
            with viz_col1:
                # Calcul des répartitions
                # Ces valeurs sont ajustées selon les pondérations entrées
                total_poids = sans_prog + avec_prog + ia_ml + deep_tech + tech_gen
                
                # Répartition par type de cours (obligatoire vs électif)
                core_pct = max(15, min(40, total_poids * 0.8 / 33 * 100))
                electives_pct = max(30, min(70, 100 - core_pct - 10))
                projets_pct = max(5, min(20, 100 - core_pct - electives_pct))
                
                # Graphique pour la répartition par type
                types_cours = [traduire('cours_common'), 
                              traduire('cours_electifs'), 
                              traduire('cours_projets')]
                valeurs_types = [core_pct, electives_pct, projets_pct]
                couleurs_types = [COULEUR_PRINCIPALE, COULEUR_SECONDAIRE, COULEUR_TECHNO]
                
                fig_types = creer_graphique_camembert(
                    categories=types_cours,
                    valeurs=valeurs_types,
                    couleurs=couleurs_types,
                    titre="Répartition par type de cours"
                )
                st.pyplot(fig_types)
            
            # Graphique d'impact par catégorie de technologie
            with viz_col2:
                categories = [traduire('cat_sans_prog'), 
                             traduire('cat_avec_prog'), 
                             traduire('cat_ia_ml'),
                             traduire('cat_deep_tech'), 
                             traduire('cat_techno_gen')]
                valeurs = [sans_prog, avec_prog, ia_ml, deep_tech, tech_gen]
                
                # Normaliser les valeurs pour l'affichage
                total = sum(valeurs)
                valeurs_norm = [v/total*100 for v in valeurs] if total > 0 else [0]*5
                
                couleurs = [COULEUR_SECONDAIRE, COULEUR_PRINCIPALE, 
                           COULEUR_IA, COULEUR_ACCENT, COULEUR_TECHNO]
                
                fig_tech = creer_graphique_camembert(
                    categories=categories,
                    valeurs=valeurs_norm,
                    couleurs=couleurs,
                    titre="Répartition des technologies"
                )
                st.pyplot(fig_tech)
            
            # Graphique radar d'impact global
            total_poids = sans_prog + avec_prog + ia_ml + deep_tech + tech_gen
            
            # Facteurs d'impact calculés
            facteur_employabilite = min(95, 50 + total_poids/33*45)
            facteur_innovation = min(95, 40 + (ia_ml*1.5 + deep_tech*2)/33*55)
            facteur_salaire = min(95, 60 + (ia_ml + deep_tech + avec_prog)/33*35)
            facteur_recherche = min(95, 30 + (deep_tech*2 + ia_ml)/33*65)
            facteur_international = min(95, 70 + total_poids/33*25)
            
            # Graphique radar des impacts
            categories_impact = ["Employabilité", "Innovation pédagogique", 
                               "Impact salarial", "Recherche & publications", 
                               "Attractivité internationale"]
            valeurs_impact = [facteur_employabilite, facteur_innovation, 
                            facteur_salaire, facteur_recherche, 
                            facteur_international]
            
            fig_radar = creer_graphique_radar(
                categories=categories_impact,
                valeurs=valeurs_impact,
                couleur=COULEUR_IA
            )
            st.pyplot(fig_radar)
            
            # Dosage global recommandé
            st.markdown("---")
            st.subheader(traduire('ui_dosage'))
            
            # Calcul du dosage recommandé
            dosage_global = total_poids
            dosage_progressif = min(40, dosage_global * 1.2)  # dosage progressif recommandé
            
            # Affichage du dosage avec jauge
            col_dosage1, col_dosage2, col_dosage3 = st.columns([1, 2, 1])
            with col_dosage2:
                # Utiliser une métrique pour afficher le dosage actuel vs recommandé
                st.metric(
                    "Dosage IA & Technologie actuel", 
                    f"{dosage_global:.1f}%", 
                    f"{dosage_progressif - dosage_global:.1f}% recommandé", 
                    delta_color="normal"
                )
                
                # Ajouter une barre de progression pour visualiser
                st.progress(dosage_global/50)  # 50% est le maximum théorique
    
    # Colonne de droite - Benchmarks et recommandations
    with col_droite:
        st.subheader(traduire('ui_benchmark'))
        
        # Données des meilleures écoles pour le benchmark
        benchmark_data = {
            "Wharton": 42,
            "MIT Sloan": 38,
            "Stanford GSB": 32,
            "INSEAD": 28,
            "HBS": 25,
            "LBS": 24,
            "HEC Paris": 22,
            "CEU": 18,
            "Moyenne Top 10": 30
        }
        
        # Créer un graphique de comparaison avec une taille augmentée et une meilleure lisibilité
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor(COULEUR_FOND)
        
        # Ajouter la référence de l'utilisateur
        total_poids = sans_prog + avec_prog + ia_ml + deep_tech + tech_gen
        
        # Sélectionner seulement les écoles les plus pertinentes pour la comparaison (top 5 + utilisateur + moyenne)
        benchmark_top = {
            "Wharton": 42,
            "MIT Sloan": 38,
            "Stanford GSB": 32,
            "Moyenne Top 10": 30,
            "Votre MBA": total_poids
        }
        
        # Ajouter l'école de référence si elle n'est pas déjà dans le top
        ecole_nom = ecole_reference.split(" (Rank")[0]
        if ecole_nom not in benchmark_top and ecole_nom != "Votre MBA":
            benchmark_top[ecole_nom] = ecoles_references[ecole_reference]
            
        # Trier les données par valeur décroissante pour meilleure lisibilité
        benchmark_top = dict(sorted(benchmark_top.items(), key=lambda x: x[1], reverse=True))
        
        # Couleurs pour le graphique
        colors = [COULEUR_IA if school == "Votre MBA" else 
                 COULEUR_ACCENT if school == ecole_nom and ecole_nom != "Votre MBA" else
                 COULEUR_SECONDAIRE if school == "Moyenne Top 10" else 
                 COULEUR_PRINCIPALE for school in benchmark_top.keys()]
        
        # Créer le graphique avec des dimensions améliorées
        bars = ax.barh(list(benchmark_top.keys()), list(benchmark_top.values()), color=colors, height=0.6)
        
        # Ajouter les valeurs à côté des barres avec une taille de police plus grande
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                   f"{width:.1f}%", ha='left', va='center', fontweight='bold', fontsize=12)
        
        # Configurer le graphique avec une meilleure lisibilité
        ax.set_xlabel("% du curriculum dédié à l'IA & Tech", fontsize=12, fontweight='bold')
        ax.set_xlim(0, 50)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='both', which='major', labelsize=12)
        
        # Titre plus visible
        ax.set_title("Comparaison avec les meilleures écoles", fontsize=14, fontweight='bold', pad=20)
        
        # Afficher le graphique avec plus d'espace
        fig.tight_layout()
        st.pyplot(fig)
        
        # Recommandations personnalisées
        st.markdown("---")
        st.subheader(traduire('ui_recommandations'))
        
        total_poids = sans_prog + avec_prog + ia_ml + deep_tech + tech_gen
        
        if total_poids < 15:
            st.markdown(f"""
            <div style="background-color: {COULEUR_FOND}; padding: 15px; border-radius: 5px; border-left: 5px solid {COULEUR_IA};">            
            <p>Votre dosage actuel est <strong>en dessous</strong> des standards 2025 des MBA internationaux. 
            Nous recommandons d'augmenter significativement votre composante IA et technologie pour rester compétitif.</p>
            
            <ul>
                <li>Ajoutez un cours obligatoire de base sur l'IA</li>
                <li>Introduisez 2-3 électifs tech sans prérequis de programmation</li>
                <li>Développez un module d'initiation aux données</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        elif total_poids < 25:
            st.markdown(f"""
            <div style="background-color: {COULEUR_FOND}; padding: 15px; border-radius: 5px; border-left: 5px solid {COULEUR_IA};">            
            <p>Votre dosage actuel est <strong>dans la moyenne basse</strong> des MBA internationaux. 
            Des ajustements modérés rendraient votre programme plus attractif.</p>
            
            <ul>
                <li>Renforcez les modules d'IA et ML dans le tronc commun</li>
                <li>Ajoutez un électif spécialisé en IA</li>
                <li>Considérez un partenariat avec une entreprise tech</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        elif total_poids < 35:
            st.markdown(f"""
            <div style="background-color: {COULEUR_FOND}; padding: 15px; border-radius: 5px; border-left: 5px solid {COULEUR_IA};">            
            <p>Votre dosage est <strong>compétitif</strong> et proche de la moyenne des top MBA. 
            Quelques optimisations amélioreraient encore votre proposition de valeur.</p>
            
            <ul>
                <li>Développez une spécialisation IA complète</li>
                <li>Intégrez des projets d'application réels avec des entreprises tech</li>
                <li>Renforcez la composante Deep Tech pour plus d'innovation</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: {COULEUR_FOND}; padding: 15px; border-radius: 5px; border-left: 5px solid {COULEUR_IA};">            
            <p>Votre dosage est <strong>excellent</strong> et comparable aux meilleurs MBA tech mondiaux. 
            Maintenez cet avantage compétitif.</p>
            
            <ul>
                <li>Assurez-vous de l'équilibre entre théorie et pratique</li>
                <li>Mesurez régulièrement le ROI pour vos diplômés</li>
                <li>Communiquez fortement sur votre avantage compétitif</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        # Impact sur la valorisation du MBA
        st.markdown("---")
        st.subheader(traduire('ui_impact'))
        
        # Calcul de l'impact financier
        impact_rank = max(0, min(15, (total_poids - 15) / 2))
        impact_salary = max(0, min(25, total_poids * 0.7))
        
        st.markdown(f"""
        <div style="font-size: 0.9rem;">
        <p>Amélioration potentielle du classement FT: <strong>+{impact_rank:.0f} places</strong></p>
        <p>Impact salarial estimé à 3 ans: <strong>+{impact_salary:.1f}%</strong></p>
        </div>
        """, unsafe_allow_html=True)

def onglet_references() -> None:
    """Affiche le contenu de l'onglet Références & Explications."""
    st.header(traduire('tech_impact_titre'))
    st.markdown(traduire('tech_impact_desc'))
    
    st.subheader(traduire('tech_tendances'))
    
    # Textes des détails technologiques à afficher (corrigés pour éviter les problèmes de formattage)
    tech_detail_1 = traduire('tech_detail_1')
    tech_detail_2 = traduire('tech_detail_2')
    tech_detail_3 = traduire('tech_detail_3')
    tech_detail_4 = traduire('tech_detail_4')
    
    # Afficher l'information sur l'impact de la technologie avec un style distinctif
    st.markdown(f"""
    <div style="background-color: {COULEUR_FOND}; padding: 20px; border-radius: 5px; border-left: 5px solid {COULEUR_TECHNO}; margin-bottom: 20px;">
        <h3 style="color: {COULEUR_TECHNO}; margin-top: 0;">{traduire('tech_curriculum')}</h3>
        <p>{tech_detail_1}</p>
        
        <h3 style="color: {COULEUR_TECHNO}; margin-top: 15px;">{traduire('tech_specialisation')}</h3>
        <p>{tech_detail_2}</p>
        
        <h3 style="color: {COULEUR_TECHNO}; margin-top: 15px;">{traduire('tech_competences')}</h3>
        <p>{tech_detail_3}</p>
        
        <h3 style="color: {COULEUR_TECHNO}; margin-top: 15px;">{traduire('tech_carriere')}</h3>
        <p>{tech_detail_4}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Références des sources d'information (rendues cliquables)
    st.subheader("Sources")
    st.markdown(f"""
    <ul style="list-style-type: none; padding-left: 0;">
        <li style="margin-bottom: 8px;">• <a href="https://rankings.ft.com/rankings/2866/mba-2025" target="_blank">Financial Times Global MBA Ranking 2025</a></li>
        <li style="margin-bottom: 8px;">• <a href="https://www.wharton.upenn.edu/mba-artificial-intelligence" target="_blank">Wharton School of Business: New MBA Major in Artificial Intelligence for Business (Avril 2025)</a></li>
        <li style="margin-bottom: 8px;">• <a href="https://www.hbs.edu/tech-integration" target="_blank">Harvard Business School: Technology Integration Report (2025)</a></li>
        <li style="margin-bottom: 8px;">• <a href="https://www.insead.edu/digital-transformation" target="_blank">INSEAD: Digital Transformation in Business Education (2025)</a></li>
        <li style="margin-bottom: 8px;">• <a href="https://www.hec.edu/fr/grande-ecole/programme-mba-tech-digital" target="_blank">HEC Paris: Programme MBA Tech & Digital (2025)</a></li>
        <li style="margin-bottom: 8px;">• <a href="https://www.london.edu/future-of-business-education" target="_blank">London Business School: Future of Business Education Survey (2025)</a></li>
    </ul>
    """, unsafe_allow_html=True)
    
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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        traduire('tab_classement'),
        traduire('tab_motivations'),
        traduire('tab_tendances'),
        traduire('tab_simulateur'),
        traduire('tab_ia_techno'),
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
        onglet_ia_et_technologie()
        
    with tab6:
        onglet_references()

    # Afficher le pied de page
    afficher_pied_de_page()

# Point d'entrée de l'application
if __name__ == "__main__":
    main()
