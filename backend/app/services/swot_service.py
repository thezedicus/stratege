"""
SWOT analysis service — covers all 8 activity types from the wizard.
Python 3.9 compatible.
"""
import copy
from typing import Dict, List, Any

SECTOR_DATA: Dict[str, Dict[str, List[str]]] = {
    "ecommerce": {
        "strengths_base": [
            "Vente directe sans intermédiaire, marges optimisées",
            "Disponibilité 24h/24 et 7j/7 sans contrainte géographique",
            "Données client et comportementales exploitables",
            "Scalabilité rapide sans coût fixe proportionnel",
        ],
        "weaknesses_base": [
            "Forte concurrence des marketplaces (Amazon, Cdiscount)",
            "Coûts d'acquisition client élevés (CAC)",
            "Gestion logistique et retours complexe",
            "Dépendance aux algorithmes des moteurs de recherche",
        ],
        "opportunities_base": [
            "Croissance du m-commerce (+25% par an)",
            "Personnalisation IA pour augmenter le panier moyen",
            "Marchés internationaux accessibles sans boutique physique",
            "Social commerce (Instagram Shop, TikTok Shop)",
        ],
        "threats_base": [
            "Hausse du coût des publicités (CPM, CPC)",
            "Nouvelles réglementations RGPD sur les cookies",
            "Saturation des niches rentables",
            "Contrefaçons et concurrence prix agressive",
        ],
    },
    "saas": {
        "strengths_base": [
            "Revenus récurrents (MRR/ARR) prévisibles",
            "Coût marginal quasi nul pour chaque nouvel utilisateur",
            "Mises à jour centralisées sans friction client",
            "Effets de réseau et forte rétention si valeur prouvée",
        ],
        "weaknesses_base": [
            "Temps long pour atteindre la rentabilité",
            "Support client chronophage en phase de croissance",
            "Churn élevé si onboarding insuffisant",
            "Dépendance aux plateformes cloud (AWS, GCP)",
        ],
        "opportunities_base": [
            "Marché SaaS mondial en croissance à 2 chiffres",
            "IA intégrée comme différenciateur compétitif fort",
            "Verticaux non-disruptés (santé, agriculture, juridique)",
            "Modèles freemium pour acquisition organique massive",
        ],
        "threats_base": [
            "Géants tech qui copient les fonctionnalités populaires",
            "Fatigue SaaS — consolidation des budgets outils",
            "Violations de données — impact réputationnel",
            "Open-source alternatives gratuites",
        ],
    },
    "service": {
        "strengths_base": [
            "Faibles coûts de démarrage, pas de stock",
            "Relation client directe et fidélisation naturelle",
            "Marges élevées si positionnement premium",
            "Expertise différenciante difficile à copier",
        ],
        "weaknesses_base": [
            "Scalabilité limitée par le temps humain",
            "Dépendance aux clients clés (concentration du CA)",
            "Difficulté à valoriser l'immatériel",
            "Irrégularité des revenus selon les cycles",
        ],
        "opportunities_base": [
            "Automatisation des tâches répétitives via IA",
            "Marchés de niche sous-servis",
            "Partenariats et apporteurs d'affaires",
            "Packagisation des services en offres fixes",
        ],
        "threats_base": [
            "Concurrence des freelances low-cost (Upwork, Fiverr)",
            "Récession économique comprime les budgets prestataires",
            "Commoditisation du service par les outils no-code",
        ],
    },
    "website": {
        "strengths_base": [
            "Vitrine professionnelle disponible en permanence",
            "Crédibilité et légitimité auprès des prospects",
            "SEO local et national activable",
            "Coût de maintenance faible une fois créé",
        ],
        "weaknesses_base": [
            "Génération de leads passive — nécessite du trafic",
            "Pas de conversion directe sans stratégie d'acquisition",
            "Contenu à maintenir à jour régulièrement",
        ],
        "opportunities_base": [
            "SEO local très accessible pour les PME",
            "Blog/contenu pour attirer des prospects qualifiés",
            "Intégration chatbot pour capturer les leads 24/7",
        ],
        "threats_base": [
            "Concurrence des annuaires et plateformes sectorielles",
            "Évolution des algorithmes Google",
            "Vitesse de chargement pénalisée si non optimisée",
        ],
    },
    "application": {
        "strengths_base": [
            "Présence permanente sur l'écran de l'utilisateur",
            "Notifications push pour ré-engagement",
            "Monétisation via abonnements, in-app ou publicités",
            "Données comportementales riches",
        ],
        "weaknesses_base": [
            "Coût de développement et de maintenance élevé",
            "Barrière à l'installation (friction de l'App Store)",
            "Dépendance aux règles Apple/Google (commissions 30%)",
            "Taux de désinstallation élevé les 30 premiers jours",
        ],
        "opportunities_base": [
            "Progressive Web Apps (PWA) comme alternative",
            "Marchés émergents avec forte adoption mobile",
            "Gamification et social pour la rétention",
            "Cross-platform (Flutter, React Native) réduit les coûts",
        ],
        "threats_base": [
            "App fatigue — utilisateurs saturés d'applications",
            "Nouvelles restrictions de tracking iOS (ATT)",
            "Concurrent fonctionnel intégré dans iOS/Android natif",
        ],
    },
    "content": {
        "strengths_base": [
            "Audience fidèle et communauté engagée",
            "Monétisation diverse (pub, sponsoring, formations, produits)",
            "Expertise perçue = autorité dans la niche",
            "Faibles coûts de production relatifs",
        ],
        "weaknesses_base": [
            "Revenus variables et dépendants des algorithmes",
            "Production régulière chronophage",
            "Burnout créatif fréquent",
            "Dépendance aux plateformes (YouTube, Instagram)",
        ],
        "opportunities_base": [
            "Boom des newsletters payantes (Substack, Beehiiv)",
            "IA pour accélérer la production de contenu",
            "Marchés anglophones pour démultiplier l'audience",
            "Formations et produits digitaux à haute marge",
        ],
        "threats_base": [
            "Contenu généré par IA qui inonde les plateformes",
            "Démonétisation soudaine par les plateformes",
            "Évolution des formats et attention décroissante",
        ],
    },
    "consulting": {
        "strengths_base": [
            "Expertise rare et difficile à reproduire",
            "Tarification à forte valeur ajoutée",
            "Faibles coûts fixes",
            "Flexibilité géographique (remote)",
        ],
        "weaknesses_base": [
            "Revenu non récurrent et irrégulier",
            "Image personnelle = marque, risque de dépendance",
            "Capacité limitée par le nombre d'heures",
            "Cycle de vente long pour les grands comptes",
        ],
        "opportunities_base": [
            "Positionnement en tant qu'expert de niche",
            "Productisation du conseil en cours en ligne",
            "Partenariats avec agences complémentaires",
            "Speaking, conférences pour la notoriété",
        ],
        "threats_base": [
            "IA qui remplace certaines missions de conseil junior",
            "Marchés saturés dans les niches populaires",
            "Clients qui internalisent les compétences après mission",
        ],
    },
    "other": {
        "strengths_base": [
            "Positionnement unique et différencié",
            "Flexibilité et agilité organisationnelle",
            "Opportunité d'innover dans un espace peu balisé",
        ],
        "weaknesses_base": [
            "Marché parfois difficile à éduquer",
            "Ressources limitées en phase d'amorçage",
            "Besoin d'évangélisation du produit/service",
        ],
        "opportunities_base": [
            "First-mover advantage dans la niche",
            "Partenariats stratégiques pour accélérer",
            "Levée de fonds ou financement participatif",
        ],
        "threats_base": [
            "Pivot nécessaire si le marché ne répond pas",
            "Concurrents bien financés qui copient l'innovation",
            "Difficultés à recruter des profils adaptés",
        ],
    },
}


