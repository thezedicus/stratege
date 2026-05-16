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
    base_actions = [
        {
            "priority": 1,
            "action": f"Créer ou optimiser votre page de destination (landing page) pour l'objectif '{_goal_label(data.goal)}'",
            "timeline": "Semaine 1",
            "effort": "Moyen",
            "impact": "Fort",
            "category": "Marketing",
        },
        {
            "priority": 2,
            "action": "Mettre en place un système de capture d'email avec lead magnet gratuit",
            "timeline": "Semaine 1-2",
            "effort": "Faible",
            "impact": "Fort",
            "category": "Marketing",
        },
        {
            "priority": 3,
            "action": f"Lancer la première campagne publicitaire sur {_main_channel(data.activityType)} avec {round(data.monthlyBudget * 0.4)}€",
            "timeline": "Semaine 2",
            "effort": "Moyen",
            "impact": "Fort",
            "category": "Publicité",
        },
        {
            "priority": 4,
            "action": "Rédiger et publier 3 articles de blog SEO ciblant les mots-clés à faible concurrence",
            "timeline": "Semaine 2-3",
            "effort": "Élevé",
            "impact": "Fort",
            "category": "SEO",
        },
        {
            "priority": 5,
            "action": "Installer et configurer Google Analytics 4 + Search Console pour un suivi précis",
            "timeline": "Semaine 1",
            "effort": "Faible",
            "impact": "Moyen",
            "category": "Stratégie",
        },
        {
            "priority": 6,
            "action": f"Créer une séquence email d'onboarding en 5 messages pour convertir les nouveaux inscrits",
            "timeline": "Semaine 2-3",
            "effort": "Moyen",
            "impact": "Fort",
            "category": "Marketing",
        },
        {
            "priority": 7,
            "action": "Mettre en place un programme de parrainage avec récompense pour les clients actuels",
            "timeline": "Semaine 3-4",
            "effort": "Faible",
            "impact": "Moyen",
            "category": "Vente",
        },
        {
            "priority": 8,
            "action": "Optimiser la vitesse du site (images WebP, cache, CDN) pour passer sous les 3 secondes",
            "timeline": "Semaine 2",
            "effort": "Moyen",
            "impact": "Moyen",
            "category": "SEO",
        },
        {
            "priority": 9,
            "action": "Créer 5 contenus Reel/TikTok présentant votre offre et votre personnalité de marque",
            "timeline": "Semaine 3",
            "effort": "Moyen",
            "impact": "Moyen",
            "category": "Contenu",
        },
        {
            "priority": 10,
            "action": "Mettre en place des témoignages clients visibles dès la homepage et les pages produits",
            "timeline": "Semaine 2",
            "effort": "Faible",
            "impact": "Fort",
            "category": "Vente",
        },
    ]

    if data.maturity == "idea":
        base_actions.insert(0, {
            "priority": 0,
            "action": "Valider votre idée avec 10 entretiens clients potentiels avant d'investir",
            "timeline": "Semaine 1",
            "effort": "Faible",
            "impact": "Fort",
            "category": "Stratégie",
        })

    return base_actions


def _generate_roi(data: AnalysisInput) -> list:
    base = data.monthlyBudget
    conversion_rate = {"idea": 0.02, "inprogress": 0.03, "launched": 0.05}.get(data.maturity, 0.03)
    avg_sale = {"ecommerce": 45, "saas": 49, "service": 200, "default": 80}.get(data.activityType, 80)

    roi_data = []
    cumulative_realistic = 0
    cumulative_optimistic = 0
    cumulative_pessimistic = 0

    for month in range(1, 13):
        growth_factor = 1 + (month - 1) * 0.15
        monthly_leads = int((base / avg_sale) * conversion_rate * growth_factor * 100)
        monthly_revenue_realistic = round(monthly_leads * avg_sale * conversion_rate * 10)
        cumulative_realistic += monthly_revenue_realistic

        roi_data.append({
            "month": month,
            "pessimistic": round(cumulative_realistic * 0.6),
            "realistic": cumulative_realistic,
            "optimistic": round(cumulative_realistic * 1.7),
        })

    return roi_data


def _generate_summary(data: AnalysisInput, swot: dict) -> str:
    strength = swot.get("strengths", ["votre expertise"])[0].lower() if swot.get("strengths") else "votre expertise"
    opportunity = swot.get("opportunities", ["le marché digital"])[0].lower() if swot.get("opportunities") else "le marché digital"

    return (
        f"Votre projet {_activity_label(data.activityType)} présente un potentiel réel pour atteindre votre objectif "
        f"de {_goal_label(data.goal)}. Avec un budget mensuel de {data.monthlyBudget}€, nous recommandons de concentrer "
        f"50% sur la publicité payante pour des résultats rapides, et 50% sur le SEO et le contenu pour une croissance "
        f"durable. Votre principal atout : {strength}. L'opportunité à saisir maintenant : {opportunity}. "
        f"En suivant le plan d'actions priorisé, vous pouvez espérer un ROI de 2-3x dans les 90 premiers jours."
    )


def _generate_key_metrics(data: AnalysisInput) -> list:
    cpm = {"ecommerce": 12, "saas": 18, "service": 15, "default": 14}.get(data.activityType, 14)
    estimated_reach = int((data.monthlyBudget * 0.5 / cpm) * 1000)
    estimated_leads = int(estimated_reach * 0.02)
    estimated_revenue = int(estimated_leads * {"ecommerce": 45, "saas": 49, "service": 200, "default": 80}.get(data.activityType, 80) * 0.3)

    return [
        {"label": "Portée mensuelle estimée", "value": f"{estimated_reach:,}".replace(",", " "), "trend": "+20%/mois"},
        {"label": "Leads estimés/mois", "value": str(estimated_leads), "trend": "+15%/mois"},
        {"label": "CA potentiel estimé", "value": f"{estimated_revenue} €", "trend": "+25%/trimestre"},
        {"label": "ROI publicité estimé", "value": "2.5-3x", "trend": "+0.3x par mois"},
    ]


def _generate_next_steps(data: AnalysisInput) -> list:
    return [
        "Créez votre compte Google Analytics 4 et connectez-le à votre site dès aujourd'hui (gratuit, 10 minutes)",
        f"Inscrivez-vous sur {_main_channel(data.activityType)} Ads et définissez votre audience cible",
        "Rédigez votre lead magnet (guide PDF ou template) pour commencer à capturer des emails",
        "Identifiez vos 3 concurrents principaux et analysez leur stratégie de contenu",
        "Prenez 3 témoignages clients existants et publiez-les avec photos sur votre site",
        "Créez votre premier contenu vidéo (Reel 30 secondes) présentant votre solution",
        "Installez un outil de heatmap (Hotjar gratuit) pour comprendre le comportement de vos visiteurs",
    ]


def _goal_label(goal: str) -> str:
    return {"awareness": "notoriété", "sales": "ventes", "leads": "génération de leads", "traffic": "trafic"}.get(goal, goal)


def _activity_label(activity: str) -> str:
    return {
        "ecommerce": "e-commerce", "saas": "SaaS", "service": "de service en ligne",
        "website": "de site vitrine", "application": "d'application mobile",
        "content": "de création de contenu", "consulting": "de conseil",
    }.get(activity, activity)


def _main_channel(activity: str) -> str:
    return {"saas": "LinkedIn", "ecommerce": "Facebook/Instagram", "service": "Google"}.get(activity, "Google/Meta")
