"""
PESTEL + Micro-environnement + Analyse concurrentielle
Cartographie le macro et micro-environnement de l'entreprise.
Python 3.9 compatible.
"""
import copy
from typing import Dict, List, Any


# ─── PESTEL par secteur ────────────────────────────────────────────────────────
PESTEL_DATA: Dict[str, Dict[str, List[Dict[str, str]]]] = {
    "ecommerce": {
        "politique": [
            {"facteur": "Régulation TVA numérique UE (OSS)", "impact": "négatif", "note": "Complexité comptable accrue pour la vente transfrontalière"},
            {"facteur": "Normes RGPD & ePrivacy", "impact": "neutre", "note": "Contrainte mais aussi avantage concurrentiel si bien géré"},
        ],
        "economique": [
            {"facteur": "Inflation des coûts logistiques (+18% en 3 ans)", "impact": "négatif", "note": "Comprimez via négociation transporteur et stocks optimisés"},
            {"facteur": "Croissance e-commerce +12%/an en France", "impact": "positif", "note": "Marché en expansion — capturez la part de marché tôt"},
            {"facteur": "Pouvoir d'achat sous pression (2025)", "impact": "négatif", "note": "Renforcez votre proposition valeur/prix et offrez des options d'échelonnement"},
        ],
        "socioculturel": [
            {"facteur": "M-commerce : 68% des achats en ligne depuis mobile", "impact": "positif", "note": "Mobile-first est désormais non-négociable"},
            {"facteur": "Exigence RSE des consommateurs (+39% vs 2022)", "impact": "neutre", "note": "Levier différenciant si vous intégrez l'impact environnemental"},
        ],
        "technologique": [
            {"facteur": "IA générative dans les recommandations produits", "impact": "positif", "note": "Personnalisation accrue = +23% de conversion en moyenne"},
            {"facteur": "Moteurs de recherche IA (Google SGE, Perplexity)", "impact": "neutre", "note": "Adaptez votre SEO à l'intention de recherche IA (GEO)"},
        ],
        "ecologique": [
            {"facteur": "Emballages durables — obligation légale 2025", "impact": "neutre", "note": "Coût d'adaptation + avantage marketing si bien communiqué"},
            {"facteur": "Carbon score produit — attente consommateur", "impact": "neutre", "note": "Différenciateur potentiel sur marché premium"},
        ],
        "legal": [
            {"facteur": "Directive Omnibus — transparence des prix", "impact": "négatif", "note": "Obligation d'afficher le prix de référence avant promotion"},
            {"facteur": "Droit de rétractation 14 jours — coût retours", "impact": "négatif", "note": "Optimisez la logistique retour pour limiter l'impact financier"},
        ],
    },
    "saas": {
        "politique": [
            {"facteur": "AI Act européen (2024-2026)", "impact": "neutre", "note": "Contraintes sur les systèmes IA à haut risque — auditez votre conformité"},
            {"facteur": "Cloud Act US vs RGPD — souveraineté des données", "impact": "neutre", "note": "Hébergement EU peut devenir un avantage pour les clients corporate"},
        ],
        "economique": [
            {"facteur": "Compression des budgets SaaS (stack fatigue)", "impact": "négatif", "note": "ROI démontrable en <30 jours devient critère de survie"},
            {"facteur": "Valorisations SaaS stabilisées — retour à la rentabilité", "impact": "neutre", "note": "Investors cherchent profitabilité — montrez votre chemin vers le profit"},
        ],
        "socioculturel": [
            {"facteur": "Remote work permanent — outils collaboratifs essentiels", "impact": "positif", "note": "Intégrations Slack/Teams/Notion deviennent des fonctionnalités must-have"},
            {"facteur": "Adoption IA par les utilisateurs finaux (+67% en 2024)", "impact": "positif", "note": "Intégrez des fonctionnalités IA pour rester compétitif"},
        ],
        "technologique": [
            {"facteur": "LLMs open-source — commoditisation de l'IA", "impact": "neutre", "note": "L'IA seule ne suffit plus — l'avantage est dans les données propriétaires"},
            {"facteur": "API-first & intégrations — ecosystème Zapier/Make", "impact": "positif", "note": "Une bonne API multiplie votre reach sans effort commercial"},
        ],
        "ecologique": [
            {"facteur": "GreenOps — empreinte carbone des serveurs", "impact": "neutre", "note": "Hébergeurs green (OVH, Scaleway) deviennent un argument marketing B2B"},
        ],
        "legal": [
            {"facteur": "RGPD + DMA — obligations plateformes numériques", "impact": "neutre", "note": "Nommez un DPO et auditez votre collecte de données régulièrement"},
            {"facteur": "Protections IP — brevets logiciels limités en EU", "impact": "neutre", "note": "Protégez via marques déposées et trade secrets plutôt que brevets"},
        ],
    },
    "service": {
        "politique": [
            {"facteur": "Réforme du travail indépendant (statuts, cotisations)", "impact": "neutre", "note": "Suivez les évolutions micro-entrepreneur/portage salarial"},
        ],
        "economique": [
            {"facteur": "Inflation : revalorisation des TJM +8-12%", "impact": "positif", "note": "Moment favorable pour augmenter vos tarifs — communiquez la valeur ajoutée"},
            {"facteur": "Budget externalisé en hausse chez les ETI (+15%)", "impact": "positif", "note": "Les ETI externalisent de plus en plus — ciblez ce segment"},
        ],
        "socioculturel": [
            {"facteur": "Économie de l'expertise : montée du conseil spécialisé", "impact": "positif", "note": "Les clients paient premium pour l'expertise niche — spécialisez-vous"},
        ],
        "technologique": [
            {"facteur": "IA générative : automatisation partielle du conseil junior", "impact": "négatif", "note": "Montez en expertise — l'IA ne remplace pas le conseil stratégique senior"},
            {"facteur": "Outils no-code — réduction du recours aux prestataires tech", "impact": "négatif", "note": "Repositionnez-vous sur la stratégie et l'accompagnement, pas l'exécution"},
        ],
        "ecologique": [
            {"facteur": "Remote consulting — réduction empreinte carbone client", "impact": "positif", "note": "Argument RSE valorisable auprès des clients engagés"},
        ],
        "legal": [
            {"facteur": "Loi sur les délais de paiement (60 jours max)", "impact": "neutre", "note": "Protégez-vous avec des CGV solides et des acomptes systématiques"},
        ],
    },
}