def generate_swot(activity_type: str, goal: str, maturity: str) -> Dict[str, Any]:
    """
    Generate a SWOT analysis adapted to the activity type, goal and maturity.
    Falls back to 'other' if the activity type is unknown.
    """
    sector = copy.deepcopy(SECTOR_DATA.get(activity_type, SECTOR_DATA["other"]))

    # Adapt based on maturity
    if maturity == "idea":
        sector["strengths_base"].insert(0, "Opportunité de construire sans dette technique ni organisationnelle")
        sector["weaknesses_base"].insert(0, "Absence de validation marché et de revenus")
    elif maturity == "inprogress":
        sector["strengths_base"].insert(0, "Développement en cours — apprentissage rapide")
        sector["weaknesses_base"].insert(0, "Produit non encore en production — risque de délai")
    elif maturity == "launched":
        sector["strengths_base"].insert(0, "Traction initiale prouvée et premiers retours clients")
        sector["opportunities_base"].insert(0, "Optimisation basée sur les données réelles d'usage")

    # Adapt based on goal
    goal_extras: Dict[str, Dict[str, str]] = {
        "awareness": {
            "opp": "Stratégie de content marketing pour construire l'autorité de marque",
        },
        "sales": {
            "opp": "Optimisation du tunnel de conversion pour maximiser le CA",
        },
        "leads": {
            "opp": "Lead magnets et marketing automation pour qualifier les prospects",
        },
        "traffic": {
            "opp": "SEO technique et stratégie de backlinks pour croissance organique",
        },
    }
    if goal in goal_extras:
        sector["opportunities_base"].append(goal_extras[goal]["opp"])

    return {
        "strengths":     sector["strengths_base"][:4],
        "weaknesses":    sector["weaknesses_base"][:4],
        "opportunities": sector["opportunities_base"][:4],
        "threats":       sector["threats_base"][:3],
    }
