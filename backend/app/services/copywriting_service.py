"""
Copywriting Service — AIDA, déclencheurs psychologiques, structures persuasives.
Le copywriting fusionne sciences comportementales et rédaction persuasive.
Python 3.9 compatible.
"""
import copy
from typing import Dict, List, Any


# ─── Templates AIDA par secteur ───────────────────────────────────────────────
AIDA_TEMPLATES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "ecommerce": {
        "attention": {
            "principe": "Headline qui interrompt le scroll",
            "exemple": "Pourquoi 94% des acheteurs reviennent toujours chez nous",
            "formules": [
                "Arrêtez de [problème] — voici pourquoi [solution inattendue]",
                "La vraie raison pour laquelle [cible] rate [résultat]",
                "[Chiffre] acheteurs ont découvert [bénéfice] — voici comment",
            ],
            "conseil": "Utilisez chiffres, questions rhétoriques et promesses spécifiques. Évitez le générique.",
        },
        "interest": {
            "principe": "Développez le problème pour créer l'identification",
            "exemple": "Vous passez des heures à chercher... pour toujours tomber sur des produits décevants",
            "formules": [
                "Comme [X] clients avant vous, vous avez peut-être déjà vécu [situation]",
                "Voici ce que personne ne vous dit sur [sujet]",
                "Le problème avec [solution classique], c'est que [raison spécifique]",
            ],
            "conseil": "Montrez que vous comprenez exactement la douleur du client — avant de parler de vous.",
        },
        "desire": {
            "principe": "Projeter le client dans l'état désiré après achat",
            "exemple": "Imaginez recevoir exactement ce que vous attendiez, livré en 48h, avec garantie satisfait ou remboursé",
            "formules": [
                "Imaginez [bénéfice émotionnel] — c'est exactement ce que [X] clients vivent",
                "[Bénéfice concret] + [bénéfice émotionnel] = votre nouvelle réalité",
                "Nos clients témoignent : '[citation courte et spécifique]'",
            ],
            "conseil": "Combinez preuve sociale, bénéfices tangibles et projetez l'état émotionnel post-achat.",
        },
        "action": {
            "principe": "CTA unique, urgent et sans friction",
            "exemple": "Commander maintenant — Livraison offerte aujourd'hui",
            "formules": [
                "Je veux [bénéfice] → [bouton d'action]",
                "Profitez-en maintenant — [raison de l'urgence réelle]",
                "Commencez sans risque — [garantie spécifique]",
            ],
            "conseil": "Un seul CTA visible, urgence authentique, garantie de risque zéro, friction minimale.",
        },
    },
    "saas": {
        "attention": {
            "principe": "Chiffrez la douleur ou promettez le résultat",
            "exemple": "Réduisez de 4h à 20min votre reporting hebdomadaire",
            "formules": [
                "[X] heures perdues chaque semaine à faire [tâche manuelle] — et si ce n'était plus le cas ?",
                "Comment [client similaire] a multiplié par [X] [métrique] en [temps]",
                "Votre concurrent utilise déjà [solution] — voici ce qu'il gagne",
            ],
            "conseil": "Les décideurs SaaS sont rationnels — commencez par un chiffre ou un résultat mesurable.",
        },
        "interest": {
            "principe": "Nommez le problème précis que seul votre outil résout",
            "exemple": "La plupart des équipes perdent 23% de leur temps dans des tâches que [Outil] automatise en un clic",
            "formules": [
                "Le vrai problème avec [workflow actuel], c'est [coût caché invisible]",
                "[Chiffre] équipes ont abandonné [ancienne méthode] — voici pourquoi",
                "Sans [fonctionnalité], chaque [événement] vous coûte [quantification]",
            ],
            "conseil": "Soyez ultra-précis sur le pain point. Plus c'est spécifique, plus ça résonne.",
        },
        "desire": {
            "principe": "Démo, cas client avec métriques, social proof B2B",
            "exemple": "[Client connu] a réduit son CAC de 34% après 60 jours — témoignage complet →",
            "formules": [
                "'Depuis [Outil], on a [résultat] en [temps]' — [Prénom, Titre, Entreprise]",
                "Rejoignez [X] équipes qui ont déjà transformé [process]",
                "Essayez gratuitement 14 jours — sans carte bancaire, sans engagement",
            ],
            "conseil": "Case studies avec métriques > témoignages génériques. Logos clients reconnus = crédibilité.",
        },
        "action": {
            "principe": "Essai gratuit sans friction ou démo personnalisée",
            "exemple": "Commencer mon essai gratuit — En ligne en 2 minutes",
            "formules": [
                "Voir une démo en 15 min → [calendrier direct]",
                "Essayer gratuitement 14 jours → aucune CB requise",
                "Obtenir mon accès maintenant → [bénéfice immédiat à l'inscription]",
            ],
            "conseil": "Réduisez le risque perçu au maximum — freemium, démo, POC — jamais de salesman dès le premier contact.",
        },
    },
}

