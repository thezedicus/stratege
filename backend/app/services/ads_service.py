from app.models.schemas import AnalysisInput
import math


def generate_ads(data: AnalysisInput) -> dict:
    total = data.monthlyBudget
    fb_budget  = round(total * 0.40)
    gads_budget = round(total * 0.35)
    other_budget = max(0.0, total - fb_budget - gads_budget)

    facebook = _facebook_campaigns(data, fb_budget)
    google   = _google_campaigns(data, gads_budget)
    organic  = _organic_strategies(data)

    mediaplan = _build_mediaplan(data, fb_budget, gads_budget, other_budget)

    return {
        "facebook": facebook,
        "google":   google,
        "organic":  organic,
        "mediaplan": mediaplan,
    }


def _build_mediaplan(data: AnalysisInput, fb: float, gads: float, other: float) -> list:
    email_budget   = round(other * 0.5)
    seo_budget     = max(0, round(other * 0.5))

    plan = [
        {
            "platform": "Facebook/Instagram Ads",
            "budget":   fb,
            "reach":    _estimate_reach(fb, "facebook"),
            "expectedCtr": "1-3 %",
            "expectedRoi": "2-3×",
        },
        {
            "platform": "Google Ads (Search)",
            "budget":   gads,
            "reach":    _estimate_reach(gads, "google"),
            "expectedCtr": "3-8 %",
            "expectedRoi": "2.5-4×",
        },
    ]
    if email_budget > 0:
        plan.append({
            "platform": "Email Marketing",
            "budget":   email_budget,
            "reach":    "Liste email × 100 %",
            "expectedCtr": "15-25 %",
            "expectedRoi": "20-42×",
        })
    if seo_budget > 0:
        plan.append({
            "platform": "SEO & Contenu Organique",
            "budget":   seo_budget,
            "reach":    "Croissance +15-25 %/mois",
            "expectedCtr": "2-5 %",
            "expectedRoi": "5-10× (long terme)",
        })
    return plan


def _facebook_campaigns(data: AnalysisInput, budget: float) -> dict:
    if budget <= 0:
        return {"campaigns": []}

    creatives_cold = _cold_creatives(data)
    campaigns = [
        {
            "name":      "Acquisition — Audience Froide",
            "objective": _fb_objective(data.goal),
            "budget":    round(budget * 0.6),
            "format":    "Reel + Carrousel",
            "creatives": creatives_cold,
        },
    ]

    if budget >= 60:
        campaigns.append({
            "name":      "Retargeting — Audience Chaude",
            "objective": "Conversions",
            "budget":    round(budget * 0.4),
            "format":    "Image unique + Story",
            "creatives": _warm_creatives(data),
        })

    return {"campaigns": campaigns}


def _google_campaigns(data: AnalysisInput, budget: float) -> dict:
    if budget <= 0:
        return {"campaigns": []}

    # Sector-specific real keywords (no generic placeholders)
    kw_map = {
        "ecommerce":   ["acheter [produit] livraison rapide", "boutique en ligne promo", "[marque] soldes"],
        "saas":        ["essai gratuit logiciel gestion", "outil productivité PME", "meilleur SaaS [catégorie]"],
        "service":     ["prestataire [service] devis", "expert [domaine] disponible", "consultant [spécialité]"],
        "website":     ["création site web [ville]", "agence web locale [ville]", "refonte site artisan"],
        "consulting":  ["consultant [domaine] PME", "accompagnement entrepreneur", "formation [métier] en ligne"],
        "content":     ["formation créateur contenu", "blog affilié revenus", "monétiser Instagram/YouTube"],
        "application": ["app [usage] télécharger", "application mobile [fonction]", "outil mobile gratuit"],
        "default":     ["solution professionnelle en ligne", "service numérique fiable", "meilleur [offre] France"],
    }
    kws = kw_map.get(data.activityType, kw_map["default"])

    campaigns = [
        {
            "name":     "Search — Intention directe",
            "type":     "Search",
            "budget":   round(budget * 0.7),
            "keywords": kws,
        },
    ]
    if budget >= 50:
        campaigns.append({
            "name":     "Display — Remarketing",
            "type":     "Display Network",
            "budget":   round(budget * 0.3),
            "keywords": ["Remarketing visiteurs 30 jours", "Audiences similaires (Lookalike 2 %)", "In-market Google"],
        })
    return {"campaigns": campaigns}


