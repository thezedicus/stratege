from app.models.schemas import AnalysisInput
import math


def generate_synthesis(
    data: AnalysisInput,
    swot: dict,
    personas: list,
    marketing: dict,
    seo: dict,
    ads: dict,
) -> dict:
    actions = _generate_actions(data, swot)
    roi = _generate_roi(data)
    summary = _generate_summary(data, swot)
    metrics = _generate_key_metrics(data)
    next_steps = _generate_next_steps(data)

    return {
        "actions": actions,
        "roi": roi,
        "summary": summary,
        "keyMetrics": metrics,
        "nextSteps": next_steps,
    }


def _generate_actions(data: AnalysisInput, swot: dict) -> list:
    actions = []
    priority = 0

    # Action 0 for idea stage — validate before spending
    if data.maturity == "idea":
        priority += 1
        actions.append({
            "priority": priority,
            "action": "Valider votre idée avec 10 entretiens de clients potentiels avant tout investissement publicitaire",
            "timeline": "Semaine 1",
            "effort": "Faible",
            "impact": "Fort",
            "category": "Stratégie",
        })

    priority += 1
    actions.append({
        "priority": priority,
        "action": "Créer ou optimiser votre page de destination pour l'objectif '{}'".format(_goal_label(data.goal)),
        "timeline": "Semaine 1",
        "effort": "Moyen",
        "impact": "Fort",
        "category": "Marketing",
    })

    priority += 1
    actions.append({
        "priority": priority,
        "action": "Installer Google Analytics 4 et Google Search Console pour un suivi précis des performances",
        "timeline": "Semaine 1",
        "effort": "Faible",
        "impact": "Moyen",
        "category": "Stratégie",
    })

    priority += 1
    actions.append({
        "priority": priority,
        "action": "Mettre en place un système de capture d'email avec un lead magnet gratuit (guide, checklist ou template)",
        "timeline": "Semaine 1-2",
        "effort": "Faible",
        "impact": "Fort",
        "category": "Marketing",
    })

    if data.monthlyBudget >= 30:
        priority += 1
        actions.append({
            "priority": priority,
            "action": "Lancer une première campagne sur {} avec {}€ pour tester les messages".format(
                _main_channel(data.activityType), round(data.monthlyBudget * 0.4)
            ),
            "timeline": "Semaine 2",
            "effort": "Moyen",
            "impact": "Fort",
            "category": "Publicité",
        })

    priority += 1
    actions.append({
        "priority": priority,
        "action": "Rédiger 3 articles de blog SEO ciblant les mots-clés à faible difficulté de votre secteur",
        "timeline": "Semaine 2-3",
        "effort": "Élevé",
        "impact": "Fort",
        "category": "SEO",
    })

    priority += 1
    actions.append({
        "priority": priority,
        "action": "Collecter 3 témoignages clients et les afficher sur votre page d'accueil et pages produits",
        "timeline": "Semaine 2",
        "effort": "Faible",
        "impact": "Fort",
        "category": "Vente",
    })

    priority += 1
    actions.append({
        "priority": priority,
        "action": "Créer une séquence email d'onboarding en 5 messages sur 10 jours pour convertir les nouveaux inscrits",
        "timeline": "Semaine 2-3",
        "effort": "Moyen",
        "impact": "Fort",
        "category": "Marketing",
    })

    priority += 1
    actions.append({
        "priority": priority,
        "action": "Optimiser la vitesse du site (images WebP, cache navigateur) pour passer sous les 3 secondes",
        "timeline": "Semaine 2",
        "effort": "Moyen",
        "impact": "Moyen",
        "category": "SEO",
    })

    priority += 1
    actions.append({
        "priority": priority,
        "action": "Créer 5 contenus vidéo courts (Reels / TikTok) présentant votre offre et votre personnalité de marque",
        "timeline": "Semaine 3",
        "effort": "Moyen",
        "impact": "Moyen",
        "category": "Contenu",
    })

    if data.monthlyBudget >= 100:
        priority += 1
        actions.append({
            "priority": priority,
            "action": "Mettre en place un programme de parrainage avec récompense double sens pour fidéliser vos clients",
            "timeline": "Semaine 3-4",
            "effort": "Faible",
            "impact": "Moyen",
            "category": "Vente",
        })

    return actions


