"""
GEO 2025 Service — Generative Engine Optimization + SEO Autorité Thématique.
En 2025, 39% des Français utilisent déjà l'IA conversationnelle au quotidien.
Python 3.9 compatible.
"""
import copy
from typing import Dict, List, Any


GEO_STAT_2025 = "39% des Français utilisent l'IA conversationnelle au quotidien (2025)"

# ─── Stratégie GEO par secteur ────────────────────────────────────────────────
GEO_STRATEGIES: Dict[str, Dict[str, Any]] = {
    "ecommerce": {
        "authority_topics": [
            "Guide ultime d'achat [produit phare] — le contenu pilier de référence",
            "Comparatif [produit A] vs [produit B] — contenu cluster haute valeur",
            "FAQ produits enrichie — capture les requêtes conversationnelles IA",
            "Avis clients structurés (schema Review) — utilisés par Google SGE",
        ],
        "content_clusters": [
            {"pilier": "Guide d'achat [niche]", "clusters": ["Comment choisir X", "Meilleur X pour Y", "X test & avis", "X prix comparatif"]},
            {"pilier": "Guide entretien / utilisation", "clusters": ["Comment utiliser X", "Erreurs à éviter avec X", "X durée de vie", "Tutoriel X"]},
        ],
        "geo_optimizations": [
            {"action": "Ajoutez des FAQ schema markup sur toutes vos fiches produit", "impact": "élevé"},
            {"action": "Répondez directement aux questions 'quel est le meilleur X pour Y' dans vos contenus", "impact": "élevé"},
            {"action": "Utilisez du langage naturel conversationnel dans vos descriptions", "impact": "moyen"},
            {"action": "Structurez vos avis en données structurées (schema Review)", "impact": "élevé"},
        ],
        "ai_search_tips": [
            "Google SGE et ChatGPT extraient des réponses directes — soyez la source citée",
            "Perplexity cite les sources — des backlinks de qualité restent essentiels",
            "Les requêtes vocales explosent — optimisez pour le langage parlé",
        ],
    },
    "saas": {
        "authority_topics": [
            "Guides pratiques ultra-complets sur les problèmes que votre outil résout",
            "Études de cas sectorielles avec métriques et ROI quantifiés",
            "Comparatifs objectifs avec vos concurrents (even-handed = crédibilité)",
            "Glossaire du secteur — topical authority signal fort pour Google",
        ],
        "content_clusters": [
            {"pilier": "Guide [fonctionnalité principale]", "clusters": ["Comment faire X sans outil", "X automatisation guide", "X pour les débutants", "X cas d'usage avancés"]},
            {"pilier": "Comparatif outils [catégorie]", "clusters": ["Vous vs Concurrent A", "Vous vs Concurrent B", "Meilleur outil X 2025", "Migrer de X vers vous"]},
        ],
        "geo_optimizations": [
            {"action": "Créez une documentation technique complète (boon for AI crawlers)", "impact": "élevé"},
            {"action": "Publiez des datasets ou benchmarks sectoriels citables par l'IA", "impact": "très élevé"},
            {"action": "Répondez aux questions 'comment [task] avec [catégorie d'outil]' exhaustivement", "impact": "élevé"},
            {"action": "Structurez vos how-to avec des étapes numérotées (schema HowTo)", "impact": "moyen"},
        ],
        "ai_search_tips": [
            "Les LLMs sont entraînés sur le web — votre contenu publié aujourd'hui formera les réponses de demain",
            "Soyez la ressource la plus citée de votre niche — qualité > quantité",
            "ChatGPT Plugins et Perplexity favoritent les sites avec API publique",
        ],
    },
    "service": {
        "authority_topics": [
            "Études de cas détaillées avant/après avec métriques précises",
            "Guides méthodologiques qui montrent votre expertise profonde",
            "Articles de fond sur les tendances de votre secteur",
            "Réponses aux questions que vos clients posent en consultation",
        ],
        "content_clusters": [
            {"pilier": "Guide [expertise principale]", "clusters": ["Introduction à X", "Les erreurs de X", "Avancé : maîtriser X", "X questions réponses"]},
            {"pilier": "Cas clients [secteur]", "clusters": ["Cas [secteur A]", "Cas [secteur B]", "Résultats chiffrés", "Témoignages"]},
        ],
        "geo_optimizations": [
            {"action": "Répondez exhaustivement aux 20 questions les plus fréquentes de vos clients", "impact": "élevé"},
            {"action": "Publiez des guides gratuits à haute valeur — les IA les citent comme référence", "impact": "élevé"},
            {"action": "Ajoutez votre expertise dans les forums sectoriels (Reddit, forums pros)", "impact": "moyen"},
            {"action": "Mettez à jour vos contenus régulièrement — les IA favorisent les contenus récents", "impact": "moyen"},
        ],
        "ai_search_tips": [
            "Google E-E-A-T (Experience, Expertise, Authoritativeness, Trust) est renforcé par l'IA",
            "Publiez sous votre vrai nom avec bio complète — l'authorité personnelle est valorisée",
            "Les contenus d'opinion et d'analyse profonde résistent mieux à la génération IA",
        ],
    },
}