_GENERIC_PESTEL: Dict[str, List[Dict[str, str]]] = {
    "politique": [
        {"facteur": "Réglementation sectorielle en évolution", "impact": "neutre", "note": "Suivez les évolutions législatives de votre secteur"},
    ],
    "economique": [
        {"facteur": "Contexte macro-économique incertain", "impact": "neutre", "note": "Anticipez les cycles et construisez une trésorerie de sécurité"},
        {"facteur": "Croissance du marché digital", "impact": "positif", "note": "Digitalisez votre offre pour capter cette croissance"},
    ],
    "socioculturel": [
        {"facteur": "Digitalisation accélérée des comportements", "impact": "positif", "note": "Votre présence digitale est désormais votre première vitrine"},
    ],
    "technologique": [
        {"facteur": "IA générative — opportunités de productivité", "impact": "positif", "note": "Intégrez des outils IA dans vos processus pour gagner en compétitivité"},
        {"facteur": "Cybersécurité — risques en hausse", "impact": "négatif", "note": "Investissez dans la sécurité de vos données et celles de vos clients"},
    ],
    "ecologique": [
        {"facteur": "Transition écologique — attente des parties prenantes", "impact": "neutre", "note": "Définissez votre politique RSE même à petite échelle"},
    ],
    "legal": [
        {"facteur": "RGPD & protection des données", "impact": "neutre", "note": "Assurez-vous de collecter uniquement les données nécessaires avec consentement"},
    ],
}


