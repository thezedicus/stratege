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
import html as _html
import urllib.parse as _urlparse
import urllib.request as _urlreq
import xml.etree.ElementTree as _ET
import re as _re
import streamlit as st
import math

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
    page_icon=":material/insights:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');
:root{--graphite:#0B2221;--graphite2:#267371;--teal:#44C1BA;--teal-pale:#C6ECD9;--jade:#267371;--jade-pale:#C6ECD9;--ivoire:#F7FBF4;--craie:#F2ECD9;--encre:#0B2221;--muted:#339999;--border:#C6ECD9;}
*,*::before,*::after{box-sizing:border-box}
html,body,[class*="css"]{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;-webkit-font-smoothing:antialiased;color:var(--encre)}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:1.25rem!important;max-width:1280px}
[data-testid="stSidebar"]{background:#F7FBF4;border-right:1px solid var(--craie)}
[data-testid="stSidebar"] label{font-weight:500;font-size:.88rem}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"]{gap:0;border-bottom:2px solid var(--craie);background:transparent}
[data-testid="stTabs"] [data-baseweb="tab"]{background:transparent;border:none;border-bottom:2px solid transparent;margin-bottom:-2px;padding:10px 16px;font-size:.76rem;font-weight:600;color:var(--muted);letter-spacing:.05em;text-transform:uppercase;transition:color .2s,border-color .2s}
[data-testid="stTabs"] [aria-selected="true"]{color:var(--graphite)!important;border-bottom-color:var(--teal)!important}
[data-testid="stTabs"] [data-baseweb="tab"]:hover{color:var(--graphite)}

/* ── Header typographique ── */
.bizi-header{display:flex;align-items:center;gap:16px;padding:0 0 18px 0;border-bottom:1px solid var(--craie);margin-bottom:22px}
.logo-bizi{font-size:1.8rem;font-weight:800;color:var(--graphite);letter-spacing:-1.5px;line-height:1}
.logo-app{font-size:1.8rem;font-weight:800;color:var(--teal);letter-spacing:-1.5px;line-height:1}
.header-sub{font-size:.68rem;color:var(--muted);letter-spacing:.07em;text-transform:uppercase;font-weight:500;margin-top:3px}

/* ── Cards ── */
.card{background:white;border-radius:12px;padding:20px 22px;border:1px solid var(--border);box-shadow:0 1px 4px rgba(0,0,0,.05);margin-bottom:14px}
.card-dark{background:linear-gradient(135deg,var(--graphite) 0%,var(--graphite2) 100%);color:white;border-radius:12px;padding:20px 24px;margin-bottom:14px}
.card-title{font-weight:700;font-size:.95rem;margin-bottom:10px;color:var(--encre)}

/* ── Feature cards (landing) ── */
.feature-card{background:white;border-radius:12px;padding:18px;border:1px solid var(--border);border-top:3px solid var(--teal);box-shadow:0 1px 4px rgba(0,0,0,.05);transition:box-shadow .2s,transform .2s}
.feature-card:hover{box-shadow:0 6px 20px rgba(0,0,0,.09);transform:translateY(-2px)}
.feature-title{font-weight:700;font-size:.88rem;color:var(--graphite);margin-bottom:5px}
.feature-desc{font-size:.78rem;color:var(--muted);line-height:1.5}

/* ── SWOT ── */
.swot-strength{border-left:4px solid #44C1BA;background:#C6ECD9}
.swot-weakness{border-left:4px solid var(--teal);background:var(--teal-pale)}
.swot-oppty{border-left:4px solid #393DAC;background:#E4E9F6}
.swot-threat{border-left:4px solid #B83D4B;background:#F7FBF4}

/* ── Badges ── */
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.7rem;font-weight:600;white-space:nowrap}
.badge-blue{background:#E4E9F6;color:#393DAC}.badge-green{background:#DCFCE7;color:#267371}
.badge-red{background:#F7FBF4;color:#B83D4B}.badge-teal{background:var(--teal-pale);color:#267371}
.badge-purple{background:#E4E9F6;color:#267371}.badge-gray{background:#E4E9F6;color:#267371}
.badge-graphite{background:var(--graphite);color:#F7FBF4}.badge-jade{background:var(--jade-pale);color:var(--jade)}

/* ── Impact dots ── */
.dot-pos{display:inline-block;width:8px;height:8px;border-radius:50%;background:#44C1BA;margin-right:6px;vertical-align:middle}
.dot-neg{display:inline-block;width:8px;height:8px;border-radius:50%;background:#B83D4B;margin-right:6px;vertical-align:middle}
.dot-neu{display:inline-block;width:8px;height:8px;border-radius:50%;background:#44C1BA;margin-right:6px;vertical-align:middle}

/* ── Score ring ── */
.score-ring{width:110px;height:110px;border-radius:50%;background:conic-gradient(var(--teal) var(--pct),#C6ECD9 0);display:flex;align-items:center;justify-content:center;font-size:1.5rem;font-weight:800;color:var(--encre);box-shadow:inset 0 0 0 18px white;margin:0 auto 8px}

/* ── Metric boxes ── */
.metric-box{text-align:center;padding:16px 12px;border-radius:12px;background:white;border:1px solid var(--border);box-shadow:0 1px 4px rgba(0,0,0,.05)}
.metric-box .val{font-size:1.6rem;font-weight:800;color:var(--encre)}
.metric-box .lbl{font-size:.75rem;color:var(--muted);margin-top:3px}

/* ── KPI tiles ── */
.kpi-tile{border:1px solid var(--craie);border-radius:12px;padding:18px 16px;text-align:center;transition:box-shadow .18s ease,transform .18s ease;cursor:default;margin-bottom:10px}
.kpi-tile:hover{box-shadow:0 4px 16px rgba(15,23,42,.10);transform:translateY(-2px)}

/* ── Table ── */
.bizi-table{width:100%;border-collapse:collapse;font-size:.84rem}
.bizi-table th{background:#F7FBF4;padding:9px 13px;text-align:left;font-weight:600;font-size:.72rem;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);border-bottom:2px solid var(--border)}
.bizi-table td{padding:9px 13px;border-bottom:1px solid #E4E9F6;color:var(--encre)}
.bizi-table tr:hover td{background:#F7FBF4}

/* ── AIDA ── */
.aida-attention{background:#F7FBF4;border-left:4px solid #B83D4B}
.aida-interest{background:#F7FBF4;border-left:4px solid #44C1BA}
.aida-desire{background:#E4E9F6;border-left:4px solid #393DAC}
.aida-action{background:#F7FBF4;border-left:4px solid #44C1BA}

/* ── Section headers ── */
.section-h{font-size:.95rem;font-weight:700;color:var(--graphite);display:flex;align-items:center;gap:10px;margin:22px 0 14px}
.section-h::before{content:"";display:inline-block;width:4px;height:16px;background:var(--teal);border-radius:2px;flex-shrink:0}

/* ── Progress ── */
.progress-bar{background:#E4E9F6;border-radius:999px;height:6px;overflow:hidden;margin:5px 0}
.progress-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--teal) 0%,#267371 100%);transition:width .5s ease}

/* ── Sidebar wizard steps ── */
.step-label{font-size:.64rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:14px 0 5px;display:flex;align-items:center;gap:6px}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:var(--graphite);color:white;font-size:.64rem;font-weight:700;flex-shrink:0}

/* ── SONCAS ── */
.soncas-securite{background:#E4E9F6;border-left:4px solid #393DAC;border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-opportunite{background:#F7FBF4;border-left:4px solid #44C1BA;border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-nouveaute{background:#E4E9F6;border-left:4px solid #393DAC;border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-confort{background:var(--teal-pale);border-left:4px solid var(--teal);border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-argent{background:var(--jade-pale);border-left:4px solid var(--jade);border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-sympathie{background:#C6ECD9;border-left:4px solid #44C1BA;border-radius:10px;padding:14px 16px;margin-bottom:10px}

/* ── URL analysis panel ── */
.url-panel{background:linear-gradient(135deg,var(--graphite) 0%,var(--graphite2) 100%);color:white;border-radius:14px;padding:22px 26px;margin-bottom:18px}
.url-panel-title{font-size:1rem;font-weight:700;margin-bottom:4px;color:white}
.url-panel-sub{font-size:.78rem;opacity:.75;margin-bottom:12px}
.url-kw{display:inline-block;background:rgba(255,255,255,.12);color:white;border-radius:4px;padding:2px 8px;font-size:.7rem;margin:2px}

/* ── Context bar ── */
.ctx-pill{background:var(--graphite);color:white;border-radius:6px;padding:4px 12px;font-size:.74rem;font-weight:600;letter-spacing:.03em}
.ctx-pill.ambre{background:var(--teal)}.ctx-pill.sauge{background:var(--jade)}.ctx-pill.blue{background:#393DAC}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:#C6ECD9}
::-webkit-scrollbar-thumb{background:var(--craie);border-radius:999px}
::-webkit-scrollbar-thumb:hover{background:#339999}

/* ── Mobile ── */
@media(max-width:768px){
  .bizi-header{flex-direction:column;gap:8px;padding-bottom:14px}
  .logo-bizi,.logo-app{font-size:1.4rem}
  [data-testid="column"]{width:100%!important;flex:1 1 100%!important}
  .card{padding:14px}.metric-box .val{font-size:1.2rem}
  .bizi-table{font-size:.74rem}
  [data-testid="stTabs"] [data-baseweb="tab"]{padding:8px 9px;font-size:.68rem}
  .feature-card{padding:14px}
}

/* ── RSE / RFM / Prix / Proposition de valeur ── */
.rse-card{background:#F7FBF4;border:1px solid #C6ECD9;border-radius:10px;padding:14px 18px;margin-bottom:10px}
.rfm-card{background:white;border:1px solid var(--craie);border-radius:12px;padding:16px;text-align:center;min-height:140px}
.prix-badge{display:inline-block;background:var(--teal-pale);color:#267371;border-radius:4px;padding:2px 8px;font-size:.65rem;font-weight:700;margin-bottom:6px}
.pv-card{border-radius:12px;padding:18px 20px;margin-bottom:10px;color:white}

/* ── Transitions webkit ── */
.kpi-tile,.feature-card{-webkit-transition:box-shadow .18s ease,transform .18s ease}
.progress-fill{-webkit-transition:width .5s ease}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# AUTHENTIFICATION OPTIONNELLE (définie tôt pour bloquer avant tout rendu)
# ─────────────────────────────────────────────────────────────────────────────
def _check_auth() -> bool:
    """Vérifie le mot de passe si auth.enabled = true dans secrets.toml"""
    try:
        cfg = st.secrets.get("auth", {})
        if not cfg.get("enabled", False):
            return True # Auth désactivée
        pwd = cfg.get("password", "")
        if not pwd:
            return True
    except Exception:
        return True # Pas de fichier secrets = pas d'auth

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    with st.container():
        st.markdown("""
        <div style="max-width:420px;margin:80px auto;background:white;border-radius:16px;
          padding:40px;box-shadow:0 4px 24px rgba(0,0,0,.1);text-align:center">
          <div style="font-size:2.5rem"></div>
          <h2 style="font-weight:800;color:#0B2221;margin:12px 0 4px">BiziApp</h2>
          <p style="color:#339999;font-size:.9rem;margin-bottom:24px">Accès protégé — entrez le mot de passe</p>
        </div>
        """, unsafe_allow_html=True)
        col = st.columns([1, 2, 1])[1]
        with col:
            _pwd_input = st.text_input("Mot de passe", type="password", label_visibility="collapsed",
                                       placeholder="Entrez le mot de passe...")
            if st.button("→ Accéder", use_container_width=True, type="primary"):
                if _pwd_input == cfg.get("password", ""):
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Mot de passe incorrect")
    st.stop()
    return False

_check_auth()

# ═════════════════════════════════════════════════════════════════════════════
# ── DATA & GENERATORS ────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

# ─── SWOT ────────────────────────────────────────────────────────────────────
_SWOT_DATA = {
    "ecommerce": {
        "strengths": [
            "Vente directe 24h/24 sans contrainte géographique",
            "Données comportementales exploitables",
            "Scalabilité rapide sans coût fixe proportionnel",
            "Marges optimisées sans intermédiaire",
        ],
        "weaknesses": [
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
        "threats": [
            "Hausse du coût des publicités (CPM, CPC)",
            "Nouvelles réglementations RGPD",
            "Saturation des niches rentables",
        ],
    },
    "saas": {
        "strengths": [
            "Revenus récurrents (MRR/ARR) prévisibles",
            "Coût marginal quasi nul par nouvel utilisateur",
            "Mises à jour centralisées",
            "Effets de réseau et forte rétention",
        ],
        "weaknesses": [
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
        "threats": [
            "Géants tech qui copient les fonctionnalités",
            "Fatigue SaaS — consolidation des budgets",
            "Open-source alternatives gratuites",
        ],
    },
    "service": {
        "strengths": [
            "Faibles coûts de démarrage, pas de stock",
            "Relation client directe et fidélisation naturelle",
            "Marges élevées si positionnement premium",
            "Expertise différenciante difficile à copier",
        ],
        "weaknesses": [
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
        "threats": [
            "Concurrence des freelances low-cost",
            "Récession comprime les budgets prestataires",
            "Commoditisation par les outils no-code",
        ],
    },
    "consulting": {
        "strengths": [
            "Expertise rare et difficile à reproduire",
            "Tarification à forte valeur ajoutée",
            "Faibles coûts fixes",
            "Flexibilité géographique (remote)",
        ],
        "weaknesses": [
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
        "threats": [
            "IA qui remplace certaines missions junior",
            "Marchés saturés dans les niches populaires",
            "Clients qui internalisent les compétences",
        ],
    },
    "content": {
        "strengths": [
            "Audience fidèle et communauté engagée",
            "Monétisation diverse (pub, sponsoring, formations)",
            "Autorité perçue dans la niche",
            "Faibles coûts de production relatifs",
        ],
        "weaknesses": [
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
        "threats": [
            "Contenu IA qui inonde les plateformes",
            "Démonétisation soudaine",
            "Évolution des formats et attention décroissante",
        ],
    },
    "other": {
        "strengths": [
            "Positionnement unique et différencié",
            "Flexibilité et agilité organisationnelle",
            "Opportunité d'innover dans un espace peu balisé",
        ],
        "weaknesses": [
            "Marché difficile à éduquer",
            "Ressources limitées en amorçage",
            "Besoin d'évangélisation du produit/service",
        ],
        "opportunities": [
            "First-mover advantage dans la niche",
            "Partenariats stratégiques pour accélérer",
            "Levée de fonds ou financement participatif",
        ],
        "threats": [
            "Pivot nécessaire si le marché ne répond pas",
            "Concurrents bien financés qui copient l'innovation",
            "Difficultés à recruter des profils adaptés",
        ],
    },
}


@st.cache_data(ttl=3600)
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
        "sales": "Optimisation du tunnel de conversion pour maximiser le CA",
        "leads": "Lead magnets et marketing automation pour qualifier les prospects",
        "traffic": "SEO technique et stratégie de backlinks pour croissance organique",
    }
    if goal in goal_opp:
        d["opportunities"].append(goal_opp[goal])
    return d


# ─── QQOQCCP ─────────────────────────────────────────────────────────────────
_QQOQCCP = {
    "ecommerce": {
        "qui": {"q": "Qui sont vos acheteurs cibles ?",
                    "r": "Consommateurs 25-45 ans, actifs digitaux, acheteurs en ligne réguliers (2-4x/mois)",
                    "a": "Segmentez par RFM (Récence, Fréquence, Montant) et créez 3 personas distincts"},
        "quoi": {"q": "Quoi vendez-vous exactement ?",
                    "r": "Produits avec proposition de valeur unique et différenciante",
                    "a": "Rédigez une USP en 10 mots max : bénéfice principal + différenciateur + cible"},
        "où": {"q": "Où vos clients achètent-ils ?",
                    "r": "Mobile (68%), desktop (29%) — majorité via Google Shopping et réseaux sociaux",
                    "a": "Priorisez l'expérience mobile-first et optimisez vos fiches Google Shopping"},
        "quand": {"q": "Quand vos clients achètent-ils ?",
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
        "qui": {"q": "Qui sont vos utilisateurs et décideurs ?",
                    "r": "Double cible : utilisateurs finaux (opérationnels) et acheteurs (dirigeants/DSI)",
                    "a": "Créez un messaging distinct pour chaque persona : bénéfice usage vs ROI business"},
        "quoi": {"q": "Quel problème résolvez-vous exactement ?",
                    "r": "Économie de temps, réduction d'erreurs ou augmentation de revenus — toujours quantifiable",
                    "a": "Quantifiez le problème : 'X heures perdues/semaine'ou 'Y% d'erreurs évitées'"},
        "où": {"q": "Où vos prospects cherchent-ils des solutions ?",
                    "r": "G2, Capterra, Product Hunt, LinkedIn, communautés Slack/Discord sectorielles",
                    "a": "Optimisez votre profil G2/Capterra + publiez sur Product Hunt au lancement"},
        "quand": {"q": "Quand un prospect décide-t-il de changer d'outil ?",
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
                    "a": "Publiez des comparatifs 'Vous vs [Concurrent]'sur des landing pages dédiées"},
    },
}
_QQOQCCP_GENERIC = {
    "qui": {"q": "Qui est votre client idéal (ICP) ?",
                "r": "Définissez précisément : secteur, taille, rôle décisionnel, budget et douleur principale",
                "a": "Réalisez 10 interviews clients pour valider et affiner votre profil ICP"},
    "quoi": {"q": "Quoi proposez-vous exactement comme valeur ?",
                "r": "Votre offre doit résoudre un problème spécifique de manière unique et mesurable",
                "a": "Rédigez votre value proposition canvas : job-to-be-done, pains, gains"},
    "où": {"q": "Où se trouvent et s'informent vos prospects ?",
                "r": "Identifiez les canaux digitaux et physiques où ils cherchent des solutions",
                "a": "Investissez prioritairement dans les 2 canaux où votre ICP passe le plus de temps"},
    "quand": {"q": "Quand votre client a-t-il besoin de vous ?",
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


@st.cache_data(ttl=3600)
def gen_qqoqccp(activity: str) -> dict:
    return copy.deepcopy(_QQOQCCP.get(activity, _QQOQCCP_GENERIC))


# ─── PESTEL ───────────────────────────────────────────────────────────────────
_PESTEL = {
    "ecommerce": {
        " Politique": [
            ("Régulation TVA numérique UE (OSS)", "négatif",
             "Complexité comptable accrue pour la vente transfrontalière"),
            ("Normes RGPD & ePrivacy", "neutre",
             "Contrainte mais avantage concurrentiel si bien géré"),
        ],
        " Économique": [
            ("Inflation des coûts logistiques +18% en 3 ans", "négatif",
             "Comprimez via négociation transporteur et stocks optimisés"),
            ("Croissance e-commerce +5-7%/an en France (FEVAD 2024)", "positif",
             "Marché en expansion — capturez la part de marché tôt"),
        ],
        "Socioculturel": [
            ("M-commerce : ~55% du trafic e-commerce depuis mobile (France)", "positif",
             "Mobile-first est désormais non-négociable"),
            ("Exigence RSE des consommateurs +39% vs 2022", "neutre",
             "Levier différenciant si vous intégrez l'impact environnemental"),
        ],
        " Technologique": [
            ("IA générative dans les recommandations produits", "positif",
             "Personnalisation accrue = +23% de conversion en moyenne"),
            ("Moteurs de recherche IA (Google SGE, Perplexity)", "neutre",
             "Adaptez votre SEO à l'intention de recherche IA (GEO)"),
        ],
        " Écologique": [
            ("Emballages durables — obligation légale 2025", "neutre",
             "Coût d'adaptation + avantage marketing si bien communiqué"),
        ],
        " Légal": [
            ("Directive Omnibus — transparence des prix", "négatif",
             "Obligation d'afficher le prix de référence avant promotion"),
            ("Droit de rétractation 14 jours — coût retours", "négatif",
             "Optimisez la logistique retour pour limiter l'impact financier"),
        ],
    },
    "saas": {
        " Politique": [
            ("AI Act européen (2024-2026)", "neutre",
             "Contraintes sur les systèmes IA à haut risque — auditez votre conformité"),
            ("Cloud Act US vs RGPD", "neutre",
             "Hébergement EU peut devenir un avantage pour les clients corporate"),
        ],
        " Économique": [
            ("Compression des budgets SaaS (stack fatigue)", "négatif",
             "ROI démontrable en <30 jours devient critère de survie"),
            ("Valorisations SaaS stabilisées — retour à la rentabilité", "neutre",
             "Les investisseurs cherchent la profitabilité"),
        ],
        "Socioculturel": [
            ("Remote work permanent — outils collaboratifs essentiels", "positif",
             "Intégrations Slack/Teams/Notion deviennent des must-have"),
            ("Adoption IA par les utilisateurs finaux +67% en 2024", "positif",
             "Intégrez des fonctionnalités IA pour rester compétitif"),
        ],
        " Technologique": [
            ("LLMs open-source — commoditisation de l'IA", "neutre",
             "L'IA seule ne suffit plus — l'avantage est dans les données propriétaires"),
            ("API-first & intégrations — ecosystème Zapier/Make", "positif",
             "Une bonne API multiplie votre reach sans effort commercial"),
        ],
        " Écologique": [
            ("GreenOps — empreinte carbone des serveurs", "neutre",
             "Hébergeurs green (OVH, Scaleway) deviennent un argument marketing B2B"),
        ],
        " Légal": [
            ("RGPD + DMA — obligations plateformes numériques", "neutre",
             "Nommez un DPO et auditez votre collecte de données régulièrement"),
        ],
    },
}
_PESTEL_GENERIC = {
    " Politique": [
        ("Réglementation sectorielle en évolution", "neutre",
         "Suivez les évolutions législatives de votre secteur"),
    ],
    " Économique": [
        ("Contexte macro-économique incertain", "neutre",
         "Anticipez les cycles et construisez une trésorerie de sécurité"),
        ("Croissance du marché digital", "positif",
         "Digitalisez votre offre pour capter cette croissance"),
    ],
    "Socioculturel": [
        ("Digitalisation accélérée des comportements", "positif",
         "Votre présence digitale est désormais votre première vitrine"),
    ],
    " Technologique": [
        ("IA générative — opportunités de productivité", "positif",
         "Intégrez des outils IA dans vos processus"),
        ("Cybersécurité — risques en hausse", "négatif",
         "Investissez dans la sécurité de vos données"),
    ],
    " Écologique": [
        ("Transition écologique — attente des parties prenantes", "neutre",
         "Définissez votre politique RSE même à petite échelle"),
    ],
    " Légal": [
        ("RGPD & protection des données", "neutre",
         "Assurez-vous de collecter uniquement les données nécessaires avec consentement"),
    ],
}


@st.cache_data(ttl=3600)
def gen_pestel(activity: str) -> dict:
    return copy.deepcopy(_PESTEL.get(activity, _PESTEL_GENERIC))


# ─── MICRO-ENV ────────────────────────────────────────────────────────────────
_MICRO_ENV = {
    "ecommerce": {
        "Clients": ("élevé",
                              "Hyperchoix, faible coût de switching — exigence maximale",
                              "Fidélisez via programme de fidélité, contenu exclusif et service irréprochable"),
        "Fournisseurs": ("moyen",
                              "Multiples sources possibles mais dépendance aux délais de livraison",
                              "Diversifiez vos sources et stockez les SKU critiques"),
        " Concurrents": ("élevé",
                              "Amazon, Cdiscount, Pure Players niche — guerre des prix permanente",
                              "Différenciez sur l'expérience, la niche et le contenu, pas sur le prix seul"),
        "Intermédiaires": ("moyen",
                              "Marketplaces, comparateurs, influenceurs — dépendance aux algorithmes",
                              "Développez votre canal direct (DTC) pour réduire les commissions tiers"),
    },
    "saas": {
        "Clients": ("élevé",
                              "Churn élevé si valeur non démontrée à J30",
                              "Customer Success proactif + tableau de bord ROI intégré au produit"),
        "Fournisseurs": ("moyen",
                              "AWS/GCP/Azure — switching coûteux mais offres compétitives",
                              "Architecture cloud-agnostic et réserves d'instances pour optimiser les coûts"),
        " Concurrents": ("très élevé",
                              "Marché SaaS ultra-compétitif, consolidation en cours (M&A)",
                              "Hyper-spécialisation verticale + intégrations natives comme barrière à l'entrée"),
        "Intermédiaires": ("faible",
                              "App stores (faible commission), intégrateurs (partenariats clés)",
                              "Programme partenaires avec certifications et marges attractives"),
    },
}
_MICRO_GENERIC = {
    "Clients": ("élevé",
                          "Le digital donne aux clients un accès immédiat aux alternatives",
                          "Créez des barrières à la sortie : intégrations, données accumulées, communauté"),
    "Fournisseurs": ("moyen",
                          "Diversification des sources possible mais risque de dépendance",
                          "Identifiez vos fournisseurs critiques et sécurisez des alternatives"),
    " Concurrents": ("élevé",
                          "La concurrence directe et indirecte s'intensifie dans tous les marchés digitaux",
                          "Analysez systématiquement vos concurrents avec des outils comme Semrush"),
    "Intermédiaires": ("moyen",
                          "Plateformes et distributeurs prélèvent une commission croissante",
                          "Développez votre canal direct (site, newsletter, communauté) en parallèle"),
}


@st.cache_data(ttl=3600)
def gen_micro_env(activity: str) -> dict:
    return copy.deepcopy(_MICRO_ENV.get(activity, _MICRO_GENERIC))


# ─── COMPETITIVE ─────────────────────────────────────────────────────────────
_COMPETITIVE = {
    "ecommerce": {
        "direct": [
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
            ("Prix", "", "", "Leaders tirent le prix vers le bas — différenciez-vous"),
            ("Expérience UX", "", "", "Levier fort si vous investissez dans le design"),
            ("Catalogue", "", "", "Ne tentez pas de rivaliser en volume — spécialisez"),
            ("SAV & fidélisation","", "", "Avantage structurel des petites structures — exploitez-le"),
            ("Contenu & SEO", "", "", "Blog expert + UGC = trafic organique gratuit"),
        ],
        "oppty": "Niche premium + contenu expert + communauté = triangle défendable",
        "moat": "Données clients propriétaires + brand community + niche expertise",
    },
    "saas": {
        "direct": [
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
            ("Fonctionnalités", "", "", "Ne copiez pas tout — identifiez votre killer feature"),
            ("Prix", "", "", "Agilité tarifaire vs les poids lourds = avantage PME"),
            ("Support", "", "", "Accès fondateur direct = différenciateur early-stage"),
            ("Intégrations", "", "", "Priorisez 5 intégrations critiques pour votre ICP"),
            ("Vitesse d'itération", "", "", "Votre agilité est un avantage compétitif majeur"),
        ],
        "oppty": "Vertical SaaS spécialisé + support fondateur + time-to-value < 48h",
        "moat": "Données propriétaires sectoriel + intégrations natives + réseau utilisateurs",
    },
}
_COMPETITIVE_GENERIC = {
    "direct": [
        "Concurrents positionnés sur votre niche exacte",
        "Alternatives directes à votre offre",
    ],
    "indirect": [
        "Solutions DIY (faire soi-même)",
        "Freelances et agences généralistes",
    ],
    "matrix": [
        ("Prix", "", "", "Analysez le prix marché et positionnez-vous stratégiquement"),
        ("Qualité", "", "", "La qualité est votre meilleur argument différenciant"),
        ("Notoriété", "", "", "Construisez une notoriété de niche avant la notoriété large"),
        ("Service client","","", "Réactivité et personnalisation = avantage structurel"),
        ("Innovation", "", "", "Votre capacité à innover rapidement est une arme"),
    ],
    "oppty": "Identifiez le segment délaissé par les leaders et devenez l'expert incontournable",
    "moat": "Expertise niche + relation client + contenu propriétaire",
}


@st.cache_data(ttl=3600)
def gen_competitive(activity: str) -> dict:
    return copy.deepcopy(_COMPETITIVE.get(activity, _COMPETITIVE_GENERIC))


# ─── SONCAS ──────────────────────────────────────────────────────────────────
_SONCAS = {
    "ecommerce": {
        "securite": {
            "label": "Sécurité", "icon": "",
            "desc": "L'acheteur en ligne a besoin de confiance avant de sortir sa carte bleue. Réduisez le risque perçu à chaque étape du parcours.",
            "args": [
                "Paiement 100% sécurisé (SSL, 3DS2) affiché en évidence",
                "Politique de retour gratuit 30 jours sans condition",
                "Avis clients vérifiés (Trustpilot, Google Reviews) avec étoiles visibles",
            ],
            "objection": "Je ne vous connais pas — comment savoir si votre site est fiable ?",
            "reponse": "Nous affichons nos +2 000 avis vérifiés Trustpilot, notre garantie satisfait ou remboursé 30 jours et notre certification SSL. Commandez sans risque.",
        },
        "opportunite": {
            "label": "Orgueil", "icon": "",
            "desc": "L'acheteur veut se sentir valorisé, reconnu et appartenir à une élite. Flattez son ego avec des produits exclusifs et un statut premium.",
            "args": [
                "Étiquette 'Édition Limitée'ou 'Réservé aux membres Premium'",
                "Personalisation du produit avec initiales ou couleurs exclusives",
                "Accès VIP en avant-première aux nouvelles collections",
            ],
            "objection": "Je n'ai pas besoin d'un produit premium.",
            "reponse": "Nos clients premium ne cherchent pas juste un produit — ils veulent une expérience unique et reconnaissable. Nos éditions limitées sont portées par des leaders et des early adopters.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "",
            "desc": "Certains acheteurs sont attirés par les nouveautés et les tendances. Mettez en avant vos dernières collections et innovations.",
            "args": [
                "Badge 'Nouveauté'ou 'Just dropped'sur les nouvelles références",
                "Email de lancement VIP en avant-première pour les abonnés",
                "Collaboration capsule ou édition limitée pour créer l'événement",
            ],
            "objection": "Je veux être sûr que ce produit est bien ce qu'il y a de plus récent.",
            "reponse": "Cette référence vient d'être ajoutée à notre catalogue cette semaine. Nos abonnés newsletter la découvrent en avant-première — rejoignez-les pour ne plus jamais rater un lancement.",
        },
        "confort": {
            "label": "Confort", "icon": "",
            "desc": "L'expérience d'achat doit être fluide, rapide et sans friction. Chaque clic de trop est un client perdu.",
            "args": [
                "Checkout en 1 étape avec pré-remplissage des infos connues",
                "Suivi de commande en temps réel par SMS et email",
                "Service client disponible 7j/7 par chat (réponse < 2 min)",
            ],
            "objection": "Je n'ai pas envie de perdre du temps si ça ne correspond pas.",
            "reponse": "Commandez en 90 secondes. Si ce n'est pas parfait, le retour est gratuit et le remboursement est traité en 48h. Zéro tracas garanti.",
        },
        "argent": {
            "label": "Argent", "icon": "",
            "desc": "La sensibilité prix est forte en e-commerce. Montrez la valeur absolue et relative de votre offre.",
            "args": [
                "Comparateur de prix intégré ou mention du prix de marché",
                "Offres bundles avec économie affichée en pourcentage et en euros",
                "Paiement en 3x sans frais pour les paniers > 100 €",
            ],
            "objection": "C'est moins cher sur Amazon.",
            "reponse": "Notre prix inclut la livraison offerte, le retour gratuit et 2 ans de garantie. Sur Amazon, ces frais s'ajoutent. Calculez le coût total — nous sommes souvent moins chers.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "",
            "desc": "Les clients achètent aussi à des marques qu'ils apprécient. Humanisez votre boutique et créez une vraie connexion.",
            "args": [
                "Histoire de marque authentique visible sur la page 'À propos'",
                "Engagement RSE ou social (local, éco-responsable, solidaire)",
                "Communauté active sur les réseaux sociaux avec réponses aux commentaires",
            ],
            "objection": "Il y a tellement de boutiques en ligne, pourquoi vous ?",
            "reponse": "Nous sommes une équipe de 5 personnes passionnées par [niche]. Chaque commande est préparée avec soin. Lisez nos avis — nos clients reviennent parce qu'ils se sentent vraiment considérés.",
        },
    },
    "saas": {
        "securite": {
            "label": "Sécurité", "icon": "",
            "desc": "Le décideur SaaS craint les risques : perte de données, downtime, contrat difficile à résilier. Minimisez chaque risque perçu.",
            "args": [
                "SOC 2 Type II / ISO 27001 — certifications de sécurité affichées",
                "SLA 99.9% uptime avec crédits automatiques en cas d'incident",
                "Export des données à tout moment — no lock-in garanti",
            ],
            "objection": "Et si vous faites faillite ou si vous augmentez les prix brutalement ?",
            "reponse": "Notre code source est en escrow, vos données sont exportables en 1 clic et notre contrat inclut un préavis de 90 jours pour toute modification tarifaire. Votre continuité est protégée.",
        },
        "opportunite": {
            "label": "Orgueil", "icon": "",
            "desc": "Le buyer SaaS veut être reconnu comme un leader technologique. Valorisez son statut de précurseur et son image de décideur visionnaire.",
            "args": [
                "Badge 'Client Pionnier'et présence dans vos références sectorielles",
                "Cas clients avec métriques avant/après dans le même secteur",
                "Early adopter pricing — accès aux nouvelles fonctionnalités en priorité",
            ],
            "objection": "Je ne vois pas vraiment ce que j'ai à gagner par rapport à ce que j'utilise déjà.",
            "reponse": "Nos clients [même secteur] sont cités comme références dans leur industrie grâce à ce gain de productivité. Je peux vous positionner parmi eux en 15 minutes de démo.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "",
            "desc": "Les early adopters technologiques veulent être à la pointe. Positionnez votre SaaS comme la solution de nouvelle génération.",
            "args": [
                "Roadmap publique pour montrer l'innovation continue",
                "Intégration IA générative comme fonctionnalité phare",
                "Accès beta aux nouvelles features pour les clients actifs",
            ],
            "objection": "L'outil que j'utilise fait ça depuis longtemps.",
            "reponse": "La différence est dans comment nous le faisons : notre moteur IA génère [résultat] en 30 secondes vs une configuration manuelle de 2 heures. Voulez-vous voir la démo ?",
        },
        "confort": {
            "label": "Confort", "icon": "",
            "desc": "L'onboarding et la prise en main sont des freins majeurs au SaaS. Promettez et livrez une expérience sans friction.",
            "args": [
                "Onboarding guidé en 10 minutes avec données de démonstration pré-chargées",
                "Migration prise en charge par notre équipe (import depuis l'outil concurrent)",
                "Formation incluse + webinaires hebdomadaires en direct",
            ],
            "objection": "Je n'ai pas le temps de former mon équipe à un nouvel outil.",
            "reponse": "Notre onboarding est conçu pour que votre équipe soit autonome en une matinée. Nous gérons l'import de vos données existantes et proposons une formation live de 45 minutes incluse.",
        },
        "argent": {
            "label": "Argent", "icon": "",
            "desc": "Le budget SaaS est scruté. Démontrez un ROI clair et un coût total de possession inférieur aux alternatives.",
            "args": [
                "Prix par utilisateur actif — payez uniquement ce que vous utilisez",
                "Consolidation de plusieurs outils en un seul = économies immédiates",
                "Essai gratuit 14 jours sans carte bancaire — aucun risque financier",
            ],
            "objection": "Votre abonnement représente X € de plus par mois dans notre budget.",
            "reponse": "Calculons ensemble : si [fonctionnalité] économise 3h/semaine à votre équipe de 5 personnes, c'est 60h/mois à votre TJM interne — soit bien plus que notre abonnement. Le ROI est positif dès le premier mois.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "",
            "desc": "En B2B, on achète aussi à des personnes. La relation et la confiance humaine restent des différenciateurs puissants.",
            "args": [
                "Accès direct aux fondateurs pour les clients early stage",
                "Communauté Slack/Discord active avec entraide et partages",
                "Compte manager dédié dès 10 utilisateurs — relation humaine garantie",
            ],
            "objection": "Avec les grandes plateformes, j'ai un support dédié. Que m'offrez-vous ?",
            "reponse": "Chez nous, votre interlocuteur connaît votre usage par cœur. Vous n'attendez pas en file d'attente — vous avez mon numéro direct. Nos clients restent parce qu'ils se sentent partenaires, pas numéros.",
        },
    },
    "service": {
        "securite": {
            "label": "Sécurité", "icon": "",
            "desc": "Le client d'un prestataire de service craint de mal choisir et de perdre son argent. Réduisez ce risque perçu par des garanties concrètes.",
            "args": [
                "Garantie résultat ou remboursement partiel sous conditions claires",
                "Contrat détaillé avec jalons et livrables définis",
                "Références clients vérifiables dans le même secteur",
            ],
            "objection": "Comment être sûr que vous livrerez ce que vous promettez ?",
            "reponse": "Notre contrat détaille chaque livrable avec des délais précis. Nous proposons des points d'étape hebdomadaires et vous pouvez contacter directement nos 3 derniers clients pour avoir leur retour.",
        },
        "opportunite": {
            "label": "Orgueil", "icon": "",
            "desc": "Le client veut être reconnu comme un dirigeant qui prend les bonnes décisions. Valorisez son image de leader stratège auprès de ses pairs.",
            "args": [
                "Témoignages de dirigeants similaires qui ont pris cette décision",
                "Rapport personnalisé avec logo client pour valoriser son image",
                "Offre 'Partenaire Stratégique'avec visibilité dans nos references",
            ],
            "objection": "Est-ce vraiment le bon moment pour investir dans ce service ?",
            "reponse": "Les dirigeants que nous accompagnons voient cela comme un signal de leadership. C'est ce qui les différencie — et qui leur permet d'être cités comme référence dans leur secteur.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "",
            "desc": "Montrez que vos méthodes et outils sont à la pointe. Un prestataire moderne rassure et inspire confiance.",
            "args": [
                "Intégration des derniers outils IA pour accélérer les livrables",
                "Méthodologie propriétaire nommée et expliquée",
                "Veille sectorielle continue partagée avec les clients (newsletter, insights)",
            ],
            "objection": "Votre approche me semble classique — qu'est-ce qui vous différencie ?",
            "reponse": "Notre méthode [Nom] intègre les dernières avancées en [domaine]. Elle nous permet de livrer en 3 semaines ce qui prenait 3 mois avec les approches traditionnelles.",
        },
        "confort": {
            "label": "Confort", "icon": "",
            "desc": "Le client veut être accompagné sans avoir à tout gérer. Promettez une expérience clé en main et sans friction.",
            "args": [
                "Gestion de projet complète — le client n'a qu'à valider",
                "Reporting clair et visuel chaque semaine sans jargon technique",
                "Disponibilité garantie avec temps de réponse < 4h ouvrées",
            ],
            "objection": "Je n'ai pas de temps à consacrer à ce projet en ce moment.",
            "reponse": "C'est exactement pour ça que nous existons. Votre implication : 1 appel de 30 min par semaine pour valider. Nous gérons tout le reste. Vous récupérez votre temps.",
        },
        "argent": {
            "label": "Argent", "icon": "",
            "desc": "Le client compare le coût du service à la valeur générée. Ancrez le prix sur le ROI, pas sur le temps passé.",
            "args": [
                "Prix fixe par livrable — pas de surprise sur la facture finale",
                "Présentation du ROI attendu : coût vs valeur générée",
                "Offre starter pour tester la collaboration à faible risque",
            ],
            "objection": "Votre tarif est élevé par rapport à d'autres prestataires.",
            "reponse": "Un prestataire moins cher qui ne livre pas résulte vous coûtera 3x plus : le temps perdu, le travail à refaire, l'opportunité manquée. Notre tarif reflète un résultat garanti — calculons ensemble le ROI.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "",
            "desc": "La relation humaine est au cœur du choix d'un prestataire. Soyez la personne avec qui ils veulent travailler.",
            "args": [
                "Appel découverte offert sans engagement pour créer le lien",
                "Communication transparente même quand il y a un problème",
                "Implication personnelle du dirigeant visible dans la relation",
            ],
            "objection": "Je préfère travailler avec quelqu'un que je connais déjà.",
            "reponse": "Tous nos clients étaient au même point avant de commencer. Un appel de 30 minutes suffit pour voir si l'entente est là. Si le courant ne passe pas, je vous le dirai moi-même.",
        },
    },
    "default": {
        "securite": {
            "label": "Sécurité", "icon": "",
            "desc": "Tout prospect a une peur fondamentale de se tromper. Votre mission : éliminer le risque perçu avant qu'il ne bloque la décision.",
            "args": [
                "Garantie satisfait ou remboursé avec conditions claires et simples",
                "Témoignages clients avec prénom, secteur et résultat chiffré",
                "Processus transparent de bout en bout sans surprise",
            ],
            "objection": "Et si ça ne correspond pas à ce que j'attends ?",
            "reponse": "Notre garantie [X jours] couvre exactement ce scénario. Si ce n'est pas parfait, nous remboursons intégralement — sans question. Vous n'avez rien à perdre.",
        },
        "opportunite": {
            "label": "Orgueil", "icon": "",
            "desc": "Le prospect veut être fier de ses choix et reconnu pour sa clairvoyance. Flattez son statut et valorisez son appartenance à une élite de décideurs.",
            "args": [
                "Positionnez-le dans une 'sélection exclusive'de clients partenaires",
                "Résultats obtenus par des profils similaires reconnus dans leur domaine",
                "Valorisez son rôle de précurseur dans son secteur",
            ],
            "objection": "Je ne vois pas encore ce que j'y gagne clairement.",
            "reponse": "Nos clients leaders ont tous pris cette décision avant leurs concurrents. C'est ce qui les distingue aujourd'hui — et qui les positionne comme références dans leur secteur.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "",
            "desc": "Certains prospects sont stimulés par l'innovation. Positionnez votre offre comme moderne, évolutive et avant-gardiste.",
            "args": [
                "Innovation différenciante expliquée en langage simple",
                "Roadmap ou évolutions prévues pour montrer la dynamique",
                "Positionnement 'nouvelle génération'vs solutions classiques",
            ],
            "objection": "Ça ressemble à ce que font déjà d'autres acteurs.",
            "reponse": "En apparence oui, mais notre approche intègre [différenciateur clé]. Cela change fondamentalement [résultat]. Laissez-moi vous montrer la différence en pratique.",
        },
        "confort": {
            "label": "Confort", "icon": "",
            "desc": "Le prospect veut une solution simple qui ne lui crée pas de nouveau problème. Promettez la facilité et tenez-la.",
            "args": [
                "Onboarding accompagné sans effort côté client",
                "Interface ou processus simple malgré la complexité sous-jacente",
                "Support réactif et humain pour toute question",
            ],
            "objection": "Je n'ai pas le temps de gérer un changement en ce moment.",
            "reponse": "Notre processus de mise en place est conçu pour prendre moins de [X heures] de votre temps. Nous gérons tout le reste. Vous verrez les résultats avant même d'avoir senti le changement.",
        },
        "argent": {
            "label": "Argent", "icon": "",
            "desc": "Le prospect évalue le rapport coût/valeur. Ancrez la discussion sur la valeur créée, pas sur le prix affiché.",
            "args": [
                "ROI calculable avec des hypothèses conservatrices",
                "Comparaison coût de votre solution vs coût de l'inaction",
                "Options flexibles de paiement adaptées à la taille du projet",
            ],
            "objection": "C'est au-dessus de notre budget prévu.",
            "reponse": "Je comprends. Calculons ensemble ce que vous coûte actuellement [problème] chaque mois. Si notre solution coûte moins que ce problème, le budget est justifié — sinon, nous trouverons une formule adaptée.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "",
            "desc": "Les décisions d'achat sont souvent émotionnelles. Créez un lien de confiance authentique avant de vendre.",
            "args": [
                "Authenticité et transparence dans la communication",
                "Intérêt réel pour la situation du prospect avant de pitcher",
                "Histoire de marque ou parcours personnel qui crée la connexion",
            ],
            "objection": "Je ne suis pas encore convaincu par votre approche.",
            "reponse": "C'est totalement normal à ce stade. Ce qui compte, c'est que vous trouviez la bonne solution pour vous — même si ce n'est pas nous. Pouvez-vous me dire ce qui vous manque pour être convaincu ?",
        },
    },
}


@st.cache_data(ttl=3600)
def gen_soncas(activity: str) -> dict:
    """Return the SONCAS data dict for a given activity type.

    Falls back to 'default'if the activity key is not found.

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
        "interest": {"p":"Développez le problème pour créer l'identification","e":"Vous passez des heures à chercher... pour toujours tomber sur des produits décevants","f":["Comme [X] clients avant vous, vous avez peut-être déjà vécu [situation]","Voici ce que personne ne vous dit sur [sujet]","Le problème avec [solution classique], c'est que [raison spécifique]"],"c":"Montrez que vous comprenez exactement la douleur du client — avant de parler de vous."},
        "desire": {"p":"Projeter le client dans l'état désiré après achat","e":"Imaginez recevoir exactement ce que vous attendiez, livré en 48h, avec garantie satisfait ou remboursé","f":["Imaginez [bénéfice émotionnel] — c'est exactement ce que [X] clients vivent","[Bénéfice concret] + [bénéfice émotionnel] = votre nouvelle réalité","Nos clients témoignent : '[citation courte et spécifique]'"],"c":"Combinez preuve sociale, bénéfices tangibles et projetez l'état émotionnel post-achat."},
        "action": {"p":"CTA unique, urgent et sans friction","e":"Commander maintenant — Livraison offerte aujourd'hui","f":["Je veux [bénéfice] → [bouton d'action]","Profitez-en maintenant — [raison de l'urgence réelle]","Commencez sans risque — [garantie spécifique]"],"c":"Un seul CTA visible, urgence authentique, garantie de risque zéro, friction minimale."},
    },
    "saas": {
        "attention": {"p":"Chiffrez la douleur ou promettez le résultat","e":"Réduisez de 4h à 20min votre reporting hebdomadaire","f":["[X] heures perdues chaque semaine à faire [tâche manuelle] — et si ce n'était plus le cas ?","Comment [client similaire] a multiplié par [X] [métrique] en [temps]","Votre concurrent utilise déjà [solution] — voici ce qu'il gagne"],"c":"Les décideurs SaaS sont rationnels — commencez par un chiffre ou un résultat mesurable."},
        "interest": {"p":"Nommez le problème précis que seul votre outil résout","e":"La plupart des équipes perdent 23% de leur temps dans des tâches que [Outil] automatise en un clic","f":["Le vrai problème avec [workflow actuel], c'est [coût caché invisible]","[Chiffre] équipes ont abandonné [ancienne méthode] — voici pourquoi","Sans [fonctionnalité], chaque [événement] vous coûte [quantification]"],"c":"Soyez ultra-précis sur le pain point. Plus c'est spécifique, plus ça résonne."},
        "desire": {"p":"Démo, cas client avec métriques, social proof B2B","e":"[Client connu] a réduit son CAC de 34% après 60 jours","f":["'Depuis [Outil], on a [résultat] en [temps]'— [Prénom, Titre, Entreprise]","Rejoignez [X] équipes qui ont déjà transformé [process]","Essayez gratuitement 14 jours — sans carte bancaire, sans engagement"],"c":"Case studies avec métriques > témoignages génériques."},
        "action": {"p":"Essai gratuit sans friction ou démo personnalisée","e":"Commencer mon essai gratuit — En ligne en 2 minutes","f":["Voir une démo en 15 min → [calendrier direct]","Essayer gratuitement 14 jours → aucune CB requise","Obtenir mon accès maintenant → [bénéfice immédiat à l'inscription]"],"c":"Réduisez le risque perçu au maximum — freemium, démo, POC — jamais de salesman dès le premier contact."},
    },
}
_AIDA_GENERIC = {
    "attention": {"p":"Captez l'attention avec un headline irrésistible","e":"Le problème que vous n'avez jamais su nommer — et notre solution","f":["[Chiffre provocateur] raisons pour lesquelles [problème persiste]","Comment [cible similaire] a obtenu [résultat] sans [obstacle perçu]","Arrêtez [action coûteuse] — il existe une meilleure façon"],"c":"Votre headline est lu 5x plus que le reste. Investissez 50% de votre temps copywriting dessus."},
    "interest": {"p":"Développez la promesse en identifiant la douleur précise","e":"Vous savez que [problème] vous coûte [temps/argent] — mais la vraie cause est ailleurs","f":["Voici ce que la plupart des [cible] ignorent sur [sujet]","Le coût invisible de [problème] : [quantification inattendue]","Comme [X personnes], vous avez peut-être essayé [solutions inefficaces]"],"c":"Empathie d'abord, solution ensuite. Montrez que vous comprenez avant de convaincre."},
    "desire": {"p":"Créez l'envie avec preuves, projections et social proof","e":"Nos clients obtiennent [résultat tangible] et [bénéfice émotionnel] — ils en témoignent","f":["Imaginez [situation désirée] — c'est possible dès [timing réaliste]","[X] personnes ont déjà [résultat] — voici leurs retours","Garantie : si vous n'obtenez pas [résultat], [engagement spécifique]"],"c":"Preuves > promesses. Spécifique > général. Résultat émotionnel > fonctionnalité technique."},
    "action": {"p":"Un seul appel à l'action, clair et sans friction","e":"Commencer maintenant — [bénéfice immédiat] → [CTA]","f":["Je veux [résultat précis] → [bouton action]","C'est gratuit jusqu'à [date/seuil] — [CTA]","[Bénéfice] sans [risque perçu] → [CTA]"],"c":"Supprimez tout ce qui pourrait faire hésiter : formulaires longs, prix cachés, processus flous."},
}

_TRIGGERS = [
    ("Urgence temporelle","Crée une pression de temps pour déclencher l'action immédiate","Offre valable jusqu'à minuit — Stock limité à 47 unités","Ventes flash, périodes de promotion, lancement de produit"," Doit être AUTHENTIQUE — la fausse urgence détruit la confiance"),
    ("Preuve sociale","Les gens imitent ce que font d'autres personnes similaires à eux","12 847 clients satisfaits — Rejoignez-les","Témoignages, compteurs d'utilisateurs, logos clients, médias"," Spécifique et vérifiable > chiffre rond et non sourcé"),
    ("Autorité","Les experts et figures d'autorité crédibilisent votre offre","Recommandé par [expert connu] · Certifié [organisme] · Cité dans [media]","Badges certifications, mentions presse, partenariats experts"," L'autorité doit être pertinente pour votre cible, pas seulement impressionnante"),
    ("Rareté","La valeur perçue augmente quand la disponibilité diminue","Plus que 3 places disponibles ce mois · Édition limitée 500 exemplaires","Services premium, places de formation, stocks limités"," La rareté inventée génère du ressentiment"),
    ("Réciprocité","Donner quelque chose de valeur crée une obligation naturelle de rendre","Guide gratuit (vraie valeur) → lead nurturing → vente naturelle","Lead magnets, contenus premium gratuits, consultations offertes"," La valeur du cadeau détermine la réciprocité — évitez les ebooks creux"),
    ("Engagement & Cohérence","Une fois qu'une personne a dit oui à quelque chose de petit, elle dit oui à plus grand","Quiz gratuit → email → webinaire → offre → vente","Funnels de conversion, séquences email, onboarding progressif"," Chaque micro-engagement doit délivrer de la valeur"),
    ("Aversion à la perte","La douleur de perdre est 2x plus intense que le plaisir de gagner","Ne laissez pas vos concurrents prendre de l'avance · Évitez de perdre X €/mois","Messaging sur les risques de ne pas agir, coûts de l'inaction"," À utiliser avec parcimonie — le fear marketing permanent génère du rejet"),
    ("Appartenance","Les humains veulent appartenir à un groupe qui partage leurs valeurs","Rejoignez 5000 entrepreneurs qui ont choisi de [valeur commune]","Positioning de marque, communication de communauté, onboarding"," La communauté doit être réelle et active"),
]

@st.cache_data(ttl=3600)
def gen_aida(activity: str) -> dict:
    return copy.deepcopy(_AIDA.get(activity, _AIDA_GENERIC))

# ─── GEO 2025 ────────────────────────────────────────────────────────────────
_GEO = {
    "ecommerce": {
        "topics": ["Guide ultime d'achat [produit phare] — le contenu pilier de référence","Comparatif [produit A] vs [produit B] — contenu cluster haute valeur","FAQ produits enrichie — capture les requêtes conversationnelles IA","Avis clients structurés (schema Review) — utilisés par Google SGE"],
        "clusters": [("Guide d'achat [niche]",["Comment choisir X","Meilleur X pour Y","X test & avis","X prix comparatif"]),("Guide entretien / utilisation",["Comment utiliser X","Erreurs à éviter","X durée de vie","Tutoriel X"])],
        "optims": [("Ajoutez des FAQ schema markup sur toutes vos fiches produit"," Élevé"),("Répondez aux questions 'quel est le meilleur X pour Y'dans vos contenus"," Élevé"),("Utilisez du langage naturel conversationnel dans vos descriptions","Moyen"),("Structurez vos avis en données structurées (schema Review)"," Élevé")],
        "tips": ["Google SGE et ChatGPT extraient des réponses directes — soyez la source citée","Perplexity cite les sources — des backlinks de qualité restent essentiels","Les requêtes vocales explosent — optimisez pour le langage parlé"],
    },
    "saas": {
        "topics": ["Guides pratiques ultra-complets sur les problèmes que votre outil résout","Études de cas sectorielles avec métriques et ROI quantifiés","Comparatifs objectifs avec vos concurrents (even-handed = crédibilité)","Glossaire du secteur — topical authority signal fort pour Google"],
        "clusters": [("Guide [fonctionnalité principale]",["Comment faire X sans outil","X automatisation guide","X pour les débutants","X cas d'usage avancés"]),("Comparatif outils [catégorie]",["Vous vs Concurrent A","Vous vs Concurrent B","Meilleur outil X 2025","Migrer de X vers vous"])],
        "optims": [("Créez une documentation technique complète (boon for AI crawlers)"," Élevé"),("Publiez des datasets ou benchmarks sectoriels citables par l'IA","Très élevé"),("Répondez aux questions 'comment [task] avec [catégorie d'outil]'exhaustivement"," Élevé"),("Structurez vos how-to avec des étapes numérotées (schema HowTo)","Moyen")],
        "tips": ["Les LLMs sont entraînés sur le web — votre contenu publié aujourd'hui formera les réponses de demain","Soyez la ressource la plus citée de votre niche — qualité > quantité","ChatGPT et Perplexity favoritent les sites avec API publique et documentation claire"],
    },
}
_GEO_GENERIC = {
    "topics": ["Contenus piliers ultra-complets sur votre thème principal","Clusters de contenu répondant à toutes les questions de votre ICP","FAQ structurée avec schema markup pour la capture des requêtes IA","Études de cas et données sectorielles propriétaires"],
    "clusters": [("Guide principal [thème]",["Introduction","Niveau avancé","Cas pratiques","FAQ"]),("Solutions aux problèmes [cible]",["Problème A → solution","Problème B → solution","Comparatif solutions","Erreurs à éviter"])],
    "optims": [("Utilisez des questions naturelles comme sous-titres H2/H3"," Élevé"),("Ajoutez un schema FAQ sur toutes vos pages clés"," Élevé"),("Répondez directement et précisément en début de section (featured snippet)"," Élevé"),("Créez du contenu E-E-A-T : Experience, Expertise, Authority, Trust","Très élevé")],
    "tips": ["39% des Français utilisent l'IA conversationnelle — optimisez maintenant pour ces moteurs","Les IA citent les sources qui répondent directement et exhaustivement","L'intention de recherche prime sur le mot-clé exact — comprenez le 'pourquoi'"],
}

_SEA_IA = [
    ("Google AI Max","Performance Max avec IA Max — diffusion automatique sur tous les canaux Google",["Diffusion sur Search, Display, YouTube, Gmail, Maps, Shopping","Optimisation en temps réel des enchères et audiences via ML","Asset generation IA — génère des variantes de titres et descriptions"],"Fournissez des assets de qualité — la qualité des inputs détermine la qualité des outputs IA"),
    ("Smart Bidding","Stratégies d'enchères automatisées par Google ML pour maximiser les conversions",["Target CPA : coût par acquisition fixe — idéal si vous connaissez votre CPA cible","Target ROAS : retour sur dépenses publicitaires — pour e-commerce avec données de valeur","Maximize Conversions : maximise le volume dans votre budget — pour démarrer","Enhanced CPC : manuel + ajustement IA — contrôle maximal pour débutants"],"Donnez au Smart Bidding 2-4 semaines d'apprentissage avant d'évaluer les performances"),
    ("AI Overviews","Google AI Overviews — réponses IA intégrées dans les résultats de recherche",["Annonces textuelles dans les AI Overviews (beta 2025) — position premium visible","Shopping ads dans les réponses IA pour les requêtes produits","Position 0 : votre annonce affichée dans la synthèse IA de Google"],"Combinez SEA (paiement garanti) + SEO GEO (organique IA) pour une visibilité maximale"),
    ("Audience Signals","Signaux d'audience pour guider l'IA vers vos meilleurs prospects",["Customer Match : uploadez vos emails clients pour trouver des similaires","Similar Audiences basées sur vos convertisseurs","In-Market Audiences : personas en phase d'achat active","Custom Intent : audiences basées sur les recherches récentes"],"Plus vous fournissez de signaux de qualité, plus l'IA cible efficacement"),
]

@st.cache_data(ttl=3600)
def gen_geo(activity: str) -> dict:
    return copy.deepcopy(_GEO.get(activity, _GEO_GENERIC))

# ─── SEO KEYWORDS ENRICHED (from backend seo_service) ───────────────────────
_KEYWORDS_ENRICHED = {
    "ecommerce": [
        ("boutique en ligne livraison rapide",        "10K-100K", "Élevé",  "Transactionnel"),
        ("acheter en ligne paiement sécurisé",        "10K-100K", "Élevé",  "Transactionnel"),
        ("meilleur site e-commerce France",            "1K-10K",   "Moyen",  "Commercial"),
        ("avis client boutique fiable",                "1K-10K",   "Facile", "Commercial"),
        ("comparatif boutique en ligne",               "500-5K",   "Facile", "Commercial"),
        ("comment choisir boutique en ligne sécurisée","1K-10K",   "Facile", "Informationnel"),
        ("promotion soldes vente flash",               "5K-50K",   "Moyen",  "Transactionnel"),
    ],
    "saas": [
        ("logiciel gestion PME gratuit",               "10K-100K", "Élevé",  "Transactionnel"),
        ("alternative logiciel concurrent",            "1K-10K",   "Moyen",  "Commercial"),
        ("meilleur outil gestion TPE",                 "500-5K",   "Facile", "Commercial"),
        ("comment automatiser sa gestion d'entreprise","1K-10K",   "Facile", "Informationnel"),
        ("prix logiciel SaaS abonnement mensuel",      "500-5K",   "Facile", "Commercial"),
        ("logiciel SaaS pour startup",                 "500-5K",   "Facile", "Transactionnel"),
        ("outil productivité équipe télétravail",      "1K-10K",   "Moyen",  "Commercial"),
    ],
    "service": [
        ("consultant freelance en ligne",              "1K-10K",   "Moyen",  "Commercial"),
        ("prestataire service en ligne tarif",         "500-5K",   "Facile", "Transactionnel"),
        ("comment trouver un expert en ligne",         "5K-50K",   "Moyen",  "Informationnel"),
        ("devis service numérique rapide",             "1K-10K",   "Facile", "Commercial"),
        ("avis consultant freelance fiable",           "500-5K",   "Facile", "Commercial"),
        ("accompagnement individuel en ligne",         "1K-10K",   "Facile", "Transactionnel"),
    ],
    "consulting": [
        ("consultant stratégie entreprise freelance",  "1K-10K",   "Moyen",  "Commercial"),
        ("accompagnement dirigeant TPE PME",           "500-5K",   "Facile", "Commercial"),
        ("conseil business plan démarrage",            "5K-50K",   "Moyen",  "Informationnel"),
        ("mentor entrepreneur en ligne",               "1K-10K",   "Facile", "Transactionnel"),
        ("diagnostic stratégique PME gratuit",         "500-5K",   "Facile", "Commercial"),
    ],
    "content": [
        ("créateur de contenu formation",              "5K-50K",   "Moyen",  "Informationnel"),
        ("stratégie contenu réseaux sociaux",          "5K-50K",   "Moyen",  "Informationnel"),
        ("blog affilié revenus passifs",               "1K-10K",   "Moyen",  "Commercial"),
        ("newsletter abonnés fidélisation",            "1K-10K",   "Facile", "Informationnel"),
        ("monétiser audience YouTube Instagram",       "5K-50K",   "Élevé",  "Commercial"),
    ],
    "default": [
        ("solution en ligne professionnelle",          "1K-10K",   "Moyen",  "Commercial"),
        ("service numérique fiable",                   "500-5K",   "Facile", "Transactionnel"),
        ("comment démarrer une activité en ligne",     "5K-50K",   "Moyen",  "Informationnel"),
        ("meilleure solution pour entrepreneurs",      "1K-10K",   "Moyen",  "Commercial"),
        ("avis et comparatif solutions web",           "500-5K",   "Facile", "Commercial"),
        ("guide complet démarrage activité web",       "500-5K",   "Facile", "Informationnel"),
        ("astuce entrepreneur débutant",               "1K-5K",    "Facile", "Informationnel"),
    ],
}

# ─── PLATFORM ENRICHED (from backend marketing_service) ──────────────────────
_PLATFORM_ENRICHED = {
    "ecommerce": [
        ("Instagram Shopping",    "haute",   "1 post/jour + 5 stories",  "Idéal pour les achats impulsifs et la découverte visuelle produit"),
        ("Pinterest",             "haute",   "5 épingles/jour",           "Fort trafic d'intention d'achat, pins durables dans le temps"),
        ("Facebook Ads",          "haute",   "2-3 campagnes actives",     "Retargeting puissant et ciblage démographique précis"),
        ("Google Shopping",       "moyenne", "Campagnes continues",       "Capture l'intention d'achat directe en phase de recherche"),
        ("TikTok",                "moyenne", "3-5 vidéos/semaine",        "Viralité produit, fort engagement Génération Z et Millennials"),
    ],
    "saas": [
        ("LinkedIn",              "haute",   "5 posts/semaine",           "Audience professionnelle B2B, décideurs et acheteurs"),
        ("Google Ads",            "haute",   "Campagnes continues",       "Capture l'intention de recherche au moment clé du besoin"),
        ("Email Marketing",       "haute",   "1-2 emails/semaine",        "Nurturing leads, séquences d'onboarding et rétention (ROI 42:1)"),
        ("YouTube",               "moyenne", "1 vidéo/semaine",           "Tutoriels, démos produit et SEO vidéo durable"),
        ("Webinaires",            "moyenne", "2/mois",                    "Conversion haute intention, démonstration valeur directe"),
    ],
    "service": [
        ("LinkedIn",              "haute",   "5 posts/semaine",           "Réseau de référence pour les services B2B et le personal branding"),
        ("Email Marketing",       "haute",   "1-2 emails/semaine",        "Canal owned, meilleur ROI pour la fidélisation client"),
        ("Google (SEO local)",    "haute",   "2 articles/semaine",        "Capte les recherches directes de prestataires qualifiés"),
        ("Instagram",             "moyenne", "4 posts/semaine",           "Montre les coulisses et humanise le prestataire"),
        ("Podcasts / YouTube",    "moyenne", "1 épisode/semaine",         "Autorité sectorielle et contenu evergreen longue traîne"),
    ],
    "consulting": [
        ("LinkedIn",              "haute",   "5 posts/semaine",           "Plateforme numéro 1 pour le personal branding B2B"),
        ("Email Marketing",       "haute",   "1/semaine",                 "Nurturing prospects, newsletter d'expertise"),
        ("Podcast / YouTube",     "haute",   "1 épisode/semaine",         "Contenu long format pour démontrer l'expertise"),
        ("Google (SEO)",          "moyenne", "2 articles/semaine",        "Articles de fond qui capturent les recherches intentionnelles"),
        ("Webinaires",            "haute",   "1-2/mois",                  "Génération de leads qualifiés et démonstration de valeur"),
    ],
    "content": [
        ("YouTube",               "haute",   "2-3 vidéos/semaine",        "Plateforme vidéo avec meilleur ROI long terme et SEO intégré"),
        ("Newsletter (Substack)", "haute",   "1-2/semaine",               "Audience owned, monétisation directe, fidélisation forte"),
        ("Instagram / TikTok",   "haute",   "1 post/jour",               "Découverte, viralité et croissance rapide d'audience"),
        ("Podcast",               "moyenne", "1 épisode/semaine",         "Audience fidèle, partenariats et brand deals"),
        ("Pinterest",             "moyenne", "5 pins/jour",               "Trafic evergreen vers blog et contenu long terme"),
    ],
    "default": [
        ("Instagram",             "haute",   "1 post/jour",               "Large audience, format visuel adapté à tous secteurs"),
        ("Email Newsletter",      "haute",   "1-2/semaine",               "Canal owned avec meilleur ROI du marketing digital (42:1)"),
        ("Facebook",              "haute",   "5 posts/semaine",           "Ciblage avancé, groupes communautaires et publicité accessible"),
        ("LinkedIn",              "moyenne", "3-4 posts/semaine",         "Réseautage professionnel et autorité sectorielle"),
        ("Google Ads",            "moyenne", "Campagnes ciblées",         "Capture l'intention de recherche directe"),
    ],
}

# ─── SEO KEYWORDS ────────────────────────────────────────────────────────────
_KEYWORDS = {
    "ecommerce": [("boutique en ligne livraison rapide","10K-100K","Facile","Transactionnel"),("acheter [produit] pas cher","10K-100K","Moyen","Transactionnel"),("meilleur [produit] 2025","5K-10K","Moyen","Commercial"),("avis [produit/marque]","5K-10K","Facile","Commercial"),("[produit] livraison gratuite","1K-5K","Facile","Transactionnel"),("comparatif [produit]","1K-5K","Moyen","Commercial")],
    "saas": [("[fonctionnalité] logiciel","5K-10K","Moyen","Commercial"),("meilleur outil [catégorie] 2025","1K-5K","Moyen","Commercial"),("[concurrent] alternative","500-1K","Facile","Commercial"),("comment automatiser [tâche]","1K-5K","Facile","Informationnel"),("[catégorie] prix tarifs","500-1K","Moyen","Transactionnel"),("[catégorie] comparatif","1K-5K","Élevé","Commercial")],
    "service": [("[service] [ville] prix","1K-5K","Facile","Transactionnel"),("prestataire [service] pro","500-1K","Facile","Commercial"),("comment choisir [prestataire]","1K-5K","Moyen","Informationnel"),("[service] avis clients","500-1K","Facile","Commercial"),("tarif [service] 2025","500-1K","Moyen","Transactionnel")],
    "default": [("[mot-clé principal] guide","1K-5K","Moyen","Informationnel"),("meilleur [produit/service] 2025","1K-5K","Moyen","Commercial"),("comment [résoudre problème]","5K-10K","Facile","Informationnel"),("[secteur] prix tarif","500-1K","Moyen","Transactionnel"),("avis [marque/service]","500-1K","Facile","Commercial")],
}

@st.cache_data(ttl=3600)
def gen_keywords(activity: str) -> list:
    enriched = _KEYWORDS_ENRICHED.get(activity, _KEYWORDS_ENRICHED["default"])
    base = copy.deepcopy(_KEYWORDS.get(activity, _KEYWORDS["default"]))
    seen = set(kw for kw, _, _, _ in enriched)
    extra = [k for k in base if k[0] not in seen]
    return enriched + extra

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
    "sales": ["Témoignage client : [résultat chiffré]","Comparatif : [votre solution] vs alternatives","Offre exclusive : [bénéfice] pour [cible]","Démonstration : comment [fonctionnalité] fonctionne"],
    "leads": ["[Lead magnet] gratuit : [titre accrocheur]","Webinaire : [résoudre problème courant]","Quiz : quel est votre niveau en [thème] ?","Étude de cas : comment [client] a obtenu [résultat]"],
    "traffic": ["Guide SEO : [mot-clé cible] expliqué","Les [X] meilleures ressources pour [sujet]","Tutorial : [processus étape par étape]","Infographie : [données secteur] en 2025"],
}

@st.cache_data(ttl=3600)
def gen_platforms(activity: str) -> list:
    enriched = _PLATFORM_ENRICHED.get(activity, _PLATFORM_ENRICHED["default"])
    return copy.deepcopy(enriched)

@st.cache_data(ttl=3600)
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

@st.cache_data(ttl=3600)
def gen_budget_reco(monthly: float) -> list:
    if monthly <= 50:
        return [
            "Budget micro (≤50€) : misez à 100% sur l'organique",
            "Outils gratuits : Canva Free, Mailchimp Free, Google Search Console, Google Analytics",
            "Stratégie : 2 posts/semaine sur 1 réseau · 1 article de blog SEO/semaine · Newsletter mensuelle",
            "ROI attendu : notoriété et premiers leads organiques en 2-4 mois",
            " Évitez la pub payante — budget insuffisant pour obtenir des données statistiques fiables",
        ]
    elif monthly <= 200:
        return [
            "Budget starter (50-200€) : organique + micro-tests paid",
            "Outils : Canva Pro (13€/mois), Brevo/Sendinblue starter, Google Ads (50-100€ test)",
            "Stratégie : 1 campagne Google Ads test · SEO content 2x/sem · Email 2x/mois",
            "ROI attendu : premiers achats/leads payants en 4-6 semaines si niche peu concurrentielle",
            " Allouez 60% du budget paid sur 1 canal unique avant de diversifier",
        ]
    elif monthly <= 500:
        return [
            "Budget PME (200-500€) : mix paid + contenu + outils",
            "Outils : CRM starter (HubSpot Free ou Pipedrive 15€), Google Ads + Meta Ads, Semrush Lite",
            "Stratégie : SEA Search + retargeting · Content 3x/sem · Email automation bienvenue + nurturing",
            "ROI attendu : ROAS 2-4x en e-commerce · CPL 15-40€ en B2B sur 60-90 jours",
            "Commencez le SEO maintenant pour réduire la dépendance au paid dans 6 mois",
        ]
    else:
        return [
            "Budget PME confirmée (500-1000€) : stratégie complète multi-canal",
            "Outils : CRM complet (HubSpot Starter 50€/mois), Google Ads + Meta + LinkedIn Ads",
            "Outils SEO : Semrush ou Ahrefs (99€/mois) + outil email marketing avancé",
            "Stratégie : SEA tous canaux + SEO agressif + content production externalisée",
            "ROI attendu : ROAS 3-6x · Croissance trafic +40%/mois sur 6 mois · CPL optimisé",
            "Considérez 1 freelance content ou growth hacker à mi-temps pour accélérer",
        ]

@st.cache_data(ttl=3600)
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

@st.cache_data(ttl=3600)
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
        "probleme": ["Avez-vous des difficultés à gérer les stocks en temps réel ?","Perdez-vous des ventes à cause d'une mauvaise expérience mobile ?","Vos fiches produit sont-elles optimisées pour le référencement ?"],
        "implication":["Si votre taux de conversion augmentait de 1%, quel serait l'impact sur votre CA annuel ?","Combien de ventes perdez-vous chaque mois à cause de l'abandon panier ?","Quel est le coût d'opportunité d'une page produit mal référencée sur 12 mois ?"],
        "besoin": ["Si vous pouviez automatiser la gestion des stocks, combien de temps libéreriez-vous ?","Quel impact un taux de conversion à 3,5% aurait-il sur vos objectifs annuels ?","Si votre site chargeait en moins de 2 secondes, combien de ventes récupéreriez-vous ?"],
    },
    "saas": {
        "situation": ["Comment vos équipes gèrent-elles [processus] aujourd'hui ?","Quels outils utilisez-vous actuellement et depuis combien de temps ?","Combien de personnes sont concernées par ce processus dans votre organisation ?"],
        "probleme": ["Qu'est-ce qui vous frustre le plus dans votre solution actuelle ?","Combien de temps vos équipes passent-elles sur des tâches manuelles liées à [processus] ?","Y a-t-il des erreurs récurrentes dues à des processus manuels ?"],
        "implication":["Si ce problème persiste 12 mois, quel sera l'impact sur votre croissance ?","Combien coûte chaque heure perdue sur ces tâches manuelles, en salaire chargé ?","Quelle opportunité manquez-vous pendant que vos équipes font ces tâches répétitives ?"],
        "besoin": ["Si vous automatisiez [processus], que pourrait faire votre équipe de ce temps gagné ?","Quel ROI attendriez-vous d'une solution qui élimine [problème] en 30 jours ?","Comment une réduction de [X]% de vos erreurs de processus affecterait-elle votre NPS ?"],
    },
    "default": {
        "situation": ["Décrivez-moi comment vous gérez [sujet] aujourd'hui ?","Qui est impliqué dans ce processus et quelle est leur charge de travail ?","Depuis combien de temps cette situation dure-t-elle ?"],
        "probleme": ["Qu'est-ce qui vous pose le plus de difficultés dans cette situation ?","Quelles en sont les conséquences les plus visibles pour votre activité ?","Avez-vous déjà essayé de résoudre ce problème ? Qu'est-ce qui n'a pas fonctionné ?"],
        "implication":["Quel est l'impact de ce problème sur vos résultats à fin d'année ?","Si rien ne change, où en serez-vous dans 6 mois ?","Combien cela vous coûte-t-il chaque mois en temps, argent ou opportunités perdues ?"],
        "besoin": ["Si vous pouviez résoudre [problème] demain, quel serait le premier bénéfice visible ?","Qu'est-ce qu'une situation idéale ressemblerait pour vous dans 90 jours ?","Quel résultat justifierait votre investissement dans cette solution ?"],
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

@st.cache_data(ttl=3600)
def gen_scripts(activity: str) -> list:
    scripts = {
        "ecommerce": [
            {"title":"Email de relance panier abandonné","type":"email_followup","content":"Objet : Votre panier vous attend \n\nBonjour [Prénom],\n\nVous avez laissé quelque chose derrière vous !\n\nVotre sélection : [Produit(s)] est encore disponible — mais le stock est limité.\n\n→ Commander maintenant et bénéficiez de la livraison offerte jusqu'à ce soir.\n\n[BOUTON : Finaliser ma commande]\n\nÀ très vite,\nL'équipe [Marque]","keyPoints":["Personnaliser avec le nom du produit exact","Ajouter l'urgence (stock limité)","Un seul CTA : finaliser la commande","Livraison offerte = levier de conversion puissant"]},
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
        ("Taux de délivrabilité", "85,7%", "Ratio emails délivrés en boîte de réception. En dessous de 85%, vérifiez SPF/DKIM/DMARC", "sauge", ">90%"),
        (" Taux d'ouverture", "33,9%", "% d'emails ouverts sur emails délivrés. Varie selon le secteur (B2B > B2C)", "ambre", ">35%"),
        (" CTR (Taux de clics)", "5,35%", "% de clics sur le nombre d'emails délivrés. Indicateur d'engagement réel", "ambre", ">6%"),
        ("CTOR (Taux de réactivité)", "~15%", "CTR / Taux d'ouverture. Mesure la qualité du contenu vu par ceux qui ouvrent", "neutral", ">15%"),
        ("Taux de désabonnement", "<0,5%", "% de désabonnements par campagne. Au-dessus de 0,5%, revisez votre segmentation", "neutral", "<0,3%"),
        ("Revenu par email envoyé", "Variable", "CA généré divisé par le nombre d'emails envoyés. KPI ROI direct", "neutral", "Calculer"),
    ],
    "conversion": [
        ("Taux de conversion e-commerce", "2,5-3%", "% de visiteurs qui achètent. La moyenne mondiale est ~2,5%. Visez 3-4%", "ambre", ">3%"),
        ("CAC (Coût d'Acquisition Client)", "~1 200€", "Coût moyen pour acquérir 1 client B2B SaaS. E-commerce : 30-100€", "neutral", "Calculer"),
        ("NPS (Net Promoter Score)", "0-100", "Score de recommandation client. >50 = excellent, >70 = world-class", "neutral", ">50"),
        ("CSAT (Satisfaction Client)", ">70%", "% clients satisfaits. En dessous de 70%, identifiez les frictions majeures", "ambre", ">80%"),
        ("Temps de résolution tickets", "<4h", "Délai moyen de résolution des demandes support. Impact direct sur le CSAT", "neutral", "<2h"),
        ("Déviation par IA", "Variable", "% de tickets résolus par chatbot/IA sans intervention humaine. Visez 30-50%", "neutral", ">30%"),
    ],
    "social": [
        ("Engagement LinkedIn", "3-3,5%", "Likes + commentaires + partages / portée. Moyenne B2B : 3-3,5%", "sauge", ">4%"),
        ("Engagement Instagram", "0,45-0,6%", "Engagement rate moyen en 2025. Les Reels ont 3-5x plus d'engagement", "ambre", ">1%"),
        ("Engagement Facebook", "0,06-0,2%", "Reach organique très faible. Facebook Ads reste pertinent en paid", "neutral", ">0,2%"),
        ("▶ Engagement YouTube", "3,4%", "Likes + commentaires / vues. Complété par Watch Time et CTR miniature", "sauge", ">4%"),
        ("Croissance liste email", "+5-10%/mois", "Croissance mensuelle nette (nouveaux - désabonnés). Objectif PME : +5%/mois", "ambre", ">8%/mois"),
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

@st.cache_data(ttl=3600)
def gen_okr(goal: str) -> list:
    return copy.deepcopy(_OKR_TEMPLATES.get(goal, _OKR_TEMPLATES["awareness"]))

# ─── SYNTHESIS ───────────────────────────────────────────────────────────────
_PRIORITIES = {
    "awareness": ["Créez votre contenu pilier (2000+ mots) sur votre thème principal","Lancez votre présence sur 2 réseaux sociaux maximum — maîtrisez avant d'étendre","Définissez votre TOV (Tone of Voice) et charte éditoriale","Construisez votre liste email dès maintenant — c'est votre actif le plus précieux"],
    "sales": ["Optimisez votre tunnel de conversion — identifiez où vous perdez les prospects","Testez 2 versions de votre CTA principal (A/B test)","Mettez en place le retargeting sur Meta et Google","Activez les emails de relance automatiques (panier abandonné, devis non signé)"],
    "leads": ["Créez votre premier lead magnet à haute valeur perçue","Configurez une séquence email de nurturing (7 emails sur 14 jours)","Optimisez vos landing pages pour un seul objectif : la conversion","Intégrez un CRM pour tracker chaque lead de A à Z"],
    "traffic": ["Publiez 2 contenus SEO par semaine minimum pendant 3 mois","Lancez votre stratégie de backlinks (guest posting, digital PR)","Optimisez vos Core Web Vitals (LCP < 2.5s, CLS < 0.1)","Créez vos clusters de contenu autour de 3 thèmes piliers"],
}
_ROADMAP = [
    ("J1-J30","Fondations","Valider l'offre · Configurer les outils · Lancer les 1ers contenus · Premiers contacts"),
    ("J31-J60","Activation","Premières campagnes payantes · Séquences email actives · Premiers retours clients"),
    ("J61-J90","Optimisation","Analyser les données · A/B tester · Doubler ce qui fonctionne · Couper ce qui ne fonctionne pas"),
    ("J91-J180","Scalabilité","Augmenter les budgets gagnants · Nouveaux canaux · Recruter/déléguer · Préparer la prochaine phase"),
]

@st.cache_data(ttl=3600)
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
        "sales": [("Taux de conversion cible","> 2.5%"),("Panier moyen cible","À définir"),("ROAS cible","3-5x")],
        "leads": [("CPL (coût par lead) cible","< 15-50 €"),("Taux de qualification","> 40%"),("Taux de closing","> 20%")],
        "traffic": [("Visiteurs organiques cible","+50%/mois"),("Position mots-clés cible","Top 10 Google"),("Taux de rebond cible","< 55%")],
    }
    return base + extras.get(goal, [])

# ─── PROPOSITION DE VALEUR (from TGC suite) ──────────────────────────────────
@st.cache_data(ttl=3600)
def gen_proposition_valeur(activity: str, site_name: str = "") -> dict:
    """Proposition de valeur 4 dimensions (Apple/Tesla/L'Oreal framework)."""
    _pv = {
        "ecommerce": {
            "slogan": "La meilleure experience d'achat, livree chez vous",
            "fonctionnelle": "Produits de qualite livres rapidement avec garantie satisfait ou rembourse",
            "economique": "Prix competitifs, livraison offerte, paiement 3x sans frais",
            "emotionnelle": "Tranquillite d'esprit, fierte du produit recu, sentiment d'etre bien traite",
            "symbolique": "Marque de confiance qui respecte ses clients et tient ses promesses",
            "differenciateurs": [
                "Service client reactif — reponse en moins de 2h",
                "Retours gratuits 30 jours sans condition",
                "Avis clients verifies et transparents",
                "Livraison express disponible",
            ],
        },
        "saas": {
            "slogan": "Votre croissance, automatisee",
            "fonctionnelle": "Automatisation des taches repetitives, gain de temps mesurable des J1",
            "economique": "ROI positif en moins de 30 jours, consolidation de plusieurs outils en un",
            "emotionnelle": "Soulagement, confiance dans les donnees, sérénité opérationnelle",
            "symbolique": "Etre une entreprise moderne qui investit dans sa productivite",
            "differenciateurs": [
                "Onboarding en moins de 10 minutes",
                "Support fondateur accessible directement",
                "Intégrations natives avec vos outils existants",
                "Données exportables — aucun lock-in",
            ],
        },
        "service": {
            "slogan": "L'expertise qui transforme votre activite",
            "fonctionnelle": "Livraison de résultats mesurables dans les délais convenus",
            "economique": "ROI démontrable, prix fixe par livrable, pas de surprise",
            "emotionnelle": "Réassurance, sentiment d'être bien accompagné, progression visible",
            "symbolique": "Travailler avec un expert reconnu dans son domaine",
            "differenciateurs": [
                "Garantie résultat ou remboursement partiel",
                "Contrat détaillé avec jalons clairs",
                "Références clients vérifiables",
                "Disponibilité et réactivité garanties",
            ],
        },
        "consulting": {
            "slogan": "La clarté strategique qui accelere votre croissance",
            "fonctionnelle": "Diagnostic précis, plan d'action actionnable, implémentation guidée",
            "economique": "Évite les erreurs coûteuses, accelere le retour sur investissement",
            "emotionnelle": "Confiance dans les decisions, clarté dans la direction, réduction du stress",
            "symbolique": "Etre accompagné par un expert reconnu qui partage votre ambition",
            "differenciateurs": [
                "Approche personnalisée — aucun template générique",
                "Expertise sectorielle pointue et vérifiable",
                "Transfert de compétences inclus",
                "Accès direct au consultant senior",
            ],
        },
        "content": {
            "slogan": "Du contenu qui construit votre audience et vos revenus",
            "fonctionnelle": "Contenu optimisé qui génère trafic, engagement et conversions",
            "economique": "Actif pérenne qui travaille pour vous 24h/24 sans coût marginal",
            "emotionnelle": "Fierté de partager quelque chose de valeur, connexion avec sa communauté",
            "symbolique": "Devenir la référence incontournable de sa niche",
            "differenciateurs": [
                "Stratégie de contenu alignée sur vos objectifs business",
                "Distribution multi-canal optimisée",
                "Monétisation diversifiée (pub, produits, sponsoring)",
                "Analyse de performance continue",
            ],
        },
        "default": {
            "slogan": "La solution qui fait vraiment la différence",
            "fonctionnelle": "Résout votre problème précis de façon simple et efficace",
            "economique": "Investissement rapidement rentabilisé, valeur supérieure au prix",
            "emotionnelle": "Satisfaction, confiance, sentiment d'avoir fait le bon choix",
            "symbolique": "Choisir la qualité et l'innovation plutôt que le compromis",
            "differenciateurs": [
                "Différenciateur unique difficile à copier",
                "Relation client personnalisée",
                "Engagement qualité transparent",
                "Support réactif et humain",
            ],
        },
    }
    data = copy.deepcopy(_pv.get(activity, _pv["default"]))
    if site_name:
        data["slogan"] = data["slogan"]
    return data


@st.cache_data(ttl=3600)
def gen_rfm_segments(activity: str, monthly_budget: float) -> list:
    """Segmentation RFM 4 segments avec CLV et actions."""
    base_clv = {"ecommerce": 350, "saas": 1200, "service": 2500, "consulting": 5000, "content": 180, "default": 800}
    clv = base_clv.get(activity, base_clv["default"])
    return [
        {
            "nom": "Champions",
            "description": "Acheteurs récents, fréquents, à fort montant — vos meilleurs clients",
            "clv": round(clv * 3.5),
            "pourcentage": 15,
            "actions": [
                "Programme VIP exclusif avec avantages premium",
                "Demande de témoignage et de référencement",
                "Accès anticipé aux nouveautés",
                "Offre de partenariat ambassadeur",
            ],
        },
        {
            "nom": "Fidèles",
            "description": "Clients réguliers avec bon montant — le coeur de votre business",
            "clv": round(clv * 1.8),
            "pourcentage": 25,
            "actions": [
                "Upsell vers l'offre supérieure avec démo personnalisée",
                "Newsletter exclusive avec contenu premium",
                "Programme de fidélité avec points et récompenses",
                "Cross-sell de produits complémentaires",
            ],
        },
        {
            "nom": "A risque",
            "description": "Clients qui n'ont pas acheté depuis longtemps — risque de churn",
            "clv": round(clv * 0.6),
            "pourcentage": 30,
            "actions": [
                "Campagne de réactivation avec offre spéciale -20%",
                "Email personnalisé rappelant la valeur reçue",
                "Enquête satisfaction pour comprendre le désengagement",
                "Offre de downgrade pour retenir à moindre coût",
            ],
        },
        {
            "nom": "Perdus",
            "description": "Clients inactifs depuis longtemps — win-back ou abandon",
            "clv": round(clv * 0.1),
            "pourcentage": 30,
            "actions": [
                "Campagne win-back avec offre agressive (-30% ou cadeau)",
                "Email de séparation honnête pour obtenir un retour",
                "Analyse des raisons de départ pour améliorer le produit",
                "Suppression de la liste si aucune réactivation sous 6 mois",
            ],
        },
    ]


@st.cache_data(ttl=3600)
def gen_rse(activity: str) -> dict:
    """Analyse RSE / ISO 26000 — 7 domaines."""
    _rse_base = {
        "Gouvernance de l'organisation": {
            "niveau": 3,
            "actions": [
                "Définir une charte éthique et des valeurs d'entreprise écrites",
                "Mettre en place un processus de prise de décision transparent",
                "Nommer un référent RSE ou intégrer la RSE aux KPIs dirigeants",
            ],
            "risques": "Décisions non éthiques, manque de confiance des parties prenantes",
        },
        "Droits de l'homme": {
            "niveau": 3,
            "actions": [
                "Vérifier les conditions de travail chez vos fournisseurs",
                "Garantir l'égalité de traitement et la non-discrimination",
                "Former les équipes à la diversité et l'inclusion",
            ],
            "risques": "Risque réputationnel, non-conformité légale, perte de talents",
        },
        "Relations et conditions de travail": {
            "niveau": 4,
            "actions": [
                "Politique de télétravail flexible et équilibre vie pro/perso",
                "Formation continue et plan de développement des compétences",
                "Baromètre salarié semestriel avec plan d'action",
            ],
            "risques": "Turnover élevé, baisse de productivité, marque employeur dégradée",
        },
        "Environnement": {
            "niveau": 2,
            "actions": [
                "Mesurer et réduire votre empreinte carbone (bilan GES simplifié)",
                "Optimiser la consommation énergétique (hébergement green, déchets)",
                "Politique d'achats responsables et éco-conception",
            ],
            "risques": "Réglementation CSRD 2025, pression clients et investisseurs, greenwashing",
        },
        "Loyauté des pratiques": {
            "niveau": 4,
            "actions": [
                "Transparence totale sur les prix, conditions et données clients",
                "Politique anti-corruption et conformité RGPD rigoureuse",
                "Processus de gestion des conflits d'intérêts",
            ],
            "risques": "Sanctions CNIL, perte de confiance clients, litiges commerciaux",
        },
        "Questions relatives aux consommateurs": {
            "niveau": 4,
            "actions": [
                "Service après-vente réactif avec délais de traitement affichés",
                "Politique de retour et remboursement claire et généreuse",
                "Recueil et traitement systématique des avis clients",
            ],
            "risques": "Mauvaise e-réputation, churn élevé, litiges consommateurs",
        },
        "Communautés et développement local": {
            "niveau": 2,
            "actions": [
                "Partenariats avec des associations ou entreprises locales",
                "Programme de mécénat ou don pro bono de compétences",
                "Communication sur votre impact local et emplois créés",
            ],
            "risques": "Image perçue comme déconnectée du territoire, manque de soutien local",
        },
    }
    if activity == "ecommerce":
        _rse_base["Environnement"]["niveau"] = 2
        _rse_base["Environnement"]["actions"].insert(0, "Emballages durables et éco-responsables (obligation légale 2025)")
    elif activity == "saas":
        _rse_base["Environnement"]["niveau"] = 3
        _rse_base["Environnement"]["actions"].insert(0, "Hébergement cloud sur serveurs à énergie renouvelable (OVH, Scaleway)")
    return copy.deepcopy(_rse_base)


@st.cache_data(ttl=3600)
def gen_negociation(activity: str, monthly_budget: float) -> dict:
    """Tactiques de négociation BATNA/ZOPA/SONCAS."""
    _batna_map = {
        "ecommerce": ("Maintenir la stratégie organique et SEO sans partenariat",
                      "Trouver une alternative fournisseur moins chère"),
        "saas": ("Continuer avec les clients existants sans nouveau partenariat",
                 "Utiliser un concurrent ou développer en interne"),
        "service": ("Continuer à prospecter directement sans intermédiaire",
                    "Faire appel à un freelance moins spécialisé"),
        "consulting": ("Développer d'autres clients dans le même secteur",
                       "Internaliser la compétence avec un recrutement"),
        "default": ("Maintenir le statu quo ou chercher une alternative",
                    "Se tourner vers un concurrent ou solution DIY"),
    }
    batna_a, batna_b = _batna_map.get(activity, _batna_map["default"])
    zopa_min = round(monthly_budget * 0.6)
    zopa_max = round(monthly_budget * 1.4)
    return {
        "batna": {
            "vendeur": batna_a,
            "acheteur": batna_b,
            "conseil": "Renforcez votre BATNA avant toute négociation — plus votre alternative est forte, plus vous négociez de haut",
        },
        "zopa": {
            "min": zopa_min,
            "max": zopa_max,
            "amplitude": round((zopa_max - zopa_min) / zopa_max * 100),
            "conseil": f"Zone d'accord probable entre {zopa_min:,} € et {zopa_max:,} € — ancrez votre première offre au-dessus de votre objectif",
        },
        "concessions": [
            "Concession conditionnelle : 'Si vous acceptez X, alors je peux faire Y'",
            "Concession de valeur perçue : offrez quelque chose qui coûte peu mais vaut beaucoup",
            "Ne jamais faire de concession sans contrepartie — chaque concession doit être échangée",
            "La dernière concession doit toujours être petite — cela donne l'impression d'avoir atteint la limite",
        ],
        "tactiques": [
            "Ancrage : première offre toujours haute pour calibrer les attentes",
            "Silence stratégique : après une offre, ne parlez pas — laissez la pression s'exercer",
            "Flinch : réaction surprise visible face à chaque demande de concession",
            "Good cop / Bad cop : jouez sur plusieurs interlocuteurs pour créer de la flexibilité",
            "Deadline artificielle : 'Notre tarif change en fin de semaine'",
        ],
        "objections_prix": [
            ("C'est trop cher", "Calculons ensemble le ROI — si notre solution rapporte plus qu'elle coûte, est-ce encore trop cher ?"),
            ("J'ai une offre moins chère", "Comparez le coût total : prix + temps d'implémentation + risques. Notre offre inclut..."),
            ("Je dois consulter ma direction", "Bien sûr. Que vous faut-il pour avoir une recommandation solide à lui présenter ?"),
            ("On n'a pas le budget", "Si je vous montrais comment financer cela sans impact trésorerie immédiat, on pourrait avancer ?"),
        ],
    }


@st.cache_data(ttl=3600)
def gen_prix_psychologiques(monthly_budget: float, activity: str) -> list:
    """7 techniques de prix psychologiques avec exemples concrets."""
    ref_price = max(29, round(monthly_budget * 0.15))
    premium = round(ref_price * 2.5)
    anchor = round(ref_price * 3.2)
    return [
        {
            "nom": "Prix en charme (X9)",
            "description": "Terminez vos prix par 9 ou 7 — le cerveau perçoit 99 € comme nettement moins que 100 €",
            "exemple": f"{ref_price - 1}€ au lieu de {ref_price}€ — gain de conversion estimé +15 à +30%",
            "impact": "Élevé",
        },
        {
            "nom": "Ancrage haut",
            "description": "Affichez d'abord le prix le plus élevé pour calibrer les attentes",
            "exemple": f"Affichez l'offre Premium {anchor}€ avant l'offre Standard {ref_price}€ — la Standard semble abordable",
            "impact": "Très élevé",
        },
        {
            "nom": "Prix barré",
            "description": "Montrez le prix de référence barré avec le prix promotionnel — active l'aversion à la perte",
            "exemple": f"~~{round(ref_price * 1.4)}€~~ {ref_price}€ — économie visible = valeur perçue augmentée",
            "impact": "Élevé",
        },
        {
            "nom": "Tarification par paliers (decoy)",
            "description": "Créez 3 offres où la médiane est votre cible — l'effet decoy pousse vers le milieu",
            "exemple": f"Starter {round(ref_price * 0.6)}€ | Pro {ref_price}€ (recommandé) | Enterprise {premium}€",
            "impact": "Très élevé",
        },
        {
            "nom": "Prix fractionnés",
            "description": "Exprimez le prix en coût journalier ou hebdomadaire pour réduire la perception du montant",
            "exemple": f"{ref_price}€/mois devient 'Moins de {round(ref_price/30)}€/jour — moins qu'un café'",
            "impact": "Moyen",
        },
        {
            "nom": "Bundle et économies affichées",
            "description": "Regroupez des produits et affichez l'économie en euros ET en pourcentage",
            "exemple": f"Pack complet {round(ref_price * 2.4)}€ au lieu de {round(ref_price * 3)}€ — économisez {round(ref_price * 0.6)}€ (20%)",
            "impact": "Élevé",
        },
        {
            "nom": "Essai gratuit puis prix",
            "description": "L'engagement progressif augmente la conversion — l'utilisateur s'est déjà approprié le produit",
            "exemple": f"14 jours gratuits sans CB → {ref_price}€/mois — réduction du risque perçu = +40% de conversion",
            "impact": "Très élevé",
        },
    ]


# ─── WEB SCRAPING — Jina.ai Reader + BeautifulSoup fallback ─────────────────
@st.cache_data(ttl=900)
def scrape_site(url: str) -> dict:
    """
    Extraction structurée via Jina.ai Reader (gratuit, sans clé API).
    Fallback BeautifulSoup si Jina est indisponible.
    """
    if not url or not url.startswith("http"):
        return {}
    parsed = _urlparse.urlparse(url)
    if not parsed.netloc:
        return {}
    result: dict = {}
    # ── Jina.ai Reader (priorité) ─────────────────────────────────────────────
    try:
        import requests as req
        r = req.get(f"https://r.jina.ai/{url}", timeout=12,
                    headers={"Accept": "text/plain", "User-Agent": "BiziApp/2.1"})
        if r.status_code == 200:
            lines = r.text.split("\n")
            def get_meta(prefix):
                return next((l.replace(prefix,"").strip() for l in lines if l.startswith(prefix)),"")
            result["title"]       = get_meta("Title:")
            result["description"] = get_meta("Description:")
            result["source"]      = "jina"
            result["status"]      = 200
            body = [l for l in lines if not l.startswith(("Title:","URL:","Description:","Published","Warning","Markdown"))]
            result["h1"] = [l.lstrip("# ").strip() for l in body if l.startswith("# ")  and 3<len(l)<120][:5]
            result["h2"] = [l.lstrip("## ").strip() for l in body if l.startswith("## ") and 3<len(l)<120][:8]
            result["h3"] = [l.lstrip("### ").strip() for l in body if l.startswith("### ")and 3<len(l)<120][:6]
            result["main_text"] = " ".join(l for l in body if l and not l.startswith("#") and len(l)>20)[:2000]
    except Exception:
        pass
    # ── Fallback BeautifulSoup ────────────────────────────────────────────────
    if not result.get("title") and _HAS_BS4:
        try:
            import requests as req
            r = req.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")
            t = soup.find("title")
            result["title"]  = t.get_text(strip=True) if t else ""
            md = soup.find("meta", attrs={"name":"description"})
            result["description"] = md.get("content","") if md else ""
            result["h1"] = [x.get_text(strip=True) for x in soup.find_all("h1")][:5]
            result["h2"] = [x.get_text(strip=True) for x in soup.find_all("h2")][:8]
            result["h3"] = [x.get_text(strip=True) for x in soup.find_all("h3")][:6]
            og_t = soup.find("meta", property="og:title")
            og_d = soup.find("meta", property="og:description")
            result["og_title"]       = og_t.get("content","") if og_t else ""
            result["og_description"] = og_d.get("content","") if og_d else ""
            kw = soup.find("meta", attrs={"name":"keywords"})
            result["keywords_meta"]  = kw.get("content","") if kw else ""
            body_text = " ".join(p.get_text(" ",strip=True) for p in soup.find_all(["p","li","h1","h2","h3"]))
            result["main_text"]    = body_text[:2000]
            result["links_count"]  = len(soup.find_all("a", href=True))
            result["images_count"] = len(soup.find_all("img"))
            result["status"]       = r.status_code
            result["source"]       = "bs4"
        except Exception as e:
            result["error"] = str(e)
    # ── Extraction mots-clés page ─────────────────────────────────────────────
    if result.get("main_text"):
        import re as _re
        stopwords = {"avec","pour","dans","une","les","des","qui","que","sur","par",
                     "cette","leur","nous","vous","mais","aussi","plus","tres","bien",
                     "tout","tous","sans","sous","entre","apres","avant","comme","sont"}
        words = _re.findall(r"\b[a-zA-ZÀ-ɏ]{4,}\b", result["main_text"].lower())
        freq: dict = {}
        for w in words:
            if w not in stopwords:
                freq[w] = freq.get(w, 0) + 1
        result["keywords_page"] = sorted(freq, key=freq.get, reverse=True)[:12]
    return result

def scrape_site_meta(url: str) -> dict:
    """Alias de compatibilité."""
    return scrape_site(url)

# ─────────────────────────────────────────────────────────────────────────────
# VEILLE — Fonctions live (Google News · DuckDuckGo · Wikipedia)
# ─────────────────────────────────────────────────────────────────────────────
_UA_VEILLE = "Mozilla/5.0 BiziApp-Veille/2.0"
_STOP_VEILLE = {
    "avec","dans","pour","les","des","une","sur","par","que","qui","pas","mais",
    "donc","aussi","très","tout","comme","nous","vous","sont","était","être",
    "avoir","peut","plus","cette","cela","leur","dont","bien","fait","même",
    "sous","vers","sans","entre","après","avant","depuis","pendant",
    "this","that","from","with","your","will","have","been","they","their",
    "what","when","where","which","there","about","would","could","should",
}

def _veille_get(url: str, timeout: int = 12, extra: dict = None) -> str:
    """GET HTTP mutualisé pour les modules de veille."""
    hdrs = {"User-Agent": _UA_VEILLE, "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"}
    if extra:
        hdrs.update(extra)
    try:
        import requests as _r
        resp = _r.get(url, timeout=timeout, headers=hdrs)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return ""
        req = _urlreq.Request(url, headers=hdrs)
        with _urlreq.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")

def _veille_keywords(text: str, top: int = 15) -> list:
    """Extrait les mots-clés fréquents d'un texte (sans stopwords)."""
    words = _re.findall(r'\b[A-Za-zÀ-ÖØ-öø-ÿ]{4,}\b', text.lower())
    freq: dict = {}
    for w in words:
        if w not in _STOP_VEILLE:
            freq[w] = freq.get(w, 0) + 1
    return sorted(freq, key=lambda k: -freq[k])[:top]

@st.cache_data(ttl=1800)
def fetch_news(query: str, lang: str = "fr", max_items: int = 12) -> list:
    """Google News RSS — actualités live. Gratuit, sans clé API. Cache 30 min."""
    try:
        encoded = _urlparse.quote(query)
        rss = (
            f"https://news.google.com/rss/search"
            f"?q={encoded}&hl={lang}&gl=FR&ceid=FR:{lang}"
        )
        text = _veille_get(rss, timeout=12)
        root = _ET.fromstring(text)
        items = []
        for item in root.findall(".//item")[:max_items]:
            pub = item.findtext("pubDate", "")
            try:
                dt = datetime.datetime.strptime(pub, "%a, %d %b %Y %H:%M:%S %Z")
                pub_fmt = dt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                pub_fmt = pub[:16]
            src_tag = item.find("source")
            items.append({
                "title": item.findtext("title", ""),
                "link":  item.findtext("link", ""),
                "pub":   pub_fmt,
                "source": src_tag.text if src_tag is not None else "",
            })
        return items
    except Exception as e:
        return [{"title": f"Erreur chargement actualités : {e}", "link": "", "pub": "", "source": ""}]

@st.cache_data(ttl=3600)
def fetch_ddg(query: str) -> dict:
    """DuckDuckGo Instant Answer API. Gratuit, sans clé. Cache 1h."""
    try:
        encoded = _urlparse.quote(query)
        text = _veille_get(
            f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1&skip_disambig=1",
            timeout=8,
        )
        d = json.loads(text)
        return {
            "abstract": d.get("AbstractText", ""),
            "source": d.get("AbstractSource", ""),
            "source_url": d.get("AbstractURL", ""),
            "related": [
                t.get("Text", "")
                for t in d.get("RelatedTopics", [])
                if isinstance(t, dict) and "Text" in t
            ][:8],
        }
    except Exception:
        return {}

@st.cache_data(ttl=3600)
def fetch_wiki(topic: str, lang: str = "fr") -> dict:
    """Wikipedia REST API — résumé d'un sujet. Cache 1h."""
    try:
        encoded = _urlparse.quote(topic)
        text = _veille_get(
            f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded}",
            timeout=8,
        )
        d = json.loads(text)
        return {
            "title":       d.get("title", ""),
            "description": d.get("description", ""),
            "extract":     d.get("extract", ""),
            "url":         d.get("content_urls", {}).get("desktop", {}).get("page", ""),
        }
    except Exception:
        return {}

@st.cache_data(ttl=900)
def scrape_competitor(url: str) -> dict:
    """Analyse complète d'un concurrent via Jina.ai. Cache 15 min."""
    if not url or not url.startswith("http"):
        return {"error": "URL invalide", "url": url}
    try:
        text = _veille_get(
            f"https://r.jina.ai/{url}",
            timeout=15,
            extra={"Accept": "text/plain"},
        )
        lines = text.split("\n")
        def _meta(prefix):
            return next((l.replace(prefix,"").strip() for l in lines if l.startswith(prefix)), "")
        skip = {"Title:","URL:","Description:","Published","Warning","Markdown","Links"}
        body = [l for l in lines if not any(l.startswith(s) for s in skip)]
        h1 = [l.lstrip("# ").strip()  for l in body if l.startswith("# ")   and 3<len(l)<160][:5]
        h2 = [l.lstrip("## ").strip() for l in body if l.startswith("## ")  and 3<len(l)<160][:12]
        h3 = [l.lstrip("### ").strip()for l in body if l.startswith("### ") and 3<len(l)<120][:8]
        paras = [l for l in body if l and not l.startswith("#") and len(l) > 35]
        main_text = " ".join(paras)[:3500]
        return {
            "title":       _meta("Title:"),
            "description": _meta("Description:"),
            "url": url,
            "h1": h1, "h2": h2, "h3": h3,
            "paragraphs":  paras[:10],
            "main_text":   main_text,
            "keywords":    _veille_keywords(main_text),
            "source":      "jina",
            "fetched_at":  datetime.datetime.now().strftime("%H:%M · %d/%m/%Y"),
        }
    except Exception as e:
        return {"error": str(e), "url": url}

# ═════════════════════════════════════════════════════════════════════════════
# ── SIDEBAR — WIZARD ─────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

# ─── ADS & MEDIA PLAN ────────────────────────────────────────────────────────
def _estimate_reach(budget: float, platform: str) -> str:
    if budget <= 0: return "0 personnes"
    if platform == "facebook":
        low, high = int(budget * 80), int(budget * 200)
        unit = "personnes/mois"
    else:
        low, high = int(budget * 20), int(budget * 80)
        unit = "clics/mois"
    def fmt(n): return f"{n:,}".replace(",", " ")
    return f"{fmt(low)} – {fmt(high)} {unit}"

@st.cache_data(ttl=3600)
def gen_ads(activity: str, goal: str, monthly_budget: float) -> dict:
    fb_budget = round(monthly_budget * 0.40)
    gads_budget = round(monthly_budget * 0.35)
    other = max(0.0, monthly_budget - fb_budget - gads_budget)
    email_b = round(other * 0.5)
    seo_b = max(0, round(other * 0.5))

    kw_map = {
        "ecommerce": ["acheter [produit] livraison rapide","boutique en ligne promo","[marque] soldes"],
        "saas": ["essai gratuit logiciel gestion","outil productivité PME","meilleur SaaS [catégorie]"],
        "service": ["prestataire [service] devis","expert [domaine] disponible","consultant [spécialité]"],
        "consulting": ["consultant [domaine] PME","accompagnement entrepreneur","formation [métier] en ligne"],
        "content": ["formation créateur contenu","blog affilié revenus","monétiser Instagram/YouTube"],
        "default": ["solution professionnelle en ligne","service numérique fiable","meilleur [offre] France"],
    }
    kws = kw_map.get(activity, kw_map["default"])

    fb_obj = {"awareness":"Notoriété de la marque","sales":"Conversions","leads":"Génération de prospects","traffic":"Trafic"}.get(goal,"Trafic")
    discount = "15%" if monthly_budget < 200 else "20%"

    mediaplan = [
        {"platform":"Facebook / Instagram Ads","budget":fb_budget,"reach":_estimate_reach(fb_budget,"facebook"),"ctr":"1-3 %","roi":"2-3×"},
        {"platform":"Google Ads (Search)","budget":gads_budget,"reach":_estimate_reach(gads_budget,"google"),"ctr":"3-8 %","roi":"2.5-4×"},
    ]
    if email_b > 0:
        mediaplan.append({"platform":"Email Marketing","budget":email_b,"reach":"Liste email × 100%","ctr":"15-25 %","roi":"20-42×"})
    if seo_b > 0:
        mediaplan.append({"platform":"SEO & Contenu Organique","budget":seo_b,"reach":"Croissance +15-25%/mois","ctr":"2-5 %","roi":"5-10× (long terme)"})

    fb_campaigns = []
    if fb_budget > 0:
        fb_campaigns.append({"name":"Acquisition — Audience Froide","objective":fb_obj,"budget":round(fb_budget*0.6),"format":"Reel + Carrousel",
            "creatives":[
                {"format":"Reel 15s","headline":"Découvrez comment [activité] peut transformer votre quotidien","cta":"En savoir plus","audience":"Lookalike 2% clients"},
                {"format":"Carrousel","headline":"3 raisons qui font la différence","cta":"Voir l'offre","audience":"Intérêts ciblés 25-45 ans"},
            ]})
        if fb_budget >= 60:
            fb_campaigns.append({"name":"Retargeting — Audience Chaude","objective":"Conversions","budget":round(fb_budget*0.4),"format":"Image + Story",
                "creatives":[
                    {"format":"Image unique","headline":"Vous n'avez pas encore sauté le pas ?","cta":f"Profitez de -{discount}","audience":"Visiteurs 30 derniers jours"},
                    {"format":"Story vidéo","headline":"Ils ont essayé. Voici ce qu'ils disent.","cta":"Voir les témoignages","audience":"Engagement page + panier abandonné"},
                ]})

    google_campaigns = []
    if gads_budget > 0:
        google_campaigns.append({"name":"Search — Intention directe","type":"Search","budget":round(gads_budget*0.7),"keywords":kws})
        if gads_budget >= 50:
            google_campaigns.append({"name":"Display — Remarketing","type":"Display Network","budget":round(gads_budget*0.3),
                "keywords":["Remarketing visiteurs 30j","Audiences similaires 2%","In-market Google"]})

    organic = [
        {"channel":"Bouche-à-oreille & Referral","tactic":"Programme de parrainage double sens (parrain + filleul)","frequency":"Continu",
         "examples":["Offrir -20% pour chaque filleul","Programme ambassadeur clients satisfaits","Demander une recommandation après chaque vente"]},
        {"channel":"Réseaux sociaux organiques","tactic":"Stratégie de contenu éducatif + engagement communautaire","frequency":"Quotidien",
         "examples":["1 conseil pratique/jour en carrousel Instagram","Répondre à tous les commentaires en <2h","Groupe Facebook/Telegram pour votre communauté"]},
        {"channel":"Email Marketing","tactic":"Séquence nurturing automatisée avec segmentation comportementale","frequency":"1-2 emails/sem",
         "examples":["Lead magnet de valeur pour capturer les emails","Séquence bienvenue 5 emails / 10 jours","Newsletter 80% valeur / 20% promo"]},
        {"channel":"SEO & Contenu","tactic":"Stratégie pillar page + topic clusters pour dominer la niche","frequency":"2-3 articles/sem",
         "examples":["Article long-form +2000 mots sur le sujet principal","Guide complet résolvant le problème n°1 de vos personas","FAQ optimisée pour la recherche vocale et les IA"]},
    ]
    return {"mediaplan": mediaplan, "facebook": fb_campaigns, "google": google_campaigns, "organic": organic}

# ─── ROI PROJECTION 12 MOIS ──────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def gen_roi_projection(activity: str, goal: str, maturity: str, monthly_budget: float) -> list:
    avg_sale = {"ecommerce":45,"saas":49,"service":200,"consulting":250,"content":60,"other":80}.get(activity,80)
    paid = monthly_budget * 0.40
    ctr = {"idea":0.015,"inprogress":0.025,"launched":0.04}.get(maturity, 0.02)
    avg_cpc = {"saas":2.5,"service":2.0,"ecommerce":0.8,"consulting":2.0}.get(activity,1.5)
    monthly_clicks = paid / max(avg_cpc, 0.1)
    leads_base = monthly_clicks * ctr
    org_mult = {"idea":0.1,"inprogress":0.2,"launched":0.4}.get(maturity, 0.2)
    l2s = {"saas":0.15,"service":0.20,"ecommerce":0.03,"consulting":0.25}.get(activity, 0.10)
    data, cumul = [], {"p":0.0,"r":0.0,"o":0.0}
    for m in range(1, 13):
        g = min(2.5, 1.0 + (m-1)*0.12)
        og = 1.0 + org_mult * (m/12)
        leads = max(0.5, leads_base * g * og)
        rev = leads * l2s * avg_sale
        cumul["r"] += rev; cumul["o"] += rev*1.7; cumul["p"] += rev*0.5
        data.append({"month":m,"pessimiste":round(cumul["p"]),"realiste":round(cumul["r"]),"optimiste":round(cumul["o"])})
    return data

# ─── PAGESPEED MOCK ───────────────────────────────────────────────────────────
@st.cache_data(ttl=1800)
def get_pagespeed(url: str) -> dict:
    """Retourne des métriques PageSpeed (mock si pas d'API key)."""
    if not url or not url.startswith("http"):
        return {}
    # Essayer l'API PageSpeed si clé disponible
    try:
        psi_key = st.secrets.get("api", {}).get("pagespeed_api_key", "")
    except Exception:
        psi_key = ""
    if psi_key and _HAS_BS4:
        try:
            import requests as req
            r = req.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
                params={"url":url,"strategy":"mobile","key":psi_key}, timeout=10)
            if r.status_code == 200:
                d = r.json()
                cats = d.get("lighthouseResult",{}).get("categories",{})
                aud = d.get("lighthouseResult",{}).get("audits",{})
                return {
                    "performance": round((cats.get("performance",{}).get("score",0.6) or 0.6)*100),
                    "seo": round((cats.get("seo",{}).get("score",0.75) or 0.75)*100),
                    "accessibility": round((cats.get("accessibility",{}).get("score",0.7) or 0.7)*100),
                    "bestPractices": round((cats.get("best-practices",{}).get("score",0.8) or 0.8)*100),
                    "lcp": aud.get("largest-contentful-paint",{}).get("displayValue","N/A"),
                    "cls": aud.get("cumulative-layout-shift",{}).get("displayValue","N/A"),
                    "source": "api",
                }
        except Exception:
            pass
    # Mock intelligente basée sur l'URL
    import hashlib
    seed = int(hashlib.md5(url.encode()).hexdigest()[:8], 16) % 30
    return {
        "performance": 58 + seed, "seo": 72 + (seed % 20),
        "accessibility": 68 + (seed % 15), "bestPractices": 75 + (seed % 18),
        "lcp": f"{2.1 + (seed%10)*0.15:.1f} s", "cls": f"{0.05 + (seed%8)*0.02:.2f}",
        "source": "mock",
    }

# ─── SCRIPTS VENTE AVANCÉS ───────────────────────────────────────────────────
_CLOSING_TECHNIQUES = [
    {"name":"Alternative","desc":"Proposez deux options favorables — évitez le oui/non binaire.","ex":"Vous préférez commencer lundi ou mercredi ?"},
    {"name":"Urgence authentique","desc":"Créez une raison valide de décider maintenant.","ex":"Notre tarif de lancement se termine vendredi. Je vous réserve une place ?"},
    {"name":"Résumé de valeur","desc":"Récapitulez tous les bénéfices avant de demander la décision.","ex":"Vous obtenez X + Y + Z + garantie 30j. Pour [budget]€/mois. On y va ?"},
    {"name":"Trial sans risque","desc":"Proposez un essai pour lever les blocages.","ex":"Et si on testait 2 semaines sans engagement ? Vous voyez les résultats, vous décidez."},
    {"name":"Concession ciblée","desc":"Offrez quelque chose en échange d'une décision immédiate.","ex":"Si vous signez aujourd'hui, j'inclus le module premium offert (valeur 150€). Marché conclu ?"},
]

_MESSAGE_TEMPLATES = [
    {"channel":"Email froid","subject":"[Prénom], [résultat en 5 mots]",
     "body":"Bonjour [Prénom],\n\nJe serai direct : la plupart des [profil] échouent à [objectif] non par manque de budget, mais par manque de stratégie.\n\nEn analysant votre secteur, j'ai identifié 3 leviers que vous n'exploitez probablement pas encore.\n\nJe vous propose 20 minutes pour vous partager l'analyse — sans engagement.\n\n[Lien calendrier]\n\n[Votre nom]"},
    {"channel":"LinkedIn InMail","subject":"Question rapide sur votre stratégie",
     "body":"Bonjour [Prénom],\n\nJ'ai vu votre profil et votre travail sur [Élément spécifique].\n\nUne question : comment gérez-vous actuellement [objectif] ?\n\nJ'aide des profils similaires à structurer ça efficacement. Ouvert à un échange de 15 min ?"},
    {"channel":"SMS / WhatsApp","subject":"",
     "body":"Bonjour [Prénom] ! Suite à notre échange : j'ai préparé votre analyse personnalisée. 3 actions concrètes pour [objectif] dès cette semaine. Je vous l'envoie par email ?"},
    {"channel":"Relance post-démo","subject":"Votre analyse + prochaine étape",
     "body":"Bonjour [Prénom],\n\nMerci pour notre échange.\n\nJ'ai finalisé votre analyse avec :\n Les 3 actions prioritaires\n L'estimation ROI sur 6 mois\n La feuille de route semaine par semaine\n\nQuestion directe : qu'est-ce qui vous retient de passer à l'étape suivante ?\n\n[Votre nom]"},
]

LABELS = {
    "ecommerce":"E-commerce","saas":"SaaS","service":"Service","consulting":"Conseil",
    "content":"Créateur de contenu","other":"Autre",
    "awareness":"Notoriété","sales":"Ventes","leads":"Leads","traffic":"Trafic",
    "idea":"Idée","inprogress":"En cours","launched":"Lancé",
}

def _sanitize_url(url: str, max_len: int = 500) -> str:
    """Valide et nettoie une URL avant utilisation. Retourne '' si invalide."""
    if not url:
        return ""
    url = url.strip()[:max_len]
    try:
        p = _urlparse.urlparse(url if url.startswith("http") else "https://" + url)
        if p.scheme not in ("http", "https") or not p.netloc:
            return ""
        # Bloquer schemes dangereux + IPs privées
        if any(url.lower().startswith(s) for s in ("javascript:", "data:", "vbscript:", "file:")):
            return ""
        # Bloquer accès réseau local (SSRF protection)
        _host = p.hostname or ""
        if _host in ("localhost", "127.0.0.1", "0.0.0.0", "::1") or _host.startswith("192.168.") or _host.startswith("10.") or _host.startswith("172."):
            return ""
        return url
    except Exception:
        return ""

def _rate_limit_ok(key: str, max_calls: int = 30, window_s: int = 3600) -> bool:
    """Contrôle rudimentaire de débit par session. Retourne False si dépassé."""
    now = datetime.datetime.now().timestamp()
    hist_key = f"_rl_{key}"
    hist = [t for t in st.session_state.get(hist_key, []) if now - t < window_s]
    if len(hist) >= max_calls:
        return False
    hist.append(now)
    st.session_state[hist_key] = hist
    return True

def _sanitize_input(text: str, max_len: int = 200) -> str:
    """Nettoie un input texte — enlève caractères de contrôle, limite la longueur."""
    if not text:
        return ""
    import unicodedata
    cleaned = "".join(c for c in str(text) if unicodedata.category(c) not in ("Cc", "Cf") or c in ("\n", "\t"))
    return cleaned[:max_len].strip()

def _site_insights(site_data: dict) -> dict:
    """Extrait des insights personnalisés depuis les données du site scrapé."""
    if not site_data or site_data.get("error"):
        return {}
    kws = site_data.get("keywords_page", [])
    h1s = site_data.get("h1", [])
    h2s = site_data.get("h2", [])
    desc = site_data.get("description", "")
    title = site_data.get("title", "")
    main = site_data.get("main_text", "")
    return {
        "name": title,
        "desc": desc,
        "top_keywords": kws[:8],
        "main_topics": h1s[:3] + h2s[:4],
        "strengths_signals": [h for h in h1s + h2s if any(
            w in h.lower() for w in ["expert","garanti","certif","leader","meilleur","n°1","unique","exclusif","premium","qualité"]
        )][:3],
        "content_signals": [h for h in h2s if len(h) > 10][:5],
        "summary": main[:400] if main else desc[:300],
    }

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:8px 0 12px">
      
      <div style="font-size:1.25rem;font-weight:800;letter-spacing:-.5px;line-height:1"><span style="color:#0B2221">BIZI</span><span style="color:#44C1BA">APP</span></div>
      <div style="font-size:.65rem;color:#339999;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-top:3px">Stratégie 360° instantanée</div>
    </div>
    """, unsafe_allow_html=True)

    # ── WIZARD PROGRESS ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:12px">
      <div style="display:flex;justify-content:space-between;font-size:.7rem;color:#339999;margin-bottom:4px">
        <span>Étape 1 sur 5 — Contexte</span><span>0%</span>
      </div>
      <div class="progress-bar"><div class="progress-fill" style="width:25%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="step-label"><span class="step-num">1</span>Activité</div>', unsafe_allow_html=True)
    activity = st.selectbox(
        "Type d'activité",
        options=["ecommerce","saas","service","consulting","content","other"],
        format_func=lambda x: {"ecommerce":"E-commerce","saas":"SaaS","service":"Service","consulting":"Conseil","content":"Créateur de contenu","other":"Autre"}[x],
        label_visibility="collapsed",
    )

    st.markdown('<div class="step-label"><span class="step-num">2</span>Objectif</div>', unsafe_allow_html=True)
    goal = st.selectbox(
        "Objectif",
        options=["awareness","sales","leads","traffic"],
        format_func=lambda x: {"awareness":"Notoriété","sales":"Ventes","leads":"Génération de leads","traffic":"Trafic"}[x],
        label_visibility="collapsed",
    )

    st.markdown('<div class="step-label"><span class="step-num">3</span>Maturité</div>', unsafe_allow_html=True)
    maturity = st.selectbox(
        "Maturité",
        options=["idea","inprogress","launched"],
        format_func=lambda x: {"idea":"Idée","inprogress":"En cours","launched":"Lancé"}[x],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown('<div class="step-label"><span class="step-num">4</span>Budget mensuel</div>', unsafe_allow_html=True)
    st.caption("De 10€ (micro-test) à 1 000€+ (PME)")
    monthly_budget = st.slider("Budget mensuel", min_value=10, max_value=1000, value=200, step=10, label_visibility="collapsed")
    st.markdown(f"<div style='text-align:center;font-size:1.1rem;font-weight:700;color:#44C1BA'>{monthly_budget} €/mois</div>", unsafe_allow_html=True)

    total_budget = st.number_input("Capital disponible (€)", min_value=0, max_value=1_000_000, value=5_000, step=500)
    website_url = st.text_input("URL du site à analyser", placeholder="https://monsite.fr")
    website_url = _sanitize_url(website_url)

    # ── VEILLE & CONCURRENTS ─────────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="step-label"><span class="step-num">5</span>Concurrents à surveiller</div>', unsafe_allow_html=True)
    st.caption("Jusqu'à 3 URLs — analysées en temps réel via Jina.ai")
    _comp1 = st.text_input("Concurrent 1", placeholder="https://concurrent1.fr", label_visibility="collapsed", key="sb_c1")
    _comp2 = st.text_input("Concurrent 2", placeholder="https://concurrent2.fr", label_visibility="collapsed", key="sb_c2")
    _comp3 = st.text_input("Concurrent 3", placeholder="https://concurrent3.fr", label_visibility="collapsed", key="sb_c3")
    comp_urls = [_sanitize_url(u if u.startswith("http") else "https://" + u)
               for u in [_comp1.strip(), _comp2.strip(), _comp3.strip()] if u.strip()]
    comp_urls = [u for u in comp_urls if u]

    st.markdown('<div class="step-label">Mots-clés veille</div>', unsafe_allow_html=True)
    st.caption("Un par ligne — alimente le flux d'actualités")
    _vkw = st.text_area("Mots-clés", placeholder="intelligence artificielle\nautomation\nstartup", height=80, label_visibility="collapsed", key="sb_vkw")
    veille_keywords = [k.strip() for k in _vkw.strip().split("\n") if k.strip()]
    veille_lang = st.selectbox("Langue actualités", ["fr", "en", "es", "de"], index=0, key="sb_vlang")

    st.divider()
    if st.button("Lancer l'analyse", type="primary", use_container_width=True):
        st.session_state["_run"] = True
    if st.session_state.get("_run") and st.button("Réinitialiser", use_container_width=True):
        st.session_state["_run"] = False
        st.rerun()
    run = st.session_state.get("_run", False)
    st.caption("Analyse personnalisée · Données live · Cache intelligent")
    if _HAS_BS4 and website_url:
        st.caption("Lecture du site activée")


# ═════════════════════════════════════════════════════════════════════════════
# ── HEADER ───────────────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('''
<div class="bizi-header">
  <div class="bizi-logo">
    <span class="logo-bizi">BIZI</span><span class="logo-app">APP</span>
  </div>
  <div>
    <div class="header-sub">SWOT · PESTEL · SONCAS · AIDA · SPIN · Challenger · GEO 2025 · KPIs · OKR</div>
  </div>
</div>
''', unsafe_allow_html=True)

# ── SOCIAL PROOF BANNER ───────────────────────────────────────────────────────
st.markdown("""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px">
  <div class="feature-card">
    <div class="feature-title">Diagnostic complet</div>
    <div class="feature-desc">SWOT · QQOQCCP · PESTEL · Forces concurrentielles</div>
  </div>
  <div class="feature-card">
    <div class="feature-title">Psychologie de vente</div>
    <div class="feature-desc">SONCAS · Personas · AIDA · SPIN · Challenger Sale</div>
  </div>
  <div class="feature-card">
    <div class="feature-title">Acquisition 360°</div>
    <div class="feature-desc">Plan média · Budgets 10–1000€/mois · ROI 12 mois</div>
  </div>
  <div class="feature-card">
    <div class="feature-title">SEO & GEO 2025</div>
    <div class="feature-desc">Mots-clés · AI Overviews · OKR · Export JSON</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LANDING PAGE (pre-run) ─────────────────────────────────────────────────────
if not st.session_state.get("_run", False):
    st.info("Remplissez le formulaire dans la barre latérale puis cliquez sur **Lancer l'analyse**")
    st.markdown("""
    #### Ce que BiziApp génère pour vous :
    | Module | Contenu |
    |--------|---------|
    | **Diagnostic** | SWOT · QQOQCCP · PESTEL · Micro-environnement · Analyse concurrentielle |
    | **Personas** | Profils clients enrichis · Framework SONCAS · Motivations · Valeurs · Habitudes |
    | **Copywriting** | AIDA adapté · 8 déclencheurs psychologiques · Principes universels |
    | **Vente** | Scripts (cold, discovery, follow-up) · SPIN Selling · Challenger Sale · Gestion objections |
    | **Marketing** | Plateformes · Budget adaptatif 10-1000€ · Calendrier éditorial 8 semaines · Règle 80/20 |
    | **SEO & GEO 2025** | Mots-clés · Clusters · AI Overviews · SEA IA (AI Max, Smart Bidding…) |
    | **KPI Dashboard** | Email · Conversion · Social · OKR · Benchmarks sectoriels |
    | **Synthèse** | Score global · Priorités · Roadmap 180 jours · Export JSON |
    """)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# GENERATE DATA
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("Génération de l'analyse en cours…"):
    swot = gen_swot(activity, goal, maturity)
    qqoqccp = gen_qqoqccp(activity)
    pestel = gen_pestel(activity)
    micro_env = gen_micro_env(activity)
    competitive = gen_competitive(activity)
    soncas = gen_soncas(activity)
    aida = gen_aida(activity)
    geo = gen_geo(activity)
    keywords = gen_keywords(activity)
    platforms = gen_platforms(activity)
    budget_alloc = gen_budget_alloc(monthly_budget)
    budget_reco = gen_budget_reco(monthly_budget)
    calendar = gen_calendar(goal)
    personas = gen_personas(activity)
    scripts = gen_scripts(activity)
    synthesis = gen_synthesis(activity, goal, maturity, monthly_budget)
    okrs = gen_okr(goal)
    spin_data = _SPIN.get(activity, _SPIN["default"])
    site_data = scrape_site(website_url) if website_url else {}
    site_meta = site_data
    # ── Personnalisation depuis les données du site ───────────────────────────
    site_ins = _site_insights(site_data)
    if site_ins:
        _sn  = site_ins.get("name", "")
        _skw = site_ins.get("top_keywords", [])
        _sst = site_ins.get("strengths_signals", [])
        _scs = site_ins.get("content_signals", [])
        # Enrichir SWOT avec données réelles du site
        if _sn:
            swot["strengths"].insert(0, f"Présence en ligne confirmée — {_html.escape(_sn[:60])}")
        if _skw:
            swot["strengths"].append(f"Positionnement sur : {', '.join(_html.escape(k) for k in _skw[:4])}")
        if not site_data.get("h1"):
            swot["weaknesses"].insert(0, "Balise H1 absente — impact SEO négatif")
        if not site_data.get("description"):
            swot["weaknesses"].insert(0, "Meta description absente — CTR organique à risque")
        if _sst:
            swot["strengths"].append(f"Signal différenciant détecté : {_html.escape(_sst[0][:80])}")
        # Enrichir keywords avec les vrais mots-clés de la page
        if _skw:
            _site_kw_tuples = [
                (kw, "réel · site scrapé", "—", "informationnel")
                for kw in _skw[:5]
            ]
            keywords = _site_kw_tuples + [k for k in keywords if k[0] not in _skw]
        # Enrichir personas avec le nom de l'entreprise
        if _sn:
            for _p in personas:
                if "brands" in _p:
                    _p["brands"] = [_sn[:30]] + _p["brands"][:2]
    # ── Concurrents ───────────────────────────────────────────────────────────
    comp_results = {}
    # Pré-charger concurrents depuis le cache session si déjà analysés
    if comp_urls:
        _ck_pre = "comp_" + str(abs(hash(tuple(sorted(comp_urls)))))
        if _ck_pre in st.session_state:
            comp_results.update(st.session_state[_ck_pre])
    # Enrichir SWOT avec données concurrents réels (si déjà en cache)
    if comp_results:
        _comp_names = []
        for _cu_r, _cd_r in comp_results.items():
            if not _cd_r.get("error") and _cd_r.get("title"):
                _comp_names.append(_html.escape(_cd_r["title"][:40]))
        if _comp_names:
            swot["threats"].insert(0, f"Concurrents identifiés : {' · '.join(_comp_names[:3])}")
            swot["opportunities"].insert(0, "Analyse concurrentielle disponible — exploitez les angles manquants")
    ads_data = gen_ads(activity, goal, monthly_budget)
    roi_data = gen_roi_projection(activity, goal, maturity, monthly_budget)
    pagespeed_data = get_pagespeed(website_url) if website_url else {}
    closing_tech = _CLOSING_TECHNIQUES
    msg_templates = _MESSAGE_TEMPLATES

# Context badges
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<span class="badge badge-graphite">{LABELS.get(activity, activity)}</span>', unsafe_allow_html=True)
c2.markdown(f'<span class="badge badge-jade">{LABELS.get(goal, goal)}</span>', unsafe_allow_html=True)
c3.markdown(f'<span class="badge badge-teal">{LABELS.get(maturity, maturity)}</span>', unsafe_allow_html=True)
c4.markdown(f'<span class="badge badge-blue">{monthly_budget:,} €/mois</span>', unsafe_allow_html=True)

if site_data.get("title"):
    st.caption(f"Site analysé : **{site_data.get('title','')}** — {site_data.get('description','')[:120]}")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Diagnostic",
    "Personas",
    "Copywriting",
    "Vente",
    "Marketing",
    "Campagnes",
    "SEO / GEO",
    "KPIs",
    "Synthèse",
    "Veille",
    "RSE",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DIAGNOSTIC
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    # ── ANALYSE DU SITE (si URL fournie) ───────────────────────────────────────
    if site_data and not site_data.get("error"):
        _sd_title = site_data.get("title","")
        _sd_desc  = site_data.get("description","")
        _sd_h1s   = site_data.get("h1",[])
        _sd_h2s   = site_data.get("h2",[])
        _sd_kws   = site_data.get("keywords_page",[])
        _kw_badges = "".join(
            f'<span class="url-kw">{_html.escape(k)}</span>' for k in _sd_kws[:10]
        )
        st.markdown(f'''
        <div class="url-panel">
          <div class="url-panel-title">{_html.escape(_sd_title or website_url)}</div>
          <div class="url-panel-sub">{_html.escape((_sd_desc or "Aucune meta description")[:160])}</div>
          <div style="margin-top:10px">{_kw_badges}</div>
        </div>
        ''', unsafe_allow_html=True)

        _col_s, _col_o = st.columns(2)
        with _col_s:
            st.markdown('<div class="section-h">Structure détectée</div>', unsafe_allow_html=True)
            for _h in (_sd_h1s or [])[:3]:
                st.markdown(f"**H1** — {_html.escape(_h)}")
            for _h in (_sd_h2s or [])[:4]:
                st.markdown(f"H2 — {_html.escape(_h)}")
            if not _sd_h1s and not _sd_h2s:
                st.caption("Aucun titre H1/H2 détecté")
        with _col_o:
            st.markdown('<div class="section-h">Observations</div>', unsafe_allow_html=True)
            _obs = []
            if not _sd_desc:
                _obs.append(("#B83D4B","Meta description absente — impact SEO direct"))
            if not _sd_h1s:
                _obs.append(("#B83D4B","Aucun H1 détecté — priorité absolue"))
            elif len(_sd_h1s)>1:
                _obs.append(("#44C1BA",f"{len(_sd_h1s)} H1 trouvés — un seul est recommandé"))
            else:
                _obs.append(("#267371",f"H1 présent : {_sd_h1s[0][:55]}"))
            if _sd_desc and len(_sd_desc)>160:
                _obs.append(("#44C1BA",f"Meta description longue ({len(_sd_desc)} car.) — viser 155 max"))
            elif _sd_desc:
                _obs.append(("#267371","Meta description bien dimensionnée"))
            if _sd_kws:
                _obs.append(("#267371",f"Thématique dominante : {_sd_kws[0]}"))
            _lc = site_data.get("links_count",0)
            if _lc:
                _obs.append(("#267371",f"{_lc} liens détectés"))
            for _c, _msg in _obs:
                st.markdown(f'<div style="padding:5px 0;border-bottom:1px solid #E4E9F6;font-size:.83rem;color:{_c}">— {_html.escape(_msg)}</div>', unsafe_allow_html=True)
        # Enrichissement SWOT avec données site
        if not _sd_h1s:
            swot["weaknesses"].insert(0,"Structure SEO à renforcer (H1 absent)")
        if not _sd_desc:
            swot["weaknesses"].insert(0,"Meta description absente — référencement à optimiser")
        if _sd_title:
            swot["strengths"].insert(0,f"Présence web établie : {_sd_title[:55]}")
        st.markdown("<br>", unsafe_allow_html=True)

        # SWOT
    st.markdown('<div class="section-h">Analyse SWOT</div>', unsafe_allow_html=True)
    st.caption("Le SWOT structure toute réflexion stratégique : Forces · Faiblesses · Opportunités · Menaces")
    col_s, col_w = st.columns(2)
    with col_s:
        st.markdown('<div class="card swot-strength"><div class="card-title"> Forces</div>'+
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {_html.escape(str(i))}</p>" for i in swot["strengths"]) +
            "</div>", unsafe_allow_html=True)
    with col_w:
        st.markdown('<div class="card swot-weakness"><div class="card-title"> Faiblesses</div>'+
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {_html.escape(str(i))}</p>" for i in swot["weaknesses"]) +
            "</div>", unsafe_allow_html=True)
    col_o, col_t = st.columns(2)
    with col_o:
        st.markdown('<div class="card swot-oppty"><div class="card-title"> Opportunités</div>'+
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {_html.escape(str(i))}</p>" for i in swot["opportunities"]) +
            "</div>", unsafe_allow_html=True)
    with col_t:
        st.markdown('<div class="card swot-threat"><div class="card-title"> Menaces</div>'+
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {_html.escape(str(i))}</p>" for i in swot["threats"]) +
            "</div>", unsafe_allow_html=True)

    # QQOQCCP
    st.markdown('<div class="section-h">Analyse QQOQCCP</div>', unsafe_allow_html=True)
    st.caption("7 questions pour ne laisser aucune zone d'ombre dans votre diagnostic stratégique")

    for key, item in qqoqccp.items():
        with st.expander(f"**{key.upper()}** — {item['q']}"):
            col_r, col_a = st.columns(2)
            with col_r:
                st.markdown("**Réponse stratégique**")
                st.info(item["r"])
            with col_a:
                st.markdown("**Action recommandée**")
                st.success(item["a"])

    # PESTEL
    st.markdown('<div class="section-h">Analyse PESTEL</div>', unsafe_allow_html=True)
    st.caption("6 dimensions macro-environnementales que vous ne contrôlez pas mais devez impérativement anticiper")
    impact_cls = {"positif":"dot-pos","négatif":"dot-neg","neutre":"dot-neu"}
    for dim, items in pestel.items():
        with st.expander(f"**{dim}** ({len(items)} facteur{'s'if len(items)>1 else ''})"):
            for facteur, impact, note in items:
                st.markdown(f'<span class="{impact_cls.get(impact,"dot-neu")}"></span>**{facteur}** `{impact}`', unsafe_allow_html=True)
                st.caption(f"→ {note}")
                st.divider()

    # MICRO-ENV
    st.markdown('<div class="section-h">Micro-environnement — Forces concurrentielles</div>', unsafe_allow_html=True)
    st.caption("Analyse des acteurs en interaction directe (modèle inspiré des 5 forces de Porter) : pouvoir de négociation et leviers d'action")
    pouvoir_color = {"élevé":"badge-red","très élevé":"badge-red","moyen":"badge-teal","faible":"badge-jade"}
    cols = st.columns(2)
    for i, (acteur, (pouvoir, desc, levier)) in enumerate(micro_env.items()):
        with cols[i % 2]:
            badge_cls = pouvoir_color.get(pouvoir, "badge-gray")
            st.markdown(f"""
            <div class="card">
              <div class="card-title">{acteur} <span class="badge {badge_cls}">Pouvoir : {pouvoir}</span></div>
              <p style='font-size:.85rem;color:#267371'>{desc}</p>
              <p style='font-size:.82rem;color:#267371'>{levier}</p>
            </div>""", unsafe_allow_html=True)

    # COMPETITIVE
    st.markdown('<div class="section-h">Analyse concurrentielle</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Rivaux directs**")
        for r in competitive["direct"]:
            st.markdown(f"• {r}")
    with c2:
        st.markdown("**Rivaux indirects**")
        for r in competitive["indirect"]:
            st.markdown(f"• {r}")
    st.markdown("**Matrice concurrentielle** ( avantage · désavantage · neutre)")
    table_html = '<table class="bizi-table"><thead><tr><th>Critère</th><th>Vous</th><th>Leader</th><th>Analyse</th></tr></thead><tbody>'
    for critere, vous, leader, note in competitive["matrix"]:
        table_html += f"<tr><td><b>{critere}</b></td><td style='text-align:center;font-size:1.1rem'>{vous}</td><td style='text-align:center;font-size:1.1rem'>{leader}</td><td style='font-size:.82rem;color:#339999'>{note}</td></tr>"
    table_html += "</tbody></table>"
    st.markdown(f'<div style="overflow-x:auto">'+ table_html +'</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**Opportunité de positionnement**\n\n{competitive['oppty']}")
    with col_b:
        st.success(f"** Votre avantage défendable (Moat)**\n\n{competitive['moat']}")

    # PROPOSITION DE VALEUR
    st.markdown('<div class="section-h">Proposition de valeur</div>', unsafe_allow_html=True)
    st.caption("Construisez une proposition de valeur differenciante sur 4 dimensions (framework Apple · Tesla · L'Oreal)")
    _pv = gen_proposition_valeur(activity, site_ins.get("name", "") if site_ins else "")
    _pv_colors = {"fonctionnelle":"#393DAC","economique":"#267371","emotionnelle":"#44C1BA","symbolique":"#393DAC"}
    _pv_labels = {"fonctionnelle":"Fonctionnelle","economique":"Economique","emotionnelle":"Emotionnelle","symbolique":"Symbolique"}
    st.markdown(f'<div class="card card-dark" style="margin-bottom:16px"><div style="font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.5);margin-bottom:6px">Slogan</div><div style="font-size:1.15rem;font-weight:700;color:white">{_html.escape(_pv["slogan"])}</div></div>', unsafe_allow_html=True)
    _pv_cols = st.columns(4)
    for _pi, (_pk, _pv_label) in enumerate(_pv_labels.items()):
        with _pv_cols[_pi]:
            _c = _pv_colors[_pk]
            st.markdown(f'<div class="pv-card" style="background:{_c}"><div style="font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;opacity:.7;margin-bottom:5px">{_pv_label}</div><div style="font-size:.85rem;line-height:1.5">{_html.escape(_pv[_pk])}</div></div>', unsafe_allow_html=True)
    if _pv.get("differenciateurs"):
        st.markdown("**Points de différenciation :**")
        for _d in _pv["differenciateurs"]:
            st.markdown(f"• {_html.escape(_d)}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PERSONAS & SONCAS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    # PERSONAS
    st.markdown('<div class="section-h">Personas clients enrichis</div>', unsafe_allow_html=True)
    st.caption("Profils semi-fictifs construits à partir de données comportementales, sectorielles et psychographiques")
    for i, p in enumerate(personas):
        initials = "".join([w[0] for w in p["name"].split()][:2]).upper()
        colors = ["#0B2221","#44C1BA","#267371","#393DAC","#B83D4B"]
        color = colors[hash(p["name"]) % len(colors)]
        fw_badge = f'<span class="badge badge-teal">{p.get("framework","")}</span>'if p.get("framework") else ""
        with st.expander(f"**{p['name']}** · {p['age']} ans · {p['job']} · {p['location']}", expanded=(i==0)):
            c1, c2, c3 = st.columns([1, 2, 2])
            with c1:
                st.markdown(f"""
                <div style="width:72px;height:72px;border-radius:50%;background:{color};
                  display:flex;align-items:center;justify-content:center;
                  font-size:1.4rem;font-weight:800;color:white;margin:0 auto 8px">
                  {initials}
                </div>
                {fw_badge}
                <p style="text-align:center;font-style:italic;font-size:.78rem;color:#339999;margin-top:6px">"{p['quote']}"</p>
                """, unsafe_allow_html=True)
                if p.get("framework_match"):
                    st.markdown(f"<small style='color:#44C1BA;font-size:.7rem'>↳ {p['framework_match']}</small>", unsafe_allow_html=True)
            with c2:
                st.markdown("**Objectifs**")
                for g in p["goals"]: st.markdown(f"{g}")
                st.markdown("**Douleurs**")
                for pa in p["pains"]: st.markdown(f"{pa}")
                if p.get("motivations"):
                    st.markdown("**Motivations**")
                    st.markdown(" ".join(f'<span class="badge badge-jade">{m}</span>'for m in p["motivations"]), unsafe_allow_html=True)
            with c3:
                st.markdown("**Canaux favoris**")
                st.markdown(" ".join(f'<span class="badge badge-blue">{c}</span>'for c in p["channels"]), unsafe_allow_html=True)
                st.markdown("<br>**Déclencheurs d'achat**", unsafe_allow_html=True)
                for t in p["triggers"]: st.markdown(f"→ {t}")
                if p.get("habits"):
                    st.markdown("**Habitudes**")
                    for h in p["habits"]: st.markdown(f"• {h}")
                if p.get("values"):
                    st.markdown("**Valeurs**")
                    st.markdown(" ".join(f'<span class="badge badge-gray">{v}</span>'for v in p["values"]), unsafe_allow_html=True)

    # SONCAS
    st.markdown('<div class="section-h">Analyse SONCAS — 6 leviers psychologiques de vente</div>', unsafe_allow_html=True)
    st.caption("SONCAS : Sécurité · Orgueil · Nouveauté · Confort · Argent · Sympathie — les 6 motivations d'achat universelles")
    soncas_css_map = {
        "securite": "soncas-securite",
        "opportunite":"soncas-opportunite",
        "nouveaute": "soncas-nouveaute",
        "confort": "soncas-confort",
        "argent": "soncas-argent",
        "sympathie": "soncas-sympathie",
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
              <p style='font-size:.8rem;color:#267371;margin-bottom:8px'>{lever['desc']}</p>
              <ul style='padding-left:14px;margin:0'>{args_html}</ul>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Objections SONCAS & réponses**")
    for key, lever in soncas.items():
        with st.expander(f"{lever['icon']} **{lever['label']}** — *\"{lever['objection']}\"*"):
            st.success(f"**Réponse recommandée :**\n\n{lever['reponse']}")

    # SEGMENTATION RFM
    st.markdown('<div class="section-h">Segmentation RFM — 4 segments clients</div>', unsafe_allow_html=True)
    st.caption("Segmentation Récence · Fréquence · Montant — identifiez où concentrer vos efforts de rétention et d'acquisition")
    _rfm_segments = gen_rfm_segments(activity, monthly_budget)
    _rfm_cols = st.columns(4)
    _rfm_colors = ["#267371","#393DAC","#44C1BA","#B83D4B"]
    for _ri, (_rseg, _rcol) in enumerate(zip(_rfm_segments, _rfm_cols)):
        with _rcol:
            _rcolor = _rfm_colors[_ri]
            st.markdown(f"""
            <div class="rfm-card" style="border-top:3px solid {_rcolor}">
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#339999;margin-bottom:3px">{_rseg['pourcentage']}% des clients</div>
              <div style="font-weight:800;font-size:.95rem;color:{_rcolor};margin-bottom:4px">{_html.escape(_rseg['nom'])}</div>
              <div style="font-size:.76rem;color:#267371;margin-bottom:8px;line-height:1.4">{_html.escape(_rseg['description'])}</div>
              <div style="font-size:.72rem;font-weight:700;color:#0B2221">CLV estimée : {_rseg['clv']:,} €</div>
            </div>
            """, unsafe_allow_html=True)
    for _rseg in _rfm_segments:
        with st.expander(f"**{_rseg['nom']}** — actions recommandées"):
            for _ract in _rseg["actions"]:
                st.markdown(f"→ {_html.escape(_ract)}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — COPYWRITING
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-h">Structure AIDA — Copywriting persuasif</div>', unsafe_allow_html=True)
    st.caption("Le copywriting fusionne sciences comportementales et rédaction persuasive pour déclencher l'action")
    aida_meta = {
        "attention": ("","ATTENTION","aida-attention"),
        "interest": ("","INTÉRÊT","aida-interest"),
        "desire": ("","DÉSIR","aida-desire"),
        "action": ("","ACTION","aida-action"),
    }
    c1, c2 = st.columns(2)
    for i, (step, content) in enumerate(aida.items()):
        _icon_e, label, css = aida_meta.get(step, ("", step.upper(), ""))
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(f"""
            <div class="card {css}">
              <div class="card-title">{label}</div>
              <p style='font-weight:600;font-size:.9rem;color:#0B2221'>{content['p']}</p>
              <div style='background:rgba(255,255,255,.7);border-radius:10px;padding:10px;margin:10px 0'>
                <small style='color:#339999;font-weight:600'>EXEMPLE :</small>
                <p style='font-style:italic;font-size:.85rem;color:#267371;margin:4px 0'>"{content['e']}"</p>
              </div>
              <small style='color:#339999;font-weight:600'>FORMULES :</small>
              {"".join(f"<p style='font-size:.8rem;color:#267371;margin:2px 0'>→ {f}</p>" for f in content['f'])}
              <div style='background:rgba(255,255,255,.5);border-radius:8px;padding:8px;margin-top:8px'>
                <small style='color:#339999'> {content['c']}</small>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-h">Principes universels du copywriting</div>', unsafe_allow_html=True)
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
            st.markdown(f'<div class="metric-box"><div class="val" style="color:#44C1BA">{num}</div><div class="lbl" style="white-space:pre-line;line-height:1.3">{pr}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-h">Déclencheurs psychologiques</div>', unsafe_allow_html=True)
    st.caption("Leviers cognitifs issus des sciences comportementales qui guident la décision d'achat")
    for name, defn, ex, usage, warn in _TRIGGERS:
        with st.expander(f"**{name}**"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Définition** : {defn}")
                st.info(f'*"{ex}"*')
            with c2:
                st.success(f"**Quand l'utiliser** : {usage}")
                st.warning(warn)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — VENTE & SPIN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-h">Scripts de vente adaptés</div>', unsafe_allow_html=True)
    type_labels = {"cold_call":"Appel à froid","follow_up":"Suivi","discovery":"Découverte","email_followup":" Email suivi","email_outreach":"Email prospection"}
    for script in scripts:
        lbl = type_labels.get(script["type"], script["type"])
        with st.expander(f"**{script['title']}** — {lbl}"):
            st.code(script["content"], language=None)
            if script.get("keyPoints"):
                st.markdown("**Points clés :**")
                for kp in script["keyPoints"]: st.markdown(f"• {kp}")

    # SPIN
    st.markdown('<div class="section-h">SPIN Selling — Questions stratégiques</div>', unsafe_allow_html=True)
    st.caption("Méthodologie SPIN : Situation → Problème → Implication → Need-payoff. La plus efficace en B2B complexe.")
    spin_tabs = st.tabs(["Situation","Problème","Implication","Need-payoff"])
    spin_keys = [("situation","Établir le contexte sans interroger — montrez que vous avez fait vos recherches"),
                 ("probleme","Identifier les douleurs précises — ne proposez pas de solution encore"),
                 ("implication","Amplifier la conséquence du problème — le client doit ressentir l'urgence"),
                 ("besoin","Faire formuler le besoin par le client lui-même — la vente devient son idée")]
    for spin_tab, (sk, hint) in zip(spin_tabs, spin_keys):
        with spin_tab:
            st.caption(f"{hint}")
            for q in spin_data.get(sk, []):
                st.markdown(f"→ {q}")

    # Challenger
    st.markdown('<div class="section-h">Challenger Sale — Vendre par la conviction</div>', unsafe_allow_html=True)
    st.caption("La méthode Challenger s'appuie sur 3 piliers : Enseigner · Adapter · Prendre le contrôle")
    chal_tabs = st.tabs(["Enseigner (Teach)","Adapter (Tailor)","Prendre le contrôle"])
    chal_keys = ["teach","tailor","take_control"]
    for ctab, ckey in zip(chal_tabs, chal_keys):
        with ctab:
            for tip in _CHALLENGER[ckey]:
                st.markdown(f"• {tip}")

    # Objections
    st.markdown('<div class="section-h">Gestion des objections</div>', unsafe_allow_html=True)
    for obj, response in _OBJECTIONS:
        with st.expander(f'*"{obj}"*'):
            st.markdown(response)

    # NÉGOCIATION
    st.markdown('<div class="section-h">Tactiques de négociation — BATNA / ZOPA / SONCAS</div>', unsafe_allow_html=True)
    st.caption("Préparez chaque négociation avec une stratégie BATNA, une zone d'accord et des tactiques testées")
    _nego = gen_negociation(activity, monthly_budget)
    _nc1, _nc2 = st.columns(2)
    with _nc1:
        st.markdown("**BATNA (Meilleure Alternative)**")
        st.info(f"**Votre BATNA :** {_html.escape(_nego['batna']['vendeur'])}")
        st.warning(f"**BATNA adverse :** {_html.escape(_nego['batna']['acheteur'])}")
        st.caption(_nego['batna']['conseil'])
    with _nc2:
        st.markdown("**ZOPA (Zone d'accord)**")
        st.success(f"**Min :** {_nego['zopa']['min']:,} € | **Max :** {_nego['zopa']['max']:,} € | **Amplitude :** {_nego['zopa']['amplitude']}%")
        st.caption(_nego['zopa']['conseil'])
    st.markdown("**Règles de concession :**")
    for _nc in _nego["concessions"]:
        st.markdown(f"• {_html.escape(_nc)}")
    st.markdown("**Tactiques de négociation :**")
    for _nt in _nego["tactiques"]:
        st.markdown(f"→ {_html.escape(_nt)}")
    st.markdown("**Objections prix & réponses :**")
    for _obj, _rep in _nego["objections_prix"]:
        with st.expander(f'*"{_html.escape(_obj)}"*'):
            st.success(_html.escape(_rep))

    # PRIX PSYCHOLOGIQUES
    st.markdown('<div class="section-h">Prix psychologiques — 7 techniques</div>', unsafe_allow_html=True)
    st.caption("Techniques de tarification issues des sciences comportementales — augmentez la valeur perçue sans changer votre produit")
    _prix_list = gen_prix_psychologiques(monthly_budget, activity)
    _impact_badge = {"Très élevé": "badge-red", "Élevé": "badge-teal", "Moyen": "badge-jade"}
    for _ptec in _prix_list:
        with st.expander(f"**{_ptec['nom']}** — Impact : {_ptec['impact']}"):
            _c1p, _c2p = st.columns([2, 1])
            with _c1p:
                st.markdown(f"**Description :** {_html.escape(_ptec['description'])}")
                st.info(f"**Exemple :** {_html.escape(_ptec['exemple'])}")
            with _c2p:
                _ibadge = _impact_badge.get(_ptec["impact"], "badge-gray")
                st.markdown(f'<div style="text-align:center;padding:16px"><span class="badge {_ibadge}" style="font-size:.8rem;padding:4px 12px">{_html.escape(_ptec["impact"])}</span><div style="font-size:.72rem;color:#339999;margin-top:6px">Impact conversion</div></div>', unsafe_allow_html=True)

    # Email templates
    st.markdown('<div class="section-h">Templates emails de prospection</div>', unsafe_allow_html=True)
    email_tmpls = [
        ("Email cold outreach — signal d'actualité","Objet : [Prénom], [résultat en 5 mots]\n\nBonjour [Prénom],\n\nJ'ai vu que [signal d'actualité de l'entreprise].\n\nOn a aidé [client similaire] à [résultat mesurable] en [délai].\n\nDisponible 15 min cette semaine pour voir si on peut faire pareil pour [Entreprise] ?\n\n[Prénom]"),
        ("Email suivi J+3 (non-réponse)","Objet : Re: [sujet précédent]\n\nBonjour [Prénom],\n\nJe me permets de revenir vers vous suite à mon message de l'autre jour.\n\nJe sais que vous êtes très occupé — une seule question : est-ce que [problème que vous résolvez] est encore d'actualité pour vous ?\n\nSi oui, 15 minutes suffisent pour voir si je peux vous aider. Sinon, dites-le moi et je ne vous recontacte plus.\n\n[Prénom]"),
        ("Email post-démo — prochaines étapes","Objet : Suite à notre échange — prochaines étapes\n\nBonjour [Prénom],\n\nMerci pour notre échange — c'était très intéressant de comprendre [problème identifié].\n\nComme convenu, voici ce que je vous propose :\n• [Offre adaptée à leur situation]\n• [Prix / modalités]\n• [Garantie ou condition de démarrage]\n\nPour avancer, la prochaine étape est [action concrète].\n\nEst-ce que [date] vous conviendrait pour [prochaine étape] ?\n\n[Prénom]"),
    ]
    for title, body in email_tmpls:
        with st.expander(f" **{title}**"):
            st.code(body, language=None)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — MARKETING
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-h">Plateformes recommandées</div>', unsafe_allow_html=True)
    prio_badge = {"haute":"badge-red","moyenne":"badge-teal","faible":"badge-jade"}
    pf_cols = st.columns(min(len(platforms), 3))
    for i, (name, prio, freq, content_types) in enumerate(platforms):
        with pf_cols[i % 3]:
            badge = prio_badge.get(prio.strip().lower(), "badge-gray")
            st.markdown(f"""
            <div class="card">
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>
                <b style='font-size:.95rem'>{name}</b>
                <span class="badge {badge}">{prio}</span>
              </div>
              <small style='color:#339999'> {freq}</small>
              <p style='font-size:.8rem;color:#267371;margin-top:6px'>{content_types}</p>
            </div>""", unsafe_allow_html=True)

    # Budget adaptatif
    st.markdown(f'<div class="section-h">Répartition budgétaire — {monthly_budget:,} €/mois</div>', unsafe_allow_html=True)
    bar_colors = ["#0B2221","#44C1BA","#267371","#393DAC"]
    for i, (cat, pct, amt) in enumerate(budget_alloc):
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.markdown(f"**{cat}**")
        c2.markdown(f"**{amt:,.0f} €**")
        c3.markdown(f"*{pct}%*")
        st.markdown(f"""
        <div style="height:8px;background:#F2ECD9;border-radius:4px;margin-bottom:12px">
          <div style="height:8px;width:{pct}%;background:{bar_colors[i%4]};border-radius:4px;transition:width .4s ease"></div>
        </div>""", unsafe_allow_html=True)

    # Recommandations budget
    st.markdown('<div class="section-h">Recommandations adaptées à votre budget</div>', unsafe_allow_html=True)
    for reco in budget_reco:
        if reco.startswith(""):
            st.success(reco)
        elif reco.startswith(""):
            st.warning(reco)
        else:
            st.info(reco)

    # Calendrier éditorial
    st.markdown('<div class="section-h">Calendrier éditorial — 8 semaines</div>', unsafe_allow_html=True)
    cal_html = '<table class="bizi-table"><thead><tr><th>Sem.</th><th>Plateforme</th><th>Sujet</th><th>Format</th></tr></thead><tbody>'
    for week, platform, topic, fmt in calendar:
        cal_html += f"<tr><td><b>S{week}</b></td><td><span class='badge badge-blue'>{platform}</span></td><td style='font-size:.82rem'>{topic}</td><td style='font-size:.82rem;color:#339999'>{fmt}</td></tr>"
    cal_html += "</tbody></table>"
    st.markdown(f'<div style="overflow-x:auto">'+ cal_html +'</div>', unsafe_allow_html=True)

    # Règle 80/20
    st.markdown('<div class="section-h">Règle 80/20 — Focus d\'action</div>', unsafe_allow_html=True)
    rules_8020 = {
        "awareness": ["Créez votre contenu pilier avant de penser à la pub","LinkedIn ou Instagram en organic — maîtrisez 1 canal à fond","La newsletter est votre actif le plus précieux — commencez maintenant"],
        "sales": ["Le retargeting génère 10x plus que la prospection froide — commencez par ça","L'email marketing a un ROI de 42:1 — c'est votre canal le plus rentable","Optimisez votre page de vente avant d'augmenter votre budget pub"],
        "leads": ["Un bon lead magnet vaut 6 mois de pub payante — investissez dedans","La séquence email post-lead est plus importante que le lead magnet lui-même","Votre formulaire de contact est trop long — réduisez à 3 champs maximum"],
        "traffic": ["Le SEO prend 3-6 mois — commencez MAINTENANT pour des résultats en milieu d'année","2 articles SEO/semaine > 10 posts sociaux/semaine","Les backlinks sont rois — 1 bon backlink vaut 100 mentions sur les réseaux"],
    }
    for i, r in enumerate(rules_8020.get(goal, rules_8020["awareness"])):
        st.markdown(f"**{i+1}.** {r}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — CAMPAGNES PUB
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('''
    <div style="background:linear-gradient(135deg,#44C1BA,#44C1BA);color:white;border-radius:14px;
      padding:18px 24px;margin-bottom:20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <span style="font-size:2rem"></span>
      <div>
        <b style="font-size:1rem">Plan média personnalisé — {budget} €/mois</b><br>
        <span style="opacity:.9;font-size:.85rem">Répartition optimale Facebook · Google Ads · Email · SEO organique</span>
      </div>
    </div>
    '''.format(budget=monthly_budget), unsafe_allow_html=True)

    # Media Plan Table
    st.markdown('<div class="section-h">Plan Média Global</div>', unsafe_allow_html=True)
    mp_html = '<table class="bizi-table"><thead><tr><th>Canal</th><th>Budget</th><th>Portée estimée</th><th>CTR cible</th><th>ROI estimé</th></tr></thead><tbody>'
    for row in ads_data["mediaplan"]:
        mp_html += f"""<tr>
          <td><b>{row['platform']}</b></td>
          <td style='font-weight:700;color:#44C1BA'>{row['budget']:,.0f} €</td>
          <td style='font-size:.82rem'>{row['reach']}</td>
          <td><span class='badge badge-jade'>{row['ctr']}</span></td>
          <td><span class='badge badge-teal'>{row['roi']}</span></td>
        </tr>"""
    mp_html += '</tbody></table>'
    st.markdown(f'<div style="overflow-x:auto">'+ mp_html +'</div>', unsafe_allow_html=True)

    # Facebook Campaigns
    if ads_data["facebook"]:
        st.markdown('<div class="section-h">Campagnes Facebook / Instagram Ads</div>', unsafe_allow_html=True)
        for camp in ads_data["facebook"]:
            with st.expander(f"**{camp['name']}** — {camp['objective']} — Budget : {camp['budget']:,} €"):
                st.markdown(f"**Format recommandé :** {camp['format']}")
                for cr in camp.get("creatives", []):
                    st.markdown(f"""
                    <div class="card" style="margin-bottom:8px">
                      <div style="display:flex;justify-content:space-between;align-items:center">
                        <span class="badge badge-blue">{cr['format']}</span>
                        <span class="badge badge-gray">{cr.get('audience','')}</span>
                      </div>
                      <p style="font-weight:600;margin:8px 0 4px">{cr['headline']}</p>
                      <p style="font-size:.82rem;color:#339999">CTA : <b>{cr['cta']}</b></p>
                    </div>""", unsafe_allow_html=True)
    else:
        st.info("Budget insuffisant pour les campagnes Facebook (minimum recommandé : 30€/mois)")

    # Google Campaigns
    if ads_data["google"]:
        st.markdown('<div class="section-h">Campagnes Google Ads</div>', unsafe_allow_html=True)
        for camp in ads_data["google"]:
            with st.expander(f"**{camp['name']}** — {camp['type']} — Budget : {camp['budget']:,} €"):
                st.markdown("**Mots-clés recommandés :**")
                for kw in camp["keywords"]:
                    st.markdown(f"• `{kw}`")
    else:
        st.info("Budget insuffisant pour Google Ads (minimum recommandé : 30€/mois)")

    # Organic strategies
    st.markdown('<div class="section-h">Stratégies Organiques (Gratuites)</div>', unsafe_allow_html=True)
    for strat in ads_data["organic"]:
        with st.expander(f"**{strat['channel']}** — {strat['frequency']}"):
            st.markdown(f"*{strat['tactic']}*")
            st.markdown("**Actions concrètes :**")
            for ex in strat["examples"]:
                st.markdown(f"→ {ex}")

    # ROI Projection
    st.markdown('<div class="section-h">Projection ROI — 12 mois</div>', unsafe_allow_html=True)
    st.caption("Estimation basée sur votre budget, votre secteur et votre maturité. Scénarios : pessimiste · réaliste · optimiste")
    if roi_data:
        col_p, col_r, col_o = st.columns(3)
        last = roi_data[-1]
        col_p.markdown(f'<div class="metric-box"><div class="val" style="color:#B83D4B">{last["pessimiste"]:,} €</div><div class="lbl">Pessimiste (12 mois)</div></div>', unsafe_allow_html=True)
        col_r.markdown(f'<div class="metric-box"><div class="val" style="color:#44C1BA">{last["realiste"]:,} €</div><div class="lbl">Réaliste (12 mois)</div></div>', unsafe_allow_html=True)
        col_o.markdown(f'<div class="metric-box"><div class="val" style="color:#267371">{last["optimiste"]:,} €</div><div class="lbl">Optimiste (12 mois)</div></div>', unsafe_allow_html=True)
        # Mini tableau mensuel
        st.markdown("<br>", unsafe_allow_html=True)
        roi_html = '<table class="bizi-table"><thead><tr><th>Mois</th><th style="color:#B83D4B">Pessimiste</th><th style="color:#44C1BA">Réaliste</th><th style="color:#267371">Optimiste</th></tr></thead><tbody>'
        for r in roi_data:
            roi_html += f"<tr><td><b>M{r['month']}</b></td><td>{r['pessimiste']:,} €</td><td><b>{r['realiste']:,} €</b></td><td>{r['optimiste']:,} €</td></tr>"
        roi_html += '</tbody></table>'
        st.markdown(f'<div style="overflow-x:auto">'+ roi_html +'</div>', unsafe_allow_html=True)
    
    # PageSpeed
    if pagespeed_data:
        st.markdown('<div class="section-h">Audit PageSpeed — Performance site</div>', unsafe_allow_html=True)
        if pagespeed_data.get("source") == "mock":
            st.caption("Données estimées (ajoutez votre clé PageSpeed API dans .streamlit/secrets.toml pour des données réelles)")
        ps_cols = st.columns(4)
        scores = [
            ("Performance", pagespeed_data.get("performance",0)),
            ("SEO technique", pagespeed_data.get("seo",0)),
            ("Accessibilité", pagespeed_data.get("accessibility",0)),
            ("Bonnes pratiques", pagespeed_data.get("bestPractices",0)),
        ]
        for col, (label, score) in zip(ps_cols, scores):
            color = "#267371" if score >= 80 else "#44C1BA" if score >= 60 else "#B83D4B"
            with col:
                st.markdown(f'<div class="metric-box"><div class="val" style="color:{color}">{score}/100</div><div class="lbl">{label}</div></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("LCP (Largest Contentful Paint)", pagespeed_data.get("lcp","N/A"), help="Doit être < 2.5s pour un bon score")
        c2.metric("CLS (Cumulative Layout Shift)", pagespeed_data.get("cls","N/A"), help="Doit être < 0.1 pour un bon score")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — SEO & GEO 2025
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:14px;
      padding:18px 24px;margin-bottom:20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <span style="font-size:2rem"></span>
      <div>
        <b style="font-size:1rem">GEO 2025 — Generative Engine Optimization</b><br>
        <span style="opacity:.85;font-size:.85rem">39% des Français utilisent l'IA conversationnelle (2025) — optimisez maintenant pour les moteurs IA</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Keywords
    st.markdown('<div class="section-h">Mots-clés prioritaires</div>', unsafe_allow_html=True)
    diff_badge = {"Facile":"badge-jade","Moyen":"badge-teal","Élevé":"badge-red"}
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
    st.markdown(f'<div style="overflow-x:auto">'+ kw_html +'</div>', unsafe_allow_html=True)

    # Topics
    st.markdown('<div class="section-h">Autorité thématique — Contenus à créer</div>', unsafe_allow_html=True)
    for topic in geo["topics"]:
        st.markdown(f"{topic}")

    # Clusters
    st.markdown('<div class="section-h">Clusters de contenu</div>', unsafe_allow_html=True)
    for pilier, clusters in geo["clusters"]:
        with st.expander(f"**Pilier : {pilier}**"):
            for cl in clusters:
                st.markdown(f"&nbsp;&nbsp;&nbsp;→ {cl}")

    # GEO optimizations
    st.markdown('<div class="section-h">Optimisations GEO prioritaires</div>', unsafe_allow_html=True)
    for action, impact in geo["optims"]:
        c1, c2 = st.columns([5, 1])
        c1.markdown(f"• {action}")
        c2.markdown(impact)

    # AI tips
    st.markdown('<div class="section-h">Conseils pour les moteurs IA (ChatGPT, Perplexity, SGE)</div>', unsafe_allow_html=True)
    for tip in geo["tips"]:
        st.info(tip)

    # SEA IA
    st.markdown('<div class="section-h">SEA IA — Publicité pilotée par l\'IA (2025)</div>', unsafe_allow_html=True)
    sea_tabs = st.tabs([s[0].strip() for s in _SEA_IA])
    for sea_tab, (name, desc, advantages, conseil) in zip(sea_tabs, _SEA_IA):
        with sea_tab:
            st.markdown(f"**{desc}**")
            st.markdown("**Avantages clés :**")
            for av in advantages:
                st.markdown(f"{av}")
            st.info(f"**Conseil pratique :** {conseil}")

# ─────────────────────────────────────────────────────────────────────────────
# HELPER — KPI tiles renderer (DRY)
# ─────────────────────────────────────────────────────────────────────────────
def _render_kpi_section(kpi_list: list) -> None:
    """Affiche un groupe de KPI en grille 3 colonnes avec code couleur."""
    _tone_colors = {"sauge": "#C6ECD9", "ambre": "#C6ECD9", "neutral": "#F2ECD9"}
    _text_colors = {"sauge": "#267371", "ambre": "#44C1BA", "neutral": "#267371"}
    cols = st.columns(min(3, len(kpi_list)))
    for i, (label, value, hint, tone, target) in enumerate(kpi_list):
        bg = _tone_colors.get(tone, "#F2ECD9")
        tc = _text_colors.get(tone, "#267371")
        with cols[i % 3]:
            st.markdown(f"""
            <div class="kpi-tile" style="background:{bg};border-left:3px solid {tc}">
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:#339999">{_html.escape(label)}</div>
              <div style="font-size:1.6rem;font-weight:800;color:{tc};margin:4px 0">{_html.escape(value)}</div>
              <div style="font-size:.7rem;color:#339999">{_html.escape(hint)}</div>
              <div style="font-size:.7rem;color:{tc};margin-top:4px;font-weight:600"> Objectif : {_html.escape(target)}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — KPI DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-h">Dashboard KPI — Benchmarks 2025</div>', unsafe_allow_html=True)
    st.caption("Tous les indicateurs clés de performance avec leurs benchmarks sectoriels. Survolez les titres pour les définitions.")

    # Email KPIs
    st.markdown('<div class="section-h">Email Marketing</div>', unsafe_allow_html=True)
    _render_kpi_section(_KPI_BENCHMARKS["email"])

    st.markdown('<div class="section-h">Conversion & Satisfaction</div>', unsafe_allow_html=True)
    _render_kpi_section(_KPI_BENCHMARKS["conversion"])

    st.markdown('<div class="section-h">Réseaux sociaux & Croissance</div>', unsafe_allow_html=True)
    _render_kpi_section(_KPI_BENCHMARKS["social"])

    # OKR
    st.markdown('<div class="section-h">OKR — Objectifs & Key Results</div>', unsafe_allow_html=True)
    st.caption("La méthode OKR (Google, Intel, LinkedIn) aligne les équipes sur des objectifs ambitieux et mesurables")
    for j, okr in enumerate(okrs):
        with st.expander(f"**OKR {j+1}** — {okr['objective']}", expanded=(j==0)):
            st.markdown(f"**Objectif :** {okr['objective']}")
            st.markdown("**Key Results :**")
            for kr in okr["key_results"]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid #F2ECD9">
                  <div style="min-width:20px;height:20px;border-radius:50%;border:2px solid #44C1BA"></div>
                  <span style="font-size:.88rem">{kr}</span>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — SYNTHÈSE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    score = synthesis["score"]

    # Score ring
    st.markdown('<div class="section-h">Score de maturité stratégique</div>', unsafe_allow_html=True)
    c_score, c_kpis = st.columns([1, 3])
    with c_score:
        score_color = "#267371" if score >= 70 else "#44C1BA" if score >= 50 else "#B83D4B"
        st.markdown(f"""
        <div style="text-align:center;padding:20px 10px">
          <div class="score-ring" style="--pct:{score * 3.6:.0f}deg;background:conic-gradient({score_color} {score * 3.6:.0f}deg,#F2ECD9 0)">
            <span style="font-size:1.4rem;font-weight:800;color:#0B2221">{score}/100</span>
          </div>
          <p style='font-size:.82rem;color:#339999;margin-top:8px'>Score stratégique global</p>
          <span class="badge {'badge-jade'if score>=70 else 'badge-teal'if score>=50 else 'badge-red'}">
            {'Bon'if score>=70 else 'À améliorer'if score>=50 else 'Attention'}
          </span>
        </div>
        """, unsafe_allow_html=True)
    with c_kpis:
        st.markdown("**KPIs cibles**")
        kpi_cols = st.columns(3)
        for i, (label, val) in enumerate(synthesis["kpis"]):
            with kpi_cols[i % 3]:
                st.markdown(f'<div class="metric-box"><div class="val" style="font-size:1.1rem;color:#44C1BA">{val}</div><div class="lbl">{label}</div></div>', unsafe_allow_html=True)

    # Priorities
    st.markdown('<div class="section-h">Priorités d\'action</div>', unsafe_allow_html=True)
    priority_colors = ["#B83D4B","#44C1BA","#0B2221","#267371"]
    for i, p in enumerate(synthesis["priorities"]):
        color = priority_colors[i % 4]
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid #F2ECD9">
          <div style="min-width:28px;height:28px;border-radius:50%;background:{color};color:white;
            display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0">{i+1}</div>
          <p style="margin:0;font-size:.9rem;color:#267371;padding-top:4px">{p}</p>
        </div>""", unsafe_allow_html=True)

    # Roadmap
    st.markdown('<div class="section-h">Roadmap 180 jours</div>', unsafe_allow_html=True)
    rm_cols = st.columns(4)
    rm_colors = ["#0B2221","#267371","#44C1BA","#393DAC"]
    for i, (period, phase, actions) in enumerate(synthesis["roadmap"]):
        with rm_cols[i]:
            st.markdown(f"""
            <div class="card" style="border-top:3px solid {rm_colors[i]}">
              <div style='font-size:.68rem;color:#339999;font-weight:600;text-transform:uppercase;letter-spacing:.05em'>{period}</div>
              <div style='font-weight:700;font-size:.95rem;color:#0B2221;margin:4px 0'>{phase}</div>
              <p style='font-size:.78rem;color:#267371;margin:0'>{actions}</p>
            </div>""", unsafe_allow_html=True)

    # Export
    st.markdown('<div class="section-h">Export de l\'analyse complète</div>', unsafe_allow_html=True)
    export_data = {
        "generated_at": datetime.datetime.now().isoformat(),
        "version": "3.1",
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
            label="Télécharger JSON",
            data=json.dumps(export_data, ensure_ascii=False, indent=2, default=str),
            file_name=f"biziapp-analyse-{activity}-{goal}-{datetime.date.today()}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_dl2:
        # CSV simple des mots-clés
        csv_kw = "mot_cle,volume,difficulte,intention\n" + "\n".join(f'"{k}","{v}","{d}","{i}"'for k,v,d,i in keywords)
        st.download_button(
            label="Mots-clés CSV",
            data=csv_kw,
            file_name=f"biziapp-keywords-{activity}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    st.caption("JSON complet · compatible CRM, Notion, Google Sheets et tout éditeur de texte")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 9 — VEILLE STRATÉGIQUE & CONCURRENTIELLE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[9]:
    if comp_urls:
        _ck = "comp_" + str(abs(hash(tuple(sorted(comp_urls)))))
        if _ck not in st.session_state:
            with st.spinner("Analyse des concurrents…"):
                for _cu in comp_urls:
                    try:
                        comp_results[_cu] = scrape_competitor(_cu)
                    except Exception:
                        comp_results[_cu] = {"error": "Echec", "url": _cu}
            st.session_state[_ck] = dict(comp_results)
        else:
            comp_results.update(st.session_state[_ck])

    _main_q = (veille_keywords[0] if veille_keywords else "") or (
        {"ecommerce":"e-commerce","saas":"logiciel SaaS","service":"prestataire service","consulting":"consultant","content":"créateur contenu","other":"entreprise"}
        .get(activity,"stratégie")
    )
    _news_queries = []
    if veille_keywords:
        for _kw in veille_keywords[:4]:
            _news_queries.append(("Mot-clé", _kw))
    if comp_urls:
        for _cu in comp_urls[:2]:
            _dom = _cu.replace("https://","").replace("http://","").replace("www.","").split("/")[0]
            _news_queries.append(("Concurrent", _dom))
    if not _news_queries:
        _news_queries = [("Secteur", _main_q)]

    # ── Analyse URL live ──────────────────────────────────────────────────────
    st.markdown('<div class="section-h">Analyse URL en temps réel</div>', unsafe_allow_html=True)
    _lcol, _rcol = st.columns([4, 1])
    with _lcol:
        _live_url = st.text_input("URL à analyser", placeholder="https://monsite.fr ou https://concurrent.fr/page", label_visibility="collapsed", key="v_liveurl")
    with _rcol:
        _do_an = st.button("Analyser", type="primary", use_container_width=True, key="v_analyze_btn")

    _target = _live_url.strip()
    if _target:
        if not _target.startswith("http"):
            _target = "https://" + _target
        with st.spinner(f"Lecture de {_target.replace('https://','').replace('http://','').split('/')[0]} via Jina.ai…"):
            _ld = scrape_competitor(_target)
        if _ld.get("error") and not _ld.get("title"):
            st.error(f"Impossible d'analyser cette URL — {_html.escape(str(_ld.get('error',''))[:120])}")
        else:
            _lsrc = {"jina":"Jina.ai Reader","bs4":"BeautifulSoup"}.get(_ld.get("source",""),_ld.get("source",""))
            st.markdown(f"""
            <div class="card-dark">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap">
                <div style="flex:1;min-width:0">
                  <div style="font-size:.62rem;color:rgba(255,255,255,.45);text-transform:uppercase;letter-spacing:.07em;margin-bottom:5px">{_html.escape(_target.replace('https://','').replace('http://','').split('/')[0][:60])}</div>
                  <div style="font-size:1.1rem;font-weight:700;color:white;margin-bottom:6px;line-height:1.3">{_html.escape(str(_ld.get('title','—'))[:120])}</div>
                  <div style="font-size:.82rem;color:rgba(255,255,255,.65);line-height:1.5">{_html.escape(str(_ld.get('description',''))[:260])}</div>
                </div>
                <div style="text-align:right;font-size:.63rem;color:rgba(255,255,255,.35);line-height:1.7;flex-shrink:0">
                  Source : {_lsrc}<br>{_ld.get('fetched_at','')}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            _lk1,_lk2,_lk3,_lk4 = st.columns(4)
            _lk1.metric("H1",len(_ld.get("h1",[])))
            _lk2.metric("H2",len(_ld.get("h2",[])))
            _lk3.metric("Paragraphes",len(_ld.get("paragraphs",[])))
            _lk4.metric("Mots-clés",len(_ld.get("keywords",[])))
            if _ld.get("keywords"):
                st.markdown('<div class="section-h">Mots-clés détectés</div>', unsafe_allow_html=True)
                _kwh = "".join(f'<span class="url-kw" style="background:var(--teal-pale);color:#267371;margin:2px;display:inline-block;border-radius:4px;padding:2px 8px;font-size:.68rem;font-weight:600">{_html.escape(str(k)[:40])}</span>' for k in _ld["keywords"])
                st.markdown(f'<div style="margin-bottom:12px">{_kwh}</div>', unsafe_allow_html=True)
            _lca, _lcb = st.columns(2)
            with _lca:
                if _ld.get("h1"):
                    st.markdown('<div class="section-h">Structure H1</div>', unsafe_allow_html=True)
                    for _h in _ld["h1"]:
                        st.markdown(f'<div class="card" style="padding:9px 14px;font-weight:600;font-size:.87rem;margin-bottom:7px">{_html.escape(str(_h)[:110])}</div>', unsafe_allow_html=True)
                if _ld.get("h2"):
                    st.markdown('<div class="section-h">Structure H2</div>', unsafe_allow_html=True)
                    for _h in _ld["h2"][:7]:
                        st.markdown(f'<div style="padding:5px 12px;border-left:2px solid var(--teal);margin-bottom:5px;font-size:.83rem;color:#267371">{_html.escape(str(_h)[:110])}</div>', unsafe_allow_html=True)
            with _lcb:
                if _ld.get("paragraphs"):
                    st.markdown('<div class="section-h">Contenu principal</div>', unsafe_allow_html=True)
                    for _p in _ld["paragraphs"][:5]:
                        st.markdown(f'<div style="font-size:.82rem;color:#339999;line-height:1.6;padding:7px 0;border-bottom:1px solid #E4E9F6">{_html.escape(str(_p)[:300])}</div>', unsafe_allow_html=True)
    else:
        st.info("Entrez une URL ci-dessus pour lancer une analyse en temps réel — fonctionne avec n'importe quelle page publique")

    st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)

    # ── Veille concurrentielle ────────────────────────────────────────────────
    if comp_urls:
        st.markdown('<div class="section-h">Analyse concurrentielle</div>', unsafe_allow_html=True)
        _nc = min(len(comp_urls), 3)
        _gcols = st.columns(_nc)
        for _ci, _cu in enumerate(comp_urls):
            _cd = comp_results.get(_cu, {})
            with _gcols[_ci % _nc]:
                _dom = _cu.replace("https://","").replace("http://","").replace("www.","").split("/")[0]
                _herr = _cd.get("error") and not _cd.get("title")
                if _herr:
                    st.markdown(f'<div style="background:#F7FBF4;border:1px solid #C6ECD9;border-radius:10px;padding:14px;font-size:.82rem"><b style="color:#B83D4B">{_html.escape(_dom)}</b><br><span style="color:#B83D4B">{_html.escape(str(_cd.get("error","Erreur"))[:80])}</span></div>', unsafe_allow_html=True)
                else:
                    _ckws = "".join(f'<span style="background:#C6ECD9;color:#267371;border-radius:3px;padding:1px 6px;font-size:.62rem;font-weight:600;margin:1px;display:inline-block">{_html.escape(str(k)[:30])}</span>' for k in _cd.get("keywords",[])[:6])
                    st.markdown(f"""
                    <div class="card">
                      <div style="font-size:.68rem;color:var(--muted);font-family:monospace">{_html.escape(_dom)}</div>
                      <div style="font-weight:700;font-size:.9rem;color:#0B2221;margin:4px 0 6px">{_html.escape(str(_cd.get('title','—'))[:65])}</div>
                      <div style="font-size:.78rem;color:#339999;line-height:1.45;margin-bottom:8px">{_html.escape(str(_cd.get('description',''))[:160])}</div>
                      <div style="margin-bottom:6px">{_ckws}</div>
                      <div style="font-size:.68rem;color:#44C1BA">{len(_cd.get('h1',[]))+len(_cd.get('h2',[]))} titres · {len(_cd.get('paragraphs',[]))} §</div>
                    </div>
                    """, unsafe_allow_html=True)
        if len(comp_results) > 1:
            st.markdown('<div class="section-h">Tableau comparatif</div>', unsafe_allow_html=True)
            _rows = []
            for _cu, _cd in comp_results.items():
                _dom = _cu.replace("https://","").replace("http://","").replace("www.","").split("/")[0]
                _rows.append({
                    "Domaine": _dom,
                    "Titre": str(_cd.get("title","—"))[:60],
                    "Description": str(_cd.get("description","—"))[:100],
                    "H1 principal": ((_cd.get("h1") or ["—"])[0])[:55],
                    "Mots-clés": " · ".join((_cd.get("keywords") or [])[:4]) or "—",
                    "H2 count": len(_cd.get("h2",[])),
                })
            if _rows:
                st.dataframe(_rows, use_container_width=True, hide_index=True)
        for _ci2, (_cu2, _cd2) in enumerate(comp_results.items()):
            _dom2 = _cu2.replace("https://","").replace("http://","").replace("www.","").split("/")[0]
            with st.expander(f"**{_html.escape(_dom2)}** — analyse éditoriale complète", expanded=(_ci2==0)):
                if _cd2.get("h2"):
                    st.markdown("**Structure éditoriale (H2)**")
                    for _h2 in _cd2["h2"][:10]:
                        st.markdown(f"- {_html.escape(str(_h2)[:130])}")
                if _cd2.get("main_text"):
                    st.markdown("**Extrait du contenu**")
                    st.markdown(f'<div style="font-size:.82rem;color:#339999;line-height:1.65;background:#F9FAFB;padding:13px;border-radius:8px;border-left:3px solid var(--teal)">{_html.escape(str(_cd2["main_text"])[:900])}</div>', unsafe_allow_html=True)

    # ── Actualités marché ─────────────────────────────────────────────────────
    st.markdown('<div class="section-h">Flux actualités en temps réel</div>', unsafe_allow_html=True)
    for _ql, _qq in _news_queries[:5]:
        with st.expander(f"**{_ql}** · {_html.escape(_qq[:60])}", expanded=(_ql == _news_queries[0][0])):
            with st.spinner(f"Chargement actualités « {_qq[:40]} »…"):
                _news = fetch_news(_qq, lang=veille_lang, max_items=12)
            for _ni in _news:
                _nt = _html.escape(str(_ni.get("title",""))[:130])
                _ns = _html.escape(str(_ni.get("source",""))[:45])
                _np = _ni.get("pub","")
                _nl = _ni.get("link","")
                _src_h = f'<span style="background:#C6ECD9;color:#267371;padding:2px 7px;border-radius:4px;font-size:.63rem;font-weight:600;margin-right:6px">{_ns}</span>' if _ns else ""
                _link_h = f' <a href="{_html.escape(_nl)}" target="_blank" rel="noopener noreferrer" style="font-size:.68rem;color:#44C1BA;text-decoration:none">Lire &rarr;</a>' if _nl else ""
                st.markdown(f'<div style="border-left:3px solid var(--teal);padding:9px 13px;margin-bottom:8px;background:white;border-radius:0 8px 8px 0"><div style="font-weight:600;font-size:.87rem;color:#0B2221;margin-bottom:3px">{_nt}{_link_h}</div><div style="font-size:.7rem;color:#339999">{_src_h}{_np}</div></div>', unsafe_allow_html=True)

    # ── Signaux stratégiques ──────────────────────────────────────────────────
    st.markdown('<div class="section-h">Signaux stratégiques</div>', unsafe_allow_html=True)
    _wt = veille_keywords[0] if veille_keywords else _main_q
    _wc1, _wc2 = st.columns(2)
    with _wc1:
        st.markdown("**Contexte Wikipedia**")
        with st.spinner("Wikipedia…"):
            _wiki = fetch_wiki(_wt, lang=veille_lang)
        if _wiki.get("extract"):
            _wurl = f'<div style="margin-top:8px"><a href="{_html.escape(_wiki.get("url",""))}" target="_blank" rel="noopener noreferrer" style="font-size:.72rem;color:#44C1BA;text-decoration:none">Lire sur Wikipedia &rarr;</a></div>' if _wiki.get("url") else ""
            st.markdown(f'<div class="card"><div style="font-weight:700;font-size:.93rem;color:#0B2221;margin-bottom:6px">{_html.escape(str(_wiki.get("title",""))[:80])}</div><div style="font-size:.82rem;color:#339999;line-height:1.6">{_html.escape(str(_wiki.get("extract",""))[:650])}</div>{_wurl}</div>', unsafe_allow_html=True)
        else:
            st.info(f"Aucun article Wikipedia pour « {_html.escape(_wt[:50])} »")
    with _wc2:
        st.markdown("**Intelligence DuckDuckGo**")
        with st.spinner("DuckDuckGo…"):
            _ddg = fetch_ddg(_wt)
        if _ddg.get("abstract"):
            st.markdown(f'<div style="background:#C6ECD9;border:1px solid #44C1BA;border-radius:10px;padding:14px;font-size:.82rem;color:#0B2221;line-height:1.6">{_html.escape(str(_ddg["abstract"])[:550])}</div>', unsafe_allow_html=True)
        if _ddg.get("related"):
            st.markdown("**Sujets connexes**")
            for _rt in _ddg["related"][:5]:
                st.markdown(f'<div style="font-size:.8rem;color:#267371;padding:5px 0;border-bottom:1px solid #E4E9F6">{_html.escape(str(_rt)[:160])}</div>', unsafe_allow_html=True)

    # ── SWOT live ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-h">Détection automatique Opportunités / Menaces</div>', unsafe_allow_html=True)
    st.caption("Analyse sémantique des actualités en temps réel")
    _opp_w = ["croissance","opportunité","innovation","lancement","expansion","partenariat","financement","investissement","hausse","boom","tendance","accélération","record"]
    _thr_w = ["crise","risque","baisse","pénurie","réglementation","sanction","fraude","concurrent","récession","inflation","perte","fermeture","licenciement","chute","amende"]
    with st.spinner("Analyse des signaux marché…"):
        _all_news = fetch_news(_main_q + " marché", lang=veille_lang, max_items=25)
    _opps = [n for n in _all_news if any(s in n.get("title","").lower() for s in _opp_w)]
    _thrs = [n for n in _all_news if any(s in n.get("title","").lower() for s in _thr_w)]
    _oc, _tc = st.columns(2)
    with _oc:
        st.markdown(f'<div style="font-weight:700;font-size:.87rem;color:#0B2221;margin-bottom:9px">Opportunités ({len(_opps)})</div>', unsafe_allow_html=True)
        if _opps:
            for _on in _opps[:5]:
                st.markdown(f'<div style="background:#C6ECD9;border:1px solid #C6ECD9;border-radius:8px;padding:8px 12px;margin-bottom:6px;font-size:.8rem;line-height:1.4">{_html.escape(str(_on.get("title",""))[:130])}<div style="font-size:.68rem;color:#44C1BA;margin-top:2px">{_on.get("pub","")}</div></div>', unsafe_allow_html=True)
        else:
            st.caption("Aucune opportunité détectée dans les actualités récentes")
    with _tc:
        st.markdown(f'<div style="font-weight:700;font-size:.87rem;color:#B83D4B;margin-bottom:9px">Menaces ({len(_thrs)})</div>', unsafe_allow_html=True)
        if _thrs:
            for _tn in _thrs[:5]:
                st.markdown(f'<div style="background:#F7FBF4;border:1px solid #C6ECD9;border-radius:8px;padding:8px 12px;margin-bottom:6px;font-size:.8rem;line-height:1.4">{_html.escape(str(_tn.get("title",""))[:130])}<div style="font-size:.68rem;color:#B83D4B;margin-top:2px">{_tn.get("pub","")}</div></div>', unsafe_allow_html=True)
        else:
            st.caption("Aucune menace détectée dans les actualités récentes")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 10 — RSE & ISO 26000
# ══════════════════════════════════════════════════════════════════════════════
with tabs[10]:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:14px;
      padding:18px 24px;margin-bottom:20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <div>
        <b style="font-size:1rem">RSE & ISO 26000 — Responsabilite Societale des Entreprises</b><br>
        <span style="opacity:.85;font-size:.85rem">7 domaines d'action · Normes ISO 26000 · Pacte Mondial ONU · Loi AGEC · CSRD 2025</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    _rse_data = gen_rse(activity)
    _rse_score_total = sum(v["niveau"] for v in _rse_data.values())
    _rse_score_max = len(_rse_data) * 5
    _rse_score_pct = round(_rse_score_total / _rse_score_max * 100)

    _rs1, _rs2, _rs3 = st.columns(3)
    _rs1.markdown(f'<div class="metric-box"><div class="val" style="color:#267371">{_rse_score_pct}/100</div><div class="lbl">Score RSE global</div></div>', unsafe_allow_html=True)
    _rs2.markdown(f'<div class="metric-box"><div class="val" style="color:#393DAC">{len(_rse_data)}</div><div class="lbl">Domaines ISO 26000</div></div>', unsafe_allow_html=True)
    _rse_label = "Leader RSE" if _rse_score_pct >= 70 else "En transition" if _rse_score_pct >= 50 else "Rattrapage nécessaire"
    _rs3.markdown(f'<div class="metric-box"><div class="val" style="font-size:1rem;color:#44C1BA">{_rse_label}</div><div class="lbl">Niveau de maturité</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-h">Les 7 domaines ISO 26000</div>', unsafe_allow_html=True)
    for _dom, _ddata in _rse_data.items():
        _niveau = _ddata["niveau"]
        _bar_filled = "█" * _niveau
        _bar_empty = "░" * (5 - _niveau)
        _ncolor = "#267371" if _niveau >= 4 else "#44C1BA" if _niveau >= 3 else "#B83D4B"
        with st.expander(f"**{_dom}** — Niveau {_niveau}/5 {_bar_filled}{_bar_empty}"):
            _dc1, _dc2 = st.columns([3, 2])
            with _dc1:
                st.markdown("**Actions recommandées :**")
                for _act in _ddata["actions"]:
                    st.markdown(f"""
                    <div class="rse-card">
                      <div style="font-size:.84rem;color:#0B2221">{_html.escape(_act)}</div>
                    </div>
                    """, unsafe_allow_html=True)
            with _dc2:
                st.markdown("**Risque si inaction :**")
                st.warning(_html.escape(_ddata["risques"]))
                st.markdown(f'<div style="margin-top:10px"><div class="progress-bar"><div class="progress-fill" style="width:{_niveau*20}%;background:{_ncolor}"></div></div><div style="font-size:.7rem;color:#339999;margin-top:3px">Maturité : {_niveau}/5</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-h">Cadre légal et normatif applicable</div>', unsafe_allow_html=True)
    _normes = [
        ("ISO 26000", "Lignes directrices RSE — référentiel international non certifiable mais reconnu"),
        ("Pacte Mondial ONU", "10 principes sur les droits humains, travail, environnement et anti-corruption"),
        ("Loi Grenelle II", "Obligation de reporting extra-financier pour les entreprises françaises"),
        ("Loi AGEC", "Economie circulaire — emballages durables, réparation, information consommateurs"),
        ("CSRD 2025", "Corporate Sustainability Reporting Directive — reporting obligatoire ESG UE"),
        ("RGPD", "Protection des données personnelles — conformité obligatoire depuis 2018"),
    ]
    for _nl, _nd in _normes:
        st.markdown(f"""
        <div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #F2ECD9;align-items:flex-start">
          <span class="badge badge-jade" style="flex-shrink:0">{_html.escape(_nl)}</span>
          <span style="font-size:.84rem;color:#267371">{_html.escape(_nd)}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-h">Plan d\'action RSE 90 jours</div>', unsafe_allow_html=True)
    _rse_roadmap = [
        ("J1-J30", "Diagnostic", "Réaliser un bilan carbone simplifié · Rédiger la charte RSE · Identifier les parties prenantes clés"),
        ("J31-J60", "Engagement", "Choisir 2-3 domaines prioritaires · Définir des objectifs mesurables · Communiquer en interne"),
        ("J61-J90", "Action", "Lancer les premières actions concrètes · Mesurer les résultats · Préparer la communication externe"),
    ]
    _rr_cols = st.columns(3)
    for _ri, (_per, _ph, _ac) in enumerate(_rse_roadmap):
        with _rr_cols[_ri]:
            st.markdown(f"""
            <div class="card" style="border-top:3px solid #267371">
              <div style="font-size:.68rem;color:#339999;font-weight:600;text-transform:uppercase">{_per}</div>
              <div style="font-weight:700;font-size:.92rem;color:#0B2221;margin:4px 0">{_ph}</div>
              <p style="font-size:.78rem;color:#267371;margin:0">{_ac}</p>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#339999;font-size:.78rem;padding:12px 0">
  <b style="color:#0B2221">BiziApp v3.1</b> — Stratégie 360° · SWOT · QQOQCCP · PESTEL · SONCAS · AIDA · SPIN · Challenger · GEO 2025 · SEA IA · KPIs · OKR · Veille Live · RSE · RFM · BATNA · Prix psychologiques<br>
  <span style="color:#44C1BA">Analyse personnalisée · Données live · Cache intelligent · Lecture URL en direct · Veille concurrentielle · Actualités Google News · Wikipedia · DuckDuckGo</span><br>
  Données live via Jina.ai · Google News RSS · DuckDuckGo · Wikipedia REST · PageSpeed · Inputs validés &amp; sécurisés (XSS, SSRF, rate-limiting)
</div>
""", unsafe_allow_html=True)