_GENERIC_GEO: Dict[str, Any] = {
    "authority_topics": [
        "Contenus piliers ultra-complets sur votre thème principal",
        "Clusters de contenu répondant à toutes les questions de votre ICP",
        "FAQ structurée avec schema markup pour la capture des requêtes IA",
        "Études de cas et données sectorielles propriétaires",
    ],
    "content_clusters": [
        {"pilier": "Guide principal [thème]", "clusters": ["Introduction", "Niveau avancé", "Cas pratiques", "FAQ"]},
        {"pilier": "Solutions aux problèmes [cible]", "clusters": ["Problème A → solution", "Problème B → solution", "Comparatif solutions", "Erreurs à éviter"]},
    ],
    "geo_optimizations": [
        {"action": "Utilisez des questions naturelles comme sous-titres H2/H3", "impact": "élevé"},
        {"action": "Ajoutez un schema FAQ sur toutes vos pages clés", "impact": "élevé"},
        {"action": "Répondez directement et précisément en début de section (featured snippet)", "impact": "élevé"},
        {"action": "Créez du contenu E-E-A-T : Experience, Expertise, Authority, Trust", "impact": "très élevé"},
    ],
    "ai_search_tips": [
        "39% des Français utilisent l'IA conversationnelle — optimisez pour ces moteurs maintenant",
        "Les IA citent les sources qui répondent directement et exhaustivement aux questions",
        "L'intention de recherche prime sur le mot-clé exact — comprenez le 'pourquoi' de chaque requête",
    ],
}


# ─── SEA IA 2025 ───────────────────────────────────────────────────────────────
SEA_AI_STRATEGIES: Dict[str, Any] = {
    "google_ai_max": {
        "description": "Performance Max avec IA Max — Google optimise automatiquement sur tous ses canaux",
        "avantages": [
            "Diffusion automatique sur Search, Display, YouTube, Gmail, Maps, Shopping",
            "Optimisation en temps réel des enchères et audiences via ML",
            "Asset generation IA — génère des variantes de titres et descriptions",
        ],
        "quand_utiliser": "Dès que vous avez 30+ conversions/mois — en dessous, le ML manque de données",
        "conseil": "Fournissez des assets de qualité (images, vidéos, textes) — la qualité des inputs détermine la qualité des outputs IA",
    },
    "smart_bidding": {
        "description": "Stratégies d'enchères automatisées par Google ML pour maximiser les conversions",
        "strategies": [
            {"nom": "Target CPA", "usage": "Objectif coût par acquisition fixe — idéal si vous connaissez votre CPA cible"},
            {"nom": "Target ROAS", "usage": "Objectif retour sur dépenses publicitaires — pour e-commerce avec données de valeur"},
            {"nom": "Maximize Conversions", "usage": "Maximise le volume de conversions dans votre budget — démarrage campaign"},
            {"nom": "Enhanced CPC", "usage": "Manuel + ajustement IA — contrôle maximal avec aide ML — pour débutants"},
        ],
        "conseil": "Donnez au Smart Bidding 2-4 semaines d'apprentissage avant d'évaluer les performances",
    },
    "ai_overviews": {
        "description": "Google AI Overviews — réponses IA intégrées dans les résultats de recherche",
        "impact": "Les AI Overviews captent du trafic organique — mais les annonces SEA maintiennent leur position",
        "opportunites": [
            "Annonces textuelles dans les AI Overviews (beta 2025) — position premium visible",
            "Shopping ads dans les réponses IA pour les requêtes produits",
            "Position 0 : votre annonce affichée dans la synthèse IA de Google",
        ],
        "conseil": "Combinez SEA (paiement garanti) + SEO GEO (organique IA) pour une visibilité maximale",
    },
    "audience_signals": {
        "description": "Signaux d'audience pour guider l'IA vers vos meilleurs prospects",
        "types": [
            "Customer Match : uploadez vos emails clients pour trouver des similaires",
            "Similar Audiences basées sur vos convertisseurs",
            "In-Market Audiences : personas en phase d'achat active",
            "Custom Intent : audiences basées sur les recherches récentes",
        ],
        "conseil": "Plus vous fournissez de signaux de qualité, plus l'IA cible efficacement",
    },
}


def generate_geo_2025(activity_type: str, goal: str, website_url: str = "") -> Dict[str, Any]:
    """Génère la stratégie SEO/GEO 2025 complète."""
    geo = copy.deepcopy(GEO_STRATEGIES.get(activity_type, _GENERIC_GEO))
    has_website = bool(website_url and website_url.startswith("http"))

    return {
        "stat_2025": GEO_STAT_2025,
        "methodology_description": (
            "En SEO 2025, la priorité est donnée à l'autorité thématique via des contenus piliers "
            "et des clusters, à l'intention de recherche plutôt qu'aux mots-clés exacts, "
            "et à l'optimisation pour les moteurs de réponse IA (GEO)."
        ),
        "authority_topics": geo["authority_topics"],
        "content_clusters": geo["content_clusters"],
        "geo_optimizations": geo["geo_optimizations"],
        "ai_search_tips": geo["ai_search_tips"],
        "sea_ai": SEA_AI_STRATEGIES,
        "has_website": has_website,
        "priority_actions": _get_priority_actions(goal, has_website),
    }


def _get_priority_actions(goal: str, has_website: bool) -> List[str]:
    base = [
        "Créez un contenu pilier de 2000+ mots sur votre thème principal",
        "Construisez 5 contenus clusters autour de ce pilier",
        "Ajoutez le schema FAQ sur votre homepage et pages produit/service",
    ]
    if goal == "traffic":
        base.insert(0, "PRIORITÉ : Publiez 2 contenus/semaine minimum les 3 premiers mois")
    elif goal == "leads":
        base.insert(0, "PRIORITÉ : Optimisez vos pages pour les requêtes 'intention d'achat'")
    if not has_website:
        base.append("Sans site existant : créez d'abord votre base SEO (domaine, structure, contenu pilier)")
    return base