_GENERIC_AIDA = {
    "attention": {
        "principe": "Captez l'attention immédiatement avec un headline irrésistible",
        "exemple": "Le problème que vous n'avez jamais su nommer — et notre solution",
        "formules": [
            "[Chiffre provocateur] raisons pour lesquelles [problème persiste]",
            "Comment [cible similaire] a obtenu [résultat] sans [obstacle perçu]",
            "Arrêtez [action coûteuse] — il existe une meilleure façon",
        ],
        "conseil": "Votre headline est lu 5x plus que le reste. Investissez 50% de votre temps copywriting dessus.",
    },
    "interest": {
        "principe": "Développez la promesse en identifiant la douleur précise",
        "exemple": "Vous savez que [problème] vous coûte [temps/argent] — mais la vraie cause est ailleurs",
        "formules": [
            "Voici ce que la plupart des [cible] ignorent sur [sujet]",
            "Le coût invisible de [problème] : [quantification inattendue]",
            "Comme [X personnes], vous avez peut-être essayé [solutions inefficaces]",
        ],
        "conseil": "Empathie d'abord, solution ensuite. Montrez que vous comprenez avant de convaincre.",
    },
    "desire": {
        "principe": "Créez l'envie avec preuves, projections et social proof",
        "exemple": "Nos clients obtiennent [résultat tangible] et [bénéfice émotionnel] — ils en témoignent",
        "formules": [
            "Imaginez [situation désirée] — c'est possible dès [timing réaliste]",
            "[X] personnes ont déjà [résultat] — voici leurs retours",
            "Garantie : si vous n'obtenez pas [résultat], [engagement spécifique]",
        ],
        "conseil": "Preuves > promesses. Spécifique > général. Résultat émotionnel > fonctionnalité technique.",
    },
    "action": {
        "principe": "Un seul appel à l'action, clair et sans friction",
        "exemple": "Commencer maintenant — [bénéfice immédiat] → [CTA]",
        "formules": [
            "Je veux [résultat précis] → [bouton action]",
            "C'est gratuit jusqu'à [date/seuil] — [CTA]",
            "[Bénéfice] sans [risque perçu] → [CTA]",
        ],
        "conseil": "Supprimez tout ce qui pourrait faire hésiter : formulaires longs, prix cachés, processus flous.",
    },
}