def _organic_strategies(data: AnalysisInput) -> dict:
    strategies = [
        {
            "channel":   "Bouche-à-oreille & Referral",
            "tactic":    "Programme de parrainage avec récompense double sens (parrain et filleul)",
            "frequency": "Continu",
            "examples":  [
                "Offrir -20 % pour chaque filleul amené",
                "Créer un programme ambassadeur pour les clients les plus satisfaits",
                "Demander systématiquement une recommandation après chaque vente réussie",
            ],
        },
        {
            "channel":   "Réseaux sociaux organiques",
            "tactic":    "Stratégie de contenu éducatif + engagement communautaire quotidien",
            "frequency": "Quotidien",
            "examples":  [
                "Publier 1 conseil pratique par jour en format carrousel Instagram",
                "Répondre à tous les commentaires dans les 2 premières heures",
                "Créer un groupe Facebook/Telegram pour votre communauté de clients",
                "Collaborer avec 3 micro-influenceurs de votre niche (5K-50K abonnés)",
            ],
        },
        {
            "channel":   "Email Marketing",
            "tactic":    "Séquence de nurturing automatisée avec segmentation comportementale",
            "frequency": "1-2 emails/semaine",
            "examples":  [
                "Lead magnet de valeur (guide, template, checklist) pour capturer les premiers emails",
                "Séquence de bienvenue en 5 emails sur 10 jours",
                "Newsletter hebdomadaire : 80 % valeur / 20 % promotion",
                "Emails de réengagement pour les inactifs depuis 30+ jours",
            ],
        },
        {
            "channel":   "SEO & Contenu",
            "tactic":    "Stratégie pillar page + topic clusters pour dominer votre niche",
            "frequency": "2-3 articles/semaine",
            "examples":  [
                "Article long-form (+2 000 mots) sur le sujet principal de votre secteur",
                "Guide complet pour résoudre le problème numéro 1 de vos personas",
                "Page FAQ optimisée pour les recherches vocales et les IA génératives",
                "Études de cas clients avec résultats chiffrés et témoignages",
            ],
        },
    ]
    return {"strategies": strategies}


def _cold_creatives(data: AnalysisInput) -> list:
    goal_headline = {
        "awareness": f"Découvrez comment {_activity_label(data.activityType)} peut transformer votre quotidien",
        "sales":     f"Profitez de notre offre exclusive — résultats garantis ou remboursé",
        "leads":     f"Téléchargez gratuitement votre guide pour {_goal_outcome(data.goal)}",
        "traffic":   f"Plus de {_get_social_proof(data.budget)} entrepreneurs font déjà confiance à notre méthode",
    }
    return [
        {
            "format":      "Reel 15s",
            "headline":    goal_headline.get(data.goal, "Découvrez notre solution"),
            "description": f"{_get_social_proof(data.budget)} utilisateurs actifs. Essai gratuit disponible.",
            "cta":         "En savoir plus",
            "audience":    "Lookalike 2 % clients actuels",
        },
        {
            "format":      "Carrousel",
            "headline":    "3 raisons qui font la différence",
            "description": "✅ Résultats mesurables. ✅ Simple d'utilisation. ✅ Support réactif.",
            "cta":         "Voir l'offre",
            "audience":    "Intérêts ciblés 25-45 ans",
        },
    ]


def _warm_creatives(data: AnalysisInput) -> list:
    discount = "15 %" if data.budget < 200 else "20 %"
    return [
        {
            "format":      "Image unique",
            "headline":    "Vous n'avez pas encore sauté le pas ?",
            "description": f"Offre spéciale -{discount} pour les visiteurs. Valable 48h seulement.",
            "cta":         "Je profite de l'offre",
            "audience":    "Visiteurs site 30 derniers jours",
        },
        {
            "format":      "Story vidéo",
            "headline":    "Ils ont essayé. Voici ce qu'ils disent.",
            "description": "Témoignages authentiques de clients satisfaits.",
            "cta":         "Voir les témoignages",
            "audience":    "Engagement page + panier abandonné",
        },
    ]


def _fb_objective(goal: str) -> str:
    return {
        "awareness": "Notoriété de la marque",
        "sales":     "Conversions",
        "leads":     "Génération de prospects",
        "traffic":   "Trafic",
    }.get(goal, "Trafic")


def _goal_outcome(goal: str) -> str:
    return {
        "awareness": "être connu dans votre secteur",
        "sales":     "doubler vos ventes",
        "leads":     "générer 50 prospects qualifiés par mois",
        "traffic":   "tripler votre trafic organique",
    }.get(goal, "atteindre vos objectifs")


def _activity_label(activity: str) -> str:
    return {
        "ecommerce":   "le commerce en ligne",
        "saas":        "votre logiciel",
        "service":     "votre expertise",
        "website":     "votre présence web",
        "consulting":  "votre conseil",
        "content":     "votre contenu",
        "application": "votre application",
        "other":       "votre projet",
    }.get(activity, "votre activité")


def _get_social_proof(budget: float) -> str:
    if budget < 100:   return "500+"
    if budget < 400:   return "1 200+"
    if budget < 700:   return "2 800+"
    return "5 000+"


def _estimate_reach(budget: float, platform: str) -> str:
    if budget <= 0:
        return "0 personnes"
    if platform == "facebook":
        # More realistic: €1 = ~80-200 people on FB/IG
        low  = int(budget * 80)
        high = int(budget * 200)
    else:
        # Google: €1 = ~20-80 clicks
        low  = int(budget * 20)
        high = int(budget * 80)

    def fmt(n: int) -> str:
        if n >= 1000:
            return f"{n // 1000} {n % 1000:03d}".replace(" ", " ")
        return str(n)

    unit = "personnes" if platform == "facebook" else "clics/mois"
    return f"{fmt(low)} – {fmt(high)} {unit}"
