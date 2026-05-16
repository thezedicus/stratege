"""
QQOQCCP Service — Qui, Quoi, Où, Quand, Comment, Combien, Pourquoi
Complément au diagnostic SWOT pour ne laisser aucune zone d'ombre.
Python 3.9 compatible.
"""
from typing import Dict, Any


QQOQCCP_TEMPLATES: Dict[str, Dict[str, Dict[str, str]]] = {
    "ecommerce": {
        "qui": {
            "question": "Qui sont vos acheteurs cibles ?",
            "reponse": "Consommateurs 25-45 ans, actifs digitaux, acheteurs en ligne réguliers (2-4x/mois)",
            "action": "Segmentez par RFM (Récence, Fréquence, Montant) et créez 3 personas distincts",
        },
        "quoi": {
            "question": "Quoi vendez-vous exactement ?",
            "reponse": "Produits physiques ou digitaux avec proposition de valeur unique et différenciante",
            "action": "Rédigez une USP en 10 mots max : bénéfice principal + différenciateur + cible",
        },
        "ou": {
            "question": "Où vos clients achètent-ils ?",
            "reponse": "Mobile (68%), desktop (29%), tablette (3%) — majoritairement Google Shopping et réseaux sociaux",
            "action": "Priorisez l'expérience mobile-first et optimisez vos fiches Google Shopping",
        },
        "quand": {
            "question": "Quand vos clients achètent-ils ?",
            "reponse": "Pics : vendredi soir, samedi matin, pauses déjeuner (12h-14h), saisons festives",
            "action": "Programmez vos campagnes et emailings sur ces créneaux + soldes/événements clés",
        },
        "comment": {
            "question": "Comment décident-ils d'acheter ?",
            "reponse": "Recherche Google → comparaison avis → réseau social → achat — cycle 2-7 jours",
            "action": "Couvrez chaque étape : SEO, reviews Trustpilot, retargeting Meta, panier abandonné",
        },
        "combien": {
            "question": "Combien sont-ils prêts à payer ?",
            "reponse": "Panier moyen cible : 45-120 € selon la niche. Sensibilité prix forte sous 30 €",
            "action": "Testez des prix psychologiques (X9), offres bundles et livraison gratuite à seuil",
        },
        "pourquoi": {
            "question": "Pourquoi vous choisiraient-ils ?",
            "reponse": "Confiance (avis/garanties), commodité (livraison), prix/qualité, expérience brand",
            "action": "Mettez en avant : étoiles Trustpilot, politique retour, badge sécurisé, UGC",
        },
    },
    "saas": {
        "qui": {
            "question": "Qui sont vos utilisateurs et décideurs ?",
            "reponse": "Double cible : utilisateurs finaux (opérationnels) et acheteurs (dirigeants/DSI)",
            "action": "Créez un messaging distinct pour chaque persona : bénéfice usage vs ROI business",
        },
        "quoi": {
            "question": "Quel problème résolvez-vous exactement ?",
            "reponse": "Économie de temps, réduction d'erreurs ou augmentation de revenus — toujours quantifiable",
            "action": "Quantifiez le problème : 'X heures perdues/semaine' ou 'Y% d'erreurs évitées'",
        },
        "ou": {
            "question": "Où vos prospects cherchent-ils des solutions ?",
            "reponse": "G2, Capterra, Product Hunt, LinkedIn, communautés Slack/Discord sectorielles",
            "action": "Optimisez votre profil G2/Capterra + publiez sur Product Hunt au lancement",
        },
        "quand": {
            "question": "Quand un prospect décide-t-il de changer d'outil ?",
            "reponse": "Lors d'un événement déclencheur : croissance, recrutement, audit, changement de direction",
            "action": "Configurez des alertes sur ces signaux d'intention (LinkedIn, news, levées de fonds)",
        },
        "comment": {
            "question": "Comment se déroule le cycle de décision ?",
            "reponse": "Découverte → essai gratuit (14-30j) → démonstration → POC → validation → achat",
            "action": "Optimisez chaque étape : onboarding J1-J7, email nurturing, CS proactif à J14",
        },
        "combien": {
            "question": "Combien votre solution leur fait-elle économiser/gagner ?",
            "reponse": "Calculez le ROI concret : temps économisé × TJM ou revenus additionnels générés",
            "action": "Créez un calculateur ROI interactif sur votre landing page",
        },
        "pourquoi": {
            "question": "Pourquoi vous plutôt que vos concurrents ?",
            "reponse": "Fonctionnalités uniques, intégrations, support, prix ou rapidité d'implémentation",
            "action": "Publiez des comparatifs 'Vous vs [Concurrent]' sur des landing pages dédiées",
        },
    },
    "service": {
        "qui": {
            "question": "Qui a le plus besoin de votre service ?",
            "reponse": "Identifiez le segment avec la plus forte douleur ET la capacité budgétaire",
            "action": "Interviewez vos 5 meilleurs clients actuels pour extraire le profil idéal (ICP)",
        },
        "quoi": {
            "question": "Quelle transformation offrez-vous concrètement ?",
            "reponse": "Un service se vend sur le résultat tangible, pas sur la prestation elle-même",
            "action": "Reformulez : 'Je [verbe d'action] pour [cible] afin de [résultat mesurable]'",
        },
        "ou": {
            "question": "Où vos prospects vous trouvent-ils ?",
            "reponse": "Bouche-à-oreille (42%), LinkedIn (31%), Google (18%), événements (9%)",
            "action": "Formalisez votre programme de référencement client avec une incitation claire",
        },
        "quand": {
            "question": "Quand ont-ils le plus besoin de vous ?",
            "reponse": "En période de croissance, de crise, de transformation ou avant des événements clés",
            "action": "Positionnez votre service comme la solution avant/pendant ces moments critiques",
        },
        "comment": {
            "question": "Comment votre service est-il délivré ?",
            "reponse": "Remote, présentiel, hybride — le format impacte directement la valeur perçue",
            "action": "Documentez et packagisez votre processus de livraison (Notion, playbook client)",
        },
        "combien": {
            "question": "Combien devez-vous facturer pour être rentable ET attractif ?",
            "reponse": "Prix = valeur perçue × positionnement. Évitez le prix coûtant + marge",
            "action": "Testez 3 niveaux de prix (bronze/argent/or) pour maximiser le panier moyen",
        },
        "pourquoi": {
            "question": "Pourquoi un client vous ferait-il confiance avant d'acheter ?",
            "reponse": "Études de cas, témoignages vidéo, certifications, échantillon de travail",
            "action": "Publiez 3 études de cas détaillées avec métriques avant/après sur votre site",
        },
    },
}