# ─── Déclencheurs psychologiques ──────────────────────────────────────────────
PSYCHOLOGICAL_TRIGGERS: List[Dict[str, str]] = [
    {
        "trigger": "Urgence temporelle",
        "definition": "Crée une pression de temps pour déclencher l'action immédiate",
        "exemple": "Offre valable jusqu'à minuit — Stock limité à 47 unités",
        "usage": "Ventes flash, périodes de promotion, lancement de produit",
        "avertissement": "Doit être AUTHENTIQUE — la fausse urgence détruit la confiance",
    },
    {
        "trigger": "Preuve sociale",
        "definition": "Les gens imitent ce que font d'autres personnes similaires à eux",
        "exemple": "12 847 clients satisfaits ⭐⭐⭐⭐⭐ — Rejoignez-les",
        "usage": "Témoignages, compteurs d'utilisateurs, logos clients, médias",
        "avertissement": "Spécifique et vérifiable > chiffre rond et non sourcé",
    },
    {
        "trigger": "Autorité",
        "definition": "Les experts et figures d'autorité crédibilisent votre offre",
        "exemple": "Recommandé par [expert connu] · Certifié [organisme] · Cité dans [media]",
        "usage": "Badges certifications, mentions presse, partenariats experts, publications",
        "avertissement": "L'autorité doit être pertinente pour votre cible, pas seulement impressionnante",
    },
    {
        "trigger": "Rareté",
        "definition": "La valeur perçue augmente quand la disponibilité diminue",
        "exemple": "Plus que 3 places disponibles ce mois · Édition limitée 500 exemplaires",
        "usage": "Services premium, places de formation, stocks limités",
        "avertissement": "Comme l'urgence, doit être réelle — la rareté inventée génère du ressentiment",
    },
    {
        "trigger": "Réciprocité",
        "definition": "Donner quelque chose de valeur crée une obligation naturelle de rendre",
        "exemple": "Guide gratuit (vraie valeur) → lead nurturing → vente naturelle",
        "usage": "Lead magnets, contenus premium gratuits, consultations offertes",
        "avertissement": "La valeur du cadeau détermine la réciprocité — évitez les ebooks de 2 pages creux",
    },
    {
        "trigger": "Engagement & Cohérence",
        "definition": "Une fois qu'une personne a dit oui à quelque chose de petit, elle est plus encline à dire oui à quelque chose de plus grand",
        "exemple": "Quiz gratuit → email → webinaire → offre → vente",
        "usage": "Funnels de conversion, séquences email, onboarding progressif",
        "avertissement": "Chaque micro-engagement doit délivrer de la valeur — pas juste collecter des données",
    },
    {
        "trigger": "Aversion à la perte",
        "definition": "La douleur de perdre est 2x plus intense que le plaisir de gagner",
        "exemple": "Ne laissez pas vos concurrents prendre de l'avance · Évitez de perdre X €/mois",
        "usage": "Messaging sur les risques de ne pas agir, coûts de l'inaction",
        "avertissement": "À utiliser avec parcimonie — le fear marketing permanent génère de l'anxiété et du rejet",
    },
    {
        "trigger": "Appartenance communautaire",
        "definition": "Les humains veulent appartenir à un groupe qui partage leurs valeurs",
        "exemple": "Rejoignez 5000 entrepreneurs qui ont choisi de [valeur commune]",
        "usage": "Positioning de marque, communication de communauté, onboarding",
        "avertissement": "La communauté doit être réelle et active — une communauté morte est pire que pas de communauté",
    },
]


def generate_copywriting(activity_type: str, goal: str) -> Dict[str, Any]:
    """Génère les éléments de copywriting AIDA adaptés."""
    aida = copy.deepcopy(AIDA_TEMPLATES.get(activity_type, _GENERIC_AIDA))

    # Adapter selon l'objectif
    if goal == "awareness":
        aida["attention"]["conseil"] += " Pour la notoriété, le storytelling de marque prime sur la vente directe."
    elif goal == "sales":
        aida["action"]["conseil"] += " Pour la conversion directe, testez A/B au moins 2 versions de CTA."
    elif goal == "leads":
        aida["action"]["formules"].insert(0, "Recevoir mon [lead magnet] gratuit → [formulaire minimal]")
    elif goal == "traffic":
        aida["attention"]["conseil"] += " Pour le trafic SEO, alignez vos headlines sur l'intention de recherche."

    return {
        "methodology": "Copywriting AIDA + Déclencheurs Psychologiques",
        "description": (
            "Le copywriting fusionne sciences comportementales et rédaction persuasive pour produire "
            "des pages de vente, emails et posts qui déclenchent l'action."
        ),
        "aida": aida,
        "triggers": PSYCHOLOGICAL_TRIGGERS[:5],  # Top 5 triggers
        "copywriting_principles": [
            "Écrivez pour une personne, pas pour 'tout le monde'",
            "Bénéfices > fonctionnalités — toujours",
            "Spécifique > général — les détails créent la crédibilité",
            "Une idée par phrase, un CTA par page",
            "Testez, mesurez, itérez — le meilleur texte est celui qui convertit",
        ],
    }
