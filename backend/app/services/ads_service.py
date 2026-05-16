from app.models.schemas import AnalysisInput
import math


def generate_ads(data: AnalysisInput) -> dict:
    total = data.monthlyBudget
    fb_budget = round(total * 0.40)
    google_budget = round(total * 0.35)
    other_budget = total - fb_budget - google_budget

    facebook = _facebook_campaigns(data, fb_budget)
    google = _google_campaigns(data, google_budget)
    organic = _organic_strategies(data)

    mediaplan = [
        {"platform": "Facebook/Instagram Ads", "budget": fb_budget, "reach": _estimate_reach(fb_budget, "facebook"), "expectedCtr": "1.5-3%", "expectedRoi": "2.5x"},
        {"platform": "Google Ads (Search)", "budget": google_budget, "reach": _estimate_reach(google_budget, "google"), "expectedCtr": "3-8%", "expectedRoi": "3x"},
        {"platform": "Email Marketing", "budget": round(other_budget * 0.5), "reach": "Liste email x100%", "expectedCtr": "15-25%", "expectedRoi": "42x"},
        {"platform": "SEO Organique", "budget": round(other_budget * 0.5), "reach": "Croissance +20%/mois", "expectedCtr": "2-5%", "expectedRoi": "5-10x (long terme)"},
    ]

    return {
        "facebook": facebook,
        "google": google,
        "organic": organic,
        "mediaplan": mediaplan,
    }


def _facebook_campaigns(data: AnalysisInput, budget: float) -> dict:
    per_campaign = math.floor(budget / 2) if budget >= 40 else budget

    campaigns = [
        {
            "name": "Campagne Acquisition — Audience Froide",
            "objective": "Conversions" if data.goal == "sales" else "Trafic",
            "budget": per_campaign,
            "format": "Carrousel + Reel",
            "creatives": [
                {
                    "format": "Reel 15s",
                    "headline": f"Découvrez comment {_goal_outcome(data.goal)} en moins de 30 jours",
                    "description": f"Plus de {_get_social_proof(data.budget)} entrepreneurs font confiance à notre méthode.",
                    "cta": "En savoir plus",
                    "audience": "Lookalike 2% clients actuels",
                },
                {
                    "format": "Carrousel",
                    "headline": f"3 raisons de choisir [Marque] pour {_goal_phrase(data.goal)}",
                    "description": "Bénéfice 1, Bénéfice 2, Bénéfice 3. Résultats garantis.",
                    "cta": "Voir l'offre",
                    "audience": "Intérêts ciblés 25-45 ans",
                },
            ],
        },
    ]

    if budget >= 80:
        campaigns.append({
            "name": "Campagne Retargeting — Audience Chaude",
            "objective": "Conversions",
            "budget": per_campaign,
            "format": "Image unique + Story",
            "creatives": [
                {
                    "format": "Image unique",
                    "headline": "Vous n'avez pas encore sauté le pas ?",
                    "description": f"Offre spéciale -{_get_discount(data.budget)} pour les visiteurs de notre site. Valable 48h.",
                    "cta": "Je profite de l'offre",
                    "audience": "Visiteurs site 30 derniers jours",
                },
                {
                    "format": "Story vidéo",
                    "headline": "Ils ont essayé. Voici ce qu'ils disent.",
                    "description": "Témoignages authentiques de clients satisfaits.",
                    "cta": "Voir les témoignages",
                    "audience": "Panier abandonné + Engagement page",
                },
            ],
        })

    return {"campaigns": campaigns}


def _google_campaigns(data: AnalysisInput, budget: float) -> dict:
    campaigns = [
        {
            "name": "Search — Mots-clés intentionnels",
            "type": "Search",
            "budget": round(budget * 0.7),
            "keywords": ["[mot-clé principal]", "[solution + problème]", "[marque concurrente] alternative"],
        },
        {
            "name": "Display — Retargeting",
            "type": "Display Network",
            "budget": round(budget * 0.3),
            "keywords": ["Remarketing liste visiteurs", "Similar audiences", "In-market [catégorie]"],
        },
    ]
    return {"campaigns": campaigns}


def _organic_strategies(data: AnalysisInput) -> dict:
    strategies = [
        {
            "channel": "Bouche-à-oreille & Referral",
            "tactic": "Programme de parrainage avec récompense double sens",
            "frequency": "Continu",
            "examples": [
                "Offrir 20% de réduction pour chaque filleul amené",
                "Créer un programme ambassadeur pour les clients les plus satisfaits",
                "Demander systématiquement une recommandation après chaque vente réussie",
            ],
        },
        {
            "channel": "Réseaux sociaux organiques",
            "tactic": "Stratégie de contenu éducatif et d'engagement communautaire",
            "frequency": "Quotidien",
            "examples": [
                "Publier des conseils pratiques en format carrousel Instagram",
                "Répondre à tous les commentaires dans les 2 premières heures",
                "Créer un groupe Facebook/Telegram pour votre communauté",
                "Collaborer avec 3 micro-influenceurs de votre niche",
            ],
        },
        {
            "channel": "Email Marketing",
            "tactic": "Séquence de nurturing automatisée avec segmentation comportementale",
            "frequency": "1-2 emails/semaine",
            "examples": [
                "Lead magnet de valeur (guide, template, checklist) pour capturer des emails",
                "Séquence de bienvenue en 5 emails sur 10 jours",
                "Newsletter hebdomadaire avec 80% valeur / 20% promotion",
                "Emails de réengagement pour les inactifs depuis 30+ jours",
            ],
        },
        {
            "channel": "SEO & Contenu",
            "tactic": "Stratégie de contenu pillar page + topic clusters",
            "frequency": "2-3 articles/semaine",
            "examples": [
                f"Article long-form (+2000 mots) sur le sujet principal de votre secteur",
                "Guide complet sur [problème principal de vos personas]",
                "Page FAQ optimisée pour les recherches vocales et GEO",
                "Études de cas clients avec résultats chiffrés",
            ],
        },
    ]
    return {"strategies": strategies}


def _goal_outcome(goal: str) -> str:
    return {
        "awareness": "être connu dans votre secteur",
        "sales": "doubler vos ventes",
        "leads": "générer 50 prospects qualifiés",
        "traffic": "tripler votre trafic",
    }.get(goal, "atteindre vos objectifs")


def _goal_phrase(goal: str) -> str:
    return {
        "awareness": "développer votre notoriété",
        "sales": "augmenter vos ventes",
        "leads": "générer des leads",
        "traffic": "augmenter votre trafic",
    }.get(goal, "atteindre vos objectifs")


def _get_social_proof(budget: float) -> str:
    if budget < 200: return "500+"
    if budget < 500: return "1 200+"
    return "3 400+"


def _get_discount(budget: float) -> str:
    if budget < 200: return "15%"
    return "20%"


def _estimate_reach(budget: float, platform: str) -> str:
    if platform == "facebook":
        low = int(budget * 200)
        high = int(budget * 500)
        return f"{low:,}-{high:,} personnes".replace(",", " ")
    else:
        low = int(budget * 50)
        high = int(budget * 150)
        return f"{low:,}-{high:,} clics/mois".replace(",", " ")