# Fallback générique pour tous les autres types
_GENERIC_QQOQCCP = {
    "qui": {
        "question": "Qui est votre client idéal (ICP) ?",
        "reponse": "Définissez précisément : secteur, taille, rôle décisionnel, budget et douleur principale",
        "action": "Réalisez 10 interviews clients pour valider et affiner votre profil ICP",
    },
    "quoi": {
        "question": "Quoi proposez-vous exactement comme valeur ?",
        "reponse": "Votre offre doit résoudre un problème spécifique de manière unique et mesurable",
        "action": "Rédigez votre value proposition canvas : job-to-be-done, pains, gains",
    },
    "ou": {
        "question": "Où se trouvent et s'informent vos prospects ?",
        "reponse": "Identifiez les canaux digitaux et physiques où ils cherchent des solutions",
        "action": "Investissez prioritairement dans les 2 canaux où votre ICP passe le plus de temps",
    },
    "quand": {
        "question": "Quand votre client a-t-il besoin de vous ?",
        "reponse": "Il existe toujours un déclencheur d'achat : événement, seuil de douleur, saison",
        "action": "Cartographiez le cycle de vie client et anticipez les moments déclencheurs",
    },
    "comment": {
        "question": "Comment votre client prend-il sa décision d'achat ?",
        "reponse": "Parcours d'achat : prise de conscience → considération → décision → fidélisation",
        "action": "Créez du contenu adapté à chaque étape du parcours (TOFU/MOFU/BOFU)",
    },
    "combien": {
        "question": "Combien votre client est-il prêt à investir ?",
        "reponse": "Le prix doit refléter la valeur perçue, pas uniquement vos coûts",
        "action": "Benchmarkez vos concurrents et testez différentes structurations de prix",
    },
    "pourquoi": {
        "question": "Pourquoi votre client vous choisit-il plutôt qu'un concurrent ?",
        "reponse": "Votre différenciateur doit être défendable, visible et valorisé par votre cible",
        "action": "Identifiez votre avantage compétitif unique et construisez tout votre messaging dessus",
    },
}


def generate_qqoqccp(activity_type: str, goal: str, maturity: str) -> Dict[str, Any]:
    """Génère l'analyse QQOQCCP adaptée au type d'activité."""
    template = QQOQCCP_TEMPLATES.get(activity_type, _GENERIC_QQOQCCP)

    return {
        "methodology": "QQOQCCP",
        "description": (
            "Le QQOQCCP systématise le questionnement stratégique pour ne laisser "
            "aucune zone d'ombre dans la compréhension d'une situation ou d'un besoin client."
        ),
        "questions": template,
        "goal_focus": _get_goal_focus(goal),
        "maturity_note": _get_maturity_note(maturity),
    }


def _get_goal_focus(goal: str) -> str:
    return {
        "awareness": "Focus QQOQCCP : concentrez-vous sur 'Qui' et 'Pourquoi' pour construire un message de notoriété percutant",
        "sales": "Focus QQOQCCP : le 'Combien' et le 'Comment' sont critiques pour optimiser votre tunnel de conversion",
        "leads": "Focus QQOQCCP : le 'Qui' et le 'Quand' définissent vos signaux d'intention — priorisez-les",
        "traffic": "Focus QQOQCCP : le 'Où' et le 'Comment' orientent votre stratégie d'acquisition de trafic qualifié",
    }.get(goal, "Analysez chaque dimension du QQOQCCP pour construire une stratégie cohérente")


def _get_maturity_note(maturity: str) -> str:
    return {
        "idea": "Phase idée : utilisez le QQOQCCP pour valider vos hypothèses AVANT d'investir",
        "inprogress": "Phase développement : le QQOQCCP vous aide à aligner produit et besoin marché",
        "launched": "Phase lancée : revisitez le QQOQCCP trimestriellement pour ajuster votre stratégie",
    }.get(maturity, "")