def _generate_roi(data: AnalysisInput) -> list:
    """
    Generates a 12-month cumulative ROI projection.
    Formula: each month, estimate the leads generated from paid budget,
    multiply by average sale value to get revenue.
    Ensures non-zero output even for minimal budgets.
    """
    budget = data.monthlyBudget
    avg_sale = {
        "ecommerce": 45, "saas": 49, "service": 200,
        "website": 100, "consulting": 250, "content": 60,
        "application": 30, "other": 80,
    }.get(data.activityType, 80)

    # Paid budget portion (40% of monthly budget)
    paid_budget = budget * 0.40

    # Conversion rates by maturity
    ctr = {"idea": 0.015, "inprogress": 0.025, "launched": 0.04}.get(data.maturity, 0.02)

    # Cost per click estimate (€) by platform category
    cpc = {"saas": 2.5, "service": 2.0, "ecommerce": 0.8, "default": 1.5}
    avg_cpc = cpc.get(data.activityType, cpc["default"])

    # Monthly clicks from paid budget
    monthly_clicks = paid_budget / max(avg_cpc, 0.1)

    # Monthly leads (clicks × CTR)
    monthly_leads_base = monthly_clicks * ctr

    # Organic growth multiplier (SEO + content, starts small)
    organic_multiplier = {"idea": 0.1, "inprogress": 0.2, "launched": 0.4}.get(data.maturity, 0.2)

    # Lead-to-sale conversion
    lead_to_sale = {"saas": 0.15, "service": 0.20, "ecommerce": 0.03, "default": 0.10}.get(
        data.activityType, 0.10
    )

    roi_data = []
    cumulative = {"pessimistic": 0.0, "realistic": 0.0, "optimistic": 0.0}

    for month in range(1, 13):
        # Growth factor: progressive ramp-up capped at 2.5x
        growth = min(2.5, 1.0 + (month - 1) * 0.12)
        organic_growth = 1.0 + organic_multiplier * (month / 12)

        leads_realistic = monthly_leads_base * growth * organic_growth
        # Ensure at least 0.5 lead/month for any budget > 0
        leads_realistic = max(0.5, leads_realistic)

        sales_realistic = leads_realistic * lead_to_sale
        revenue_realistic = sales_realistic * avg_sale

        cumulative["realistic"] += revenue_realistic
        cumulative["optimistic"] += revenue_realistic * 1.7
        cumulative["pessimistic"] += revenue_realistic * 0.5

        roi_data.append({
            "month": month,
            "pessimistic": round(cumulative["pessimistic"]),
            "realistic": round(cumulative["realistic"]),
            "optimistic": round(cumulative["optimistic"]),
        })

    return roi_data


def _generate_summary(data: AnalysisInput, swot: dict) -> str:
    strengths = swot.get("strengths", [])
    opportunities = swot.get("opportunities", [])
    strength_txt = strengths[0].lower() if strengths else "votre expertise"
    opportunity_txt = opportunities[0].lower() if opportunities else "le marché digital"

    budget_advice = ""
    if data.monthlyBudget < 50:
        budget_advice = (
            "Avec un budget de {}€/mois, nous recommandons de concentrer 100% de vos efforts "
            "sur le SEO organique et les réseaux sociaux gratuits pour maximiser l'impact.".format(int(data.monthlyBudget))
        )
    elif data.monthlyBudget < 200:
        budget_advice = (
            "Avec {}€/mois, répartissez entre SEO/contenu (60%) et une campagne publicitaire "
            "ciblée (40%) pour un équilibre court/long terme.".format(int(data.monthlyBudget))
        )
    else:
        budget_advice = (
            "Avec {}€/mois, combinez publicité payante (50%) et contenu organique (50%) "
            "pour des résultats rapides et une croissance durable.".format(int(data.monthlyBudget))
        )

    return (
        "Votre projet {} présente un potentiel réel pour atteindre votre objectif de {}. "
        "{} Votre principal atout : {}. "
        "L'opportunité à saisir en priorité : {}. "
        "En suivant les actions priorisées ci-dessous, vous pouvez espérer un retour sur investissement "
        "de 2 à 5× dans les 6 premiers mois.".format(
            _activity_label(data.activityType),
            _goal_label(data.goal),
            budget_advice,
            strength_txt,
            opportunity_txt,
        )
    )


