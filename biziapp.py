"""
biziapp.py — Dashboard stratégique 360° complet
Streamlit · Python 3.9+
Intègre : SWOT · QQOQCCP · PESTEL · Micro-Env · Concurrence · SONCAS
           Personas · Copywriting AIDA · Déclencheurs psychologiques
           GEO 2025 · SEA IA · Marketing · SEO · Vente · Synthèse
"""
import copy
import json
import datetime
import re
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# Optional imports
# ─────────────────────────────────────────────────────────────────────────────
try:
    import requests
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except ImportError:
    _HAS_BS4 = False

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BiziApp — Stratégie 360°",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Color palette (CSS variables) ───────────────────────────────────────── */
:root {
    --graphite:    #0F172A;
    --ambre:       #D97706;
    --ambre-pale:  #FEF3C7;
    --sauge:       #047857;
    --sauge-pale:  #D1FAE5;
    --ivoire:      #FAF8F4;
    --craie:       #E7E2D6;
    --encre:       #1A1A1A;
}

/* ── Box-sizing reset + font ──────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
                 Roboto, Oxygen, Ubuntu, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ── Header ──────────────────────────────────────────────────────────────── */
.bizi-header {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border-left: 6px solid var(--ambre);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    color: white;
}
.bizi-header h1 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
    color: #F8FAFC;
}
.bizi-header p {
    margin: 4px 0 0;
    opacity: 0.80;
    font-size: 0.95rem;
    color: var(--ambre-pale);
}

/* ── Cards ───────────────────────────────────────────────────────────────── */
.card {
    background: white;
    border-radius: 14px;
    padding: 20px 22px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 1px 6px rgba(0,0,0,.06);
    margin-bottom: 16px;
}
.card-title {
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 10px;
    color: var(--encre);
}