# ─── Micro-environnement ───────────────────────────────────────────────────────
MICRO_ENV_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "ecommerce": {
        "clients": {
            "pouvoir": "élevé",
            "description": "Hyperchoix sur le marché, faible coût de switching — exigence maximale",
            "levier": "Fidélisez via programme de fidélité, contenu exclusif et service irréprochable",
        },
        "fournisseurs": {
            "pouvoir": "moyen",
            "description": "Multiples sources possibles mais dépendance aux délais de livraison",
            "levier": "Diversifiez vos sources et stockez les SKU critiques",
        },
        "concurrents": {
            "pouvoir": "élevé",
            "description": "Amazon, Cdiscount, Pure Players niche — guerre des prix permanente",
            "levier": "Différenciez sur l'expérience, la niche et le contenu, pas sur le prix seul",
        },
        "intermediaires": {
            "pouvoir": "moyen",
            "description": "Marketplaces, comparateurs, influenceurs — dépendance aux algorithmes",
            "levier": "Développez votre canal direct (DTC) pour réduire les commissions tiers",
        },
    },
    "saas": {
        "clients": {
            "pouvoir": "élevé",
            "description": "Contrats annuels mais churn élevé si valeur non démontrée à J30",
            "levier": "Customer Success proactif + tableau de bord ROI intégré au produit",
        },
        "fournisseurs": {
            "pouvoir": "moyen",
            "description": "AWS/GCP/Azure — switching coûteux mais offres compétitives",
            "levier": "Architecture cloud-agnostic et réserves d'instances pour optimiser les coûts",
        },
        "concurrents": {
            "pouvoir": "très élevé",
            "description": "Marché SaaS ultra-compétitif, consolidation en cours (M&A)",
            "levier": "Hyper-spécialisation verticale + intégrations natives comme barrière à l'entrée",
        },
        "intermediaires": {
            "pouvoir": "faible",
            "description": "App stores (faible commission), intégrateurs (partenariats clés)",
            "levier": "Programme partenaires avec certifications et marges attractives pour intégrateurs",
        },
    },
}

_GENERIC_MICRO_ENV: Dict[str, Any] = {
    "clients": {
        "pouvoir": "élevé",
        "description": "Le digital donne aux clients un accès immédiat aux alternatives — leur pouvoir augmente",
        "levier": "Créez des barrières à la sortie : intégrations, données accumulées, communauté",
    },
    "fournisseurs": {
        "pouvoir": "moyen",
        "description": "Diversification des sources possible mais risque de dépendance sur les ressources clés",
        "levier": "Identifiez vos fournisseurs critiques et sécurisez des alternatives dès maintenant",
    },
    "concurrents": {
        "pouvoir": "élevé",
        "description": "La concurrence directe et indirecte s'intensifie dans tous les marchés digitaux",
        "levier": "Analysez systématiquement vos concurrents (pages, prix, avis) avec des outils comme Semrush",
    },
    "intermediaires": {
        "pouvoir": "moyen",
        "description": "Plateformes, comparateurs et distributeurs prélèvent une commission croissante",
        "levier": "Développez votre canal direct (site, newsletter, communauté) en parallèle",
    },
}


