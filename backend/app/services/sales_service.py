from app.models.schemas import AnalysisInput

def generate_sales(data: AnalysisInput, personas: list) -> dict:
    scripts = [
        {
            "framework": "SPIN Selling",
            "intro": f"Bonjour [Prénom], je vous contacte car nous aidons les {data.activityType == 'saas' and 'entreprises' or 'entrepreneurs'} à {_goal_phrase(data.goal)} sans effort supplémentaire.",
            "qualification": "Pour mieux vous aider, j'aimerais comprendre votre situation actuelle. Quelle est votre principale source de clients aujourd'hui ? Êtes-vous satisfait des résultats ?",
            "pitch": f"Grâce à notre approche, nos clients dans votre secteur ont en moyenne multiplié leur {_goal_metric(data.goal)} par 2,5 en 90 jours, avec un budget maîtrisé de {data.monthlyBudget}€/mois.",
            "objections": [
                {"objection": "C'est trop cher pour moi.", "response": f"Je comprends. Sur un budget de {data.monthlyBudget}€, nos clients génèrent en moyenne 3x leur investissement initial. Voulez-vous que je vous montre comment ?"},
                {"objection": "J'ai déjà essayé et ça n'a pas marché.", "response": "Qu'est-ce qui n'a pas fonctionné exactement ? Souvent c'est une question de ciblage ou de timing. Nous pouvons analyser ça ensemble."},
                {"objection": "Je dois en parler à mon associé.", "response": "Bien sûr ! Voulez-vous que je prépare une synthèse chiffrée de 2 pages pour faciliter votre décision ensemble ?"},
                {"objection": "Je n'ai pas le temps en ce moment.", "response": "Je comprends — c'est justement pourquoi notre solution est conçue pour être opérationnelle en 48h maximum, sans vous mobiliser."},
            ],
            "closing": "Voici ce que je vous propose : on commence par un essai sur 30 jours. Si vous ne voyez pas de résultats tangibles, vous ne payez rien. Qu'en pensez-vous ?",
            "followUp": f"Suite à notre échange, je vous envoie ci-joint les 3 cas clients les plus proches de votre situation avec les résultats obtenus. Disponible pour un appel de 20 min cette semaine ?",
        },
        {
            "framework": "Challenger Sale",
            "intro": f"La plupart des {data.activityType == 'saas' and 'entreprises' or 'entrepreneurs'} pensent que le problème est le budget. En réalité, 78% des échecs viennent d'un positionnement inadapté. Je vous explique pourquoi.",
            "qualification": "Avez-vous déjà calculé combien vous coûte réellement l'absence d'une stratégie {_goal_phrase(data.goal)} structurée ? Je vous aide à chiffrer ça en 5 minutes.",
            "pitch": f"Voici ce que font les leaders de votre marché que vous ne faites probablement pas encore : ils concentrent 80% de leur budget ({data.monthlyBudget * 0.8:.0f}€) sur les 2-3 canaux qui génèrent 90% des résultats.",
            "objections": [
                {"objection": "On gère ça en interne.", "response": "Excellent. Est-ce que votre équipe interne a le temps de tester 15 variations de message par semaine et d'analyser les données en temps réel ?"},
                {"objection": "On va attendre de voir.", "response": "Pendant que vous attendez, vos concurrents occupent les positions sur Google et capturent vos clients. Le coût de l'inaction est souvent supérieur au coût de l'action."},
                {"objection": "Montrez-moi d'abord des résultats.", "response": "Absolument. Voici 3 cas dans votre secteur avec les chiffres exacts. Quel aspect vous intéresse le plus ?"},
            ],
            "closing": "Regardons ensemble où vous en êtes dans 90 jours si vous faites X versus si vous continuez comme aujourd'hui. La différence justifie amplement l'investissement. On commence quand ?",
            "followUp": "J'ai préparé une analyse personnalisée de votre marché avec les 5 opportunités les plus rapides à saisir. Je vous l'envoie ?",
        },
        {
            "framework": "SONCAS",
            "intro": f"Vous cherchez à {_goal_phrase(data.goal)} de façon sécurisée et rentable. Nous travaillons avec des profils comme le vôtre depuis plusieurs années avec des résultats mesurables.",
            "qualification": "Qu'est-ce qui est le plus important pour vous : la sécurité de l'investissement, la rapidité des résultats, ou le confort de la mise en place ?",
            "pitch": _soncas_pitch(data),
            "objections": [
                {"objection": "Je ne suis pas sûr que ça marche pour moi.", "response": "Sécurité avant tout : c'est pourquoi nous commençons par un audit gratuit pour valider le potentiel spécifiquement dans votre cas avant tout engagement."},
                {"objection": "Vos concurrents sont moins chers.", "response": "Le prix bas cache souvent des coûts cachés. Notre approche premium vous économise en moyenne 8h/semaine, soit 400€/mois de valeur temps."},
                {"objection": "Je veux réfléchir.", "response": "Bien sûr. Pour vous aider à structurer votre réflexion, voici les 3 questions clés à vous poser avant de décider."},
            ],
            "closing": "Pour votre confort total : on commence avec notre formule sans engagement. Résultats en 30 jours, ou on rembourse. C'est notre engagement qualité.",
            "followUp": "J'ai pensé à vous en préparant ce document — il répond exactement aux questions que vous m'aviez posées. Votre avis ?",
        },
    ]

    closing_techniques = [
        {
            "name": "Closing par l'alternative",
            "description": "Proposez deux options favorables, évitez le oui/non binaire.",
            "example": "Vous préférez commencer lundi ou mercredi de cette semaine ?",
        },
        {
            "name": "Closing par l'urgence",
            "description": "Créez une raison valide de décider maintenant.",
            "example": "Notre tarif de lancement se termine vendredi. Après, c'est +30%. Je vous réserve une place ?",
        },
        {
            "name": "Closing par résumé de valeur",
            "description": "Récapitulez tous les bénéfices avant de demander la décision.",
            "example": "Donc vous obtenez : X, Y, Z, garantie 30 jours, et le support prioritaire. Pour {budget}€/mois. On y va ?",
        },
        {
            "name": "Closing Trial",
            "description": "Proposez un essai à faible risque pour lever les blocages.",
            "example": "Et si on testait sur 2 semaines sans engagement ? Vous voyez les résultats, vous décidez.",
        },
        {
            "name": "Closing par concession",
            "description": "Offrez quelque chose en échange d'une décision immédiate.",
            "example": "Si vous signez aujourd'hui, j'inclus le module premium offert (valeur 150€). Marché conclu ?",
        },
    ]

    message_templates = [
        {
            "channel": "Email froid",
            "subject": f"[{data.activityType.upper()}] Comment {_goal_phrase(data.goal)} x3 en 90 jours",
            "body": f"""Bonjour [Prénom],

Je serai direct : la plupart des {data.activityType == 'saas' and 'SaaS' or 'projets'} échouent à {_goal_phrase(data.goal)} non par manque de budget, mais par manque de stratégie.

En analysant votre secteur, j'ai identifié 3 leviers que vous n'exploitez probablement pas encore.

Je vous propose 20 minutes pour vous partager l'analyse — sans engagement.

[Lien calendrier]

Cordialement,
[Votre nom]""",
        },
        {
            "channel": "LinkedIn InMail",
            "subject": "Question rapide sur votre stratégie",
            "body": f"""Bonjour [Prénom],

J'ai vu votre profil et votre travail sur [Élément spécifique].

Une question : comment gérez-vous actuellement {_goal_phrase(data.goal)} ?

J'aide des profils similaires à structurer ça efficacement avec {data.monthlyBudget}€/mois. Je suis curieux de savoir si ça fait écho à vos défis actuels.

Ouvert à un échange de 15 min ?""",
        },
        {
            "channel": "SMS / WhatsApp",
            "subject": "",
            "body": f"Bonjour [Prénom] ! Suite à notre échange : j'ai préparé votre analyse personnalisée. 3 actions concrètes pour {_goal_phrase(data.goal)} dès cette semaine. Je vous l'envoie par email ?",
        },
        {
            "channel": "Relance post-démo",
            "subject": "Votre analyse personnalisée + prochaine étape",
            "body": f"""Bonjour [Prénom],

Merci pour notre échange de [date/heure].

Suite à notre discussion, j'ai finalisé votre analyse avec :
✅ Les 3 actions prioritaires pour votre cas
✅ L'estimation ROI sur 6 mois
✅ La feuille de route semaine par semaine

Voir l'analyse complète : [Lien]

Question directe : qu'est-ce qui vous retient de passer à l'étape suivante ?

[Votre nom]""",
        },
    ]

    return {
        "scripts": scripts,
        "closingTechniques": closing_techniques,
        "messageTemplates": message_templates,
    }


def _goal_phrase(goal: str) -> str:
    return {
        "awareness": "développer votre notoriété",
        "sales": "augmenter vos ventes",
        "leads": "générer des prospects qualifiés",
        "traffic": "augmenter votre trafic",
    }.get(goal, "atteindre vos objectifs")


def _goal_metric(goal: str) -> str:
    return {
        "awareness": "visibilité",
        "sales": "chiffre d'affaires",
        "leads": "génération de leads",
        "traffic": "trafic organique",
    }.get(goal, "performance")


def _soncas_pitch(data: AnalysisInput) -> str:
    return (
        f"Sécurité : garantie 30 jours sans question. "
        f"Orgueil : rejoignez les leaders de votre secteur. "
        f"Nouveauté : technologie de pointe adaptée à votre budget de {data.monthlyBudget}€. "
        f"Confort : clé en main en 48h. "
        f"Argent : ROI moyen de 300% en 90 jours. "
        f"Sympathie : une équipe dédiée à votre succès."
    )
