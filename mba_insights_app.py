# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk
import webbrowser

class GestionnairePolice:
    """Classe pour gérer les polices adaptatives en fonction de la taille de la fenêtre."""
    def __init__(self, fenetre_racine):
        self.fenetre_racine = fenetre_racine
        self.largeur_base = 1000  # Largeur de référence
        self.hauteur_base = 700   # Hauteur de référence
        
        # Tailles de police de base
        self.tailles_base = {
            "titre_principal": 24,
            "titre_onglet": 16,
            "sous_titre": 14,
            "normal": 12,
            "petit": 10,
            "très_petit": 9
        }
        
        # Dictionnaire pour stocker les polices actuelles
        self.polices = {}
        
        # Configurer le gestionnaire d'événements de redimensionnement
        self.fenetre_racine.bind("<Configure>", self.actualiser_polices)
        
    def obtenir_police(self, type_police, gras=False, italique=False):
        """Obtenir une police adaptée à la taille actuelle de la fenêtre."""
        # Calculer le facteur d'échelle
        largeur_actuelle = self.fenetre_racine.winfo_width()
        hauteur_actuelle = self.fenetre_racine.winfo_height()
        
        # Éviter la division par zéro lors de l'initialisation
        if largeur_actuelle < 50 or hauteur_actuelle < 50:
            return ("Helvetica", self.tailles_base[type_police], "bold" if gras else "normal")
        
        # Calculer le facteur d'échelle (moyenne des rapports de largeur et hauteur)
        facteur_largeur = largeur_actuelle / self.largeur_base
        facteur_hauteur = hauteur_actuelle / self.hauteur_base
        facteur = (facteur_largeur + facteur_hauteur) / 2
        
        # Limiter le facteur pour éviter des polices trop petites ou trop grandes
        facteur = max(0.7, min(facteur, 1.3))
        
        # Calculer la nouvelle taille de police
        taille_police = max(8, int(self.tailles_base[type_police] * facteur))
        
        # Définir le style de police
        style = ""
        if gras:
            style = "bold"
        if italique:
            style = "italic" if style == "" else style + " italic"
        style = "normal" if style == "" else style
        
        # Retourner la police configurée
        return ("Helvetica", taille_police, style)
        
    def actualiser_polices(self, event=None):
        """Mettre à jour les polices en fonction de la taille de la fenêtre."""
        # Cette méthode sera appelée lors du redimensionnement de la fenêtre
        # Calculer le facteur d'échelle pour le wraplength
        largeur_actuelle = self.fenetre_racine.winfo_width()
        if largeur_actuelle < 50:  # Éviter la division par zéro lors de l'initialisation
            return
            
        # Calculer le facteur d'échelle pour le wraplength
        facteur_largeur = largeur_actuelle / self.largeur_base
        # Limiter le facteur pour éviter des wraplength trop petits ou trop grands
        facteur_largeur = max(0.6, min(facteur_largeur, 1.4))
        
        # Mettre à jour le wraplength de base pour les labels
        self.wraplength_base = int(largeur_actuelle * 0.85)  # 85% de la largeur de la fenêtre

class MBAInsightsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MBA Global Insights - Analyse Interactive")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialiser le gestionnaire de polices
        self.gestionnaire_police = GestionnairePolice(root)
        
        # Listes pour stocker les références aux widgets
        self.widgets_texte = []  # Pour les polices
        self.widgets_wraplength = []  # Pour les widgets avec wraplength
        self.figures = []  # Pour stocker les références aux figures matplotlib
        self.canvases = []  # Pour stocker les références aux canvas matplotlib

        # Définir les couleurs et le style
        self.primary_color = "#1a5276"  # Bleu foncé professionnel
        self.secondary_color = "#2980b9"  # Bleu plus clair
        self.accent_color = "#f39c12"  # Orange pour l'accent
        self.bg_color = "#f0f0f0"  # Fond gris clair

        # Configurer le style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        
        # Utiliser le gestionnaire de polices pour les onglets
        police_onglet = self.gestionnaire_police.obtenir_police("normal", gras=True)
        style.configure("TNotebook.Tab", background=self.bg_color, foreground=self.primary_color,
                        padding=[20, 10], font=police_onglet)
        style.map("TNotebook.Tab", background=[("selected", self.primary_color)],
                 foreground=[("selected", "white")])
        style.configure("TFrame", background=self.bg_color)
        
        # Configurer la mise à jour des polices lors du redimensionnement
        self.root.bind("<Configure>", self.actualiser_interface)

        # Créer le titre principal
        self.header_frame = tk.Frame(root, bg=self.primary_color, height=80)
        self.header_frame.pack(fill=tk.X)

        # Utiliser le gestionnaire de polices pour le titre principal
        police_titre = self.gestionnaire_police.obtenir_police("titre_principal", gras=True)
        self.title_label = tk.Label(self.header_frame,
                                   text="MBA GLOBAL INSIGHTS",
                                   font=police_titre,
                                   fg="white",
                                   bg=self.primary_color)
        self.title_label.pack(pady=20)
        
        # Ajouter le widget à la liste pour la mise à jour des polices
        self.widgets_texte.append((self.title_label, "titre_principal", True, False))

        # Créer le notebook (onglets)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Créer les onglets
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Classement FT")
        self.notebook.add(self.tab2, text="Motivations des Candidats")
        self.notebook.add(self.tab3, text="Tendances Mondiales")
        self.notebook.add(self.tab4, text="Simulateur de Classement")

        # Initialiser les onglets
        self.setup_ranking_tab()
        self.setup_motivations_tab()
        self.setup_trends_tab()
        self.setup_simulator_tab()

        # Pied de page
        self.footer_frame = tk.Frame(root, bg=self.primary_color, height=30)
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        police_footer = self.gestionnaire_police.obtenir_police("petit")
        self.footer_label = tk.Label(self.footer_frame,
                                    text="© 2025 MBA Global Insights - Développé avec Python",
                                    font=police_footer,
                                    fg="white",
                                    bg=self.primary_color)
        self.footer_label.pack(pady=5)
        
        # Ajouter le widget à la liste pour la mise à jour des polices
        self.widgets_texte.append((self.footer_label, "petit", False, False))
    
    def actualiser_interface(self, event=None):
        """Mettre à jour l'interface lors du redimensionnement de la fenêtre."""
        # Ne pas traiter les événements trop fréquemment pour éviter les ralentissements
        try:
            if hasattr(self, '_derniere_mise_a_jour') and int(event.time) - int(self._derniere_mise_a_jour) < 100:
                return
        except (TypeError, ValueError):
            # En cas d'erreur de conversion, continuer
            pass
        self._derniere_mise_a_jour = event.time
        
        # Mettre à jour le gestionnaire de polices
        self.gestionnaire_police.actualiser_polices(event)
        
        # Obtenir la largeur actuelle pour le wraplength
        largeur_actuelle = self.root.winfo_width()
        if largeur_actuelle < 50:  # Éviter les calculs lors de l'initialisation
            return
            
        # Calculer le wraplength de base (85% de la largeur de la fenêtre)
        wraplength_base = int(largeur_actuelle * 0.85)
        
        # Mettre à jour les polices de tous les widgets enregistrés
        for widget, type_police, gras, italique in self.widgets_texte:
            try:
                police = self.gestionnaire_police.obtenir_police(type_police, gras, italique)
                widget.configure(font=police)
            except Exception as e:
                print(f"Erreur lors de la mise à jour de la police: {e}")
        
        # Mettre à jour le wraplength des widgets qui en ont besoin
        for widget, ratio in self.widgets_wraplength:
            try:
                widget.configure(wraplength=int(wraplength_base * ratio))
            except Exception as e:
                print(f"Erreur lors de la mise à jour du wraplength: {e}")
        
        # Mettre à jour le style des onglets
        style = ttk.Style()
        police_onglet = self.gestionnaire_police.obtenir_police("normal", gras=True)
        style.configure("TNotebook.Tab", font=police_onglet)
        
        # Redimensionner les graphiques si nécessaire
        self.redimensionner_graphiques()
        
    def redimensionner_graphiques(self):
        """Redimensionner les graphiques matplotlib lors du redimensionnement de la fenêtre."""
        if not hasattr(self, 'figures') or not self.figures:
            return
            
        # Obtenir la taille actuelle de la fenêtre
        largeur_actuelle = self.root.winfo_width()
        hauteur_actuelle = self.root.winfo_height()
        
        if largeur_actuelle < 50 or hauteur_actuelle < 50:
            return
            
        # Calculer le facteur d'échelle
        facteur_largeur = largeur_actuelle / 1000  # Largeur de référence
        facteur_hauteur = hauteur_actuelle / 700   # Hauteur de référence
        facteur = min(facteur_largeur, facteur_hauteur)
        
        # Limiter le facteur pour éviter des graphiques trop petits ou trop grands
        facteur = max(0.6, min(facteur, 1.4))
        
        # Taille de police de base pour les graphiques
        taille_titre = max(8, int(14 * facteur))
        taille_axes = max(8, int(12 * facteur))
        taille_etiquettes = max(8, int(10 * facteur))
        
        # Mettre à jour chaque figure
        for i, (figure, canvas) in enumerate(zip(self.figures, self.canvases)):
            try:
                # Mise à jour des polices dans la figure
                for ax in figure.axes:
                    # Titre
                    if ax.get_title():
                        ax.set_title(ax.get_title(), fontsize=taille_titre)
                    
                    # Étiquettes des axes
                    ax.tick_params(axis='both', labelsize=taille_etiquettes)
                    
                    # Labels des axes
                    if ax.get_xlabel():
                        ax.set_xlabel(ax.get_xlabel(), fontsize=taille_axes)
                    if ax.get_ylabel():
                        ax.set_ylabel(ax.get_ylabel(), fontsize=taille_axes)
                    
                    # Légende
                    if ax.get_legend():
                        for text in ax.get_legend().get_texts():
                            text.set_fontsize(taille_etiquettes)
                    
                    # Textes dans le graphique
                    for text in ax.texts:
                        text.set_fontsize(taille_etiquettes)
                
                # Redessiner la figure
                figure.tight_layout()
                canvas.draw()
            except Exception as e:
                print(f"Erreur lors du redimensionnement du graphique {i}: {e}")

    def setup_ranking_tab(self):
        """Configure l'onglet du classement FT"""
        # Titre de l'onglet
        police_titre = self.gestionnaire_police.obtenir_police("titre_onglet", gras=True)
        title_label = tk.Label(self.tab1,
                              text="Méthodologie du Classement Financial Times",
                              font=police_titre,
                              fg=self.primary_color,
                              bg=self.bg_color)
        title_label.pack(pady=10)
        self.widgets_texte.append((title_label, "titre_onglet", True, False))

        # Description
        desc_text = """Le Financial Times utilise une méthodologie rigoureuse pour son classement mondial des MBA,
basée sur trois grandes catégories de critères. Explorez le graphique ci-dessous pour comprendre
l'importance relative de chaque facteur dans le classement global."""

        police_normale = self.gestionnaire_police.obtenir_police("normal")
        desc_label = tk.Label(self.tab1,
                             text=desc_text,
                             font=police_normale,
                             fg="black",
                             bg=self.bg_color,
                             justify=tk.LEFT,
                             wraplength=900)  # Ajout d'un wraplength pour gérer le texte long
        desc_label.pack(pady=10, padx=20, anchor="w")
        self.widgets_texte.append((desc_label, "normal", False, False))
        self.widgets_wraplength.append((desc_label, 0.9))  # 90% de la largeur de base

        # Créer le graphique de répartition des critères
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor(self.bg_color)

        # Données pour le graphique
        categories = ['Critères Alumni', 'Données Écoles', 'Recherche']
        values = [56, 34, 10]
        colors = [self.secondary_color, self.accent_color, '#27ae60']

        # Créer le graphique
        wedges, texts, autotexts = ax.pie(values, labels=categories, autopct='%1.1f%%',
                                         startangle=90, colors=colors)

        # Égaliser l'aspect du graphique
        ax.axis('equal')
        
        # Configurer les tailles de police initiales
        taille_etiquettes = int(10 * (self.root.winfo_width() / 1000))
        taille_etiquettes = max(8, taille_etiquettes)  # Au moins 8pt
        
        plt.setp(autotexts, size=taille_etiquettes, weight="bold")
        plt.setp(texts, size=taille_etiquettes+2)
        
        # Appliquer tight_layout pour ajuster les marges
        fig.tight_layout()

        # Ajouter le graphique à l'interface
        canvas = FigureCanvasTkAgg(fig, master=self.tab1)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Stocker les références pour le redimensionnement
        self.figures.append(fig)
        self.canvases.append(canvas)

        # Détails des critères
        details_frame = tk.Frame(self.tab1, bg=self.bg_color)
        details_frame.pack(fill=tk.X, padx=20, pady=10)

        # Critères Alumni
        police_sous_titre = self.gestionnaire_police.obtenir_police("normal", gras=True)
        alumni_frame = tk.LabelFrame(details_frame, text="Critères Alumni (56%)",
                                    font=police_sous_titre,
                                    fg=self.secondary_color,
                                    bg=self.bg_color)
        alumni_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.widgets_texte.append((alumni_frame, "normal", True, False))

        alumni_criteria = [
            "Salaire moyen pondéré (16%)",
            "Augmentation de salaire (16%)",
            "Rapport qualité-prix (5%)",
            "Progression de carrière (3%)",
            "Réalisation des objectifs (4%)",
            "Réseau d'anciens élèves (4%)"
        ]

        police_petit = self.gestionnaire_police.obtenir_police("petit")
        for criterion in alumni_criteria:
            lbl = tk.Label(alumni_frame, text="• " + criterion,
                          font=police_petit,
                          fg="black", bg=self.bg_color,
                          anchor="w",
                          wraplength=400)  # Wraplength pour éviter les débordements
            lbl.pack(fill=tk.X, padx=5, pady=2)
            self.widgets_texte.append((lbl, "petit", False, False))
            self.widgets_wraplength.append((lbl, 0.4))  # 40% de la largeur de base

        # Critères Écoles
        school_frame = tk.LabelFrame(details_frame, text="Critères Écoles (34%)",
                                    font=police_sous_titre,
                                    fg=self.accent_color,
                                    bg=self.bg_color)
        school_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.widgets_texte.append((school_frame, "normal", True, False))

        school_criteria = [
            "Diversité de genre",
            "Diversité internationale",
            "Mobilité internationale",
            "Expérience internationale",
            "Professeurs avec doctorat",
            "Critères ESG"
        ]

        for criterion in school_criteria:
            lbl = tk.Label(school_frame, text="• " + criterion,
                          font=police_petit,
                          fg="black", bg=self.bg_color,
                          anchor="w",
                          wraplength=400)  # Wraplength pour éviter les débordements
            lbl.pack(fill=tk.X, padx=5, pady=2)
            self.widgets_texte.append((lbl, "petit", False, False))
            self.widgets_wraplength.append((lbl, 0.4))  # 40% de la largeur de base

    def setup_motivations_tab(self):
        """Configure l'onglet des motivations des candidats"""
        # Titre de l'onglet
        police_titre = self.gestionnaire_police.obtenir_police("titre_onglet", gras=True)
        title_label = tk.Label(self.tab2,
                              text="Principales Motivations des Candidats MBA",
                              font=police_titre,
                              fg=self.primary_color,
                              bg=self.bg_color)
        title_label.pack(pady=10)
        self.widgets_texte.append((title_label, "titre_onglet", True, False))

        # Description
        desc_text = """Découvrez pourquoi les étudiants du monde entier choisissent de poursuivre un MBA.
Les données montrent que les motivations varient mais se concentrent autour de quelques thèmes clés."""

        police_normale = self.gestionnaire_police.obtenir_police("normal")
        desc_label = tk.Label(self.tab2,
                             text=desc_text,
                             font=police_normale,
                             fg="black",
                             bg=self.bg_color,
                             justify=tk.LEFT,
                             wraplength=900)  # Ajout d'un wraplength pour gérer le texte long
        desc_label.pack(pady=10, padx=20, anchor="w")
        self.widgets_texte.append((desc_label, "normal", False, False))
        self.widgets_wraplength.append((desc_label, 0.9))  # 90% de la largeur de base

        # Créer le graphique des motivations
        fig, ax = plt.subplots(figsize=(9, 4))
        fig.patch.set_facecolor(self.bg_color)

        # Données pour le graphique
        motivations = ['Progression\nde carrière', 'Augmentation\nsalariale',
                      'Réseau\nprofessionnel', 'Compétences\nmanagériales',
                      'Changement\nde secteur', 'Entrepreneuriat']
        percentages = [85, 70, 65, 60, 45, 30]

        # Créer le graphique à barres
        bars = ax.bar(motivations, percentages, color=self.secondary_color)

        # Configurer les tailles de police initiales
        largeur_actuelle = self.root.winfo_width()
        taille_etiquettes = int(10 * (largeur_actuelle / 1000))
        taille_etiquettes = max(8, taille_etiquettes)  # Au moins 8pt
        taille_titre = taille_etiquettes + 4
        taille_axe = taille_etiquettes + 2
        
        # Ajouter les pourcentages au-dessus des barres
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{int(height)}%', ha='center', va='bottom',
                   fontweight='bold', fontsize=taille_etiquettes)

        ax.set_ylim(0, 100)
        ax.set_ylabel('Pourcentage de candidats (%)', fontsize=taille_axe)
        ax.set_title('Principales motivations pour faire un MBA', fontsize=taille_titre, pad=15)
        ax.tick_params(axis='both', labelsize=taille_etiquettes)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Ajuster l'espacement du graphique
        fig.tight_layout()

        # Ajouter le graphique à l'interface
        canvas = FigureCanvasTkAgg(fig, master=self.tab2)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Stocker les références pour le redimensionnement
        self.figures.append(fig)
        self.canvases.append(canvas)

        # Détails des motivations
        motivations_frame = tk.Frame(self.tab2, bg=self.bg_color)
        motivations_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Colonne 1
        col1_frame = tk.Frame(motivations_frame, bg=self.bg_color)
        col1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Polices adaptatives
        police_sous_titre = self.gestionnaire_police.obtenir_police("sous_titre", gras=True)
        police_petit = self.gestionnaire_police.obtenir_police("petit")
        
        # Titre section 1
        titre_dev = tk.Label(col1_frame,
                text="Développement Professionnel",
                font=police_sous_titre,
                fg=self.primary_color,
                bg=self.bg_color)
        titre_dev.pack(anchor="w", pady=(0, 5))
        self.widgets_texte.append((titre_dev, "sous_titre", True, False))

        dev_text = """• Progression vers des postes de direction
• Acquisition de compétences stratégiques
• Préparation au leadership global
• Développement de la pensée critique"""

        # Contenu section 1
        contenu_dev = tk.Label(col1_frame,
                text=dev_text,
                font=police_petit,
                fg="black",
                bg=self.bg_color,
                justify=tk.LEFT,
                wraplength=400)
        contenu_dev.pack(anchor="w", padx=10)
        self.widgets_texte.append((contenu_dev, "petit", False, False))
        self.widgets_wraplength.append((contenu_dev, 0.4))

        # Titre section 2
        titre_reseau = tk.Label(col1_frame,
                text="Réseau et Opportunités",
                font=police_sous_titre,
                fg=self.primary_color,
                bg=self.bg_color)
        titre_reseau.pack(anchor="w", pady=(15, 5))
        self.widgets_texte.append((titre_reseau, "sous_titre", True, False))

        network_text = """• Construction d'un réseau international
• Accès à des opportunités mondiales
• Connexions avec des leaders d'industrie
• Mobilité internationale accrue"""

        # Contenu section 2
        contenu_reseau = tk.Label(col1_frame,
                text=network_text,
                font=police_petit,
                fg="black",
                bg=self.bg_color,
                justify=tk.LEFT,
                wraplength=400)
        contenu_reseau.pack(anchor="w", padx=10)
        self.widgets_texte.append((contenu_reseau, "petit", False, False))
        self.widgets_wraplength.append((contenu_reseau, 0.4))

        # Colonne 2
        col2_frame = tk.Frame(motivations_frame, bg=self.bg_color)
        col2_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Titre section 3
        titre_secteur = tk.Label(col2_frame,
                text="Spécialisation Sectorielle",
                font=police_sous_titre,
                fg=self.primary_color,
                bg=self.bg_color)
        titre_secteur.pack(anchor="w", pady=(0, 5))
        self.widgets_texte.append((titre_secteur, "sous_titre", True, False))

        sector_text = """• Orientation vers le conseil et la finance
• Transition vers la tech et l'innovation
• Préparation à l'entrepreneuriat
• Expertise dans des domaines spécifiques"""

        # Contenu section 3
        contenu_secteur = tk.Label(col2_frame,
                text=sector_text,
                font=police_petit,
                fg="black",
                bg=self.bg_color,
                justify=tk.LEFT,
                wraplength=400)
        contenu_secteur.pack(anchor="w", padx=10)
        self.widgets_texte.append((contenu_secteur, "petit", False, False))
        self.widgets_wraplength.append((contenu_secteur, 0.4))

        # Titre section 4
        titre_priorites = tk.Label(col2_frame,
                text="Évolution des Priorités",
                font=police_sous_titre,
                fg=self.primary_color,
                bg=self.bg_color)
        titre_priorites.pack(anchor="w", pady=(15, 5))
        self.widgets_texte.append((titre_priorites, "sous_titre", True, False))

        priorities_text = """• Intérêt pour l'éthique et la durabilité
• Focus sur le retour sur investissement
• Préférence pour l'apprentissage en présentiel
• Équilibre entre carrière et développement personnel"""

        # Contenu section 4
        contenu_priorites = tk.Label(col2_frame,
                text=priorities_text,
                font=police_petit,
                fg="black",
                bg=self.bg_color,
                justify=tk.LEFT,
                wraplength=400)
        contenu_priorites.pack(anchor="w", padx=10)
        self.widgets_texte.append((contenu_priorites, "petit", False, False))
        self.widgets_wraplength.append((contenu_priorites, 0.4))

    def setup_trends_tab(self):
        """Configure l'onglet des tendances mondiales"""
        # Titre de l'onglet
        police_titre = self.gestionnaire_police.obtenir_police("titre_onglet", gras=True)
        title_label = tk.Label(self.tab3,
                              text="Tendances Mondiales des MBA",
                              font=police_titre,
                              fg=self.primary_color,
                              bg=self.bg_color)
        title_label.pack(pady=10)
        self.widgets_texte.append((title_label, "titre_onglet", True, False))

        # Description
        desc_text = """Explorez les tendances émergentes dans le monde des MBA à travers différentes régions.
Ces tendances reflètent l'évolution des besoins du marché et des attentes des étudiants."""

        police_normale = self.gestionnaire_police.obtenir_police("normal")
        desc_label = tk.Label(self.tab3,
                             text=desc_text,
                             font=police_normale,
                             fg="black",
                             bg=self.bg_color,
                             justify=tk.LEFT,
                             wraplength=900)  # Ajout d'un wraplength pour gérer le texte long
        desc_label.pack(pady=10, padx=20, anchor="w")
        self.widgets_texte.append((desc_label, "normal", False, False))
        self.widgets_wraplength.append((desc_label, 0.9))  # 90% de la largeur de base

        # Créer le cadre pour les tendances régionales
        regions_frame = tk.Frame(self.tab3, bg=self.bg_color)
        regions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Polices adaptatives
        police_sous_titre = self.gestionnaire_police.obtenir_police("normal", gras=True)
        police_petit = self.gestionnaire_police.obtenir_police("petit")

        # Amérique du Nord
        na_frame = tk.LabelFrame(regions_frame, text="Amérique du Nord",
                               font=police_sous_titre,
                               fg=self.primary_color,
                               bg=self.bg_color)
        na_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.widgets_texte.append((na_frame, "normal", True, False))

        na_trends = """• Intégration de l'IA et de l'analytique
• Programmes spécialisés en tech
• Accent sur l'entrepreneuriat
• Flexibilité des formats d'apprentissage
• Diversité et inclusion renforcées"""

        na_label = tk.Label(na_frame, text=na_trends,
                font=police_petit,
                fg="black", bg=self.bg_color,
                justify=tk.LEFT,
                wraplength=350)  # Wraplength adapté à la taille du cadre
        na_label.pack(padx=10, pady=10, anchor="w")
        self.widgets_texte.append((na_label, "petit", False, False))
        self.widgets_wraplength.append((na_label, 0.35))

        # Europe
        eu_frame = tk.LabelFrame(regions_frame, text="Europe",
                               font=police_sous_titre,
                               fg=self.primary_color,
                               bg=self.bg_color)
        eu_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.widgets_texte.append((eu_frame, "normal", True, False))

        eu_trends = """• Leadership en durabilité et ESG
• Programmes plus courts (12-15 mois)
• Internationalisation accrue
• Partenariats inter-écoles
• Focus sur l'impact social"""

        eu_label = tk.Label(eu_frame, text=eu_trends,
                font=police_petit,
                fg="black", bg=self.bg_color,
                justify=tk.LEFT,
                wraplength=350)  # Wraplength adapté à la taille du cadre
        eu_label.pack(padx=10, pady=10, anchor="w")
        self.widgets_texte.append((eu_label, "petit", False, False))
        self.widgets_wraplength.append((eu_label, 0.35))

        # Asie
        asia_frame = tk.LabelFrame(regions_frame, text="Asie",
                                 font=police_sous_titre,
                                 fg=self.primary_color,
                                 bg=self.bg_color)
        asia_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.widgets_texte.append((asia_frame, "normal", True, False))

        asia_trends = """• Croissance des programmes locaux
• Partenariats avec entreprises tech
• Accent sur l'innovation
• Développement du leadership asiatique
• Expansion des campus satellites"""

        asia_label = tk.Label(asia_frame, text=asia_trends,
                font=police_petit,
                fg="black", bg=self.bg_color,
                justify=tk.LEFT,
                wraplength=350)  # Wraplength adapté à la taille du cadre
        asia_label.pack(padx=10, pady=10, anchor="w")
        self.widgets_texte.append((asia_label, "petit", False, False))
        self.widgets_wraplength.append((asia_label, 0.35))

        # Reste du monde
        row_frame = tk.LabelFrame(regions_frame, text="Reste du monde",
                                font=police_sous_titre,
                                fg=self.primary_color,
                                bg=self.bg_color)
        row_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.widgets_texte.append((row_frame, "normal", True, False))

        row_trends = """• Programmes adaptés aux marchés locaux
• MBA en ligne plus accessibles
• Focus sur les économies émergentes
• Partenariats public-privé
• Entrepreneuriat social"""

        row_label = tk.Label(row_frame, text=row_trends,
                font=police_petit,
                fg="black", bg=self.bg_color,
                justify=tk.LEFT,
                wraplength=350)  # Wraplength adapté à la taille du cadre
        row_label.pack(padx=10, pady=10, anchor="w")
        self.widgets_texte.append((row_label, "petit", False, False))
        self.widgets_wraplength.append((row_label, 0.35))

        # Configurer le grid pour qu'il s'étende correctement
        regions_frame.grid_columnconfigure(0, weight=1)
        regions_frame.grid_columnconfigure(1, weight=1)
        regions_frame.grid_rowconfigure(0, weight=1)
        regions_frame.grid_rowconfigure(1, weight=1)

        # Tendances générales
        police_sous_titre_grand = self.gestionnaire_police.obtenir_police("sous_titre", gras=True)
        trends_frame = tk.LabelFrame(self.tab3, text="Tendances Générales 2025",
                                   font=police_sous_titre_grand,
                                   fg=self.primary_color,
                                   bg=self.bg_color)
        trends_frame.pack(fill=tk.X, padx=30, pady=15)
        self.widgets_texte.append((trends_frame, "sous_titre", True, False))

        general_trends = """• Retour à la préférence pour les formats en présentiel après la pandémie
• Intérêt croissant pour l'intelligence artificielle et les compétences numériques
• Évolution des modes de financement (plus d'aide financière, moins de soutien parental)
• Légère baisse d'intérêt pour le secteur technologique au profit de la finance durable
• Importance accrue des compétences en gestion de crise et résilience"""

        police_normale = self.gestionnaire_police.obtenir_police("normal")
        trends_label = tk.Label(trends_frame, text=general_trends,
                font=police_normale,
                fg="black", bg=self.bg_color,
                justify=tk.LEFT,
                wraplength=850)  # Wraplength adapté à la largeur du cadre
        trends_label.pack(padx=10, pady=10, anchor="w")
        self.widgets_texte.append((trends_label, "normal", False, False))
        self.widgets_wraplength.append((trends_label, 0.85))

    def setup_simulator_tab(self):
        """Configure l'onglet du simulateur de classement"""
        # Titre de l'onglet
        police_titre = self.gestionnaire_police.obtenir_police("titre_onglet", gras=True)
        title_label = tk.Label(self.tab4,
                              text="Simulateur de Classement MBA",
                              font=police_titre,
                              fg=self.primary_color,
                              bg=self.bg_color)
        title_label.pack(pady=10)
        self.widgets_texte.append((title_label, "titre_onglet", True, False))

        # Description
        desc_text = """Explorez l'impact des différents critères sur le classement d'une école de commerce.
Ajustez les curseurs pour voir comment les changements dans chaque domaine affectent le score global."""

        police_normale = self.gestionnaire_police.obtenir_police("normal")
        desc_label = tk.Label(self.tab4,
                             text=desc_text,
                             font=police_normale,
                             fg="black",
                             bg=self.bg_color,
                             justify=tk.LEFT,
                             wraplength=900)  # Ajout d'un wraplength pour gérer le texte long
        desc_label.pack(pady=10, padx=20, anchor="w")
        self.widgets_texte.append((desc_label, "normal", False, False))
        self.widgets_wraplength.append((desc_label, 0.9))  # 90% de la largeur de base

        # Cadre principal
        main_frame = tk.Frame(self.tab4, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Cadre pour les sliders
        sliders_frame = tk.Frame(main_frame, bg=self.bg_color)
        sliders_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Variables pour les sliders
        self.salary_var = tk.DoubleVar(value=70)
        self.career_var = tk.DoubleVar(value=65)
        self.network_var = tk.DoubleVar(value=60)
        self.diversity_var = tk.DoubleVar(value=50)
        self.research_var = tk.DoubleVar(value=55)
        self.esg_var = tk.DoubleVar(value=45)
        
        # Stocker les figures et les canvas pour le redimensionnement
        if not hasattr(self, 'figures'):
            self.figures = []
            self.canvases = []

        # Cadre pour le graphique et le score
        results_frame = tk.Frame(main_frame, bg=self.bg_color)
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Créer le graphique radar
        fig = plt.Figure(figsize=(5, 4))
        fig.patch.set_facecolor(self.bg_color)
        ax = fig.add_subplot(111, polar=True)

        # Catégories pour le graphique radar
        categories = [
            'Salaire',
            'Carrière',
            'Réseau',
            'Diversité',
            'Recherche',
            'ESG'
        ]

        # Nombre de catégories
        N = len(categories)

        # Angles pour le graphique radar
        angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()

        # Fermer le graphique
        values = [
            self.salary_var.get(),
            self.career_var.get(),
            self.network_var.get(),
            self.diversity_var.get(),
            self.research_var.get(),
            self.esg_var.get()
        ]
        values += values[:1]
        angles += angles[:1]
        
        # Configurer les tailles de police initiales
        largeur_actuelle = self.root.winfo_width()
        taille_etiquettes = int(10 * (largeur_actuelle / 1000))
        taille_etiquettes = max(8, taille_etiquettes)  # Au moins 8pt

        # Tracer le graphique
        ax.plot(angles, values, 'o-', linewidth=2, color=self.secondary_color)
        ax.fill(angles, values, alpha=0.25, color=self.secondary_color)
        ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=taille_etiquettes)
        ax.set_ylim(0, 100)
        ax.grid(True)
        
        # Ajuster les tailles des étiquettes pour que tout soit bien visible
        for label in ax.get_xticklabels():
            label.set_fontsize(taille_etiquettes)
        for label in ax.get_yticklabels():
            label.set_fontsize(taille_etiquettes)
        
        # Appliquer tight_layout pour ajuster les marges
        fig.tight_layout()

        # Ajouter le graphique à l'interface
        canvas = FigureCanvasTkAgg(fig, master=results_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Stocker les références pour le redimensionnement
        self.figures.append(fig)
        self.canvases.append(canvas)

        # Cadre pour le score
        score_frame = tk.Frame(results_frame, bg=self.bg_color)
        score_frame.pack(pady=10)
        
        # Polices adaptatives
        police_sous_titre = self.gestionnaire_police.obtenir_police("sous_titre", gras=True)
        police_titre_principal = self.gestionnaire_police.obtenir_police("titre_principal", gras=True)
        police_normale = self.gestionnaire_police.obtenir_police("normal")
        
        # Label Score global
        score_text_label = tk.Label(score_frame,
                text="Score global:",
                font=police_sous_titre,
                fg=self.primary_color,
                bg=self.bg_color)
        score_text_label.pack(side=tk.LEFT, padx=5)
        self.widgets_texte.append((score_text_label, "sous_titre", True, False))

        # Valeur du score
        score_label = tk.Label(score_frame,
                              text="65.0",
                              font=police_titre_principal,
                              fg=self.secondary_color,
                              bg=self.bg_color)
        score_label.pack(side=tk.LEFT, padx=5)
        self.widgets_texte.append((score_label, "titre_principal", True, False))

        # Label /100
        score_max_label = tk.Label(score_frame,
                text="/100",
                font=police_normale,
                fg=self.primary_color,
                bg=self.bg_color)
        score_max_label.pack(side=tk.LEFT)
        self.widgets_texte.append((score_max_label, "normal", False, False))

        # Rang estimé
        rank_frame = tk.Frame(results_frame, bg=self.bg_color)
        rank_frame.pack(pady=5)

        # Label Rang estimé
        rank_text_label = tk.Label(rank_frame,
                text="Rang estimé:",
                font=police_normale,
                fg=self.primary_color,
                bg=self.bg_color)
        rank_text_label.pack(side=tk.LEFT, padx=5)
        self.widgets_texte.append((rank_text_label, "normal", True, False))

        # Valeur du rang
        rank_label = tk.Label(rank_frame,
                             text="Top 50 mondial",
                             font=police_normale,
                             fg=self.accent_color,
                             bg=self.bg_color)
        rank_label.pack(side=tk.LEFT, padx=5)
        self.widgets_texte.append((rank_label, "normal", True, False))

        # Fonction pour mettre à jour le score
        def update_score(*args):
            # Calculer le score pondéré
            salary_score = self.salary_var.get() * 0.16
            career_score = self.career_var.get() * 0.16
            network_score = self.network_var.get() * 0.08
            diversity_score = self.diversity_var.get() * 0.10
            research_score = self.research_var.get() * 0.10
            esg_score = self.esg_var.get() * 0.05

            # Score total (sur 65% des critères totaux pour simplifier)
            total_score = salary_score + career_score + network_score + diversity_score + research_score + esg_score
            normalized_score = total_score / 0.65  # Normaliser sur 100

            # Mettre à jour l'affichage du score
            score_label.config(text=f"{normalized_score:.1f}")

            # Déterminer le rang approximatif
            if normalized_score >= 85:
                rank_text = "Top 10 mondial"
                rank_color = "#27ae60"  # Vert
            elif normalized_score >= 75:
                rank_text = "Top 25 mondial"
                rank_color = "#2ecc71"  # Vert clair
            elif normalized_score >= 65:
                rank_text = "Top 50 mondial"
                rank_color = self.accent_color  # Orange
            elif normalized_score >= 55:
                rank_text = "Top 100 mondial"
                rank_color = "#e67e22"  # Orange foncé
            else:
                rank_text = "Hors top 100"
                rank_color = "#e74c3c"  # Rouge

            rank_label.config(text=rank_text, fg=rank_color)

            # Mettre à jour le graphique radar
            values = [
                self.salary_var.get(),
                self.career_var.get(),
                self.network_var.get(),
                self.diversity_var.get(),
                self.research_var.get(),
                self.esg_var.get()
            ]

            # Effacer le graphique précédent
            ax.clear()
            
            # Configurer les tailles de police actuelles en fonction de la taille de la fenêtre
            largeur_actuelle = self.root.winfo_width()
            taille_etiquettes = int(10 * (largeur_actuelle / 1000))
            taille_etiquettes = max(8, taille_etiquettes)  # Au moins 8pt

            # Recréer le graphique radar
            angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
            values += values[:1]  # Fermer le polygone
            angles += angles[:1]  # Fermer le polygone

            ax.plot(angles, values, 'o-', linewidth=2, color=self.secondary_color)
            ax.fill(angles, values, alpha=0.25, color=self.secondary_color)
            ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=taille_etiquettes)
            ax.set_ylim(0, 100)
            ax.grid(True)
            
            # Ajuster les tailles des étiquettes
            for label in ax.get_xticklabels():
                label.set_fontsize(taille_etiquettes)
            for label in ax.get_yticklabels():
                label.set_fontsize(taille_etiquettes)
            
            # Ajuster l'espacement du graphique
            fig.tight_layout()

            canvas.draw()

        # Créer les sliders
        police_normale_gras = self.gestionnaire_police.obtenir_police("normal", gras=True)
        
        # Slider 1: Salaire
        salaire_label = tk.Label(sliders_frame, text="Salaire et progression (16%)",
                font=police_normale_gras,
                fg=self.primary_color,
                bg=self.bg_color)
        salaire_label.pack(anchor="w")
        self.widgets_texte.append((salaire_label, "normal", True, False))

        salary_slider = ttk.Scale(sliders_frame, from_=0, to=100,
                                 orient=tk.HORIZONTAL,
                                 variable=self.salary_var,
                                 command=lambda x: update_score())
        salary_slider.pack(fill=tk.X, pady=(0, 15))

        # Slider 2: Carrière
        carriere_label = tk.Label(sliders_frame, text="Progression de carrière (16%)",
                font=police_normale_gras,
                fg=self.primary_color,
                bg=self.bg_color)
        carriere_label.pack(anchor="w")
        self.widgets_texte.append((carriere_label, "normal", True, False))

        career_slider = ttk.Scale(sliders_frame, from_=0, to=100,
                                 orient=tk.HORIZONTAL,
                                 variable=self.career_var,
                                 command=lambda x: update_score())
        career_slider.pack(fill=tk.X, pady=(0, 15))

        # Slider 3: Réseau
        reseau_label = tk.Label(sliders_frame, text="Réseau d'anciens élèves (8%)",
                font=police_normale_gras,
                fg=self.primary_color,
                bg=self.bg_color)
        reseau_label.pack(anchor="w")
        self.widgets_texte.append((reseau_label, "normal", True, False))

        network_slider = ttk.Scale(sliders_frame, from_=0, to=100,
                                  orient=tk.HORIZONTAL,
                                  variable=self.network_var,
                                  command=lambda x: update_score())
        network_slider.pack(fill=tk.X, pady=(0, 15))

        # Slider 4: Diversité
        diversite_label = tk.Label(sliders_frame, text="Diversité internationale (10%)",
                font=police_normale_gras,
                fg=self.primary_color,
                bg=self.bg_color)
        diversite_label.pack(anchor="w")
        self.widgets_texte.append((diversite_label, "normal", True, False))

        diversity_slider = ttk.Scale(sliders_frame, from_=0, to=100,
                                    orient=tk.HORIZONTAL,
                                    variable=self.diversity_var,
                                    command=lambda x: update_score())
        diversity_slider.pack(fill=tk.X, pady=(0, 15))

        # Slider 5: Recherche
        recherche_label = tk.Label(sliders_frame, text="Recherche académique (10%)",
                font=police_normale_gras,
                fg=self.primary_color,
                bg=self.bg_color)
        recherche_label.pack(anchor="w")
        self.widgets_texte.append((recherche_label, "normal", True, False))

        research_slider = ttk.Scale(sliders_frame, from_=0, to=100,
                                   orient=tk.HORIZONTAL,
                                   variable=self.research_var,
                                   command=lambda x: update_score())
        research_slider.pack(fill=tk.X, pady=(0, 15))

        # Slider 6: ESG
        esg_label = tk.Label(sliders_frame, text="Critères ESG (5%)",
                font=police_normale_gras,
                fg=self.primary_color,
                bg=self.bg_color)
        esg_label.pack(anchor="w")
        self.widgets_texte.append((esg_label, "normal", True, False))

        esg_slider = ttk.Scale(sliders_frame, from_=0, to=100,
                              orient=tk.HORIZONTAL,
                              variable=self.esg_var,
                              command=lambda x: update_score())
        esg_slider.pack(fill=tk.X, pady=(0, 15))

        # Initialiser le score
        update_score()

# Code principal pour lancer l'application
if __name__ == "__main__":
    # Configuration pour macOS (éviter les problèmes de rendu)
    import platform
    if platform.system() == "Darwin":
        import os
        os.environ['TK_SILENCE_DEPRECATION'] = '1'  # Supprimer les avertissements de dépréciation
        
    root = tk.Tk()
    # Optimisations pour macOS
    root.update_idletasks()  # Mettre à jour les tâches en attente
    app = MBAInsightsApp(root)
    root.mainloop()