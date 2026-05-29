"""
Synthesis service — generates strategic score, summary, action plan, ROI and milestones.
Python 3.9 compatible.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def generate_synthesis(
    swot: dict,
    personas: list,
    marketing: Optional[dict],
    seo: Optional[dict],
    ads: Optional[dict],
    input_data: dict,
) -> dict:
    # Wrap the raw input dict in a simple namespace for attribute-style access
    class _D:
        pass
    data = _D()
    data.activityType = input_data.get("activityType", "other")
    data.goal = input_data.get("goal", "awareness")
    data.maturity = input_data.get("maturity", "idea")
    data.monthlyBudget = float(input_data.get("monthlyBudget", 0))

    actions   = _generate_actions(data, swot)
    roi       = _generate_roi(data)
    summary   = _generate_summary(data, swot)
    metrics   = _generate_key_metrics(data)
    next_steps = _generate_next_steps(data)
    score     = _compute_score(data, swot, seo, ads)
    priorities = _generate_priorities(data, swot)
    milestones = _generate_milestones(data)

    # Reshape keyMetrics from list to Record<label, value> for frontend
    key_metrics_dict = {m["label"]: m["value"] for m in metrics}

    # Reshape actions to match frontend's actionPlan shape
    action_plan = [
        {
            "action": a["action"],
            "priority": _map_priority(a.get("impact", "Moyen")),
            "timeline": a["timeline"],
            "expectedResult": "{} — Effort : {}".format(a.get("category", ""), a.get("effort", "")),
        }
        for a in actions
    ]

    return {
        "score":             score,
        "summary":           summary,
        "priorities":        priorities,
        "keyMetrics":        key_metrics_dict,
        "actionPlan":        action_plan,
        "monthlyMilestones": milestones,
        "roi":               roi,
        "nextSteps":         next_steps,
    }


def _map_priority(impact: str) -> str:
    return {"Fort": "haute", "Élevé": "haute", "Moyen": "moyenne", "Faible": "faible"}.get(impact, "moyenne")


def _compute_score(data: Any, swot: dict, seo: Optional[dict], ads: Optional[dict]) -> int:
    score = 40  # baseline

    # Maturity bonus
    score += {"idea": 0, "inprogress": 10, "launched": 20}.get(data.maturity, 0)

    # SWOT strengths vs threats
    strengths = len(swot.get("strengths", []))
    threats   = len(swot.get("threats", []))
    score += min(strengths * 4, 12)
    score -= min(threats * 2, 8)

    # Budget adequacy
    if data.monthlyBudget >= 500:
        score += 15
    elif data.monthlyBudget >= 100:
        score += 8
    elif data.monthlyBudget >= 30:
        score += 4

    # Bonus for having SEO and ads data
    if seo:
        score += 5
    if ads:
        score += 5

    return min(max(score, 10), 98)


def _generate_priorities(data: Any, swot: dict) -> List[str]:
    priorities = []
    goal_map = {
        "awareness": "Développer la notoriété via contenu organique + SEO",
        "sales":     "Optimiser le tunnel de conversion et les pages produits",
        "leads":     "Mettre en place un système de capture et nurturing email",
        "traffic":   "Lancer une stratégie SEO + publicité pour augmenter les visites",
    }
    if data.goal in goal_map:
        priorities.append(goal_map[data.goal])

    opps = swot.get("opportunities", [])
    if opps:
        priorities.append("Saisir l'opportunité : " + opps[0])

    if data.monthlyBudget >= 100:
        priorities.append("Allouer {}€ à la publicité payante dès le mois 1".format(round(data.monthlyBudget * 0.4)))

    priorities.append("Suivre les métriques clés chaque semaine (trafic, leads, CA)")
    return priorities


def _generate_milestones(data: Any) -> list:
    milestones = [
        {
            "month": 1,
            "objective": "Mise en place des outils d'analyse et lancement des premières actions",
            "kpi": "Google Analytics installé, 1ère campagne active",
        },
        {
            "month": 2,
            "objective": "Premiers résultats et ajustements de la stratégie",
            "kpi": "100+ visiteurs/semaine, 10+ leads capturés",
        },
        {
            "month": 3,
            "objective": "Accélération et optimisation des canaux performants",
            "kpi": "CAC mesuré, taux de conversion > 2%",
        },
        {
            "month": 6,
            "objective": "Croissance stable et récurrence des revenus",
            "kpi": "ROI publicitaire > 2×, liste email > 500 contacts",
        },
        {
            "month": 12,
            "objective": "Projet rentable avec processus d'acquisition reproductibles",
            "kpi": "CA mensuel récurrent, NPS > 40",
        },
    ]
    if data.maturity == "launched":
        milestones[0]["objective"] = "Analyser les sources de clients actuelles et doubler le budget sur les meilleures"
        milestones[0]["kpi"] = "Top 3 canaux identifiés, budget réalloué"
    return milestones


def _generate_actions(data: Any, swot: dict) -> list:
    actions = []
    priority = 0

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


def _generate_roi(data: Any) -> list:
    budget = data.monthlyBudget
    avg_sale = {
        "ecommerce": 45, "saas": 49, "service": 200,
        "website": 100, "consulting": 250, "content": 60,
        "application": 30, "other": 80,
    }.get(data.activityType, 80)

    paid_budget = budget * 0.40
    ctr = {"idea": 0.015, "inprogress": 0.025, "launched": 0.04}.get(data.maturity, 0.02)
    cpc_map = {"saas": 2.5, "service": 2.0, "ecommerce": 0.8}
    avg_cpc = cpc_map.get(data.activityType, 1.5)
    monthly_clicks = paid_budget / max(avg_cpc, 0.1)
    monthly_leads_base = monthly_clicks * ctr
    organic_multiplier = {"idea": 0.1, "inprogress": 0.2, "launched": 0.4}.get(data.maturity, 0.2)
    lead_to_sale = {"saas": 0.15, "service": 0.20, "ecommerce": 0.03}.get(data.activityType, 0.10)

    roi_data = []
    cumulative = {"pessimistic": 0.0, "realistic": 0.0, "optimistic": 0.0}

    for month in range(1, 13):
        growth = min(2.5, 1.0 + (month - 1) * 0.12)
        organic_growth = 1.0 + organic_multiplier * (month / 12)
        leads = max(0.5, monthly_leads_base * growth * organic_growth)
        revenue = leads * lead_to_sale * avg_sale
        cumulative["realistic"]  += revenue
        cumulative["optimistic"] += revenue * 1.7
        cumulative["pessimistic"] += revenue * 0.5
        roi_data.append({
            "month":       month,
            "pessimistic": round(cumulative["pessimistic"]),
            "realistic":   round(cumulative["realistic"]),
            "optimistic":  round(cumulative["optimistic"]),
        })

    return roi_data


def _generate_summary(data: Any, swot: dict) -> str:
    strengths    = swot.get("strengths", [])
    opportunities = swot.get("opportunities", [])
    strength_txt    = strengths[0].lower()    if strengths    else "votre expertise"
    opportunity_txt = opportunities[0].lower() if opportunities else "le marché digital"

    if data.monthlyBudget < 50:
        budget_advice = "Avec {}€/mois, concentrez 100% de vos efforts sur le SEO organique et les réseaux sociaux gratuits.".format(int(data.monthlyBudget))
    elif data.monthlyBudget < 200:
        budget_advice = "Avec {}€/mois, répartissez SEO/contenu (60%) et publicité ciblée (40%).".format(int(data.monthlyBudget))
    else:
        budget_advice = "Avec {}€/mois, combinez publicité payante (50%) et contenu organique (50%) pour des résultats rapides et durables.".format(int(data.monthlyBudget))

    return (
        "Votre projet {} présente un potentiel réel pour atteindre votre objectif de {}. "
        "{} Votre principal atout : {}. "
        "L'opportunité prioritaire : {}. "
        "En suivant les actions ci-dessous, visez un ROI de 2 à 5× dans les 6 premiers mois.".format(
            _activity_label(data.activityType),
            _goal_label(data.goal),
            budget_advice,
            strength_txt,
            opportunity_txt,
        )
    )


def _generate_key_metrics(data: Any) -> list:
    budget = data.monthlyBudget
    cpm = {"saas": 18, "service": 15, "ecommerce": 10}.get(data.activityType, 12)
    paid_portion = budget * 0.40
    impressions = int((paid_portion / max(cpm, 1)) * 1000)
    total_reach = impressions + int(impressions * 0.3)
    estimated_leads = max(1, int(total_reach * 0.02))
    avg_sale = {"ecommerce": 45, "saas": 49, "service": 200}.get(data.activityType, 80)
    estimated_revenue = int(estimated_leads * avg_sale * 0.15)
    roi_mult = round(estimated_revenue / max(paid_portion, 1), 1) if paid_portion > 0 else 0

    return [
        {"label": "Portée mensuelle estimée", "value": f"{total_reach:,}".replace(",", " "), "trend": "+15-20%/mois"},
        {"label": "Leads estimés/mois",        "value": str(estimated_leads),                     "trend": "+15%/mois"},
        {"label": "CA potentiel estimé",       "value": f"{estimated_revenue} €",                 "trend": "+20%/trimestre"},
        {"label": "ROI publicité estimé",      "value": f"{roi_mult}×",                           "trend": "Croissant"},
    ]


def _generate_next_steps(data: Any) -> list:
    steps = [
        "Créez votre compte Google Analytics 4 et connectez-le à votre site (gratuit, moins de 15 minutes)",
        "Ouvrez un compte sur {} Ads et définissez votre audience cible avant toute dépense".format(_main_channel(data.activityType)),
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
    return {"awareness": "notoriété", "sales": "ventes", "leads": "génération de leads", "traffic": "trafic"}.get(goal, goal)


def _activity_label(activity: str) -> str:
    return {
        "ecommerce": "e-commerce", "saas": "SaaS", "service": "de service en ligne",
        "website": "de site vitrine", "application": "d'application mobile",
        "content": "de création de contenu", "consulting": "de conseil", "other": "en ligne",
    }.get(activity, activity)


def _main_channel(activity: str) -> str:
    return {"saas": "LinkedIn", "ecommerce": "Meta (Facebook/Instagram)", "service": "Google", "consulting": "LinkedIn"}.get(activity, "Google/Meta")