# ─── Analyse concurrentielle ───────────────────────────────────────────────────
COMPETITIVE_BY_SECTOR: Dict[str, Dict[str, Any]] = {
    "ecommerce": {
        "direct_rivals": ["Amazon / Cdiscount (généralistes)", "Pure Players de la niche", "Boutiques Shopify concurrentes"],
        "indirect_rivals": ["Leboncoin / Vinted (occasion)", "Grandes surfaces en ligne", "Marketplace B2B sectorielles"],
        "competitive_matrix": [
            {"critere": "Prix", "vous": "⚪", "leader": "🔴", "note": "Leaders tirent le prix vers le bas — différenciez-vous"},
            {"critere": "Expérience UX", "vous": "⚪", "leader": "🟢", "note": "Levier fort si vous investissez dans le design"},
            {"critere": "Catalogue produits", "vous": "⚪", "leader": "🔴", "note": "Ne tentez pas de rivaliser en volume — spécialisez"},
            {"critere": "SAV & fidélisation", "vous": "🟢", "leader": "⚪", "note": "Avantage structurel des petites structures — exploitez-le"},
            {"critere": "Contenu & SEO", "vous": "🟢", "leader": "⚪", "note": "Blog expert + UGC = trafic organique gratuit"},
        ],
        "positioning_opportunity": "Niche premium + contenu expert + communauté = triangle défendable",
        "moat": "Données clients propriétaires + brand community + niche expertise",
    },
    "saas": {
        "direct_rivals": ["Solutions VC-backed bien financées", "Outils intégrés (suites Microsoft/Google)", "Concurrents de niche similaires"],
        "indirect_rivals": ["Outils no-code (Notion, Airtable)", "Agences qui font manuellement", "Solutions open-source"],
        "competitive_matrix": [
            {"critere": "Fonctionnalités", "vous": "⚪", "leader": "🔴", "note": "Ne copiez pas tout — identifiez votre killer feature"},
            {"critere": "Prix", "vous": "🟢", "leader": "⚪", "note": "Agilité tarifaire vs les poids lourds = avantage PME"},
            {"critere": "Support", "vous": "🟢", "leader": "⚪", "note": "Accès fondateur direct = différenciateur early-stage"},
            {"critere": "Intégrations", "vous": "⚪", "leader": "🔴", "note": "Priorisez 5 intégrations critiques pour votre ICP"},
            {"critere": "Vitesse d'itération", "vous": "🟢", "leader": "⚪", "note": "Votre agilité est un avantage compétitif majeur"},
        ],
        "positioning_opportunity": "Vertical SaaS spécialisé + support fondateur + time-to-value < 48h",
        "moat": "Données propriétaires sectoriel + intégrations natives + réseau utilisateurs",
    },
}

_GENERIC_COMPETITIVE: Dict[str, Any] = {
    "direct_rivals": ["Concurrents positionnés sur votre niche exacte", "Alternatives directes à votre offre"],
    "indirect_rivals": ["Solutions DIY (faire soi-même)", "Freelances et agences généralistes"],
    "competitive_matrix": [
        {"critere": "Prix", "vous": "⚪", "leader": "🔴", "note": "Analysez le prix marché et positionnez-vous stratégiquement"},
        {"critere": "Qualité", "vous": "🟢", "leader": "⚪", "note": "La qualité est votre meilleur argument différenciant"},
        {"critere": "Notoriété", "vous": "⚪", "leader": "🔴", "note": "Construisez une notoriété de niche avant la notoriété large"},
        {"critere": "Service client", "vous": "🟢", "leader": "⚪", "note": "Réactivité et personnalisation = avantage structurel"},
        {"critere": "Innovation", "vous": "🟢", "leader": "⚪", "note": "Votre capacité à innover rapidement est une arme"},
    ],
    "positioning_opportunity": "Identifiez le segment délaissé par les leaders et devenez l'expert incontournable",
    "moat": "Expertise niche + relation client + contenu propriétaire",
}


def generate_pestel(activity_type: str) -> Dict[str, Any]:
    """Génère l'analyse PESTEL adaptée au secteur."""
    data = copy.deepcopy(PESTEL_DATA.get(activity_type, _GENERIC_PESTEL))
    return {
        "methodology": "PESTEL",
        "description": (
            "L'analyse PESTEL cartographie le macro-environnement — ces forces externes que "
            "l'entreprise ne contrôle pas mais qu'elle doit impérativement anticiper."
        ),
        "dimensions": data,
    }


def generate_micro_env(activity_type: str) -> Dict[str, Any]:
    """Génère l'analyse du micro-environnement."""
    data = copy.deepcopy(MICRO_ENV_TEMPLATES.get(activity_type, _GENERIC_MICRO_ENV))
    return {
        "description": (
            "Le micro-environnement englobe les acteurs en interaction directe avec l'entreprise "
            "dont le pouvoir de négociation et l'influence modèlent la chaîne de valeur au quotidien."
        ),
        "acteurs": data,
    }


def generate_competitive(activity_type: str) -> Dict[str, Any]:
    """Génère l'analyse concurrentielle."""
    data = copy.deepcopy(COMPETITIVE_BY_SECTOR.get(activity_type, _GENERIC_COMPETITIVE))
    return {
        "description": (
            "L'analyse concurrentielle identifie rivaux directs et indirects, décrypte leur "
            "positionnement pour révéler des avantages compétitifs inexploités."
        ),
        **data,
    }