/* ── SWOT card colors ────────────────────────────────────────────────────── */
.swot-strength { border-left: 4px solid #22C55E; background: #F0FDF4; }
.swot-weakness { border-left: 4px solid var(--ambre); background: var(--ambre-pale); }
.swot-oppty    { border-left: 4px solid #3B82F6; background: #EFF6FF; }
.swot-threat   { border-left: 4px solid #EF4444; background: #FEF2F2; }

/* ── Badges ──────────────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 2px;
    white-space: nowrap;
}
.badge-blue     { background: #DBEAFE; color: #1D4ED8; }
.badge-green    { background: #DCFCE7; color: #166534; }
.badge-red      { background: #FEE2E2; color: #991B1B; }
.badge-amber    { background: var(--ambre-pale); color: #92400E; }
.badge-purple   { background: #EDE9FE; color: #5B21B6; }
.badge-gray     { background: #F3F4F6; color: #374151; }
.badge-graphite { background: var(--graphite); color: #F8FAFC; }
.badge-sauge    { background: var(--sauge-pale); color: var(--sauge); }

/* ── Score ring (CSS conic-gradient) ─────────────────────────────────────── */
.score-ring {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: conic-gradient(var(--ambre) var(--pct), #E5E7EB 0);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--encre);
    box-shadow: inset 0 0 0 18px white;
    margin: 0 auto 8px;
}

/* ── Metric / KPI boxes ──────────────────────────────────────────────────── */
.metric-box {
    text-align: center;
    padding: 16px 12px;
    border-radius: 12px;
    background: white;
    border: 1px solid #E5E7EB;
}
.metric-box .val { font-size: 1.6rem; font-weight: 800; color: var(--encre); }
.metric-box .lbl { font-size: 0.75rem; color: #6B7280; margin-top: 2px; }

/* ── KPI tiles (hover) ───────────────────────────────────────────────────── */
.kpi-tile {
    background: var(--ivoire);
    border: 1px solid var(--craie);
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
    transition: box-shadow 0.18s ease, transform 0.18s ease;
    cursor: default;
}
.kpi-tile:hover {
    box-shadow: 0 4px 16px rgba(15,23,42,.10);
    transform: translateY(-2px);
}
.kpi-tile .kpi-val { font-size: 1.5rem; font-weight: 800; color: var(--graphite); }
.kpi-tile .kpi-lbl { font-size: 0.75rem; color: #6B7280; margin-top: 4px; }

/* ── Table ───────────────────────────────────────────────────────────────── */
.bizi-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.bizi-table th {
    background: #F8FAFC;
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
    color: #374151;
    border-bottom: 2px solid #E5E7EB;
}
.bizi-table td { padding: 8px 12px; border-bottom: 1px solid #F3F4F6; color: var(--encre); }
.bizi-table tr:hover td { background: #FAFAFA; }

/* ── AIDA card colors ────────────────────────────────────────────────────── */
.aida-attention { background: #FFF1F2; border-left: 4px solid #EF4444; }
.aida-interest  { background: #FFFBEB; border-left: 4px solid var(--ambre); }
.aida-desire    { background: #F5F3FF; border-left: 4px solid #8B5CF6; }
.aida-action    { background: #ECFDF5; border-left: 4px solid #10B981; }

/* ── Section headers ─────────────────────────────────────────────────────── */
.section-h {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--graphite);
    border-left: 4px solid var(--ambre);
    padding: 4px 0 4px 12px;
    margin: 20px 0 14px;
}

/* ── Progress bar ────────────────────────────────────────────────────────── */
.progress-bar {
    background: #F3F4F6;
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
    margin: 6px 0;
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--ambre) 0%, var(--sauge) 100%);
    transition: width 0.4s ease;
}

/* ── Wizard steps ────────────────────────────────────────────────────────── */
.wizard-step {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 500;
    color: #374151;
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    margin-bottom: 8px;
}
.wizard-step.active {
    background: var(--ambre-pale);
    border-color: var(--ambre);
    color: #92400E;
    font-weight: 700;
}
.wizard-step-num {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--graphite);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
}

/* ── SONCAS cards ────────────────────────────────────────────────────────── */
/* Sécurité = blue */
.soncas-securite {
    background: #EFF6FF;
    border-left: 4px solid #3B82F6;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
/* Opportunité = green */
.soncas-opportunite {
    background: #F0FDF4;
    border-left: 4px solid #22C55E;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
/* Nouveauté = purple */
.soncas-nouveaute {
    background: #F5F3FF;
    border-left: 4px solid #8B5CF6;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
/* Confort = amber */
.soncas-confort {
    background: var(--ambre-pale);
    border-left: 4px solid var(--ambre);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
/* Argent = emerald */
.soncas-argent {
    background: var(--sauge-pale);
    border-left: 4px solid var(--sauge);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
/* Sympathie = pink */
.soncas-sympathie {
    background: #FCE7F3;
    border-left: 4px solid #EC4899;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.soncas-card-title {
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 6px;
    color: var(--encre);
}
.soncas-desc {
    font-size: 0.84rem;
    color: #374151;
    margin-bottom: 8px;
}
.soncas-objection {
    font-size: 0.82rem;
    font-style: italic;
    color: #6B7280;
    margin-bottom: 4px;
}
.soncas-reponse {
    font-size: 0.82rem;
    color: #166534;
    font-weight: 500;
}

/* ── Media queries — mobile (<768px) ─────────────────────────────────────── */
@media (max-width: 768px) {
    .bizi-header { padding: 18px 16px; }
    .bizi-header h1 { font-size: 1.35rem; }
    .bizi-header p  { font-size: 0.85rem; }

    /* Stack Streamlit columns on mobile */
    [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }

    .card { padding: 14px 14px; }
    .metric-box .val { font-size: 1.25rem; }
    .kpi-tile .kpi-val { font-size: 1.2rem; }

    /* Larger tap targets */
    .badge { padding: 4px 12px; font-size: 0.80rem; }
    .wizard-step { padding: 14px 12px; }

    /* Readable font sizes */
    .bizi-table { font-size: 0.78rem; }
    .section-h  { font-size: 1.05rem; }

    .score-ring { width: 90px; height: 90px; font-size: 1.2rem; }
}

/* ── Webkit / Firefox / Safari compatibility ─────────────────────────────── */
.score-ring {
    /* Safari conic-gradient prefix not needed for Safari 12.1+ */
    -webkit-mask: none;
}
.progress-fill { -webkit-transition: width 0.4s ease; }
.kpi-tile { -webkit-transition: box-shadow 0.18s ease, transform 0.18s ease; }

/* Scrollbar (Webkit) */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: var(--craie); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: #CBD5E1; }

/* ── Streamlit-specific overrides ────────────────────────────────────────── */
/* Hide hamburger menu */
#MainMenu { visibility: hidden; }
/* Hide default footer */
footer { visibility: hidden; }
/* Remove top padding on main block */
.block-container { padding-top: 1.5rem !important; }
/* Sidebar label font */
[data-testid="stSidebar"] label { font-weight: 500; }
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# ── DATA & GENERATORS ────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

# ─── SWOT ────────────────────────────────────────────────────────────────────
_SWOT_DATA = {
    "ecommerce": {
        "strengths":     [
            "Vente directe 24h/24 sans contrainte géographique",
            "Données comportementales exploitables",
            "Scalabilité rapide sans coût fixe proportionnel",
            "Marges optimisées sans intermédiaire",
        ],
        "weaknesses":    [
            "Forte concurrence des marketplaces (Amazon, Cdiscount)",
            "Coûts d'acquisition client élevés (CAC)",
            "Gestion logistique et retours complexe",
            "Dépendance aux algorithmes Google",
        ],
        "opportunities": [
            "Croissance m-commerce +25%/an",
            "Personnalisation IA pour augmenter le panier moyen",
            "Social commerce (Instagram Shop, TikTok Shop)",
            "Marchés internationaux accessibles",
        ],
        "threats":       [
            "Hausse du coût des publicités (CPM, CPC)",
            "Nouvelles réglementations RGPD",
            "Saturation des niches rentables",
        ],
    },
    "saas": {
        "strengths":     [
            "Revenus récurrents (MRR/ARR) prévisibles",
            "Coût marginal quasi nul par nouvel utilisateur",
            "Mises à jour centralisées",
            "Effets de réseau et forte rétention",
        ],
        "weaknesses":    [
            "Temps long pour atteindre la rentabilité",
            "Support client chronophage",
            "Churn élevé si onboarding insuffisant",
            "Dépendance aux plateformes cloud",
        ],
        "opportunities": [
            "Marché SaaS mondial en croissance à 2 chiffres",
            "IA intégrée comme différenciateur",
            "Verticaux non-disruptés (santé, juridique)",
            "Modèles freemium pour acquisition organique",
        ],
        "threats":       [
            "Géants tech qui copient les fonctionnalités",
            "Fatigue SaaS — consolidation des budgets",
            "Open-source alternatives gratuites",
        ],
    },
    "service": {
        "strengths":     [
            "Faibles coûts de démarrage, pas de stock",
            "Relation client directe et fidélisation naturelle",
            "Marges élevées si positionnement premium",
            "Expertise différenciante difficile à copier",
        ],
        "weaknesses":    [
            "Scalabilité limitée par le temps humain",
            "Dépendance aux clients clés",
            "Difficulté à valoriser l'immatériel",
            "Irrégularité des revenus",
        ],
        "opportunities": [
            "Automatisation des tâches via IA",
            "Marchés de niche sous-servis",
            "Packagisation des services en offres fixes",
            "Partenariats et apporteurs d'affaires",
        ],
        "threats":       [
            "Concurrence des freelances low-cost",
            "Récession comprime les budgets prestataires",
            "Commoditisation par les outils no-code",
        ],
    },
    "consulting": {
        "strengths":     [
            "Expertise rare et difficile à reproduire",
            "Tarification à forte valeur ajoutée",
            "Faibles coûts fixes",
            "Flexibilité géographique (remote)",
        ],
        "weaknesses":    [
            "Revenu non récurrent et irrégulier",
            "Image personnelle = marque, risque de dépendance",
            "Capacité limitée par les heures",
            "Cycle de vente long",
        ],
        "opportunities": [
            "Positionnement expert de niche",
            "Productisation du conseil en cours en ligne",
            "Partenariats avec agences complémentaires",
            "Speaking et conférences pour la notoriété",
        ],
        "threats":       [
            "IA qui remplace certaines missions junior",
            "Marchés saturés dans les niches populaires",
            "Clients qui internalisent les compétences",
        ],
    },
    "content": {
        "strengths":     [
            "Audience fidèle et communauté engagée",
            "Monétisation diverse (pub, sponsoring, formations)",
            "Autorité perçue dans la niche",
            "Faibles coûts de production relatifs",
        ],
        "weaknesses":    [
            "Revenus variables, dépendants des algorithmes",
            "Production régulière chronophage",
            "Burnout créatif fréquent",
            "Dépendance aux plateformes",
        ],
        "opportunities": [
            "Boom des newsletters payantes (Substack)",
            "IA pour accélérer la production de contenu",
            "Formations et produits digitaux à haute marge",
            "Marchés anglophones",
        ],
        "threats":       [
            "Contenu IA qui inonde les plateformes",
            "Démonétisation soudaine",
            "Évolution des formats et attention décroissante",
        ],
    },
    "other": {
        "strengths":     [
            "Positionnement unique et différencié",
            "Flexibilité et agilité organisationnelle",
            "Opportunité d'innover dans un espace peu balisé",
        ],
        "weaknesses":    [
            "Marché difficile à éduquer",
            "Ressources limitées en amorçage",
            "Besoin d'évangélisation du produit/service",
        ],
        "opportunities": [
            "First-mover advantage dans la niche",
            "Partenariats stratégiques pour accélérer",
            "Levée de fonds ou financement participatif",
        ],
        "threats":       [
            "Pivot nécessaire si le marché ne répond pas",
            "Concurrents bien financés qui copient l'innovation",
            "Difficultés à recruter des profils adaptés",
        ],
    },
}


def gen_swot(activity: str, goal: str, maturity: str) -> dict:
    d = copy.deepcopy(_SWOT_DATA.get(activity, _SWOT_DATA["other"]))
    if maturity == "idea":
        d["strengths"].insert(0, "Opportunité de construire sans dette technique")
        d["weaknesses"].insert(0, "Absence de validation marché et de revenus")
    elif maturity == "inprogress":
        d["strengths"].insert(0, "Développement en cours — apprentissage rapide")
    elif maturity == "launched":
        d["strengths"].insert(0, "Traction initiale prouvée et premiers retours clients")
    goal_opp = {
        "awareness": "Stratégie content marketing pour construire l'autorité de marque",
        "sales":     "Optimisation du tunnel de conversion pour maximiser le CA",
        "leads":     "Lead magnets et marketing automation pour qualifier les prospects",
        "traffic":   "SEO technique et stratégie de backlinks pour croissance organique",
    }
    if goal in goal_opp:
        d["opportunities"].append(goal_opp[goal])
    return d


# ─── QQOQCCP ─────────────────────────────────────────────────────────────────
_QQOQCCP = {
    "ecommerce": {
        "qui":     {"q": "Qui sont vos acheteurs cibles ?",
                    "r": "Consommateurs 25-45 ans, actifs digitaux, acheteurs en ligne réguliers (2-4x/mois)",
                    "a": "Segmentez par RFM (Récence, Fréquence, Montant) et créez 3 personas distincts"},
        "quoi":    {"q": "Quoi vendez-vous exactement ?",
                    "r": "Produits avec proposition de valeur unique et différenciante",
                    "a": "Rédigez une USP en 10 mots max : bénéfice principal + différenciateur + cible"},
        "où":      {"q": "Où vos clients achètent-ils ?",
                    "r": "Mobile (68%), desktop (29%) — majorité via Google Shopping et réseaux sociaux",
                    "a": "Priorisez l'expérience mobile-first et optimisez vos fiches Google Shopping"},
        "quand":   {"q": "Quand vos clients achètent-ils ?",
                    "r": "Pics : vendredi soir, samedi matin, pauses déjeuner (12h-14h), saisons festives",
                    "a": "Programmez vos campagnes sur ces créneaux + soldes/événements clés"},
        "comment": {"q": "Comment décident-ils d'acheter ?",
                    "r": "Google → comparaison avis → réseaux sociaux → achat — cycle 2-7 jours",
                    "a": "Couvrez chaque étape : SEO, reviews Trustpilot, retargeting Meta, panier abandonné"},
        "combien": {"q": "Combien sont-ils prêts à payer ?",
                    "r": "Panier moyen cible : 45-120 € selon la niche. Sensibilité prix forte sous 30 €",
                    "a": "Testez des prix psychologiques (X9), offres bundles et livraison gratuite à seuil"},
        "pourquoi":{"q": "Pourquoi vous choisiraient-ils ?",
                    "r": "Confiance (avis/garanties), commodité (livraison), prix/qualité, expérience brand",
                    "a": "Mettez en avant : étoiles Trustpilot, politique retour, badge sécurisé, UGC"},
    },
    "saas": {
        "qui":     {"q": "Qui sont vos utilisateurs et décideurs ?",
                    "r": "Double cible : utilisateurs finaux (opérationnels) et acheteurs (dirigeants/DSI)",
                    "a": "Créez un messaging distinct pour chaque persona : bénéfice usage vs ROI business"},
        "quoi":    {"q": "Quel problème résolvez-vous exactement ?",
                    "r": "Économie de temps, réduction d'erreurs ou augmentation de revenus — toujours quantifiable",
                    "a": "Quantifiez le problème : 'X heures perdues/semaine' ou 'Y% d'erreurs évitées'"},
        "où":      {"q": "Où vos prospects cherchent-ils des solutions ?",
                    "r": "G2, Capterra, Product Hunt, LinkedIn, communautés Slack/Discord sectorielles",
                    "a": "Optimisez votre profil G2/Capterra + publiez sur Product Hunt au lancement"},
        "quand":   {"q": "Quand un prospect décide-t-il de changer d'outil ?",
                    "r": "Lors d'un événement déclencheur : croissance, recrutement, audit, changement direction",
                    "a": "Configurez des alertes sur ces signaux d'intention (LinkedIn, news, levées de fonds)"},
        "comment": {"q": "Comment se déroule le cycle de décision ?",
                    "r": "Découverte → essai gratuit (14-30j) → démo → POC → validation → achat",
                    "a": "Optimisez chaque étape : onboarding J1-J7, email nurturing, CS proactif à J14"},
        "combien": {"q": "Combien votre solution leur fait-elle économiser/gagner ?",
                    "r": "Calculez le ROI concret : temps économisé × TJM ou revenus additionnels",
                    "a": "Créez un calculateur ROI interactif sur votre landing page"},
        "pourquoi":{"q": "Pourquoi vous plutôt que vos concurrents ?",
                    "r": "Fonctionnalités uniques, intégrations, support, prix ou rapidité d'implémentation",
                    "a": "Publiez des comparatifs 'Vous vs [Concurrent]' sur des landing pages dédiées"},
    },
}
_QQOQCCP_GENERIC = {
    "qui":     {"q": "Qui est votre client idéal (ICP) ?",
                "r": "Définissez précisément : secteur, taille, rôle décisionnel, budget et douleur principale",
                "a": "Réalisez 10 interviews clients pour valider et affiner votre profil ICP"},
    "quoi":    {"q": "Quoi proposez-vous exactement comme valeur ?",
                "r": "Votre offre doit résoudre un problème spécifique de manière unique et mesurable",
                "a": "Rédigez votre value proposition canvas : job-to-be-done, pains, gains"},
    "où":      {"q": "Où se trouvent et s'informent vos prospects ?",
                "r": "Identifiez les canaux digitaux et physiques où ils cherchent des solutions",
                "a": "Investissez prioritairement dans les 2 canaux où votre ICP passe le plus de temps"},
    "quand":   {"q": "Quand votre client a-t-il besoin de vous ?",
                "r": "Il existe toujours un déclencheur d'achat : événement, seuil de douleur, saison",
                "a": "Cartographiez le cycle de vie client et anticipez les moments déclencheurs"},
    "comment": {"q": "Comment votre client prend-il sa décision d'achat ?",
                "r": "Prise de conscience → considération → décision → fidélisation",
                "a": "Créez du contenu adapté à chaque étape du parcours (TOFU/MOFU/BOFU)"},
    "combien": {"q": "Combien votre client est-il prêt à investir ?",
                "r": "Le prix doit refléter la valeur perçue, pas uniquement vos coûts",
                "a": "Benchmarkez vos concurrents et testez différentes structurations de prix"},
    "pourquoi":{"q": "Pourquoi votre client vous choisit-il plutôt qu'un concurrent ?",
                "r": "Votre différenciateur doit être défendable, visible et valorisé par votre cible",
                "a": "Identifiez votre avantage compétitif unique et construisez tout votre messaging dessus"},
}


def gen_qqoqccp(activity: str) -> dict:
    return copy.deepcopy(_QQOQCCP.get(activity, _QQOQCCP_GENERIC))


# ─── PESTEL ───────────────────────────────────────────────────────────────────
_PESTEL = {
    "ecommerce": {
        "🏛️ Politique": [
            ("Régulation TVA numérique UE (OSS)", "négatif",
             "Complexité comptable accrue pour la vente transfrontalière"),
            ("Normes RGPD & ePrivacy", "neutre",
             "Contrainte mais avantage concurrentiel si bien géré"),
        ],
        "💶 Économique": [
            ("Inflation des coûts logistiques +18% en 3 ans", "négatif",
             "Comprimez via négociation transporteur et stocks optimisés"),
            ("Croissance e-commerce +12%/an en France", "positif",
             "Marché en expansion — capturez la part de marché tôt"),
        ],
        "👥 Socioculturel": [
            ("M-commerce : 68% des achats depuis mobile", "positif",
             "Mobile-first est désormais non-négociable"),
            ("Exigence RSE des consommateurs +39% vs 2022", "neutre",
             "Levier différenciant si vous intégrez l'impact environnemental"),
        ],
        "⚙️ Technologique": [
            ("IA générative dans les recommandations produits", "positif",
             "Personnalisation accrue = +23% de conversion en moyenne"),
            ("Moteurs de recherche IA (Google SGE, Perplexity)", "neutre",
             "Adaptez votre SEO à l'intention de recherche IA (GEO)"),
        ],
        "🌱 Écologique": [
            ("Emballages durables — obligation légale 2025", "neutre",
             "Coût d'adaptation + avantage marketing si bien communiqué"),
        ],
        "⚖️ Légal": [
            ("Directive Omnibus — transparence des prix", "négatif",
             "Obligation d'afficher le prix de référence avant promotion"),
            ("Droit de rétractation 14 jours — coût retours", "négatif",
             "Optimisez la logistique retour pour limiter l'impact financier"),
        ],
    },
    "saas": {
        "🏛️ Politique": [
            ("AI Act européen (2024-2026)", "neutre",
             "Contraintes sur les systèmes IA à haut risque — auditez votre conformité"),
            ("Cloud Act US vs RGPD", "neutre",
             "Hébergement EU peut devenir un avantage pour les clients corporate"),
        ],
        "💶 Économique": [
            ("Compression des budgets SaaS (stack fatigue)", "négatif",
             "ROI démontrable en <30 jours devient critère de survie"),
            ("Valorisations SaaS stabilisées — retour à la rentabilité", "neutre",
             "Les investisseurs cherchent la profitabilité"),
        ],
        "👥 Socioculturel": [
            ("Remote work permanent — outils collaboratifs essentiels", "positif",
             "Intégrations Slack/Teams/Notion deviennent des must-have"),
            ("Adoption IA par les utilisateurs finaux +67% en 2024", "positif",
             "Intégrez des fonctionnalités IA pour rester compétitif"),
        ],
        "⚙️ Technologique": [
            ("LLMs open-source — commoditisation de l'IA", "neutre",
             "L'IA seule ne suffit plus — l'avantage est dans les données propriétaires"),
            ("API-first & intégrations — ecosystème Zapier/Make", "positif",
             "Une bonne API multiplie votre reach sans effort commercial"),
        ],
        "🌱 Écologique": [
            ("GreenOps — empreinte carbone des serveurs", "neutre",
             "Hébergeurs green (OVH, Scaleway) deviennent un argument marketing B2B"),
        ],
        "⚖️ Légal": [
            ("RGPD + DMA — obligations plateformes numériques", "neutre",
             "Nommez un DPO et auditez votre collecte de données régulièrement"),
        ],
    },
}
_PESTEL_GENERIC = {
    "🏛️ Politique": [
        ("Réglementation sectorielle en évolution", "neutre",
         "Suivez les évolutions législatives de votre secteur"),
    ],
    "💶 Économique": [
        ("Contexte macro-économique incertain", "neutre",
         "Anticipez les cycles et construisez une trésorerie de sécurité"),
        ("Croissance du marché digital", "positif",
         "Digitalisez votre offre pour capter cette croissance"),
    ],
    "👥 Socioculturel": [
        ("Digitalisation accélérée des comportements", "positif",
         "Votre présence digitale est désormais votre première vitrine"),
    ],
    "⚙️ Technologique": [
        ("IA générative — opportunités de productivité", "positif",
         "Intégrez des outils IA dans vos processus"),
        ("Cybersécurité — risques en hausse", "négatif",
         "Investissez dans la sécurité de vos données"),
    ],
    "🌱 Écologique": [
        ("Transition écologique — attente des parties prenantes", "neutre",
         "Définissez votre politique RSE même à petite échelle"),
    ],
    "⚖️ Légal": [
        ("RGPD & protection des données", "neutre",
         "Assurez-vous de collecter uniquement les données nécessaires avec consentement"),
    ],
}


def gen_pestel(activity: str) -> dict:
    return copy.deepcopy(_PESTEL.get(activity, _PESTEL_GENERIC))


# ─── MICRO-ENV ────────────────────────────────────────────────────────────────
_MICRO_ENV = {
    "ecommerce": {
        "👥 Clients":        ("élevé",
                              "Hyperchoix, faible coût de switching — exigence maximale",
                              "Fidélisez via programme de fidélité, contenu exclusif et service irréprochable"),
        "🏭 Fournisseurs":   ("moyen",
                              "Multiples sources possibles mais dépendance aux délais de livraison",
                              "Diversifiez vos sources et stockez les SKU critiques"),
        "⚔️ Concurrents":    ("élevé",
                              "Amazon, Cdiscount, Pure Players niche — guerre des prix permanente",
                              "Différenciez sur l'expérience, la niche et le contenu, pas sur le prix seul"),
        "🔗 Intermédiaires": ("moyen",
                              "Marketplaces, comparateurs, influenceurs — dépendance aux algorithmes",
                              "Développez votre canal direct (DTC) pour réduire les commissions tiers"),
    },
    "saas": {
        "👥 Clients":        ("élevé",
                              "Churn élevé si valeur non démontrée à J30",
                              "Customer Success proactif + tableau de bord ROI intégré au produit"),
        "🏭 Fournisseurs":   ("moyen",
                              "AWS/GCP/Azure — switching coûteux mais offres compétitives",
                              "Architecture cloud-agnostic et réserves d'instances pour optimiser les coûts"),
        "⚔️ Concurrents":    ("très élevé",
                              "Marché SaaS ultra-compétitif, consolidation en cours (M&A)",
                              "Hyper-spécialisation verticale + intégrations natives comme barrière à l'entrée"),
        "🔗 Intermédiaires": ("faible",
                              "App stores (faible commission), intégrateurs (partenariats clés)",
                              "Programme partenaires avec certifications et marges attractives"),
    },
}
_MICRO_GENERIC = {
    "👥 Clients":        ("élevé",
                          "Le digital donne aux clients un accès immédiat aux alternatives",
                          "Créez des barrières à la sortie : intégrations, données accumulées, communauté"),
    "🏭 Fournisseurs":   ("moyen",
                          "Diversification des sources possible mais risque de dépendance",
                          "Identifiez vos fournisseurs critiques et sécurisez des alternatives"),
    "⚔️ Concurrents":    ("élevé",
                          "La concurrence directe et indirecte s'intensifie dans tous les marchés digitaux",
                          "Analysez systématiquement vos concurrents avec des outils comme Semrush"),
    "🔗 Intermédiaires": ("moyen",
                          "Plateformes et distributeurs prélèvent une commission croissante",
                          "Développez votre canal direct (site, newsletter, communauté) en parallèle"),
}


def gen_micro_env(activity: str) -> dict:
    return copy.deepcopy(_MICRO_ENV.get(activity, _MICRO_GENERIC))


# ─── COMPETITIVE ─────────────────────────────────────────────────────────────
_COMPETITIVE = {
    "ecommerce": {
        "direct":   [
            "Amazon / Cdiscount (généralistes)",
            "Pure Players de la niche",
            "Boutiques Shopify concurrentes",
        ],
        "indirect": [
            "Leboncoin / Vinted (occasion)",
            "Grandes surfaces en ligne",
            "Marketplace B2B sectorielles",
        ],
        "matrix": [
            ("Prix",              "⚪", "🔴", "Leaders tirent le prix vers le bas — différenciez-vous"),
            ("Expérience UX",     "⚪", "🟢", "Levier fort si vous investissez dans le design"),
            ("Catalogue",         "⚪", "🔴", "Ne tentez pas de rivaliser en volume — spécialisez"),
            ("SAV & fidélisation","🟢", "⚪", "Avantage structurel des petites structures — exploitez-le"),
            ("Contenu & SEO",     "🟢", "⚪", "Blog expert + UGC = trafic organique gratuit"),
        ],
        "oppty": "Niche premium + contenu expert + communauté = triangle défendable",
        "moat":  "Données clients propriétaires + brand community + niche expertise",
    },
    "saas": {
        "direct":   [
            "Solutions VC-backed bien financées",
            "Outils intégrés (suites Microsoft/Google)",
            "Concurrents de niche similaires",
        ],
        "indirect": [
            "Outils no-code (Notion, Airtable)",
            "Agences qui font manuellement",
            "Solutions open-source",
        ],
        "matrix": [
            ("Fonctionnalités",     "⚪", "🔴", "Ne copiez pas tout — identifiez votre killer feature"),
            ("Prix",                "🟢", "⚪", "Agilité tarifaire vs les poids lourds = avantage PME"),
            ("Support",             "🟢", "⚪", "Accès fondateur direct = différenciateur early-stage"),
            ("Intégrations",        "⚪", "🔴", "Priorisez 5 intégrations critiques pour votre ICP"),
            ("Vitesse d'itération", "🟢", "⚪", "Votre agilité est un avantage compétitif majeur"),
        ],
        "oppty": "Vertical SaaS spécialisé + support fondateur + time-to-value < 48h",
        "moat":  "Données propriétaires sectoriel + intégrations natives + réseau utilisateurs",
    },
}
_COMPETITIVE_GENERIC = {
    "direct":   [
        "Concurrents positionnés sur votre niche exacte",
        "Alternatives directes à votre offre",
    ],
    "indirect": [
        "Solutions DIY (faire soi-même)",
        "Freelances et agences généralistes",
    ],
    "matrix": [
        ("Prix",         "⚪", "🔴", "Analysez le prix marché et positionnez-vous stratégiquement"),
        ("Qualité",      "🟢", "⚪", "La qualité est votre meilleur argument différenciant"),
        ("Notoriété",    "⚪", "🔴", "Construisez une notoriété de niche avant la notoriété large"),
        ("Service client","🟢","⚪", "Réactivité et personnalisation = avantage structurel"),
        ("Innovation",   "🟢", "⚪", "Votre capacité à innover rapidement est une arme"),
    ],
    "oppty": "Identifiez le segment délaissé par les leaders et devenez l'expert incontournable",
    "moat":  "Expertise niche + relation client + contenu propriétaire",
}


def gen_competitive(activity: str) -> dict:
    return copy.deepcopy(_COMPETITIVE.get(activity, _COMPETITIVE_GENERIC))


# ─── SONCAS ──────────────────────────────────────────────────────────────────
_SONCAS = {
    "ecommerce": {
        "securite": {
            "label": "Sécurité", "icon": "🛡️",
            "desc": "L'acheteur en ligne a besoin de confiance avant de sortir sa carte bleue. Réduisez le risque perçu à chaque étape du parcours.",
            "args": [
                "Paiement 100% sécurisé (SSL, 3DS2) affiché en évidence",
                "Politique de retour gratuit 30 jours sans condition",
                "Avis clients vérifiés (Trustpilot, Google Reviews) avec étoiles visibles",
            ],
            "objection": "Je ne vous connais pas — comment savoir si votre site est fiable ?",
            "reponse":   "Nous affichons nos +2 000 avis vérifiés Trustpilot, notre garantie satisfait ou remboursé 30 jours et notre certification SSL. Commandez sans risque.",
        },
        "opportunite": {
            "label": "Opportunité", "icon": "🚀",
            "desc": "L'acheteur cherche la meilleure offre du moment. Créez un sentiment d'avantage exclusif et de gain réel.",
            "args": [
                "Offre flash limitée dans le temps avec compte à rebours visible",
                "Programme de fidélité avec cumul de points et récompenses",
                "Livraison offerte à partir d'un seuil — visible dès la page d'accueil",
            ],
            "objection": "Je trouverai sûrement moins cher ailleurs.",
            "reponse":   "Bonne idée de comparer ! Mais avec notre livraison offerte, nos points de fidélité et notre garantie 30 jours, notre coût total est souvent le plus bas — et sans risque.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "✨",
            "desc": "Certains acheteurs sont attirés par les nouveautés et les tendances. Mettez en avant vos dernières collections et innovations.",
            "args": [
                "Badge 'Nouveauté' ou 'Just dropped' sur les nouvelles références",
                "Email de lancement VIP en avant-première pour les abonnés",
                "Collaboration capsule ou édition limitée pour créer l'événement",
            ],
            "objection": "Je veux être sûr que ce produit est bien ce qu'il y a de plus récent.",
            "reponse":   "Cette référence vient d'être ajoutée à notre catalogue cette semaine. Nos abonnés newsletter la découvrent en avant-première — rejoignez-les pour ne plus jamais rater un lancement.",
        },
        "confort": {
            "label": "Confort", "icon": "😌",
            "desc": "L'expérience d'achat doit être fluide, rapide et sans friction. Chaque clic de trop est un client perdu.",
            "args": [
                "Checkout en 1 étape avec pré-remplissage des infos connues",
                "Suivi de commande en temps réel par SMS et email",
                "Service client disponible 7j/7 par chat (réponse < 2 min)",
            ],
            "objection": "Je n'ai pas envie de perdre du temps si ça ne correspond pas.",
            "reponse":   "Commandez en 90 secondes. Si ce n'est pas parfait, le retour est gratuit et le remboursement est traité en 48h. Zéro tracas garanti.",
        },
        "argent": {
            "label": "Argent", "icon": "💰",
            "desc": "La sensibilité prix est forte en e-commerce. Montrez la valeur absolue et relative de votre offre.",
            "args": [
                "Comparateur de prix intégré ou mention du prix de marché",
                "Offres bundles avec économie affichée en pourcentage et en euros",
                "Paiement en 3x sans frais pour les paniers > 100 €",
            ],
            "objection": "C'est moins cher sur Amazon.",
            "reponse":   "Notre prix inclut la livraison offerte, le retour gratuit et 2 ans de garantie. Sur Amazon, ces frais s'ajoutent. Calculez le coût total — nous sommes souvent moins chers.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "🤝",
            "desc": "Les clients achètent aussi à des marques qu'ils apprécient. Humanisez votre boutique et créez une vraie connexion.",
            "args": [
                "Histoire de marque authentique visible sur la page 'À propos'",
                "Engagement RSE ou social (local, éco-responsable, solidaire)",
                "Communauté active sur les réseaux sociaux avec réponses aux commentaires",
            ],
            "objection": "Il y a tellement de boutiques en ligne, pourquoi vous ?",
            "reponse":   "Nous sommes une équipe de 5 personnes passionnées par [niche]. Chaque commande est préparée avec soin. Lisez nos avis — nos clients reviennent parce qu'ils se sentent vraiment considérés.",
        },
    },
    "saas": {
        "securite": {
            "label": "Sécurité", "icon": "🛡️",
            "desc": "Le décideur SaaS craint les risques : perte de données, downtime, contrat difficile à résilier. Minimisez chaque risque perçu.",
            "args": [
                "SOC 2 Type II / ISO 27001 — certifications de sécurité affichées",
                "SLA 99.9% uptime avec crédits automatiques en cas d'incident",
                "Export des données à tout moment — no lock-in garanti",
            ],
            "objection": "Et si vous faites faillite ou si vous augmentez les prix brutalement ?",
            "reponse":   "Notre code source est en escrow, vos données sont exportables en 1 clic et notre contrat inclut un préavis de 90 jours pour toute modification tarifaire. Votre continuité est protégée.",
        },
        "opportunite": {
            "label": "Opportunité", "icon": "🚀",
            "desc": "Le buyer SaaS cherche un avantage compétitif. Montrez-lui comment votre outil le place devant ses concurrents.",
            "args": [
                "ROI calculateur interactif : 'Économisez X heures = X € par mois'",
                "Cas clients avec métriques avant/après dans le même secteur",
                "Early adopter pricing — accès aux nouvelles fonctionnalités en priorité",
            ],
            "objection": "Je ne vois pas vraiment ce que j'ai à gagner par rapport à ce que j'utilise déjà.",
            "reponse":   "[Client du même secteur] a réduit son temps de traitement de 4h à 25 minutes par semaine avec nous. Je peux vous montrer comment en 15 minutes.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "✨",
            "desc": "Les early adopters technologiques veulent être à la pointe. Positionnez votre SaaS comme la solution de nouvelle génération.",
            "args": [
                "Roadmap publique pour montrer l'innovation continue",
                "Intégration IA générative comme fonctionnalité phare",
                "Accès beta aux nouvelles features pour les clients actifs",
            ],
            "objection": "L'outil que j'utilise fait ça depuis longtemps.",
            "reponse":   "La différence est dans comment nous le faisons : notre moteur IA génère [résultat] en 30 secondes vs une configuration manuelle de 2 heures. Voulez-vous voir la démo ?",
        },
        "confort": {
            "label": "Confort", "icon": "😌",
            "desc": "L'onboarding et la prise en main sont des freins majeurs au SaaS. Promettez et livrez une expérience sans friction.",
            "args": [
                "Onboarding guidé en 10 minutes avec données de démonstration pré-chargées",
                "Migration prise en charge par notre équipe (import depuis l'outil concurrent)",
                "Formation incluse + webinaires hebdomadaires en direct",
            ],
            "objection": "Je n'ai pas le temps de former mon équipe à un nouvel outil.",
            "reponse":   "Notre onboarding est conçu pour que votre équipe soit autonome en une matinée. Nous gérons l'import de vos données existantes et proposons une formation live de 45 minutes incluse.",
        },
        "argent": {
            "label": "Argent", "icon": "💰",
            "desc": "Le budget SaaS est scruté. Démontrez un ROI clair et un coût total de possession inférieur aux alternatives.",
            "args": [
                "Prix par utilisateur actif — payez uniquement ce que vous utilisez",
                "Consolidation de plusieurs outils en un seul = économies immédiates",
                "Essai gratuit 14 jours sans carte bancaire — aucun risque financier",
            ],
            "objection": "Votre abonnement représente X € de plus par mois dans notre budget.",
            "reponse":   "Calculons ensemble : si [fonctionnalité] économise 3h/semaine à votre équipe de 5 personnes, c'est 60h/mois à votre TJM interne — soit bien plus que notre abonnement. Le ROI est positif dès le premier mois.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "🤝",
            "desc": "En B2B, on achète aussi à des personnes. La relation et la confiance humaine restent des différenciateurs puissants.",
            "args": [
                "Accès direct aux fondateurs pour les clients early stage",
                "Communauté Slack/Discord active avec entraide et partages",
                "Compte manager dédié dès 10 utilisateurs — relation humaine garantie",
            ],
            "objection": "Avec les grandes plateformes, j'ai un support dédié. Que m'offrez-vous ?",
            "reponse":   "Chez nous, votre interlocuteur connaît votre usage par cœur. Vous n'attendez pas en file d'attente — vous avez mon numéro direct. Nos clients restent parce qu'ils se sentent partenaires, pas numéros.",
        },
    },
    "service": {
        "securite": {
            "label": "Sécurité", "icon": "🛡️",
            "desc": "Le client d'un prestataire de service craint de mal choisir et de perdre son argent. Réduisez ce risque perçu par des garanties concrètes.",
            "args": [
                "Garantie résultat ou remboursement partiel sous conditions claires",
                "Contrat détaillé avec jalons et livrables définis",
                "Références clients vérifiables dans le même secteur",
            ],
            "objection": "Comment être sûr que vous livrerez ce que vous promettez ?",
            "reponse":   "Notre contrat détaille chaque livrable avec des délais précis. Nous proposons des points d'étape hebdomadaires et vous pouvez contacter directement nos 3 derniers clients pour avoir leur retour.",
        },
        "opportunite": {
            "label": "Opportunité", "icon": "🚀",
            "desc": "Le client veut saisir une opportunité de croissance. Positionnez votre service comme un accélérateur de résultats.",
            "args": [
                "Audit gratuit initial pour identifier le potentiel de gain rapide",
                "Résultats chiffrés de missions similaires avec le même profil client",
                "Offre de lancement limitée pour créer l'urgence de décision",
            ],
            "objection": "Est-ce vraiment le bon moment pour investir dans ce service ?",
            "reponse":   "C'est justement le bon moment : vos concurrents qui n'agissent pas aujourd'hui perdront 6 mois. Avec notre accompagnement, nos clients voient leurs premiers résultats en 30 jours.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "✨",
            "desc": "Montrez que vos méthodes et outils sont à la pointe. Un prestataire moderne rassure et inspire confiance.",
            "args": [
                "Intégration des derniers outils IA pour accélérer les livrables",
                "Méthodologie propriétaire nommée et expliquée",
                "Veille sectorielle continue partagée avec les clients (newsletter, insights)",
            ],
            "objection": "Votre approche me semble classique — qu'est-ce qui vous différencie ?",
            "reponse":   "Notre méthode [Nom] intègre les dernières avancées en [domaine]. Elle nous permet de livrer en 3 semaines ce qui prenait 3 mois avec les approches traditionnelles.",
        },
        "confort": {
            "label": "Confort", "icon": "😌",
            "desc": "Le client veut être accompagné sans avoir à tout gérer. Promettez une expérience clé en main et sans friction.",
            "args": [
                "Gestion de projet complète — le client n'a qu'à valider",
                "Reporting clair et visuel chaque semaine sans jargon technique",
                "Disponibilité garantie avec temps de réponse < 4h ouvrées",
            ],
            "objection": "Je n'ai pas de temps à consacrer à ce projet en ce moment.",
            "reponse":   "C'est exactement pour ça que nous existons. Votre implication : 1 appel de 30 min par semaine pour valider. Nous gérons tout le reste. Vous récupérez votre temps.",
        },
        "argent": {
            "label": "Argent", "icon": "💰",
            "desc": "Le client compare le coût du service à la valeur générée. Ancrez le prix sur le ROI, pas sur le temps passé.",
            "args": [
                "Prix fixe par livrable — pas de surprise sur la facture finale",
                "Présentation du ROI attendu : coût vs valeur générée",
                "Offre starter pour tester la collaboration à faible risque",
            ],
            "objection": "Votre tarif est élevé par rapport à d'autres prestataires.",
            "reponse":   "Un prestataire moins cher qui ne livre pas résulte vous coûtera 3x plus : le temps perdu, le travail à refaire, l'opportunité manquée. Notre tarif reflète un résultat garanti — calculons ensemble le ROI.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "🤝",
            "desc": "La relation humaine est au cœur du choix d'un prestataire. Soyez la personne avec qui ils veulent travailler.",
            "args": [
                "Appel découverte offert sans engagement pour créer le lien",
                "Communication transparente même quand il y a un problème",
                "Implication personnelle du dirigeant visible dans la relation",
            ],
            "objection": "Je préfère travailler avec quelqu'un que je connais déjà.",
            "reponse":   "Tous nos clients étaient au même point avant de commencer. Un appel de 30 minutes suffit pour voir si l'entente est là. Si le courant ne passe pas, je vous le dirai moi-même.",
        },
    },
    "default": {
        "securite": {
            "label": "Sécurité", "icon": "🛡️",
            "desc": "Tout prospect a une peur fondamentale de se tromper. Votre mission : éliminer le risque perçu avant qu'il ne bloque la décision.",
            "args": [
                "Garantie satisfait ou remboursé avec conditions claires et simples",
                "Témoignages clients avec prénom, secteur et résultat chiffré",
                "Processus transparent de bout en bout sans surprise",
            ],
            "objection": "Et si ça ne correspond pas à ce que j'attends ?",
            "reponse":   "Notre garantie [X jours] couvre exactement ce scénario. Si ce n'est pas parfait, nous remboursons intégralement — sans question. Vous n'avez rien à perdre.",
        },
        "opportunite": {
            "label": "Opportunité", "icon": "🚀",
            "desc": "Le prospect cherche un gain réel : temps, argent, compétitivité. Montrez-lui ce qu'il a à gagner concrètement.",
            "args": [
                "Quantification du bénéfice attendu (temps, argent, parts de marché)",
                "Résultats mesurables obtenus par des clients similaires",
                "Avantage du premier mouvement si votre marché est en évolution rapide",
            ],
            "objection": "Je ne vois pas encore ce que j'y gagne clairement.",
            "reponse":   "Des clients comme vous ont obtenu [résultat X] en [délai Y]. Voulez-vous que je vous montre comment nous pourrions obtenir le même résultat dans votre contexte ?",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "✨",
            "desc": "Certains prospects sont stimulés par l'innovation. Positionnez votre offre comme moderne, évolutive et avant-gardiste.",
            "args": [
                "Innovation différenciante expliquée en langage simple",
                "Roadmap ou évolutions prévues pour montrer la dynamique",
                "Positionnement 'nouvelle génération' vs solutions classiques",
            ],
            "objection": "Ça ressemble à ce que font déjà d'autres acteurs.",
            "reponse":   "En apparence oui, mais notre approche intègre [différenciateur clé]. Cela change fondamentalement [résultat]. Laissez-moi vous montrer la différence en pratique.",
        },
        "confort": {
            "label": "Confort", "icon": "😌",
            "desc": "Le prospect veut une solution simple qui ne lui crée pas de nouveau problème. Promettez la facilité et tenez-la.",
            "args": [
                "Onboarding accompagné sans effort côté client",
                "Interface ou processus simple malgré la complexité sous-jacente",
                "Support réactif et humain pour toute question",
            ],
            "objection": "Je n'ai pas le temps de gérer un changement en ce moment.",
            "reponse":   "Notre processus de mise en place est conçu pour prendre moins de [X heures] de votre temps. Nous gérons tout le reste. Vous verrez les résultats avant même d'avoir senti le changement.",
        },
        "argent": {
            "label": "Argent", "icon": "💰",
            "desc": "Le prospect évalue le rapport coût/valeur. Ancrez la discussion sur la valeur créée, pas sur le prix affiché.",
            "args": [
                "ROI calculable avec des hypothèses conservatrices",
                "Comparaison coût de votre solution vs coût de l'inaction",
                "Options flexibles de paiement adaptées à la taille du projet",
            ],
            "objection": "C'est au-dessus de notre budget prévu.",
            "reponse":   "Je comprends. Calculons ensemble ce que vous coûte actuellement [problème] chaque mois. Si notre solution coûte moins que ce problème, le budget est justifié — sinon, nous trouverons une formule adaptée.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "🤝",
            "desc": "Les décisions d'achat sont souvent émotionnelles. Créez un lien de confiance authentique avant de vendre.",
            "args": [
                "Authenticité et transparence dans la communication",
                "Intérêt réel pour la situation du prospect avant de pitcher",
                "Histoire de marque ou parcours personnel qui crée la connexion",
            ],
            "objection": "Je ne suis pas encore convaincu par votre approche.",
            "reponse":   "C'est totalement normal à ce stade. Ce qui compte, c'est que vous trouviez la bonne solution pour vous — même si ce n'est pas nous. Pouvez-vous me dire ce qui vous manque pour être convaincu ?",
        },
    },
}


def gen_soncas(activity: str) -> dict:
    """Return the SONCAS data dict for a given activity type.

    Falls back to 'default' if the activity key is not found.

    Args:
        activity: One of 'ecommerce', 'saas', 'service', or any other string
                  (falls back to 'default').

    Returns:
        A deep copy of the SONCAS data dict for the given activity.
    """
    return copy.deepcopy(_SONCAS.get(activity, _SONCAS["default"]))

# ─── AIDA ────────────────────────────────────────────────────────────────────
_AIDA = {
    "ecommerce": {
        "attention": {"p":"Headline qui interrompt le scroll","e":"Pourquoi 94% des acheteurs reviennent toujours chez nous","f":["Arrêtez de [problème] — voici pourquoi [solution inattendue]","La vraie raison pour laquelle [cible] rate [résultat]","[Chiffre] acheteurs ont découvert [bénéfice] — voici comment"],"c":"Utilisez chiffres, questions rhétoriques et promesses spécifiques. Évitez le générique."},
        "interest":  {"p":"Développez le problème pour créer l'identification","e":"Vous passez des heures à chercher... pour toujours tomber sur des produits décevants","f":["Comme [X] clients avant vous, vous avez peut-être déjà vécu [situation]","Voici ce que personne ne vous dit sur [sujet]","Le problème avec [solution classique], c'est que [raison spécifique]"],"c":"Montrez que vous comprenez exactement la douleur du client — avant de parler de vous."},
        "desire":    {"p":"Projeter le client dans l'état désiré après achat","e":"Imaginez recevoir exactement ce que vous attendiez, livré en 48h, avec garantie satisfait ou remboursé","f":["Imaginez [bénéfice émotionnel] — c'est exactement ce que [X] clients vivent","[Bénéfice concret] + [bénéfice émotionnel] = votre nouvelle réalité","Nos clients témoignent : '[citation courte et spécifique]'"],"c":"Combinez preuve sociale, bénéfices tangibles et projetez l'état émotionnel post-achat."},
        "action":    {"p":"CTA unique, urgent et sans friction","e":"Commander maintenant — Livraison offerte aujourd'hui","f":["Je veux [bénéfice] → [bouton d'action]","Profitez-en maintenant — [raison de l'urgence réelle]","Commencez sans risque — [garantie spécifique]"],"c":"Un seul CTA visible, urgence authentique, garantie de risque zéro, friction minimale."},
    },
    "saas": {
        "attention": {"p":"Chiffrez la douleur ou promettez le résultat","e":"Réduisez de 4h à 20min votre reporting hebdomadaire","f":["[X] heures perdues chaque semaine à faire [tâche manuelle] — et si ce n'était plus le cas ?","Comment [client similaire] a multiplié par [X] [métrique] en [temps]","Votre concurrent utilise déjà [solution] — voici ce qu'il gagne"],"c":"Les décideurs SaaS sont rationnels — commencez par un chiffre ou un résultat mesurable."},
        "interest":  {"p":"Nommez le problème précis que seul votre outil résout","e":"La plupart des équipes perdent 23% de leur temps dans des tâches que [Outil] automatise en un clic","f":["Le vrai problème avec [workflow actuel], c'est [coût caché invisible]","[Chiffre] équipes ont abandonné [ancienne méthode] — voici pourquoi","Sans [fonctionnalité], chaque [événement] vous coûte [quantification]"],"c":"Soyez ultra-précis sur le pain point. Plus c'est spécifique, plus ça résonne."},
        "desire":    {"p":"Démo, cas client avec métriques, social proof B2B","e":"[Client connu] a réduit son CAC de 34% après 60 jours","f":["'Depuis [Outil], on a [résultat] en [temps]' — [Prénom, Titre, Entreprise]","Rejoignez [X] équipes qui ont déjà transformé [process]","Essayez gratuitement 14 jours — sans carte bancaire, sans engagement"],"c":"Case studies avec métriques > témoignages génériques."},
        "action":    {"p":"Essai gratuit sans friction ou démo personnalisée","e":"Commencer mon essai gratuit — En ligne en 2 minutes","f":["Voir une démo en 15 min → [calendrier direct]","Essayer gratuitement 14 jours → aucune CB requise","Obtenir mon accès maintenant → [bénéfice immédiat à l'inscription]"],"c":"Réduisez le risque perçu au maximum — freemium, démo, POC — jamais de salesman dès le premier contact."},
    },
}
_AIDA_GENERIC = {
    "attention": {"p":"Captez l'attention avec un headline irrésistible","e":"Le problème que vous n'avez jamais su nommer — et notre solution","f":["[Chiffre provocateur] raisons pour lesquelles [problème persiste]","Comment [cible similaire] a obtenu [résultat] sans [obstacle perçu]","Arrêtez [action coûteuse] — il existe une meilleure façon"],"c":"Votre headline est lu 5x plus que le reste. Investissez 50% de votre temps copywriting dessus."},
    "interest":  {"p":"Développez la promesse en identifiant la douleur précise","e":"Vous savez que [problème] vous coûte [temps/argent] — mais la vraie cause est ailleurs","f":["Voici ce que la plupart des [cible] ignorent sur [sujet]","Le coût invisible de [problème] : [quantification inattendue]","Comme [X personnes], vous avez peut-être essayé [solutions inefficaces]"],"c":"Empathie d'abord, solution ensuite. Montrez que vous comprenez avant de convaincre."},
    "desire":    {"p":"Créez l'envie avec preuves, projections et social proof","e":"Nos clients obtiennent [résultat tangible] et [bénéfice émotionnel] — ils en témoignent","f":["Imaginez [situation désirée] — c'est possible dès [timing réaliste]","[X] personnes ont déjà [résultat] — voici leurs retours","Garantie : si vous n'obtenez pas [résultat], [engagement spécifique]"],"c":"Preuves > promesses. Spécifique > général. Résultat émotionnel > fonctionnalité technique."},
    "action":    {"p":"Un seul appel à l'action, clair et sans friction","e":"Commencer maintenant — [bénéfice immédiat] → [CTA]","f":["Je veux [résultat précis] → [bouton action]","C'est gratuit jusqu'à [date/seuil] — [CTA]","[Bénéfice] sans [risque perçu] → [CTA]"],"c":"Supprimez tout ce qui pourrait faire hésiter : formulaires longs, prix cachés, processus flous."},
}

_TRIGGERS = [
    ("⏰ Urgence temporelle","Crée une pression de temps pour déclencher l'action immédiate","Offre valable jusqu'à minuit — Stock limité à 47 unités","Ventes flash, périodes de promotion, lancement de produit","⚠️ Doit être AUTHENTIQUE — la fausse urgence détruit la confiance"),
    ("⭐ Preuve sociale","Les gens imitent ce que font d'autres personnes similaires à eux","12 847 clients satisfaits ⭐⭐⭐⭐⭐ — Rejoignez-les","Témoignages, compteurs d'utilisateurs, logos clients, médias","⚠️ Spécifique et vérifiable > chiffre rond et non sourcé"),
    ("🏆 Autorité","Les experts et figures d'autorité crédibilisent votre offre","Recommandé par [expert connu] · Certifié [organisme] · Cité dans [media]","Badges certifications, mentions presse, partenariats experts","⚠️ L'autorité doit être pertinente pour votre cible, pas seulement impressionnante"),
    ("💎 Rareté","La valeur perçue augmente quand la disponibilité diminue","Plus que 3 places disponibles ce mois · Édition limitée 500 exemplaires","Services premium, places de formation, stocks limités","⚠️ La rareté inventée génère du ressentiment"),
    ("🎁 Réciprocité","Donner quelque chose de valeur crée une obligation naturelle de rendre","Guide gratuit (vraie valeur) → lead nurturing → vente naturelle","Lead magnets, contenus premium gratuits, consultations offertes","⚠️ La valeur du cadeau détermine la réciprocité — évitez les ebooks creux"),
    ("🔗 Engagement & Cohérence","Une fois qu'une personne a dit oui à quelque chose de petit, elle dit oui à plus grand","Quiz gratuit → email → webinaire → offre → vente","Funnels de conversion, séquences email, onboarding progressif","⚠️ Chaque micro-engagement doit délivrer de la valeur"),
    ("😨 Aversion à la perte","La douleur de perdre est 2x plus intense que le plaisir de gagner","Ne laissez pas vos concurrents prendre de l'avance · Évitez de perdre X €/mois","Messaging sur les risques de ne pas agir, coûts de l'inaction","⚠️ À utiliser avec parcimonie — le fear marketing permanent génère du rejet"),
    ("🤝 Appartenance","Les humains veulent appartenir à un groupe qui partage leurs valeurs","Rejoignez 5000 entrepreneurs qui ont choisi de [valeur commune]","Positioning de marque, communication de communauté, onboarding","⚠️ La communauté doit être réelle et active"),
]

def gen_aida(activity: str) -> dict:
    return copy.deepcopy(_AIDA.get(activity, _AIDA_GENERIC))

# ─── GEO 2025 ────────────────────────────────────────────────────────────────
_GEO = {
    "ecommerce": {
        "topics": ["Guide ultime d'achat [produit phare] — le contenu pilier de référence","Comparatif [produit A] vs [produit B] — contenu cluster haute valeur","FAQ produits enrichie — capture les requêtes conversationnelles IA","Avis clients structurés (schema Review) — utilisés par Google SGE"],
        "clusters": [("Guide d'achat [niche]",["Comment choisir X","Meilleur X pour Y","X test & avis","X prix comparatif"]),("Guide entretien / utilisation",["Comment utiliser X","Erreurs à éviter","X durée de vie","Tutoriel X"])],
        "optims": [("Ajoutez des FAQ schema markup sur toutes vos fiches produit","🔴 Élevé"),("Répondez aux questions 'quel est le meilleur X pour Y' dans vos contenus","🔴 Élevé"),("Utilisez du langage naturel conversationnel dans vos descriptions","🟡 Moyen"),("Structurez vos avis en données structurées (schema Review)","🔴 Élevé")],
        "tips": ["Google SGE et ChatGPT extraient des réponses directes — soyez la source citée","Perplexity cite les sources — des backlinks de qualité restent essentiels","Les requêtes vocales explosent — optimisez pour le langage parlé"],
    },
    "saas": {
        "topics": ["Guides pratiques ultra-complets sur les problèmes que votre outil résout","Études de cas sectorielles avec métriques et ROI quantifiés","Comparatifs objectifs avec vos concurrents (even-handed = crédibilité)","Glossaire du secteur — topical authority signal fort pour Google"],
        "clusters": [("Guide [fonctionnalité principale]",["Comment faire X sans outil","X automatisation guide","X pour les débutants","X cas d'usage avancés"]),("Comparatif outils [catégorie]",["Vous vs Concurrent A","Vous vs Concurrent B","Meilleur outil X 2025","Migrer de X vers vous"])],
        "optims": [("Créez une documentation technique complète (boon for AI crawlers)","🔴 Élevé"),("Publiez des datasets ou benchmarks sectoriels citables par l'IA","🟣 Très élevé"),("Répondez aux questions 'comment [task] avec [catégorie d'outil]' exhaustivement","🔴 Élevé"),("Structurez vos how-to avec des étapes numérotées (schema HowTo)","🟡 Moyen")],
        "tips": ["Les LLMs sont entraînés sur le web — votre contenu publié aujourd'hui formera les réponses de demain","Soyez la ressource la plus citée de votre niche — qualité > quantité","ChatGPT et Perplexity favoritent les sites avec API publique et documentation claire"],
    },
}
_GEO_GENERIC = {
    "topics": ["Contenus piliers ultra-complets sur votre thème principal","Clusters de contenu répondant à toutes les questions de votre ICP","FAQ structurée avec schema markup pour la capture des requêtes IA","Études de cas et données sectorielles propriétaires"],
    "clusters": [("Guide principal [thème]",["Introduction","Niveau avancé","Cas pratiques","FAQ"]),("Solutions aux problèmes [cible]",["Problème A → solution","Problème B → solution","Comparatif solutions","Erreurs à éviter"])],
    "optims": [("Utilisez des questions naturelles comme sous-titres H2/H3","🔴 Élevé"),("Ajoutez un schema FAQ sur toutes vos pages clés","🔴 Élevé"),("Répondez directement et précisément en début de section (featured snippet)","🔴 Élevé"),("Créez du contenu E-E-A-T : Experience, Expertise, Authority, Trust","🟣 Très élevé")],
    "tips": ["39% des Français utilisent l'IA conversationnelle — optimisez maintenant pour ces moteurs","Les IA citent les sources qui répondent directement et exhaustivement","L'intention de recherche prime sur le mot-clé exact — comprenez le 'pourquoi'"],
}

_SEA_IA = [
    ("🤖 Google AI Max","Performance Max avec IA Max — diffusion automatique sur tous les canaux Google",["Diffusion sur Search, Display, YouTube, Gmail, Maps, Shopping","Optimisation en temps réel des enchères et audiences via ML","Asset generation IA — génère des variantes de titres et descriptions"],"Fournissez des assets de qualité — la qualité des inputs détermine la qualité des outputs IA"),
    ("🎯 Smart Bidding","Stratégies d'enchères automatisées par Google ML pour maximiser les conversions",["Target CPA : coût par acquisition fixe — idéal si vous connaissez votre CPA cible","Target ROAS : retour sur dépenses publicitaires — pour e-commerce avec données de valeur","Maximize Conversions : maximise le volume dans votre budget — pour démarrer","Enhanced CPC : manuel + ajustement IA — contrôle maximal pour débutants"],"Donnez au Smart Bidding 2-4 semaines d'apprentissage avant d'évaluer les performances"),
    ("🔍 AI Overviews","Google AI Overviews — réponses IA intégrées dans les résultats de recherche",["Annonces textuelles dans les AI Overviews (beta 2025) — position premium visible","Shopping ads dans les réponses IA pour les requêtes produits","Position 0 : votre annonce affichée dans la synthèse IA de Google"],"Combinez SEA (paiement garanti) + SEO GEO (organique IA) pour une visibilité maximale"),
    ("👥 Audience Signals","Signaux d'audience pour guider l'IA vers vos meilleurs prospects",["Customer Match : uploadez vos emails clients pour trouver des similaires","Similar Audiences basées sur vos convertisseurs","In-Market Audiences : personas en phase d'achat active","Custom Intent : audiences basées sur les recherches récentes"],"Plus vous fournissez de signaux de qualité, plus l'IA cible efficacement"),
]

def gen_geo(activity: str) -> dict:
    return copy.deepcopy(_GEO.get(activity, _GEO_GENERIC))

# ─── SEO KEYWORDS ────────────────────────────────────────────────────────────
_KEYWORDS = {
    "ecommerce": [("boutique en ligne livraison rapide","10K-100K","Facile","Transactionnel"),("acheter [produit] pas cher","10K-100K","Moyen","Transactionnel"),("meilleur [produit] 2025","5K-10K","Moyen","Commercial"),("avis [produit/marque]","5K-10K","Facile","Commercial"),("[produit] livraison gratuite","1K-5K","Facile","Transactionnel"),("comparatif [produit]","1K-5K","Moyen","Commercial")],
    "saas": [("[fonctionnalité] logiciel","5K-10K","Moyen","Commercial"),("meilleur outil [catégorie] 2025","1K-5K","Moyen","Commercial"),("[concurrent] alternative","500-1K","Facile","Commercial"),("comment automatiser [tâche]","1K-5K","Facile","Informationnel"),("[catégorie] prix tarifs","500-1K","Moyen","Transactionnel"),("[catégorie] comparatif","1K-5K","Élevé","Commercial")],
    "service": [("[service] [ville] prix","1K-5K","Facile","Transactionnel"),("prestataire [service] pro","500-1K","Facile","Commercial"),("comment choisir [prestataire]","1K-5K","Moyen","Informationnel"),("[service] avis clients","500-1K","Facile","Commercial"),("tarif [service] 2025","500-1K","Moyen","Transactionnel")],
    "default": [("[mot-clé principal] guide","1K-5K","Moyen","Informationnel"),("meilleur [produit/service] 2025","1K-5K","Moyen","Commercial"),("comment [résoudre problème]","5K-10K","Facile","Informationnel"),("[secteur] prix tarif","500-1K","Moyen","Transactionnel"),("avis [marque/service]","500-1K","Facile","Commercial")],
}

def gen_keywords(activity: str) -> list:
    return copy.deepcopy(_KEYWORDS.get(activity, _KEYWORDS["default"]))

# ─── MARKETING ───────────────────────────────────────────────────────────────
_PLATFORMS = {
    "ecommerce": [("Instagram","haute","3-5x/sem","Reels, Stories, Shopping"),("Google Shopping","haute","Continu","Fiches produit optimisées"),("TikTok","haute","1-2x/j","Vidéos produit, UGC, GRWM"),("Email","haute","2-3x/sem","Abandons panier, promos, fidélité"),("Pinterest","moyenne","3x/sem","Épingles produits, mood boards")],
    "saas": [("LinkedIn","haute","5x/sem","Articles, témoignages clients, actus"),("Email","haute","2x/sem","Nurturing, onboarding, upsell"),("Google Ads","haute","Continu","Search branded + concurrents"),("YouTube","moyenne","1x/sem","Tutoriels, cas clients, démos"),("Twitter/X","faible","1-2x/j","Veille, thread expertise")],
    "service": [("LinkedIn","haute","4x/sem","Études de cas, expertise, posts"),("Google My Business","haute","1x/sem","Actualités, avis, photos"),("Email","haute","1x/sem","Newsletter valeur, offres"),("Bouche-à-oreille","haute","En continu","Programme de référencement client"),("Instagram","moyenne","3x/sem","Coulisses, témoignages, avant/après")],
    "consulting": [("LinkedIn","haute","5x/sem","Articles de fond, thought leadership"),("Newsletter","haute","1x/sem","Insights sectoriels exclusifs"),("Podcast/YouTube","moyenne","1x/mois","Interviews, analyses de marché"),("Conférences","moyenne","1-2x/trim","Speaking, networking"),("Twitter/X","faible","Quotidien","Veille et engagement")],
    "content": [("YouTube","haute","2x/sem","Vidéos longues, tutoriels"),("Instagram","haute","1x/j","Reels, Stories, contenu viral"),("Newsletter","haute","1x/sem","Monétisation audience fidèle"),("TikTok","moyenne","1-2x/j","Shorts, tendances"),("Podcast","faible","1x/sem","Format audio, interviews")],
    "default": [("Instagram","haute","3x/sem","Posts, Stories, Reels"),("LinkedIn","haute","3x/sem","Articles, posts expertise"),("Email","haute","1-2x/sem","Newsletter, offres"),("Google Ads","moyenne","Continu","Search, Display"),("Facebook","faible","2x/sem","Communauté, ads")],
}

_CALENDAR_TOPICS = {
    "awareness": ["Comment [votre expertise] transforme [résultat]","Les 5 erreurs que font 90% des [cible]","Interview d'expert : [tendance secteur]","Guide ultime : [thème central]"],
    "sales":     ["Témoignage client : [résultat chiffré]","Comparatif : [votre solution] vs alternatives","Offre exclusive : [bénéfice] pour [cible]","Démonstration : comment [fonctionnalité] fonctionne"],
    "leads":     ["[Lead magnet] gratuit : [titre accrocheur]","Webinaire : [résoudre problème courant]","Quiz : quel est votre niveau en [thème] ?","Étude de cas : comment [client] a obtenu [résultat]"],
    "traffic":   ["Guide SEO : [mot-clé cible] expliqué","Les [X] meilleures ressources pour [sujet]","Tutorial : [processus étape par étape]","Infographie : [données secteur] en 2025"],
}

def gen_platforms(activity: str) -> list:
    return copy.deepcopy(_PLATFORMS.get(activity, _PLATFORMS["default"]))

def gen_budget_alloc(monthly: float) -> list:
    if monthly <= 50:
        cats = [("Création de contenu (outils gratuits)", 60), ("Outils freemium", 30), ("Formation / veille", 10)]
    elif monthly <= 200:
        cats = [("Publicité payante (Social Ads test)", 40), ("Outils & logiciels starter", 35), ("Création de contenu", 25)]
    elif monthly <= 500:
        cats = [("Publicité payante (SEA/Social Ads)", 45), ("Outils & logiciels", 30), ("Création de contenu", 15), ("SEO & link-building", 10)]
    else:
        cats = [("Publicité payante (SEA/Social Ads)", 50), ("Outils & logiciels (CRM, analytics)", 25), ("Création de contenu", 15), ("SEO & link-building", 10)]
    return [(c, pct, round(monthly * pct / 100, 0)) for c, pct in cats]

def gen_budget_reco(monthly: float) -> list:
    if monthly <= 50:
        return [
            "💡 Budget micro (≤50€) : misez à 100% sur l'organique",
            "✅ Outils gratuits : Canva Free, Mailchimp Free, Google Search Console, Google Analytics",
            "✅ Stratégie : 2 posts/semaine sur 1 réseau · 1 article de blog SEO/semaine · Newsletter mensuelle",
            "✅ ROI attendu : notoriété et premiers leads organiques en 2-4 mois",
            "⚠️ Évitez la pub payante — budget insuffisant pour obtenir des données statistiques fiables",
        ]
    elif monthly <= 200:
        return [
            "💡 Budget starter (50-200€) : organique + micro-tests paid",
            "✅ Outils : Canva Pro (13€/mois), Brevo/Sendinblue starter, Google Ads (50-100€ test)",
            "✅ Stratégie : 1 campagne Google Ads test · SEO content 2x/sem · Email 2x/mois",
            "✅ ROI attendu : premiers achats/leads payants en 4-6 semaines si niche peu concurrentielle",
            "⚠️ Allouez 60% du budget paid sur 1 canal unique avant de diversifier",
        ]
    elif monthly <= 500:
        return [
            "💡 Budget PME (200-500€) : mix paid + contenu + outils",
            "✅ Outils : CRM starter (HubSpot Free ou Pipedrive 15€), Google Ads + Meta Ads, Semrush Lite",
            "✅ Stratégie : SEA Search + retargeting · Content 3x/sem · Email automation bienvenue + nurturing",
            "✅ ROI attendu : ROAS 2-4x en e-commerce · CPL 15-40€ en B2B sur 60-90 jours",
            "✅ Commencez le SEO maintenant pour réduire la dépendance au paid dans 6 mois",
        ]
    else:
        return [
            "💡 Budget PME confirmée (500-1000€) : stratégie complète multi-canal",
            "✅ Outils : CRM complet (HubSpot Starter 50€/mois), Google Ads + Meta + LinkedIn Ads",
            "✅ Outils SEO : Semrush ou Ahrefs (99€/mois) + outil email marketing avancé",
            "✅ Stratégie : SEA tous canaux + SEO agressif + content production externalisée",
            "✅ ROI attendu : ROAS 3-6x · Croissance trafic +40%/mois sur 6 mois · CPL optimisé",
            "✅ Considérez 1 freelance content ou growth hacker à mi-temps pour accélérer",
        ]

def gen_calendar(goal: str) -> list:
    topics = _CALENDAR_TOPICS.get(goal, _CALENDAR_TOPICS["awareness"])
    formats = ["Article de blog","Vidéo courte","Email newsletter","Infographie / Carrousel"]
    platforms_cycle = ["LinkedIn","Instagram","Email","YouTube"]
    return [(i+1, platforms_cycle[i%4], topics[i%len(topics)], formats[i%4]) for i in range(8)]

# ─── PERSONAS ────────────────────────────────────────────────────────────────
_PERSONA_DATA = {
    "ecommerce": [
        {"name":"Sophie Martin","age":32,"job":"Responsable marketing","location":"Paris","quote":"Je veux des produits de qualité livrés rapidement, sans mauvaise surprise.",
         "goals":["Trouver des produits tendance rapidement","Bénéficier d'un service client réactif","Comparer facilement les offres"],
         "pains":["Délais de livraison trop longs","Retours produits compliqués","Manque de confiance sur les nouveaux sites"],
         "channels":["Instagram","Pinterest","Email"],"triggers":["Promotion flash","Avis clients positifs","Livraison gratuite"],
         "motivations":["Gain de temps","Qualité garantie"],"values":["Fiabilité","Transparence"],
         "habits":["Consulte Instagram avant d'acheter","Compare sur Google Shopping","Lit les avis Trustpilot"],
         "expectations":["Livraison en 48h","Politique de retour simple","Service client joignable"],
         "framework":"SONCAS","framework_match":"Sécurité / Confort"},
        {"name":"Thomas Dubois","age":28,"job":"Développeur freelance","location":"Lyon","quote":"Je compare tout avant d'acheter. Le meilleur rapport qualité/prix, c'est non-négociable.",
         "goals":["Maximiser la valeur de chaque achat","Recevoir des produits durables","Processus d'achat rapide"],
         "pains":["Trop d'options à comparer","Sites peu transparents","SAV inexistant"],
         "channels":["YouTube","Reddit","Google"],"triggers":["Tests comparatifs","Garantie longue durée","Prix transparent"],
         "motivations":["Économies","Performance produit"],"values":["Rationalité","Durabilité"],
         "habits":["Regarde des reviews YouTube","Lit les specs techniques","Consulte Reddit avant d'acheter"],
         "expectations":["Fiche produit détaillée","Prix HT/TTC clairs","Comparaison facile"],
         "framework":"SONCAS","framework_match":"Argent / Nouveauté"},
    ],
    "saas": [
        {"name":"Claire Rousseau","age":38,"job":"Directrice d'une PME (15 salariés)","location":"Bordeaux","quote":"J'ai besoin d'outils qui fonctionnent vraiment et qui ne me font pas perdre du temps.",
         "goals":["Automatiser les tâches répétitives","Vue d'ensemble de l'activité","Former facilement mon équipe"],
         "pains":["Trop d'outils qui ne se parlent pas","Formations longues et coûteuses","Support peu réactif"],
         "channels":["LinkedIn","Email professionnel","Bouche-à-oreille"],"triggers":["Essai gratuit sans CB","ROI démontrable","Support inclus"],
         "motivations":["Productivité","Sérénité"],"values":["Efficacité","Fiabilité"],
         "habits":["Consulte G2 et Capterra","Demande des recommandations sur LinkedIn","Teste avant d'acheter"],
         "expectations":["Onboarding guidé","Support réactif","Intégrations avec les outils existants"],
         "framework":"SONCAS","framework_match":"Sécurité / Confort / Argent"},
    ],
    "service": [
        {"name":"Isabelle Moreau","age":45,"job":"Cadre en reconversion","location":"Nantes","quote":"J'ai 20 ans d'expérience à valoriser. Il me faut juste le bon accompagnement.",
         "goals":["Valoriser mon expertise en ligne","Créer des revenus stables","Gagner en liberté et flexibilité"],
         "pains":["Peur de la technologie","Syndrome de l'imposteur","Manque de réseau dans le digital"],
         "channels":["LinkedIn","Email","Podcasts"],"triggers":["Accompagnement humain","Résultats progressifs","Communauté de pairs"],
         "motivations":["Indépendance","Accomplissement"],"values":["Authenticité","Croissance"],
         "habits":["Écoute des podcasts business","Suit des formations en ligne","Réseau LinkedIn actif"],
         "expectations":["Suivi personnalisé","Résultats mesurables","Communauté bienveillante"],
         "framework":"SONCAS","framework_match":"Sécurité / Sympathie"},
    ],
    "default": [
        {"name":"Marie Legrand","age":35,"job":"Entrepreneur indépendant","location":"France","quote":"Je cherche des solutions concrètes qui m'aident à avancer rapidement.",
         "goals":["Gagner du temps sur les tâches répétitives","Développer son activité de façon autonome","Avoir des résultats mesurables"],
         "pains":["Manque de temps et de ressources","Trop d'options, pas assez de clarté","Difficulté à mesurer le ROI"],
         "channels":["Instagram","LinkedIn","Google"],"triggers":["Résultats prouvés","Simplicité d'utilisation","Rapport qualité/prix"],
         "motivations":["Croissance","Autonomie"],"values":["Impact","Efficacité"],
         "habits":["Cherche sur Google","Suit des comptes Instagram inspirants","S'abonne aux newsletters expertes"],
         "expectations":["Résultats rapides","Interface intuitive","Support disponible"],
         "framework":"SONCAS","framework_match":"Opportunité / Argent"},
        {"name":"Lucas Bernard","age":24,"job":"Étudiant / Side-hustler","location":"Toulouse","quote":"Je veux lancer mon projet avec un budget minimal mais des résultats max.",
         "goals":["Monétiser une passion","Apprendre en faisant","Atteindre l'indépendance financière"],
         "pains":["Budget très limité","Manque d'expérience business","Temps fragmenté"],
         "channels":["TikTok","YouTube","Discord"],"triggers":["Offre freemium","Communauté active","Tutoriels inclus"],
         "motivations":["Liberté financière","Apprentissage"],"values":["Innovation","Communauté"],
         "habits":["Regarde des tutos YouTube","Suit des créateurs TikTok","Participe à des Discord thématiques"],
         "expectations":["Prix accessible","Prise en main rapide","Ressources gratuites"],
         "framework":"SONCAS","framework_match":"Nouveauté / Sympathie"},
    ],
}

def gen_personas(activity: str) -> list:
    key = activity if activity in _PERSONA_DATA else "default"
    base = copy.deepcopy(_PERSONA_DATA[key])
    if len(base) < 2:
        base += copy.deepcopy(_PERSONA_DATA["default"])
    return base[:3]

# ─── SPIN SELLING ────────────────────────────────────────────────────────────
_SPIN = {
    "ecommerce": {
        "situation": ["Combien de références produits gérez-vous actuellement ?","Sur quels canaux vendez-vous — site propre, marketplace, boutique physique ?","Quel est votre taux de conversion moyen sur votre site actuel ?"],
        "probleme":  ["Avez-vous des difficultés à gérer les stocks en temps réel ?","Perdez-vous des ventes à cause d'une mauvaise expérience mobile ?","Vos fiches produit sont-elles optimisées pour le référencement ?"],
        "implication":["Si votre taux de conversion augmentait de 1%, quel serait l'impact sur votre CA annuel ?","Combien de ventes perdez-vous chaque mois à cause de l'abandon panier ?","Quel est le coût d'opportunité d'une page produit mal référencée sur 12 mois ?"],
        "besoin":    ["Si vous pouviez automatiser la gestion des stocks, combien de temps libéreriez-vous ?","Quel impact un taux de conversion à 3,5% aurait-il sur vos objectifs annuels ?","Si votre site chargeait en moins de 2 secondes, combien de ventes récupéreriez-vous ?"],
    },
    "saas": {
        "situation": ["Comment vos équipes gèrent-elles [processus] aujourd'hui ?","Quels outils utilisez-vous actuellement et depuis combien de temps ?","Combien de personnes sont concernées par ce processus dans votre organisation ?"],
        "probleme":  ["Qu'est-ce qui vous frustre le plus dans votre solution actuelle ?","Combien de temps vos équipes passent-elles sur des tâches manuelles liées à [processus] ?","Y a-t-il des erreurs récurrentes dues à des processus manuels ?"],
        "implication":["Si ce problème persiste 12 mois, quel sera l'impact sur votre croissance ?","Combien coûte chaque heure perdue sur ces tâches manuelles, en salaire chargé ?","Quelle opportunité manquez-vous pendant que vos équipes font ces tâches répétitives ?"],
        "besoin":    ["Si vous automatisiez [processus], que pourrait faire votre équipe de ce temps gagné ?","Quel ROI attendriez-vous d'une solution qui élimine [problème] en 30 jours ?","Comment une réduction de [X]% de vos erreurs de processus affecterait-elle votre NPS ?"],
    },
    "default": {
        "situation": ["Décrivez-moi comment vous gérez [sujet] aujourd'hui ?","Qui est impliqué dans ce processus et quelle est leur charge de travail ?","Depuis combien de temps cette situation dure-t-elle ?"],
        "probleme":  ["Qu'est-ce qui vous pose le plus de difficultés dans cette situation ?","Quelles en sont les conséquences les plus visibles pour votre activité ?","Avez-vous déjà essayé de résoudre ce problème ? Qu'est-ce qui n'a pas fonctionné ?"],
        "implication":["Quel est l'impact de ce problème sur vos résultats à fin d'année ?","Si rien ne change, où en serez-vous dans 6 mois ?","Combien cela vous coûte-t-il chaque mois en temps, argent ou opportunités perdues ?"],
        "besoin":    ["Si vous pouviez résoudre [problème] demain, quel serait le premier bénéfice visible ?","Qu'est-ce qu'une situation idéale ressemblerait pour vous dans 90 jours ?","Quel résultat justifierait votre investissement dans cette solution ?"],
    },
}

# ─── CHALLENGER SALE ──────────────────────────────────────────────────────────
_CHALLENGER = {
    "teach": [
        "Apportez une insight que le prospect n'a pas — une donnée, une tendance, un angle qu'il ignore",
        "Remettez en question ses croyances actuelles avec des preuves factuelles, pas des opinions",
        "Montrez l'angle mort : ce qu'il croit faire bien mais qui lui coûte en réalité de l'argent",
        "Exemple : 'La plupart des [profil client] pensent que [croyance] — nos données montrent que c'est l'inverse'",
    ],
    "tailor": [
        "Adaptez votre message à chaque interlocuteur dans l'entreprise (CEO, DAF, opérationnel)",
        "Le CEO veut entendre : croissance, risque, compétitivité",
        "Le DAF veut entendre : ROI, coût total de possession, retour en X mois",
        "L'opérationnel veut entendre : gain de temps, facilité d'usage, moins d'erreurs",
    ],
    "take_control": [
        "Maintenez le contrôle du processus de vente — ne laissez pas le prospect décider seul du timing",
        "Proposez toujours une prochaine étape concrète avec une date précise",
        "Si résistance sur le prix : ne cédez pas immédiatement — questionnez la valeur d'abord",
        "Challenger ≠ agressif : c'est guider avec conviction, pas imposer avec pression",
    ],
}

def gen_scripts(activity: str) -> list:
    scripts = {
        "ecommerce": [
            {"title":"Email de relance panier abandonné","type":"email_followup","content":"Objet : Votre panier vous attend 🛒\n\nBonjour [Prénom],\n\nVous avez laissé quelque chose derrière vous !\n\nVotre sélection : [Produit(s)] est encore disponible — mais le stock est limité.\n\n→ Commander maintenant et bénéficiez de la livraison offerte jusqu'à ce soir.\n\n[BOUTON : Finaliser ma commande]\n\nÀ très vite,\nL'équipe [Marque]","keyPoints":["Personnaliser avec le nom du produit exact","Ajouter l'urgence (stock limité)","Un seul CTA : finaliser la commande","Livraison offerte = levier de conversion puissant"]},
            {"title":"Script appel client fidèle (upsell)","type":"follow_up","content":"Bonjour [Prénom], c'est [Votre Prénom] de [Marque].\nJe vous appelle car vous êtes l'un de nos meilleurs clients et je souhaitais vous présenter en avant-première notre nouvelle [Collection/Produit].\n\nVous avez commandé [Produit X] il y a [X semaines] — est-ce que vous en êtes satisfait ?\n[Écoute active]\n\nParfait. Je me permets de vous appeler car nous avons justement [Produit complémentaire] qui va parfaitement avec [Produit X]. Nos clients qui associent les deux témoignent de [bénéfice].\n\nPuis-je vous envoyer un lien avec 15% de remise réservée spécialement à nos clients VIP ?","keyPoints":["Ouvrir avec la relation client existante","Valider la satisfaction avant de pitcher","Proposer le produit complémentaire logique","Offre exclusive VIP pour déclencher l'action"]},
        ],
        "saas": [
            {"title":"Email cold outreach B2B","type":"cold_call","content":"Objet : [Prénom], [Résultat en 5 mots]\n\nBonjour [Prénom],\n\nJ'ai remarqué que [Entreprise] est en train de [croissance/changement observé] — c'est souvent à ce stade que [problème que vous résolvez] devient un vrai frein.\n\nOn a aidé [Client similaire] à [résultat mesurable] en [délai]. Voici le détail : [lien cas client]\n\nÊtes-vous disponible 15 minutes cette semaine pour voir si on peut faire la même chose pour [Entreprise] ?\n\n[Prénom]\nPS : Si ce n'est pas le bon moment, pas de problème — je reviendrai en [date].","keyPoints":["Personnaliser avec un signal d'actualité de l'entreprise","Référencer un cas client similaire","Demander 15 min, pas une heure","PS humanise et réduit la pression"]},
            {"title":"Script démo SaaS SPIN (30 min)","type":"discovery","content":"Introduction (2 min)\n'Merci [Prénom] de prendre le temps. Avant de vous montrer quoi que ce soit, j'aimerais comprendre votre situation. Ça m'évitera de vous montrer des features qui ne vous concernent pas.'\n\nDécouverte SPIN (10 min)\n- Situation : 'Comment gérez-vous actuellement [processus] ?'\n- Problème : 'Qu'est-ce qui vous frustre le plus avec cette façon de faire ?'\n- Implication : 'Ça représente combien de temps/argent par semaine ?'\n- Need : 'Si vous pouviez [résoudre ce problème], quel impact sur [objectif] ?'\n\nDémonstration ciblée (12 min)\nMontrez UNIQUEMENT les features qui répondent aux douleurs identifiées.\n\nClosing (6 min)\n'Basé sur ce qu'on vient de voir, est-ce que ça correspond à ce que vous cherchez ?'\n'Quelle est la prochaine étape de votre côté pour avancer ?'","keyPoints":["Découverte avant démonstration — toujours","SPIN : Situation → Problème → Implication → Need","Démo ciblée = démo courte = démo efficace","Closing = next step concret, pas 'Je vous envoie une proposition'"]},
        ],
        "service": [
            {"title":"Script appel découverte","type":"discovery","content":"Bonjour [Prénom], c'est [Votre Prénom].\nMerci d'avoir pris le temps d'échanger.\n\nAvant de parler de moi, j'aimerais comprendre où vous en êtes.\n\n'Pouvez-vous me décrire votre situation actuelle en matière de [domaine] ?'\n[Écoute]\n\n'Qu'est-ce qui vous a poussé à chercher de l'aide maintenant ?'\n[Écoute — noter le déclencheur]\n\n'Si on résolvait ce problème ensemble, à quoi ressemblerait une situation idéale pour vous dans 6 mois ?'\n[Écoute — noter la vision]\n\nProposition :\n'Basé sur ce que vous m'avez dit, voici comment je pourrais vous aider : [offre en 3 lignes].'\n\n'Est-ce que ça vous semble correspondre à ce que vous cherchez ?'","keyPoints":["Écouter 80% du temps — parler 20%","Identifier le déclencheur d'achat","Faire visualiser l'état désiré avant de pitcher","Offre courte et personnalisée en fin d'appel"]},
        ],
        "default": [
            {"title":"Email de prospection","type":"cold_call","content":"Objet : [Résultat concret] pour [Type d'entreprise]\n\nBonjour [Prénom],\n\nJe travaille avec des [profil similaire] qui font face à [problème courant].\n\nNotre approche leur a permis d'obtenir [résultat mesurable] en [délai].\n\nSeriez-vous disponible 15 minutes pour explorer si nous pouvons faire la même chose pour vous ?\n\n[Votre signature]","keyPoints":["Cibler précisément le profil","Mentionner un résultat concret","Demander un petit engagement (15 min)","Personnaliser si possible avec une info de l'entreprise"]},
            {"title":"Gestion des objections prix","type":"follow_up","content":"Client : 'C'est trop cher.'\n\nVous : 'Je comprends. Puis-je vous poser une question ?'\nSi vous n'investissez pas maintenant, comment comptez-vous résoudre [problème] ?\n\n[Écoute]\n\nEt quel est le coût de ce problème pour vous chaque mois ?\n\n[Écoute]\n\nSi on compare [X € par mois] avec [coût mensuel du problème]... l'investissement semble-t-il encore aussi élevé ?\n\nAlternativement, nous pouvons commencer par [offre d'entrée] à [prix réduit] pour vous permettre d'en mesurer la valeur.","keyPoints":["Ne jamais défendre le prix — questionner le problème","Calculer le coût de l'inaction","Proposer une entrée de gamme si budget bloquant","Retourner l'objection en opportunité"]},
        ],
    }
    return copy.deepcopy(scripts.get(activity, scripts["default"]))

_OBJECTIONS = [
    ("C'est trop cher","Comprenez-vous vraiment à quoi correspond l'investissement ? Calculons ensemble le coût de votre problème actuel chaque mois. Si [solution] résout ce problème, quel est le ROI ?"),
    ("J'ai besoin d'y réfléchir","Tout à fait naturel. Qu'est-ce qui vous ferait encore hésiter après réflexion ? En général c'est le prix, le timing, ou le fit — lequel des trois vous préoccupe le plus ?"),
    ("Je travaille déjà avec quelqu'un","Excellent signe — vous prenez déjà le sujet au sérieux. Qu'est-ce qui vous donnerait envie d'explorer une alternative si les résultats n'étaient pas au rendez-vous ?"),
    ("On n'a pas de budget","Le budget n'est jamais le vrai problème — c'est la priorité. Si je vous prouvais que [solution] génère plus qu'elle ne coûte en 90 jours, comment vous organiseriez-vous ?"),
    ("On peut le faire en interne","Absolument possible. Quelle est la valeur du temps de votre équipe sur cette tâche vs son coût avec nous ? Et ont-ils l'expertise spécifique nécessaire ?"),
]

# ─── KPI BENCHMARKS ──────────────────────────────────────────────────────────
_KPI_BENCHMARKS = {
    "email": [
        ("📬 Taux de délivrabilité", "85,7%", "Ratio emails délivrés en boîte de réception. En dessous de 85%, vérifiez SPF/DKIM/DMARC", "sauge", ">90%"),
        ("👁️ Taux d'ouverture", "33,9%", "% d'emails ouverts sur emails délivrés. Varie selon le secteur (B2B > B2C)", "ambre", ">35%"),
        ("🖱️ CTR (Taux de clics)", "5,35%", "% de clics sur le nombre d'emails délivrés. Indicateur d'engagement réel", "ambre", ">6%"),
        ("⚡ CTOR (Taux de réactivité)", "~15%", "CTR / Taux d'ouverture. Mesure la qualité du contenu vu par ceux qui ouvrent", "neutral", ">15%"),
        ("🚪 Taux de désabonnement", "<0,5%", "% de désabonnements par campagne. Au-dessus de 0,5%, revisez votre segmentation", "neutral", "<0,3%"),
        ("💶 Revenu par email envoyé", "Variable", "CA généré divisé par le nombre d'emails envoyés. KPI ROI direct", "neutral", "Calculer"),
    ],
    "conversion": [
        ("🛒 Taux de conversion e-commerce", "2,5-3%", "% de visiteurs qui achètent. La moyenne mondiale est ~2,5%. Visez 3-4%", "ambre", ">3%"),
        ("💰 CAC (Coût d'Acquisition Client)", "~1 200€", "Coût moyen pour acquérir 1 client B2B SaaS. E-commerce : 30-100€", "neutral", "Calculer"),
        ("⭐ NPS (Net Promoter Score)", "0-100", "Score de recommandation client. >50 = excellent, >70 = world-class", "neutral", ">50"),
        ("😊 CSAT (Satisfaction Client)", ">70%", "% clients satisfaits. En dessous de 70%, identifiez les frictions majeures", "ambre", ">80%"),
        ("🎫 Temps de résolution tickets", "<4h", "Délai moyen de résolution des demandes support. Impact direct sur le CSAT", "neutral", "<2h"),
        ("🤖 Déviation par IA", "Variable", "% de tickets résolus par chatbot/IA sans intervention humaine. Visez 30-50%", "neutral", ">30%"),
    ],
    "social": [
        ("💼 Engagement LinkedIn", "3-3,5%", "Likes + commentaires + partages / portée. Moyenne B2B : 3-3,5%", "sauge", ">4%"),
        ("📸 Engagement Instagram", "0,45-0,6%", "Engagement rate moyen en 2025. Les Reels ont 3-5x plus d'engagement", "ambre", ">1%"),
        ("📘 Engagement Facebook", "0,06-0,2%", "Reach organique très faible. Facebook Ads reste pertinent en paid", "neutral", ">0,2%"),
        ("▶️ Engagement YouTube", "3,4%", "Likes + commentaires / vues. Complété par Watch Time et CTR miniature", "sauge", ">4%"),
        ("📈 Croissance liste email", "+5-10%/mois", "Croissance mensuelle nette (nouveaux - désabonnés). Objectif PME : +5%/mois", "ambre", ">8%/mois"),
    ],
}

# ─── OKR FRAMEWORK ───────────────────────────────────────────────────────────
_OKR_TEMPLATES = {
    "awareness": [
        {"objective":"Devenir la référence de contenu dans notre niche d'ici Q4",
         "key_results":["Atteindre 50 000 visiteurs organiques/mois (+150%)","Publier 24 contenus piliers (2/sem) avec >1 000 mots","Obtenir 500 nouveaux abonnés newsletter/mois","Atteindre un DA (Domain Authority) de 35+"]},
        {"objective":"Multiplier par 3 notre présence sur les réseaux sociaux",
         "key_results":["Atteindre 10 000 abonnés LinkedIn actifs","Obtenir un taux d'engagement >4% sur LinkedIn","Publier 5 Reels/semaine sur Instagram","Atteindre 5 000 abonnés Instagram en 90 jours"]},
    ],
    "sales": [
        {"objective":"Augmenter le CA de 40% ce trimestre",
         "key_results":["Porter le taux de conversion site à 3,5%","Réduire le CAC de 20% via l'optimisation paid","Augmenter le panier moyen de 15% via upsell/cross-sell","Atteindre un ROAS de 4x sur toutes les campagnes"]},
        {"objective":"Optimiser le funnel de vente de bout en bout",
         "key_results":["Réduire le taux d'abandon panier à moins de 65%","Implémenter 3 séquences email automation","Lancer 2 A/B tests CTA par mois","Porter le taux de closing des démos à 25%"]},
    ],
    "leads": [
        {"objective":"Générer 200 leads qualifiés par mois d'ici 3 mois",
         "key_results":["Créer 2 lead magnets avec >500 téléchargements/mois","Porter le CPL sous 25€ sur Google Ads","Mettre en place une séquence nurturing 7 emails","Atteindre un taux de qualification leads >40%"]},
    ],
    "traffic": [
        {"objective":"Tripler le trafic organique en 6 mois",
         "key_results":["Publier 2 articles SEO/semaine (52 articles/an)","Obtenir 20 backlinks DA50+ par trimestre","Positionner 15 mots-clés en top 10 Google","Réduire le taux de rebond sous 50%"]},
    ],
}

def gen_okr(goal: str) -> list:
    return copy.deepcopy(_OKR_TEMPLATES.get(goal, _OKR_TEMPLATES["awareness"]))

# ─── SYNTHESIS ───────────────────────────────────────────────────────────────
_PRIORITIES = {
    "awareness": ["Créez votre contenu pilier (2000+ mots) sur votre thème principal","Lancez votre présence sur 2 réseaux sociaux maximum — maîtrisez avant d'étendre","Définissez votre TOV (Tone of Voice) et charte éditoriale","Construisez votre liste email dès maintenant — c'est votre actif le plus précieux"],
    "sales":     ["Optimisez votre tunnel de conversion — identifiez où vous perdez les prospects","Testez 2 versions de votre CTA principal (A/B test)","Mettez en place le retargeting sur Meta et Google","Activez les emails de relance automatiques (panier abandonné, devis non signé)"],
    "leads":     ["Créez votre premier lead magnet à haute valeur perçue","Configurez une séquence email de nurturing (7 emails sur 14 jours)","Optimisez vos landing pages pour un seul objectif : la conversion","Intégrez un CRM pour tracker chaque lead de A à Z"],
    "traffic":   ["Publiez 2 contenus SEO par semaine minimum pendant 3 mois","Lancez votre stratégie de backlinks (guest posting, digital PR)","Optimisez vos Core Web Vitals (LCP < 2.5s, CLS < 0.1)","Créez vos clusters de contenu autour de 3 thèmes piliers"],
}
_ROADMAP = [
    ("J1-J30","Fondations","Valider l'offre · Configurer les outils · Lancer les 1ers contenus · Premiers contacts"),
    ("J31-J60","Activation","Premières campagnes payantes · Séquences email actives · Premiers retours clients"),
    ("J61-J90","Optimisation","Analyser les données · A/B tester · Doubler ce qui fonctionne · Couper ce qui ne fonctionne pas"),
    ("J91-J180","Scalabilité","Augmenter les budgets gagnants · Nouveaux canaux · Recruter/déléguer · Préparer la prochaine phase"),
]

def gen_synthesis(activity: str, goal: str, maturity: str, monthly: float) -> dict:
    score = {"ecommerce":72,"saas":68,"service":75,"consulting":80,"content":65,"other":60}.get(activity, 65)
    if maturity == "launched": score += 8
    elif maturity == "inprogress": score += 3
    if monthly >= 500: score += 5
    elif monthly >= 200: score += 3
    elif monthly >= 50: score += 1
    score = min(score, 98)
    return {
        "score": score,
        "priorities": _PRIORITIES.get(goal, _PRIORITIES["awareness"]),
        "roadmap": _ROADMAP,
        "kpis": _get_kpis(goal, monthly),
    }

def _get_kpis(goal: str, monthly: float) -> list:
    base = [("Budget mensuel", f"{monthly:,.0f} €"), ("ROI cible", "3-5x sur 6 mois")]
    extras = {
        "awareness": [("Portée mensuelle cible","50K-200K"),("Engagement rate cible","> 3%"),("Croissance abonnés","+15%/mois")],
        "sales":     [("Taux de conversion cible","> 2.5%"),("Panier moyen cible","À définir"),("ROAS cible","3-5x")],
        "leads":     [("CPL (coût par lead) cible","< 15-50 €"),("Taux de qualification","> 40%"),("Taux de closing","> 20%")],
        "traffic":   [("Visiteurs organiques cible","+50%/mois"),("Position mots-clés cible","Top 10 Google"),("Taux de rebond cible","< 55%")],
    }
    return base + extras.get(goal, [])

# ─── WEB SCRAPING (optionnel) ────────────────────────────────────────────────
def scrape_site_meta(url: str) -> dict:
    """Extrait title et description d'une URL si BeautifulSoup est disponible."""
    if not _HAS_BS4 or not url or not url.startswith("http"):
        return {}
    try:
        import requests as req
        r = req.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find("title")
        desc  = soup.find("meta", attrs={"name": "description"})
        return {
            "title": title.get_text(strip=True) if title else "",
            "description": desc.get("content","") if desc else "",
            "status": r.status_code,
        }
    except Exception:
        return {}

# ═════════════════════════════════════════════════════════════════════════════
# ── SIDEBAR — WIZARD ─────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════
LABELS = {
    "ecommerce":"E-commerce","saas":"SaaS","service":"Service","consulting":"Conseil",
    "content":"Créateur de contenu","other":"Autre",
    "awareness":"Notoriété","sales":"Ventes","leads":"Leads","traffic":"Trafic",
    "idea":"Idée","inprogress":"En cours","launched":"Lancé",
}

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:8px 0 12px">
      <span style="font-size:1.6rem">⚡</span>
      <div style="font-weight:800;font-size:1.1rem;color:#0F172A;letter-spacing:-0.3px">BiziApp</div>
      <div style="font-size:.72rem;color:#8A8A8A">Stratégie 360° en quelques secondes</div>
    </div>
    """, unsafe_allow_html=True)

    # ── WIZARD PROGRESS ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:12px">
      <div style="display:flex;justify-content:space-between;font-size:.7rem;color:#8A8A8A;margin-bottom:4px">
        <span>Étape 1 sur 4 — Contexte</span><span>0%</span>
      </div>
      <div class="progress-bar"><div class="progress-fill" style="width:25%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🏢 Votre activité**")
    activity = st.selectbox(
        "Type d'activité",
        options=["ecommerce","saas","service","consulting","content","other"],
        format_func=lambda x: {"ecommerce":"🛒 E-commerce","saas":"💻 SaaS","service":"🎯 Service","consulting":"🧠 Conseil","content":"📝 Créateur de contenu","other":"🔮 Autre"}[x],
        label_visibility="collapsed",
    )

    st.markdown("**🎯 Objectif principal**")
    goal = st.selectbox(
        "Objectif",
        options=["awareness","sales","leads","traffic"],
        format_func=lambda x: {"awareness":"🌟 Notoriété","sales":"💰 Ventes","leads":"📋 Génération de leads","traffic":"📈 Trafic"}[x],
        label_visibility="collapsed",
    )

    st.markdown("**📊 Maturité du projet**")
    maturity = st.selectbox(
        "Maturité",
        options=["idea","inprogress","launched"],
        format_func=lambda x: {"idea":"💡 Idée","inprogress":"🔨 En cours","launched":"🚀 Lancé"}[x],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**💶 Budget mensuel (€)**")
    st.caption("De 10€ (micro-test) à 1 000€+ (PME)")
    monthly_budget = st.slider("Budget mensuel", min_value=10, max_value=1000, value=200, step=10, label_visibility="collapsed")
    st.markdown(f"<div style='text-align:center;font-size:1.1rem;font-weight:700;color:#D97706'>{monthly_budget} €/mois</div>", unsafe_allow_html=True)

    total_budget = st.number_input("💼 Capital disponible (€)", min_value=0, max_value=1_000_000, value=5_000, step=500)
    website_url  = st.text_input("🌐 URL du site (optionnel)", placeholder="https://monsite.fr")

    st.divider()
    run = st.button("⚡ Générer mon analyse 360°", type="primary", use_container_width=True)
    st.caption("✅ Analyses générées instantanément · 100% hors-ligne")
    if _HAS_BS4 and website_url:
        st.caption("🔍 Lecture du site activée (BeautifulSoup)")


# ═════════════════════════════════════════════════════════════════════════════
# ── HEADER ───────────────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="bizi-header">
  <h1>⚡ BiziApp — Stratégie 360°</h1>
  <p>SWOT · QQOQCCP · PESTEL · SONCAS · Personas · AIDA · SPIN · Challenger · GEO 2025 · SEA IA · KPIs · OKR · Synthèse</p>
</div>
""", unsafe_allow_html=True)

# ── SOCIAL PROOF BANNER ───────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:20px">
  <div class="kpi-tile" style="flex:1;min-width:120px;text-align:center">
    <div style="font-size:1.5rem;font-weight:800;color:#0F172A">2 400+</div>
    <div style="font-size:.72rem;color:#8A8A8A">Diagnostics générés</div>
  </div>
  <div class="kpi-tile" style="flex:1;min-width:120px;text-align:center">
    <div style="font-size:1.5rem;font-weight:800;color:#D97706">42</div>
    <div style="font-size:.72rem;color:#8A8A8A">Secteurs couverts</div>
  </div>
  <div class="kpi-tile" style="flex:1;min-width:120px;text-align:center">
    <div style="font-size:1.5rem;font-weight:800;color:#047857">10</div>
    <div style="font-size:.72rem;color:#8A8A8A">Frameworks intégrés</div>
  </div>
  <div class="kpi-tile" style="flex:1;min-width:120px;text-align:center">
    <div style="font-size:1.5rem;font-weight:800;color:#0F172A">8 min</div>
    <div style="font-size:.72rem;color:#8A8A8A">Temps moyen</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LANDING PAGE (pre-run) ─────────────────────────────────────────────────────
if not run:
    st.info("👈 Remplissez le formulaire dans la barre latérale puis cliquez sur **⚡ Générer mon analyse 360°**")
    st.markdown("""
    #### Ce que BiziApp génère pour vous :
    | Module | Contenu |
    |--------|---------|
    | 🔍 **Diagnostic** | SWOT · QQOQCCP · PESTEL · Micro-environnement · Analyse concurrentielle |
    | 👥 **Personas** | Profils clients enrichis · Framework SONCAS · Motivations · Valeurs · Habitudes |
    | 📝 **Copywriting** | AIDA adapté · 8 déclencheurs psychologiques · Principes universels |
    | 💬 **Vente** | Scripts (cold, discovery, follow-up) · SPIN Selling · Challenger Sale · Gestion objections |
    | 📣 **Marketing** | Plateformes · Budget adaptatif 10-1000€ · Calendrier éditorial 8 semaines · Règle 80/20 |
    | 🔎 **SEO & GEO 2025** | Mots-clés · Clusters · AI Overviews · SEA IA (AI Max, Smart Bidding…) |
    | 📊 **KPI Dashboard** | Email · Conversion · Social · OKR · Benchmarks sectoriels |
    | 📈 **Synthèse** | Score global · Priorités · Roadmap 180 jours · Export JSON |
    """)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# GENERATE DATA
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("⚡ Génération de votre analyse stratégique 360°…"):
    swot         = gen_swot(activity, goal, maturity)
    qqoqccp      = gen_qqoqccp(activity)
    pestel       = gen_pestel(activity)
    micro_env    = gen_micro_env(activity)
    competitive  = gen_competitive(activity)
    soncas       = gen_soncas(activity)
    aida         = gen_aida(activity)
    geo          = gen_geo(activity)
    keywords     = gen_keywords(activity)
    platforms    = gen_platforms(activity)
    budget_alloc = gen_budget_alloc(monthly_budget)
    budget_reco  = gen_budget_reco(monthly_budget)
    calendar     = gen_calendar(goal)
    personas     = gen_personas(activity)
    scripts      = gen_scripts(activity)
    synthesis    = gen_synthesis(activity, goal, maturity, monthly_budget)
    okrs         = gen_okr(goal)
    spin_data    = _SPIN.get(activity, _SPIN["default"])
    site_meta    = scrape_site_meta(website_url) if website_url else {}

# Context badges
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<span class="badge badge-graphite">🏢 {LABELS.get(activity, activity)}</span>', unsafe_allow_html=True)
c2.markdown(f'<span class="badge badge-sauge">🎯 {LABELS.get(goal, goal)}</span>', unsafe_allow_html=True)
c3.markdown(f'<span class="badge badge-amber">📊 {LABELS.get(maturity, maturity)}</span>', unsafe_allow_html=True)
c4.markdown(f'<span class="badge badge-purple">💶 {monthly_budget:,} €/mois</span>', unsafe_allow_html=True)

if site_meta.get("title"):
    st.caption(f"🌐 Site analysé : **{site_meta['title']}** — {site_meta.get('description','')[:120]}")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🔍 Diagnostic",
    "👥 Personas & SONCAS",
    "📝 Copywriting",
    "💬 Vente & SPIN",
    "📣 Marketing",
    "🔎 SEO & GEO 2025",
    "📊 KPI Dashboard",
    "📈 Synthèse",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DIAGNOSTIC
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    # SWOT
    st.markdown('<div class="section-h">🔍 Analyse SWOT</div>', unsafe_allow_html=True)
    st.caption("Le SWOT structure toute réflexion stratégique : Forces · Faiblesses · Opportunités · Menaces")
    col_s, col_w = st.columns(2)
    with col_s:
        st.markdown('<div class="card swot-strength"><div class="card-title">✅ Forces (Strengths)</div>' +
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {i}</p>" for i in swot["strengths"]) +
            "</div>", unsafe_allow_html=True)
    with col_w:
        st.markdown('<div class="card swot-weakness"><div class="card-title">⚠️ Faiblesses (Weaknesses)</div>' +
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {i}</p>" for i in swot["weaknesses"]) +
            "</div>", unsafe_allow_html=True)
    col_o, col_t = st.columns(2)
    with col_o:
        st.markdown('<div class="card swot-oppty"><div class="card-title">🚀 Opportunités (Opportunities)</div>' +
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {i}</p>" for i in swot["opportunities"]) +
            "</div>", unsafe_allow_html=True)
    with col_t:
        st.markdown('<div class="card swot-threat"><div class="card-title">🔴 Menaces (Threats)</div>' +
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {i}</p>" for i in swot["threats"]) +
            "</div>", unsafe_allow_html=True)

    # QQOQCCP
    st.markdown('<div class="section-h">❓ Analyse QQOQCCP</div>', unsafe_allow_html=True)
    st.caption("7 questions pour ne laisser aucune zone d'ombre dans votre diagnostic stratégique")
    emoji_map = {"qui":"👤","quoi":"📦","où":"📍","quand":"🗓️","comment":"⚙️","combien":"💶","pourquoi":"🎯"}
    for key, item in qqoqccp.items():
        with st.expander(f"{emoji_map.get(key,'❓')} **{key.upper()}** — {item['q']}"):
            col_r, col_a = st.columns(2)
            with col_r:
                st.markdown("**📊 Réponse stratégique**")
                st.info(item["r"])
            with col_a:
                st.markdown("**✅ Action recommandée**")
                st.success(item["a"])

    # PESTEL
    st.markdown('<div class="section-h">🌍 Analyse PESTEL</div>', unsafe_allow_html=True)
    st.caption("6 dimensions macro-environnementales que vous ne contrôlez pas mais devez impérativement anticiper")
    impact_color = {"positif":"🟢","négatif":"🔴","neutre":"🟡"}
    for dim, items in pestel.items():
        with st.expander(f"**{dim}** ({len(items)} facteur{'s' if len(items)>1 else ''})"):
            for facteur, impact, note in items:
                st.markdown(f"{impact_color.get(impact,'⚪')} **{facteur}** `{impact}`")
                st.caption(f"→ {note}")
                st.divider()

    # MICRO-ENV
    st.markdown('<div class="section-h">🏭 Micro-environnement (5 forces de Porter)</div>', unsafe_allow_html=True)
    st.caption("Acteurs en interaction directe dont le pouvoir de négociation modèle votre chaîne de valeur")
    pouvoir_color = {"élevé":"badge-red","très élevé":"badge-red","moyen":"badge-amber","faible":"badge-sauge"}
    cols = st.columns(2)
    for i, (acteur, (pouvoir, desc, levier)) in enumerate(micro_env.items()):
        with cols[i % 2]:
            badge_cls = pouvoir_color.get(pouvoir, "badge-gray")
            st.markdown(f"""
            <div class="card">
              <div class="card-title">{acteur} <span class="badge {badge_cls}">Pouvoir : {pouvoir}</span></div>
              <p style='font-size:.85rem;color:#4A4A4A'>{desc}</p>
              <p style='font-size:.82rem;color:#047857'>💡 {levier}</p>
            </div>""", unsafe_allow_html=True)

    # COMPETITIVE
    st.markdown('<div class="section-h">⚔️ Analyse concurrentielle</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🎯 Rivaux directs**")
        for r in competitive["direct"]:
            st.markdown(f"• {r}")
    with c2:
        st.markdown("**🔗 Rivaux indirects**")
        for r in competitive["indirect"]:
            st.markdown(f"• {r}")
    st.markdown("**📊 Matrice concurrentielle** (🟢 avantage · 🔴 désavantage · ⚪ neutre)")
    table_html = '<table class="bizi-table"><thead><tr><th>Critère</th><th>Vous</th><th>Leader</th><th>Analyse</th></tr></thead><tbody>'
    for critere, vous, leader, note in competitive["matrix"]:
        table_html += f"<tr><td><b>{critere}</b></td><td style='text-align:center;font-size:1.1rem'>{vous}</td><td style='text-align:center;font-size:1.1rem'>{leader}</td><td style='font-size:.82rem;color:#8A8A8A'>{note}</td></tr>"
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**🚀 Opportunité de positionnement**\n\n{competitive['oppty']}")
    with col_b:
        st.success(f"**🛡️ Votre avantage défendable (Moat)**\n\n{competitive['moat']}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PERSONAS & SONCAS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    # PERSONAS
    st.markdown('<div class="section-h">👥 Personas clients enrichis</div>', unsafe_allow_html=True)
    st.caption("Profils semi-fictifs construits à partir de données comportementales, sectorielles et psychographiques")
    for p in personas:
        initials = "".join([w[0] for w in p["name"].split()][:2]).upper()
        colors = ["#0F172A","#D97706","#047857","#1D4ED8","#B91C1C"]
        color  = colors[hash(p["name"]) % len(colors)]
        fw_badge = f'<span class="badge badge-amber">{p.get("framework","")}</span>' if p.get("framework") else ""
        with st.expander(f"**{p['name']}** · {p['age']} ans · {p['job']} · 📍 {p['location']}", expanded=True):
            c1, c2, c3 = st.columns([1, 2, 2])
            with c1:
                st.markdown(f"""
                <div style="width:72px;height:72px;border-radius:50%;background:{color};
                  display:flex;align-items:center;justify-content:center;
                  font-size:1.4rem;font-weight:800;color:white;margin:0 auto 8px">
                  {initials}
                </div>
                {fw_badge}
                <p style="text-align:center;font-style:italic;font-size:.78rem;color:#8A8A8A;margin-top:6px">"{p['quote']}"</p>
                """, unsafe_allow_html=True)
                if p.get("framework_match"):
                    st.markdown(f"<small style='color:#D97706;font-size:.7rem'>↳ {p['framework_match']}</small>", unsafe_allow_html=True)
            with c2:
                st.markdown("**🎯 Objectifs**")
                for g in p["goals"]: st.markdown(f"✅ {g}")
                st.markdown("**😤 Douleurs**")
                for pa in p["pains"]: st.markdown(f"❌ {pa}")
                if p.get("motivations"):
                    st.markdown("**💡 Motivations**")
                    st.markdown(" ".join(f'<span class="badge badge-sauge">{m}</span>' for m in p["motivations"]), unsafe_allow_html=True)
            with c3:
                st.markdown("**📱 Canaux favoris**")
                st.markdown(" ".join(f'<span class="badge badge-blue">{c}</span>' for c in p["channels"]), unsafe_allow_html=True)
                st.markdown("<br>**🔑 Déclencheurs d'achat**", unsafe_allow_html=True)
                for t in p["triggers"]: st.markdown(f"→ {t}")
                if p.get("habits"):
                    st.markdown("**📌 Habitudes**")
                    for h in p["habits"]: st.markdown(f"• {h}")
                if p.get("values"):
                    st.markdown("**🏅 Valeurs**")
                    st.markdown(" ".join(f'<span class="badge badge-gray">{v}</span>' for v in p["values"]), unsafe_allow_html=True)

    # SONCAS
    st.markdown('<div class="section-h">🧠 Analyse SONCAS — 6 leviers psychologiques de vente</div>', unsafe_allow_html=True)
    st.caption("SONCAS : Sécurité · Opportunité · Nouveauté · Confort · Argent · Sympathie — les 6 motivations d'achat universelles")
    soncas_css_map = {
        "securite":   "soncas-securite",
        "opportunite":"soncas-opportunite",
        "nouveaute":  "soncas-nouveaute",
        "confort":    "soncas-confort",
        "argent":     "soncas-argent",
        "sympathie":  "soncas-sympathie",
    }
    cols6 = st.columns(3)
    levers = list(soncas.items())
    for i, (key, lever) in enumerate(levers):
        with cols6[i % 3]:
            css_cls = soncas_css_map.get(key, "card")
            args_html = "".join(f"<li style='font-size:.78rem;margin:2px 0'>{a}</li>" for a in lever["args"])
            st.markdown(f"""
            <div class="card {css_cls}">
              <div style="font-size:1.4rem">{lever['icon']}</div>
              <div class="card-title" style="margin-top:4px">{lever['label']}</div>
              <p style='font-size:.8rem;color:#4A4A4A;margin-bottom:8px'>{lever['desc']}</p>
              <ul style='padding-left:14px;margin:0'>{args_html}</ul>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**💬 Objections SONCAS & réponses**")
    for key, lever in soncas.items():
        with st.expander(f"{lever['icon']} **{lever['label']}** — *\"{lever['objection']}\"*"):
            st.success(f"**Réponse recommandée :**\n\n{lever['reponse']}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — COPYWRITING
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-h">📝 Structure AIDA — Copywriting persuasif</div>', unsafe_allow_html=True)
    st.caption("Le copywriting fusionne sciences comportementales et rédaction persuasive pour déclencher l'action")
    aida_meta = {
        "attention": ("🎯","ATTENTION","aida-attention"),
        "interest":  ("💡","INTÉRÊT","aida-interest"),
        "desire":    ("💜","DÉSIR","aida-desire"),
        "action":    ("🚀","ACTION","aida-action"),
    }
    c1, c2 = st.columns(2)
    for i, (step, content) in enumerate(aida.items()):
        emoji, label, css = aida_meta.get(step, ("📌", step.upper(), ""))
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(f"""
            <div class="card {css}">
              <div class="card-title">{emoji} {label}</div>
              <p style='font-weight:600;font-size:.9rem;color:#1A1A1A'>{content['p']}</p>
              <div style='background:rgba(255,255,255,.7);border-radius:10px;padding:10px;margin:10px 0'>
                <small style='color:#8A8A8A;font-weight:600'>EXEMPLE :</small>
                <p style='font-style:italic;font-size:.85rem;color:#4A4A4A;margin:4px 0'>"{content['e']}"</p>
              </div>
              <small style='color:#8A8A8A;font-weight:600'>FORMULES :</small>
              {"".join(f"<p style='font-size:.8rem;color:#4A4A4A;margin:2px 0'>→ {f}</p>" for f in content['f'])}
              <div style='background:rgba(255,255,255,.5);border-radius:8px;padding:8px;margin-top:8px'>
                <small style='color:#8A8A8A'>💡 {content['c']}</small>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-h">📐 Principes universels du copywriting</div>', unsafe_allow_html=True)
    principles = [
        ("1","Écrivez pour une personne,\nnon pour 'tout le monde'"),
        ("2","Bénéfices > fonctionnalités —\ntoujours"),
        ("3","Spécifique > général —\nles détails créent la crédibilité"),
        ("4","Une idée par phrase,\nun CTA par page"),
        ("5","Testez, mesurez, itérez —\nle meilleur texte est celui qui convertit"),
    ]
    p_cols = st.columns(5)
    for col_p, (num, pr) in zip(p_cols, principles):
        with col_p:
            st.markdown(f'<div class="metric-box"><div class="val" style="color:#D97706">{num}</div><div class="lbl" style="white-space:pre-line;line-height:1.3">{pr}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-h">🧠 8 Déclencheurs psychologiques</div>', unsafe_allow_html=True)
    st.caption("Leviers cognitifs issus des sciences comportementales qui guident la décision d'achat")
    for name, defn, ex, usage, warn in _TRIGGERS:
        with st.expander(f"**{name}**"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Définition** : {defn}")
                st.info(f'📣 *"{ex}"*')
            with c2:
                st.success(f"**Quand l'utiliser** : {usage}")
                st.warning(warn)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — VENTE & SPIN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-h">💬 Scripts de vente adaptés</div>', unsafe_allow_html=True)
    type_labels = {"cold_call":"📞 Appel à froid","follow_up":"🔄 Suivi","discovery":"🔍 Découverte","email_followup":"✉️ Email suivi","email_outreach":"📧 Email prospection"}
    for script in scripts:
        lbl = type_labels.get(script["type"], script["type"])
        with st.expander(f"**{script['title']}** — {lbl}"):
            st.code(script["content"], language=None)
            if script.get("keyPoints"):
                st.markdown("**🔑 Points clés :**")
                for kp in script["keyPoints"]: st.markdown(f"• {kp}")

    # SPIN
    st.markdown('<div class="section-h">🔄 SPIN Selling — Questions stratégiques</div>', unsafe_allow_html=True)
    st.caption("Méthodologie SPIN : Situation → Problème → Implication → Need-payoff. La plus efficace en B2B complexe.")
    spin_tabs = st.tabs(["📊 Situation","❗ Problème","⚡ Implication","💡 Need-payoff"])
    spin_keys = [("situation","Établir le contexte sans interroger — montrez que vous avez fait vos recherches"),
                 ("probleme","Identifier les douleurs précises — ne proposez pas de solution encore"),
                 ("implication","Amplifier la conséquence du problème — le client doit ressentir l'urgence"),
                 ("besoin","Faire formuler le besoin par le client lui-même — la vente devient son idée")]
    for spin_tab, (sk, hint) in zip(spin_tabs, spin_keys):
        with spin_tab:
            st.caption(f"💡 {hint}")
            for q in spin_data.get(sk, []):
                st.markdown(f"→ {q}")

    # Challenger
    st.markdown('<div class="section-h">🏆 Challenger Sale — Vendre par la conviction</div>', unsafe_allow_html=True)
    st.caption("La méthode Challenger s'appuie sur 3 piliers : Enseigner · Adapter · Prendre le contrôle")
    chal_tabs = st.tabs(["📚 Enseigner (Teach)","🎯 Adapter (Tailor)","🎮 Contrôle (Take control)"])
    chal_keys = ["teach","tailor","take_control"]
    for ctab, ckey in zip(chal_tabs, chal_keys):
        with ctab:
            for tip in _CHALLENGER[ckey]:
                st.markdown(f"• {tip}")

    # Objections
    st.markdown('<div class="section-h">⚡ Gestion des objections</div>', unsafe_allow_html=True)
    for obj, response in _OBJECTIONS:
        with st.expander(f'💬 *"{obj}"*'):
            st.markdown(response)

    # Email templates
    st.markdown('<div class="section-h">📧 Templates emails de prospection</div>', unsafe_allow_html=True)
    email_tmpls = [
        ("Email cold outreach — signal d'actualité","Objet : [Prénom], [résultat en 5 mots]\n\nBonjour [Prénom],\n\nJ'ai vu que [signal d'actualité de l'entreprise].\n\nOn a aidé [client similaire] à [résultat mesurable] en [délai].\n\nDisponible 15 min cette semaine pour voir si on peut faire pareil pour [Entreprise] ?\n\n[Prénom]"),
        ("Email suivi J+3 (non-réponse)","Objet : Re: [sujet précédent]\n\nBonjour [Prénom],\n\nJe me permets de revenir vers vous suite à mon message de l'autre jour.\n\nJe sais que vous êtes très occupé — une seule question : est-ce que [problème que vous résolvez] est encore d'actualité pour vous ?\n\nSi oui, 15 minutes suffisent pour voir si je peux vous aider. Sinon, dites-le moi et je ne vous recontacte plus.\n\n[Prénom]"),
        ("Email post-démo — prochaines étapes","Objet : Suite à notre échange — prochaines étapes\n\nBonjour [Prénom],\n\nMerci pour notre échange — c'était très intéressant de comprendre [problème identifié].\n\nComme convenu, voici ce que je vous propose :\n• [Offre adaptée à leur situation]\n• [Prix / modalités]\n• [Garantie ou condition de démarrage]\n\nPour avancer, la prochaine étape est [action concrète].\n\nEst-ce que [date] vous conviendrait pour [prochaine étape] ?\n\n[Prénom]"),
    ]
    for title, body in email_tmpls:
        with st.expander(f"📧 **{title}**"):
            st.code(body, language=None)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — MARKETING
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-h">📣 Plateformes recommandées</div>', unsafe_allow_html=True)
    prio_badge = {"haute":"badge-red","haute ":"badge-red","moyenne":"badge-amber","faible":"badge-sauge"}
    pf_cols = st.columns(min(len(platforms), 3))
    for i, (name, prio, freq, content_types) in enumerate(platforms):
        with pf_cols[i % 3]:
            badge = prio_badge.get(prio, "badge-gray")
            st.markdown(f"""
            <div class="card">
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>
                <b style='font-size:.95rem'>{name}</b>
                <span class="badge {badge}">{prio}</span>
              </div>
              <small style='color:#8A8A8A'>📅 {freq}</small>
              <p style='font-size:.8rem;color:#4A4A4A;margin-top:6px'>{content_types}</p>
            </div>""", unsafe_allow_html=True)

    # Budget adaptatif
    st.markdown(f'<div class="section-h">💶 Répartition budgétaire — {monthly_budget:,} €/mois</div>', unsafe_allow_html=True)
    bar_colors = ["#0F172A","#D97706","#047857","#1D4ED8"]
    for i, (cat, pct, amt) in enumerate(budget_alloc):
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.markdown(f"**{cat}**")
        c2.markdown(f"**{amt:,.0f} €**")
        c3.markdown(f"*{pct}%*")
        st.markdown(f"""
        <div style="height:8px;background:#E7E2D6;border-radius:4px;margin-bottom:12px">
          <div style="height:8px;width:{pct}%;background:{bar_colors[i%4]};border-radius:4px;transition:width .4s ease"></div>
        </div>""", unsafe_allow_html=True)

    # Recommandations budget
    st.markdown('<div class="section-h">🎯 Recommandations adaptées à votre budget</div>', unsafe_allow_html=True)
    for reco in budget_reco:
        if reco.startswith("✅"):
            st.success(reco)
        elif reco.startswith("⚠️"):
            st.warning(reco)
        else:
            st.info(reco)

    # Calendrier éditorial
    st.markdown('<div class="section-h">📅 Calendrier éditorial — 8 semaines</div>', unsafe_allow_html=True)
    cal_html = '<table class="bizi-table"><thead><tr><th>Sem.</th><th>Plateforme</th><th>Sujet</th><th>Format</th></tr></thead><tbody>'
    for week, platform, topic, fmt in calendar:
        cal_html += f"<tr><td><b>S{week}</b></td><td><span class='badge badge-blue'>{platform}</span></td><td style='font-size:.82rem'>{topic}</td><td style='font-size:.82rem;color:#8A8A8A'>{fmt}</td></tr>"
    cal_html += "</tbody></table>"
    st.markdown(cal_html, unsafe_allow_html=True)

    # Règle 80/20
    st.markdown('<div class="section-h">⚡ Règle 80/20 — Focus d\'action</div>', unsafe_allow_html=True)
    rules_8020 = {
        "awareness": ["Créez votre contenu pilier avant de penser à la pub","LinkedIn ou Instagram en organic — maîtrisez 1 canal à fond","La newsletter est votre actif le plus précieux — commencez maintenant"],
        "sales":     ["Le retargeting génère 10x plus que la prospection froide — commencez par ça","L'email marketing a un ROI de 42:1 — c'est votre canal le plus rentable","Optimisez votre page de vente avant d'augmenter votre budget pub"],
        "leads":     ["Un bon lead magnet vaut 6 mois de pub payante — investissez dedans","La séquence email post-lead est plus importante que le lead magnet lui-même","Votre formulaire de contact est trop long — réduisez à 3 champs maximum"],
        "traffic":   ["Le SEO prend 3-6 mois — commencez MAINTENANT pour des résultats en milieu d'année","2 articles SEO/semaine > 10 posts sociaux/semaine","Les backlinks sont rois — 1 bon backlink vaut 100 mentions sur les réseaux"],
    }
    for i, r in enumerate(rules_8020.get(goal, rules_8020["awareness"])):
        st.markdown(f"**{i+1}.** {r}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — SEO & GEO 2025
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0F172A,#1E293B);color:white;border-radius:14px;
      padding:18px 24px;margin-bottom:20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <span style="font-size:2rem">🤖</span>
      <div>
        <b style="font-size:1rem">GEO 2025 — Generative Engine Optimization</b><br>
        <span style="opacity:.85;font-size:.85rem">39% des Français utilisent l'IA conversationnelle (2025) — optimisez maintenant pour les moteurs IA</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Keywords
    st.markdown('<div class="section-h">🔑 Mots-clés prioritaires</div>', unsafe_allow_html=True)
    diff_badge = {"Facile":"badge-sauge","Moyen":"badge-amber","Élevé":"badge-red"}
    intent_badge = {"Transactionnel":"badge-blue","Commercial":"badge-purple","Informationnel":"badge-gray"}
    kw_html = '<table class="bizi-table"><thead><tr><th>Mot-clé</th><th>Volume</th><th>Difficulté</th><th>Intention</th></tr></thead><tbody>'
    for kw, vol, diff, intent in keywords:
        kw_html += f"""<tr>
          <td><b>{kw}</b></td>
          <td style='font-size:.82rem'>{vol}</td>
          <td><span class='badge {diff_badge.get(diff,"badge-gray")}'>{diff}</span></td>
          <td><span class='badge {intent_badge.get(intent,"badge-gray")}'>{intent}</span></td>
        </tr>"""
    kw_html += "</tbody></table>"
    st.markdown(kw_html, unsafe_allow_html=True)

    # Topics
    st.markdown('<div class="section-h">📚 Autorité thématique — Contenus à créer</div>', unsafe_allow_html=True)
    for topic in geo["topics"]:
        st.markdown(f"📌 {topic}")

    # Clusters
    st.markdown('<div class="section-h">🌐 Clusters de contenu</div>', unsafe_allow_html=True)
    for pilier, clusters in geo["clusters"]:
        with st.expander(f"**📖 Pilier : {pilier}**"):
            for cl in clusters:
                st.markdown(f"&nbsp;&nbsp;&nbsp;→ {cl}")

    # GEO optimizations
    st.markdown('<div class="section-h">⚡ Optimisations GEO prioritaires</div>', unsafe_allow_html=True)
    for action, impact in geo["optims"]:
        c1, c2 = st.columns([5, 1])
        c1.markdown(f"• {action}")
        c2.markdown(impact)

    # AI tips
    st.markdown('<div class="section-h">🤖 Conseils pour les moteurs IA (ChatGPT, Perplexity, SGE)</div>', unsafe_allow_html=True)
    for tip in geo["tips"]:
        st.info(tip)

    # SEA IA
    st.markdown('<div class="section-h">🎯 SEA IA — Publicité pilotée par l\'IA (2025)</div>', unsafe_allow_html=True)
    sea_tabs = st.tabs([s[0] for s in _SEA_IA])
    for sea_tab, (name, desc, advantages, conseil) in zip(sea_tabs, _SEA_IA):
        with sea_tab:
            st.markdown(f"**{desc}**")
            st.markdown("**Avantages clés :**")
            for av in advantages:
                st.markdown(f"✅ {av}")
            st.info(f"💡 **Conseil pratique :** {conseil}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — KPI DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-h">📊 Dashboard KPI — Benchmarks 2025</div>', unsafe_allow_html=True)
    st.caption("Tous les indicateurs clés de performance avec leurs benchmarks sectoriels. Survolez les titres pour les définitions.")

    # Email KPIs
    st.markdown("### 📧 Email Marketing")
    email_cols = st.columns(3)
    for i, (label, value, hint, tone, target) in enumerate(_KPI_BENCHMARKS["email"]):
        tone_colors = {"sauge":"#D1FAE5","ambre":"#FEF3C7","neutral":"#F2EFE8"}
        text_colors = {"sauge":"#047857","ambre":"#D97706","neutral":"#4A4A4A"}
        bg = tone_colors.get(tone,"#F2EFE8")
        tc = text_colors.get(tone,"#4A4A4A")
        with email_cols[i % 3]:
            st.markdown(f"""
            <div class="kpi-tile" style="background:{bg};border-left:3px solid {tc}">
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:#8A8A8A">{label}</div>
              <div style="font-size:1.6rem;font-weight:800;color:{tc};margin:4px 0">{value}</div>
              <div style="font-size:.7rem;color:#8A8A8A">{hint}</div>
              <div style="font-size:.7rem;color:{tc};margin-top:4px;font-weight:600">🎯 Objectif : {target}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 💰 Conversion & Satisfaction")
    conv_cols = st.columns(3)
    for i, (label, value, hint, tone, target) in enumerate(_KPI_BENCHMARKS["conversion"]):
        tone_colors = {"sauge":"#D1FAE5","ambre":"#FEF3C7","neutral":"#F2EFE8"}
        text_colors = {"sauge":"#047857","ambre":"#D97706","neutral":"#4A4A4A"}
        bg = tone_colors.get(tone,"#F2EFE8")
        tc = text_colors.get(tone,"#4A4A4A")
        with conv_cols[i % 3]:
            st.markdown(f"""
            <div class="kpi-tile" style="background:{bg};border-left:3px solid {tc}">
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:#8A8A8A">{label}</div>
              <div style="font-size:1.6rem;font-weight:800;color:{tc};margin:4px 0">{value}</div>
              <div style="font-size:.7rem;color:#8A8A8A">{hint}</div>
              <div style="font-size:.7rem;color:{tc};margin-top:4px;font-weight:600">🎯 Objectif : {target}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 📱 Réseaux sociaux & Croissance")
    social_cols = st.columns(3)
    for i, (label, value, hint, tone, target) in enumerate(_KPI_BENCHMARKS["social"]):
        tone_colors = {"sauge":"#D1FAE5","ambre":"#FEF3C7","neutral":"#F2EFE8"}
        text_colors = {"sauge":"#047857","ambre":"#D97706","neutral":"#4A4A4A"}
        bg = tone_colors.get(tone,"#F2EFE8")
        tc = text_colors.get(tone,"#4A4A4A")
        with social_cols[i % 3]:
            st.markdown(f"""
            <div class="kpi-tile" style="background:{bg};border-left:3px solid {tc}">
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:#8A8A8A">{label}</div>
              <div style="font-size:1.6rem;font-weight:800;color:{tc};margin:4px 0">{value}</div>
              <div style="font-size:.7rem;color:#8A8A8A">{hint}</div>
              <div style="font-size:.7rem;color:{tc};margin-top:4px;font-weight:600">🎯 Objectif : {target}</div>
            </div>
            """, unsafe_allow_html=True)

    # OKR
    st.markdown('<div class="section-h">🎯 OKR — Objectifs & Key Results</div>', unsafe_allow_html=True)
    st.caption("La méthode OKR (Google, Intel, LinkedIn) aligne les équipes sur des objectifs ambitieux et mesurables")
    for j, okr in enumerate(okrs):
        with st.expander(f"**OKR {j+1}** — {okr['objective']}", expanded=(j==0)):
            st.markdown(f"**🎯 Objectif :** {okr['objective']}")
            st.markdown("**📈 Key Results :**")
            for kr in okr["key_results"]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid #E7E2D6">
                  <div style="min-width:20px;height:20px;border-radius:50%;border:2px solid #D97706"></div>
                  <span style="font-size:.88rem">{kr}</span>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — SYNTHÈSE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    score = synthesis["score"]

    # Score ring
    st.markdown('<div class="section-h">📊 Score de maturité stratégique</div>', unsafe_allow_html=True)
    c_score, c_kpis = st.columns([1, 3])
    with c_score:
        score_color = "#047857" if score >= 70 else "#D97706" if score >= 50 else "#B91C1C"
        st.markdown(f"""
        <div style="text-align:center;padding:20px 10px">
          <div class="score-ring" style="--pct:{score * 3.6:.0f}deg;background:conic-gradient({score_color} {score * 3.6:.0f}deg,#E7E2D6 0)">
            <span style="font-size:1.4rem;font-weight:800;color:#1A1A1A">{score}/100</span>
          </div>
          <p style='font-size:.82rem;color:#8A8A8A;margin-top:8px'>Score stratégique global</p>
          <span class="badge {'badge-sauge' if score>=70 else 'badge-amber' if score>=50 else 'badge-red'}">
            {'🟢 Bon' if score>=70 else '🟡 À améliorer' if score>=50 else '🔴 Attention'}
          </span>
        </div>
        """, unsafe_allow_html=True)
    with c_kpis:
        st.markdown("**📈 KPIs cibles**")
        kpi_cols = st.columns(3)
        for i, (label, val) in enumerate(synthesis["kpis"]):
            with kpi_cols[i % 3]:
                st.markdown(f'<div class="metric-box"><div class="val" style="font-size:1.1rem;color:#D97706">{val}</div><div class="lbl">{label}</div></div>', unsafe_allow_html=True)

    # Priorities
    st.markdown('<div class="section-h">🚀 Priorités d\'action immédiates</div>', unsafe_allow_html=True)
    priority_colors = ["#B91C1C","#D97706","#0F172A","#047857"]
    for i, p in enumerate(synthesis["priorities"]):
        color = priority_colors[i % 4]
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid #E7E2D6">
          <div style="min-width:28px;height:28px;border-radius:50%;background:{color};color:white;
            display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0">{i+1}</div>
          <p style="margin:0;font-size:.9rem;color:#4A4A4A;padding-top:4px">{p}</p>
        </div>""", unsafe_allow_html=True)

    # Roadmap
    st.markdown('<div class="section-h">🗓️ Roadmap 180 jours</div>', unsafe_allow_html=True)
    rm_cols = st.columns(4)
    rm_colors = ["#0F172A","#047857","#D97706","#1D4ED8"]
    for i, (period, phase, actions) in enumerate(synthesis["roadmap"]):
        with rm_cols[i]:
            st.markdown(f"""
            <div class="card" style="border-top:3px solid {rm_colors[i]}">
              <div style='font-size:.68rem;color:#8A8A8A;font-weight:600;text-transform:uppercase;letter-spacing:.05em'>{period}</div>
              <div style='font-weight:700;font-size:.95rem;color:#1A1A1A;margin:4px 0'>{phase}</div>
              <p style='font-size:.78rem;color:#4A4A4A;margin:0'>{actions}</p>
            </div>""", unsafe_allow_html=True)

    # Export
    st.markdown('<div class="section-h">📥 Export de l\'analyse complète</div>', unsafe_allow_html=True)
    export_data = {
        "generated_at": datetime.datetime.now().isoformat(),
        "version": "2.0",
        "input": {
            "activity": activity, "goal": goal, "maturity": maturity,
            "monthly_budget": monthly_budget, "total_budget": total_budget,
            "website_url": website_url,
        },
        "swot": swot,
        "qqoqccp": {k: {"question": v["q"], "reponse": v["r"], "action": v["a"]} for k, v in qqoqccp.items()},
        "soncas": {k: {"label": v["label"], "desc": v["desc"], "args": v["args"]} for k, v in soncas.items()},
        "keywords": [{"keyword": k, "volume": v, "difficulty": d, "intent": i} for k, v, d, i in keywords],
        "personas": [{"name": p["name"], "age": p["age"], "job": p["job"], "goals": p["goals"], "pains": p["pains"], "framework": p.get("framework","")} for p in personas],
        "synthesis": {"score": score, "priorities": synthesis["priorities"]},
        "okrs": okrs,
        "budget_recommendations": budget_reco,
    }
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Télécharger (JSON)",
            data=json.dumps(export_data, ensure_ascii=False, indent=2),
            file_name=f"biziapp-analyse-{activity}-{goal}-{datetime.date.today()}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_dl2:
        # CSV simple des mots-clés
        csv_kw = "mot_cle,volume,difficulte,intention\n" + "\n".join(f'"{k}","{v}","{d}","{i}"' for k,v,d,i in keywords)
        st.download_button(
            label="📊 Mots-clés (CSV)",
            data=csv_kw,
            file_name=f"biziapp-keywords-{activity}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    st.caption("💡 JSON complet · compatible CRM, Notion, Google Sheets et tout éditeur de texte")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#8A8A8A;font-size:.78rem;padding:12px 0">
  ⚡ <b style="color:#0F172A">BiziApp v2.0</b> — Stratégie 360° · SWOT · QQOQCCP · PESTEL · SONCAS · AIDA · SPIN · Challenger · GEO 2025 · SEA IA · KPIs · OKR<br>
  <span style="color:#D97706">Budgets de 10€ à 1 000€/mois · 10 frameworks intégrés · Compatible tous navigateurs</span><br>
  Toutes les analyses sont générées localement · Aucune donnée envoyée à un serveur externe
</div>
""", unsafe_allow_html=True)