def _generate_key_metrics(data: AnalysisInput) -> list:
    budget = data.monthlyBudget
    # Realistic CPM by sector
    cpm = {"saas": 18, "service": 15, "ecommerce": 10, "default": 12}.get(data.activityType, 12)
    paid_portion = budget * 0.40
    impressions = int((paid_portion / max(cpm, 1)) * 1000)
    # Organic multiplier
    organic_extra = int(impressions * 0.3)
    total_reach = impressions + organic_extra

    # Leads: 2% of reach
    estimated_leads = max(1, int(total_reach * 0.02))

    # Revenue: leads × sale value × 15% close rate
    avg_sale = {"ecommerce": 45, "saas": 49, "service": 200, "default": 80}.get(data.activityType, 80)
    estimated_revenue = int(estimated_leads * avg_sale * 0.15)

    # ROI on paid spend
    roi_mult = round(estimated_revenue / max(paid_portion, 1), 1) if paid_portion > 0 else 0

    return [
        {"label": "Portée mensuelle estimée",   "value": f"{total_reach:,}".replace(",", " "), "trend": "+15-20%/mois"},
        {"label": "Leads estimés/mois",         "value": str(estimated_leads),                "trend": "+15%/mois"},
        {"label": "CA potentiel estimé",        "value": f"{estimated_revenue} €",            "trend": "+20%/trimestre"},
        {"label": "ROI publicité estimé",       "value": f"{roi_mult}×",                      "trend": "Croissant"},
    ]


def _generate_next_steps(data: AnalysisInput) -> list:
    steps = [
        "Créez votre compte Google Analytics 4 et connectez-le à votre site (gratuit, moins de 15 minutes)",
        "Ouvrez un compte sur {} Ads et définissez votre audience cible avant toute dépense".format(
            _main_channel(data.activityType)
        ),
        "Rédigez votre lead magnet (guide PDF ou template) pour capturer les premiers emails dès cette semaine",
        "Identifiez vos 3 principaux concurrents et analysez leur stratégie de contenu (gratuit avec SimilarWeb)",
        "Créez votre premier contenu vidéo de 30 secondes présentant votre solution et partagez-le aujourd'hui",
    ]
    if data.maturity == "launched":
        steps.insert(0, "Analysez vos 3 meilleures sources de clients actuels et doublez le budget alloué à chacune")
    if data.monthlyBudget < 100:
        steps.append("Rejoignez 3 groupes Facebook ou communautés Discord de votre secteur pour du trafic gratuit")
    return steps


def _goal_label(goal: str) -> str:
    return {
        "awareness": "notoriété",
        "sales":     "ventes",
        "leads":     "génération de leads",
        "traffic":   "trafic",
    }.get(goal, goal)


def _activity_label(activity: str) -> str:
    return {
        "ecommerce":   "e-commerce",
        "saas":        "SaaS",
        "service":     "de service en ligne",
        "website":     "de site vitrine",
        "application": "d'application mobile",
        "content":     "de création de contenu",
        "consulting":  "de conseil",
        "other":       "en ligne",
    }.get(activity, activity)


def _main_channel(activity: str) -> str:
    return {
        "saas":      "LinkedIn",
        "ecommerce": "Meta (Facebook/Instagram)",
        "service":   "Google",
        "consulting": "LinkedIn",
    }.get(activity, "Google/Meta")
