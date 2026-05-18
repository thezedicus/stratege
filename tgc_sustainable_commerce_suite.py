#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║         TGC SUSTAINABLE COMMERCE SUITE v1.0                              ║
║  Analyse RSE | Proposition de Valeur | Segmentation Clients | Veille      ║
╚═══════════════════════════════════════════════════════════════════════════╝

Synthèse des documents professionnels :
- Proposition de valeur (Apple, Tesla, L'Oréal)
- RSE et ISO 26000
- Gestion portefeuille clients (CLV, RFM, Pareto)
- Plan d'actions (PESTEL, SWOT)
- Veille stratégique et détection greenwashing
- Négociation commerciale (BATNA, ZOPA, SONCAS)

Auteur : TGC
Licence : MIT
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import statistics

# ============================================================================
# SECTION 1 : PROPOSITION DE VALEUR
# ============================================================================

class PropositionDeValeur:
    """Analyse et construction de propositions de valeur robustes."""
    
    DIMENSIONS = {
        'fonctionnelle': 'Performance, simplicité d\'usage, gain de temps',
        'economique': 'Coût total, économies réalisées, rentabilité',
        'emotionnelle': 'Sécurité, plaisir, fierté, confiance',
        'symbolique': 'Image, appartenance, statut, valeur personnelle'
    }
    
    EXEMPLES_MARQUES = {
        'Apple': {
            'slogan': 'L\'expérience est le produit',
            'dimensions': {
                'fonctionnelle': 'Performance + simplicité d\'usage',
                'economique': 'Premium pricing justifié',
                'emotionnelle': 'Statut, fierté d\'appartenance',
                'symbolique': 'Innovation, qualité, design iconic'
            }
        },
        'Tesla': {
            'slogan': 'Voitures électriques, sans compromis',
            'dimensions': {
                'fonctionnelle': 'Autonomie + performances sportives',
                'economique': 'Coûts énergétiques réduits',
                'emotionnelle': 'Impact environnemental positif',
                'symbolique': 'Leadership technologique, vision future'
            }
        },
        'L\'Oréal': {
            'slogan': 'Parce que vous le valez bien',
            'dimensions': {
                'fonctionnelle': 'Produits innovants et sûrs',
                'economique': 'Gamme à tous les prix',
                'emotionnelle': 'Empowerment, confiance en soi',
                'symbolique': 'Inclusivité, diversité, auto-affirmation'
            }
        },
        'Too Good To Go': {
            'slogan': 'Sauvez de la nourriture',
            'dimensions': {
                'fonctionnelle': 'Accès à des produits de qualité',
                'economique': '~70% de réduction',
                'emotionnelle': 'Impact environnemental personnel',
                'symbolique': 'Responsabilité, communauté de change-makers'
            }
        }
    }
    
    def __init__(self, nom_entreprise: str, produit: str, public_cible: str):
        self.nom = nom_entreprise
        self.produit = produit
        self.public_cible = public_cible
        self.dimensions = {}
        self.slogan = ""
        self.points_differenciateurs = []
    
    def ajouter_dimension(self, dimension: str, contenu: str) -> None:
        """Ajoute une dimension de valeur."""
        if dimension not in self.DIMENSIONS:
            raise ValueError(f"Dimension inconnue. Utilisez : {list(self.DIMENSIONS.keys())}")
        self.dimensions[dimension] = contenu
    
    def definir_slogan(self, slogan: str) -> None:
        """Définit le slogan principal (max 7 mots, mémorable)."""
        words = slogan.split()
        if len(words) > 7:
            print(f"⚠️  Slogan long ({len(words)} mots). Idéal : 7 mots max pour la mémorisation.")
        self.slogan = slogan
    
    def ajouter_differenciateur(self, point: str) -> None:
        """Ajoute un point de différenciation vs concurrence."""
        self.points_differenciateurs.append(point)
    
    def generer_rapport(self) -> str:
        """Génère un rapport structuré de la proposition de valeur."""
        rapport = f"""
╔════════════════════════════════════════════════════════════════╗
║  PROPOSITION DE VALEUR : {self.nom}
╚════════════════════════════════════════════════════════════════╝

📊 CONTEXTE
───────────
Entreprise       : {self.nom}
Produit/Service  : {self.produit}
Public cible     : {self.public_cible}

💡 SLOGAN PRINCIPAL
───────────────────
"{self.slogan}"

🎯 DIMENSIONS DE LA VALEUR
──────────────────────────
"""
        for dim, contenu in self.dimensions.items():
            rapport += f"\n✓ {dim.upper():15} : {contenu}"
        
        if self.points_differenciateurs:
            rapport += f"\n\n🔥 POINTS DE DIFFÉRENCIATION"
            rapport += "\n──────────────────────────\n"
            for i, point in enumerate(self.points_differenciateurs, 1):
                rapport += f"{i}. {point}\n"
        
        rapport += "\n" + "="*60 + "\n"
        return rapport
    
    @staticmethod
    def afficher_exemples() -> str:
        """Affiche les exemples de marques avec leurs propositions."""
        texte = "\n📚 EXEMPLES DE PROPOSITIONS DE VALEUR RÉUSSIES\n"
        texte += "=" * 65 + "\n"
        for marque, details in PropositionDeValeur.EXEMPLES_MARQUES.items():
            texte += f"\n🏢 {marque}\n"
            texte += f"   Slogan : \"{details['slogan']}\"\n"
            texte += "   Dimensions :\n"
            for dim, desc in details['dimensions'].items():
                texte += f"     • {dim.capitalize():15} : {desc}\n"
        return texte


# ============================================================================
# SECTION 2 : SEGMENTATION CLIENTS & CLV
# ============================================================================

class SegmentationClients:
    """Analyse RFM, CLV, loi de Pareto (80/20) et segmentation ABC."""
    
    def __init__(self):
        self.clients = {}  # {id: {nom, date_derniere_achat, nb_achats, montant_total}}
    
    def ajouter_client(self, client_id: str, nom: str, date_dernier_achat: str,
                       nb_achats: int, montant_total: float) -> None:
        """Ajoute un client avec ses données transactionnelles."""
        self.clients[client_id] = {
            'nom': nom,
            'date_dernier_achat': datetime.strptime(date_dernier_achat, '%Y-%m-%d'),
            'nb_achats': nb_achats,
            'montant_total': montant_total
        }
    
    def calculer_rfm(self, date_reference: datetime = None) -> Dict[str, Dict]:
        """
        Calcule RFM : Récence, Fréquence, Montant.
        Retourne un scoring 1-5 par dimension.
        """
        if date_reference is None:
            date_reference = datetime.now()
        
        rfm_data = {}
        recences = []
        frequences = []
        montants = []
        
        # Calcul des valeurs brutes
        for cid, data in self.clients.items():
            jours_depuis = (date_reference - data['date_dernier_achat']).days
            recences.append(jours_depuis)
            frequences.append(data['nb_achats'])
            montants.append(data['montant_total'])
        
        if not recences:
            return rfm_data
        
        # Quantiles pour scoring
        rec_quartiles = sorted(list(set([min(recences)] + list(statistics.quantiles(recences, n=4)) + [max(recences)])))
        freq_quartiles = sorted(list(set([min(frequences)] + list(statistics.quantiles(frequences, n=4)) + [max(frequences)])))
        mont_quartiles = sorted(list(set([min(montants)] + list(statistics.quantiles(montants, n=4)) + [max(montants)])))
        
        # Scoring
        for cid, data in self.clients.items():
            jours = (date_reference - data['date_dernier_achat']).days
            
            # Récence : moins recent = meilleur score (1=très ancien, 5=très récent)
            r_count = sum(1 for q in rec_quartiles if jours > q)
            r_score = max(1, 5 - r_count)
            
            # Fréquence : plus élevé = meilleur score
            f_count = sum(1 for q in freq_quartiles if data['nb_achats'] >= q)
            f_score = min(5, max(1, f_count))
            
            # Montant : plus élevé = meilleur score
            m_count = sum(1 for q in mont_quartiles if data['montant_total'] >= q)
            m_score = min(5, max(1, m_count))
            
            rfm_data[cid] = {
                'nom': data['nom'],
                'recence_jours': jours,
                'recence_score': r_score,
                'frequence': data['nb_achats'],
                'frequence_score': f_score,
                'montant': data['montant_total'],
                'montant_score': m_score,
                'score_rfm': (r_score + f_score + m_score) / 3
            }
        
        return rfm_data
    
    def segmentation_abc(self) -> Dict[str, List[str]]:
        """
        Loi de Pareto (80/20) : segmente en 3 groupes ABC.
        A : 20% des clients = 80% du CA
        B : Clients intermédiaires
        C : Clients faibles contribution
        """
        sorted_clients = sorted(
            self.clients.items(),
            key=lambda x: x[1]['montant_total'],
            reverse=True
        )
        
        total_ca = sum(c[1]['montant_total'] for c in sorted_clients)
        cumul_ca = 0
        segments = {'A': [], 'B': [], 'C': []}
        
        for cid, data in sorted_clients:
            cumul_ca += data['montant_total']
            pct = (cumul_ca / total_ca) * 100
            
            if pct <= 80:
                segments['A'].append(cid)
            elif pct <= 95:
                segments['B'].append(cid)
            else:
                segments['C'].append(cid)
        
        return segments
    
    def calculer_churn_nps(self, clients_actifs_derniers_mois: int = 12,
                           clients_satisfaits: int = None) -> Dict[str, float]:
        """
        Churn rate : % clients perdus
        NPS : Net Promoter Score (simplifié, nécessite données satisfaction réelles)
        """
        churn = (1 - len(self.clients) / max(len(self.clients), 1)) * 100
        
        nps = 50 if clients_satisfaits is None else (clients_satisfaits * 100 / max(len(self.clients), 1))
        
        return {
            'churn_rate': round(churn, 2),
            'nps_estimated': round(nps, 1)
        }
    
    def generer_rapport_segmentation(self) -> str:
        """Rapport complet de segmentation."""
        rfm = self.calculer_rfm()
        abc = self.segmentation_abc()
        churn_nps = self.calculer_churn_nps()
        
        rapport = f"""
╔════════════════════════════════════════════════════════════════╗
║  SEGMENTATION CLIENTS & ANALYSE CLV
╚════════════════════════════════════════════════════════════════╝

📊 ANALYSE RFM (Récence-Fréquence-Montant)
────────────────────────────────────────────
"""
        
        for cid, rfm_data in sorted(rfm.items(), key=lambda x: x[1]['score_rfm'], reverse=True)[:10]:
            rapport += f"\n{rfm_data['nom']:<20} | "
            rapport += f"Récence: {rfm_data['recence_jours']:3d}j (score:{rfm_data['recence_score']}) | "
            rapport += f"Fréquence: {rfm_data['frequence']} (score:{rfm_data['frequence_score']}) | "
            rapport += f"Montant: €{rfm_data['montant']:.0f} (score:{rfm_data['montant_score']}) | "
            rapport += f"RFM: {rfm_data['score_rfm']:.1f}/5"
        
        rapport += f"\n\n🎯 SEGMENTATION ABC (Loi de Pareto 80/20)"
        rapport += f"\n───────────────────────────────────────────"
        rapport += f"\n✓ Segment A ({len(abc['A'])} clients) : 80% du CA - PRIORITÉ RÉTENTION"
        rapport += f"\n✓ Segment B ({len(abc['B'])} clients) : 15% du CA - DÉVELOPPEMENT"
        rapport += f"\n✓ Segment C ({len(abc['C'])} clients) : 5% du CA  - AUTOMATION"
        
        rapport += f"\n\n📈 INDICATEURS CLÉS"
        rapport += f"\n─────────────────"
        rapport += f"\nChurn Rate        : {churn_nps['churn_rate']}%"
        rapport += f"\nNPS (estimé)      : {churn_nps['nps_estimated']}/100"
        rapport += f"Nombre clients    : {len(self.clients)}"
        
        rapport += "\n" + "="*60 + "\n"
        return rapport


# ============================================================================
# SECTION 3 : RSE & ISO 26000
# ============================================================================

class MatriceRSE:
    """Matrice d'intégration RSE : dimensions économique, sociale, environnementale."""
    
    DIMENSIONS_RSE = {
        'economique': {
            'elements': ['Rentabilité', 'Création d\'emploi', 'Innovation', 'Gouvernance'],
            'normes': ['ISO 26000', 'Pacte Mondial ONU', 'Reporting DPEF']
        },
        'social': {
            'elements': ['Bien-être salarié', 'Santé & sécurité', 'Formation', 'Diversité'],
            'normes': ['Loi Grenelle II', 'Convention ILO', 'Code du Travail']
        },
        'environnemental': {
            'elements': ['Émissions carbone', 'Eau', 'Déchets', 'Biodiversité'],
            'normes': ['Protocole Kyoto', 'ISO 14001', 'Loi AGEC', 'Plan vigilance']
        }
    }
    
    def __init__(self, nom_entreprise: str):
        self.nom = nom_entreprise
        self.scores = {}
    
    def evaluer_maturite(self, dimension: str, score: int) -> None:
        """Score de maturité 1-5 par dimension RSE."""
        if dimension not in self.DIMENSIONS_RSE:
            raise ValueError(f"Dimension inconnue : {dimension}")
        if not 1 <= score <= 5:
            raise ValueError("Score doit être entre 1 et 5")
        self.scores[dimension] = score
    
    def generer_rapport_rse(self) -> str:
        """Rapport d'audit RSE simplifié."""
        rapport = f"""
╔════════════════════════════════════════════════════════════════╗
║  MATRICE RSE & ISO 26000 : {self.nom}
╚════════════════════════════════════════════════════════════════╝

📋 NORMES & LÉGISLATION APPLICABLES
────────────────────────────────────
✓ ISO 26000 (Lignes directrices RSE)
✓ Pacte Mondial ONU (10 principes)
✓ Lois Grenelle II & Agec (Économie circulaire)
✓ Plan de vigilance (Devoir de diligence)
✓ DPEF (Déclaration Performance Extra-Financière)

"""
        
        for dimension, content in self.DIMENSIONS_RSE.items():
            score = self.scores.get(dimension, 0)
            barre = "█" * score + "░" * (5 - score)
            rapport += f"\n{dimension.upper():20} [{barre}] {score}/5\n"
            rapport += f"  Éléments        : {', '.join(content['elements'])}\n"
            rapport += f"  Normes          : {', '.join(content['normes'])}\n"
        
        score_moyen = sum(self.scores.values()) / len(self.scores) if self.scores else 0
        rapport += f"\n\n📊 SCORE GLOBAL RSE : {score_moyen:.1f}/5"
        
        if score_moyen >= 4:
            rapport += " ✅ LEADER RSE"
        elif score_moyen >= 3:
            rapport += " 🟡 EN TRANSITION"
        else:
            rapport += " ⚠️  RATTRAPAGE NÉCESSAIRE"
        
        rapport += "\n" + "="*60 + "\n"
        return rapport


# ============================================================================
# SECTION 4 : NÉGOCIATION COMMERCIALE
# ============================================================================

class NegociationCommerciale:
    """6 phases de négociation : BATNA, ZOPA, SONCAS, arguments."""
    
    SONCAS = {
        'S': 'Sécurité',
        'O': 'Orgueil',
        'N': 'Nouveauté',
        'C': 'Confort',
        'A': 'Argent',
        'S2': 'Sympathie'
    }
    
    PHASES = [
        '1. Préparation (BATNA, ZOPA)',
        '2. Ouverture (Ancrage)',
        '3. Échanges d\'informations',
        '4. Argumentation (Concessions conditionnelles)',
        '5. Clôture de l\'accord',
        '6. Bilan post-négociation'
    ]
    
    def __init__(self, nom_nego: str, partie_a: str, partie_b: str):
        self.nom = nom_nego
        self.partie_a = partie_a
        self.partie_b = partie_b
        self.batna_a = ""
        self.batna_b = ""
        self.zopa = None
    
    def definir_batna(self, partie: str, batna: str) -> None:
        """BATNA : Best Alternative To Negotiated Agreement."""
        if partie == 'A':
            self.batna_a = batna
        elif partie == 'B':
            self.batna_b = batna
    
    def definir_zopa(self, prix_min: float, prix_max: float) -> None:
        """ZOPA : Zone Of Possible Agreement."""
        self.zopa = {'min': prix_min, 'max': prix_max, 'amplitude': prix_max - prix_min}
    
    def generer_rapport_nego(self) -> str:
        """Rapport structuré de la négociation."""
        rapport = f"""
╔════════════════════════════════════════════════════════════════╗
║  NÉGOCIATION COMMERCIALE : {self.nom}
╚════════════════════════════════════════════════════════════════╝

👥 PARTIES EN PRÉSENCE
──────────────────────
Partie A : {self.partie_a}
Partie B : {self.partie_b}

🎯 STRATÉGIE PRÉPARATOIRE
─────────────────────────
BATNA {self.partie_a:20} : {self.batna_a}
BATNA {self.partie_b:20} : {self.batna_b}
"""
        
        if self.zopa:
            rapport += f"\n📊 ZONE D'ACCORD (ZOPA)"
            rapport += f"\n──────────────────────"
            rapport += f"\nPrix minimum : €{self.zopa['min']:.2f}"
            rapport += f"\nPrix maximum : €{self.zopa['max']:.2f}"
            rapport += f"\nAmplitude    : €{self.zopa['amplitude']:.2f} ({(self.zopa['amplitude']/self.zopa['max']*100):.1f}%)"
        
        rapport += f"\n\n💬 TACTIQUES SONCAS"
        rapport += f"\n───────────────────"
        for code, valeur in self.SONCAS.items():
            rapport += f"\n✓ {code}: {valeur}"
        
        rapport += f"\n\n📈 6 PHASES DE NÉGOCIATION"
        rapport += f"\n──────────────────────────"
        for phase in self.PHASES:
            rapport += f"\n  {phase}"
        
        rapport += "\n" + "="*60 + "\n"
        return rapport


# ============================================================================
# SECTION 5 : VEILLE STRATÉGIQUE & DÉTECTION GREENWASHING
# ============================================================================

class VeilleStrategique:
    """Détection tendances, greenwashing, rainbow washing, feminism washing."""
    
    GREENWASHING_PATTERNS = [
        r"(100\%\s+)?écologique",
        r"(complètement\s+)?vert|green",
        r"responsable.*environn",
        r"durable",
        r"carbon.*neutral|neutre.*carbone",
        r"zéro.*déchet|zero.*waste",
        r"bio|organic"
    ]
    
    RAINBOW_WASHING_PATTERNS = [
        r"inclusiv",
        r"diversité|diversity",
        r"lgbtq|lgbtqia",
        r"drapeaux.*arc|rainbow.*flag",
        r"mois.*fierté|pride.*month"
    ]
    
    FEMINISM_WASHING_PATTERNS = [
        r"fémin|empowerment",
        r"femmes|women's",
        r"égalité.*genre|gender.*equality",
        r"droits.*femm|women's.*right"
    ]
    
    def __init__(self):
        self.articles = []
    
    def ajouter_article(self, titre: str, contenu: str, source: str, date: str) -> None:
        """Ajoute un article de veille."""
        self.articles.append({
            'titre': titre,
            'contenu': contenu,
            'source': source,
            'date': date
        })
    
    def detecter_greenwashing(self, texte: str) -> Tuple[bool, List[str]]:
        """Détecte patterns de greenwashing sans preuve factuelle."""
        matches = []
        for pattern in self.GREENWASHING_PATTERNS:
            if re.search(pattern, texte.lower()):
                matches.append(pattern)
        
        risque = len(matches) >= 3 and not any(
            keyword in texte.lower() 
            for keyword in ['certifié', 'vérifié', 'audit', 'certificat', 'norme']
        )
        
        return risque, matches
    
    def generer_rapport_veille(self) -> str:
        """Rapport d'analyse de veille."""
        rapport = f"""
╔════════════════════════════════════════════════════════════════╗
║  VEILLE STRATÉGIQUE & ANALYSE DE RISQUES
╚════════════════════════════════════════════════════════════════╝

📰 ARTICLES ANALYSÉS : {len(self.articles)}
────────────────────────────────────────────────

"""
        
        for article in self.articles:
            risque, patterns = self.detecter_greenwashing(article['contenu'])
            rapport += f"\n{article['titre']}"
            rapport += f"\n  Source  : {article['source']} ({article['date']})"
            rapport += f"\n  Risque  : {'⚠️  GREENWASHING DÉTECTÉ' if risque else '✓ Conforme'}"
            if patterns:
                rapport += f"\n  Patterns: {', '.join(patterns[:2])}"
        
        rapport += f"\n\n🎯 PRINCIPES DE VEILLE (4 Piliers)"
        rapport += f"\n──────────────────────────────────"
        rapport += f"\n1️⃣  CAPTER     : Collecter données (NewsAPI, réseaux sociaux)"
        rapport += f"\n2️⃣  FILTRER    : Qualifier pertinence & fiabilité"
        rapport += f"\n3️⃣  ANALYSER   : Détecter tendances & anomalies"
        rapport += f"\n4️⃣  ALERTER    : Déclencher action/décision"
        
        rapport += "\n" + "="*60 + "\n"
        return rapport


# ============================================================================
# SECTION 6 : ANALYSE PESTEL & SWOT
# ============================================================================

class AnalysePEStelSWOT:
    """Diagnostic stratégique complet : PESTEL + SWOT."""
    
    def __init__(self, nom_projet: str):
        self.nom = nom_projet
        self.pestel = {}
        self.swot = {'forces': [], 'faiblesses': [], 'opportunites': [], 'menaces': []}
    
    def ajouter_pestel(self, facteur: str, analyse: str) -> None:
        """P=Politique, E=Économique, S=Social, T=Technologique, E=Environnemental, L=Légal."""
        self.pestel[facteur] = analyse
    
    def ajouter_swot(self, categorie: str, point: str) -> None:
        """Ajoute point force/faiblesse/opportunité/menace."""
        if categorie in self.swot:
            self.swot[categorie].append(point)
    
    def generer_rapport_strategique(self) -> str:
        """Rapport PESTEL + SWOT."""
        rapport = f"""
╔════════════════════════════════════════════════════════════════╗
║  ANALYSE STRATÉGIQUE : {self.nom}
╚════════════════════════════════════════════════════════════════╝

🌍 ANALYSE PESTEL
─────────────────
"""
        
        pestel_labels = {
            'P': 'Politique',
            'E': 'Économique',
            'S': 'Social',
            'T': 'Technologique',
            'E2': 'Environnemental',
            'L': 'Légal'
        }
        
        for code, label in pestel_labels.items():
            if code in self.pestel:
                rapport += f"\n{label.upper():15} : {self.pestel[code]}"
        
        rapport += f"\n\n📊 MATRICE SWOT"
        rapport += f"\n───────────────\n"
        
        for categorie, couleur in [('forces', '💪'), ('faiblesses', '⚠️ '), 
                                    ('opportunites', '🚀'), ('menaces', '⛔')]:
            rapport += f"\n{couleur} {categorie.upper()}"
            for point in self.swot[categorie]:
                rapport += f"\n   • {point}"
        
        rapport += "\n" + "="*60 + "\n"
        return rapport


# ============================================================================
# SECTION 7 : PRIX PSYCHOLOGIQUE
# ============================================================================

class CalculPrixPsychologique:
    """Calcule le prix optimal via courbe d'insatisfaction cumulative."""
    
    def __init__(self):
        self.points_prix = {}  # {prix: nb_insatisfaits}
    
    def ajouter_point_test(self, prix: float, nb_insatisfaits: int) -> None:
        """Ajoute un test de prix avec nombre de consommateurs insatisfaits."""
        self.points_prix[prix] = nb_insatisfaits
    
    def calculer_prix_optimal(self) -> Dict[str, float]:
        """Trouve le prix minimisant l'insatisfaction cumulative."""
        if not self.points_prix:
            return {}
        
        sorted_prix = sorted(self.points_prix.keys())
        insatisfaits_cumul = {}
        cumul = 0
        
        for prix in sorted_prix:
            cumul += self.points_prix[prix]
            insatisfaits_cumul[prix] = cumul
        
        prix_optimal = min(insatisfaits_cumul.items(), key=lambda x: x[1])[0]
        
        return {
            'prix_optimal': prix_optimal,
            'insatisfaits_minimaux': insatisfaits_cumul[prix_optimal],
            'courbe': dict(sorted(insatisfaits_cumul.items()))
        }
    
    def generer_rapport_prix(self) -> str:
        """Rapport analyse prix."""
        optimal = self.calculer_prix_optimal()
        
        rapport = f"""
╔════════════════════════════════════════════════════════════════╗
║  ANALYSE PRIX PSYCHOLOGIQUE
╚════════════════════════════════════════════════════════════════╝

💰 TESTS DE PRIX
────────────────
"""
        
        for prix in sorted(self.points_prix.keys()):
            rapport += f"\n€{prix:7.2f} : {self.points_prix[prix]:3d} insatisfaits"
        
        if optimal:
            rapport += f"\n\n✨ PRIX OPTIMAL : €{optimal['prix_optimal']:.2f}"
            rapport += f"\n   Insatisfaits : {optimal['insatisfaits_minimaux']}"
        
        rapport += "\n" + "="*60 + "\n"
        return rapport


# ============================================================================
# MAIN : DÉMO & SYNTHÈSE
# ============================================================================

def main():
    """Démonstration complète de la suite TGC."""
    
    print("\n" + "╔" + "═"*62 + "╗")
    print("║" + " "*15 + "TGC SUSTAINABLE COMMERCE SUITE v1.0" + " "*14 + "║")
    print("╚" + "═"*62 + "╝\n")
    
    # ---- 1. PROPOSITION DE VALEUR ----
    print(PropositionDeValeur.afficher_exemples())
    
    # Créer une proposition personnalisée
    pvtgc = PropositionDeValeur(
        'TGC',
        'Sustainable Digital Challenge 2024',
        'Entreprises socio-responsables (SME + grands groupes)'
    )
    pvtgc.definir_slogan('Leader du numérique durable')
    pvtgc.ajouter_dimension('fonctionnelle', 
        'Plateforme d\'événements avec recrutement de 12 entreprises')
    pvtgc.ajouter_dimension('economique',
        'Accès à un vivier de talentspour RSE, ROI mesurable')
    pvtgc.ajouter_dimension('emotionnelle',
        'Impact positif carbone, fierté d\'appartenance à mouvement')
    pvtgc.ajouter_dimension('symbolique',
        'Visibilité leadership RSE, image innovante')
    pvtgc.ajouter_differenciateur('Targeting : anciennes & nouvelles marques')
    pvtgc.ajouter_differenciateur('Chiffrage impact CO2 réel post-événement')
    print(pvtgc.generer_rapport())
    
    # ---- 2. SEGMENTATION CLIENTS ----
    seg = SegmentationClients()
    seg.ajouter_client('C001', 'SNCF', '2024-05-15', 5, 50000)
    seg.ajouter_client('C002', 'BlaBlaCar', '2024-04-20', 3, 25000)
    seg.ajouter_client('C003', 'PME Tech', '2024-02-10', 8, 15000)
    seg.ajouter_client('C004', 'Startup', '2024-01-05', 1, 5000)
    seg.ajouter_client('C005', 'Groupe Industriel', '2024-05-01', 12, 120000)
    print(seg.generer_rapport_segmentation())
    
    # ---- 3. RSE & ISO 26000 ----
    rse = MatriceRSE('TGC')
    rse.evaluer_maturite('economique', 4)
    rse.evaluer_maturite('social', 3)
    rse.evaluer_maturite('environnemental', 5)
    print(rse.generer_rapport_rse())
    
    # ---- 4. NÉGOCIATION COMMERCIALE ----
    nego = NegociationCommerciale(
        'Sponsoring Entreprise',
        'TGC',
        'SNCF'
    )
    nego.definir_batna('A', 'Pas d\'événement / partenariat minimal')
    nego.definir_batna('B', 'Sponsoring concurrent ou intégration faible')
    nego.definir_zopa(15000, 35000)
    print(nego.generer_rapport_nego())
    
    # ---- 5. VEILLE STRATÉGIQUE ----
    veille = VeilleStrategique()
    veille.ajouter_article(
        'Volkswagen lance "Green Initiative"',
        'Volkswagen annonce 100% vert, écologique, durable',
        'Automotive News',
        '2024-05-10'
    )
    veille.ajouter_article(
        'McDonald\'s Pride Month (sans actions)',
        'Rainbow flags visible in June, lgbtq friendly',
        'Social Media Monitor',
        '2024-06-01'
    )
    print(veille.generer_rapport_veille())
    
    # ---- 6. PESTEL + SWOT ----
    strategie = AnalysePEStelSWOT('Plan d\'Actions TGC 2024')
    strategie.ajouter_pestel('P', 'Loi Grenelle II, AGEC, plan vigilance')
    strategie.ajouter_pestel('E', 'Crise post-Covid, inflation, réorientation RSE')
    strategie.ajouter_pestel('S', 'Demand croissante numérique durable')
    strategie.ajouter_pestel('T', 'IA sentiment analysis, APIs NewsAPI, Hugging Face')
    strategie.ajouter_pestel('E2', 'Cible carbone neutral 2030')
    strategie.ajouter_pestel('L', 'RGPD, reporting DPEF')
    
    strategie.ajouter_swot('forces', 'Positionnement unique RSE + Tech')
    strategie.ajouter_swot('forces', 'Partenariats marques établies')
    strategie.ajouter_swot('faiblesses', 'Visibilité limitée vs géants')
    strategie.ajouter_swot('faiblesses', 'Équipe réduite pour scale-up')
    strategie.ajouter_swot('opportunites', '+1000 abonnés LinkedIn cible')
    strategie.ajouter_swot('opportunites', 'Événements satellites (autres villes)')
    strategie.ajouter_swot('menaces', 'Événements RSE concurrents')
    strategie.ajouter_swot('menaces', 'Volatilité engagement RSE post-événement')
    print(strategie.generer_rapport_strategique())
    
    # ---- 7. PRIX PSYCHOLOGIQUE ----
    prix = CalculPrixPsychologique()
    prix.ajouter_point_test(5000, 120)
    prix.ajouter_point_test(10000, 85)
    prix.ajouter_point_test(15000, 45)
    prix.ajouter_point_test(20000, 65)
    prix.ajouter_point_test(25000, 100)
    print(prix.generer_rapport_prix())
    
    # ---- RÉSUMÉ SYNTHÉTIQUE ----
    print("\n" + "╔" + "═"*62 + "╗")
    print("║" + " "*18 + "SYNTHÈSE TGC 2024" + " "*27 + "║")
    print("╚" + "═"*62 + "╝\n")
    
    synthese = """
📋 OBJECTIFS TGC - SUSTAINABLE DIGITAL CHALLENGE 2024
───────────────────────────────────────────────────────

🎯 RECRUTEMENT ENTREPRISES
   • Cible : 12 entreprises (SNCF, BlaBlaCar, et nouveaux)
   • Segmentation : Groupe A (20%) = 80% CA
   • Messages : "Participez et devenez leader" (conatif)

📱 COMMUNICATION DIGITALE
   • Canaux : LinkedIn (+1000 abonnés), presse spécialisée
   • Landing page : Proposition de valeur claire & testimonials
   • Période : avant/pendant/après événement

🌍 IMPACT RSE
   • Dimensions : Économique (4/5) | Social (3/5) | Environnemental (5/5)
   • Cadre légal : ISO 26000, Grenelle II, AGEC, Pacte vigilance

💼 NÉGOCIATION SPONSORING
   • BATNA TGC : partenariat minimal
   • ZOPA : €15k-€35k (amplitude 26%)
   • Tactiques : SONCAS (Sécurité, Orgueil, Nouveauté, Confort, Argent)

📊 SEGMENTATION CLIENT
   • Analyse RFM (Récence-Fréquence-Montant)
   • Loi Pareto : Segment A = €120k (SNCF + Groupe Industriel)
   • NPS estimé : 50/100 (base départ)

🔍 VEILLE & RISQUES
   • Détection greenwashing : 4 piliers (Capter→Filtrer→Analyser→Alerter)
   • Monitoring : Rainbow washing, Feminism washing
   • Outils : NewsAPI, Sentiment Analysis (Hugging Face)

💡 OUTILS PYTHON GRATUITS
   ✓ NewsAPI (veille actualités)
   ✓ Hugging Face (sentiment, génération texte)
   ✓ TextBlob (analyse locale)
   ✓ SerpAPI (veille concurrentielle)
   ✓ spaCy + Rake-NLTK (mots-clés)
   ✓ pandas + sklearn (RFM, scoring, clustering)

📈 PRIX PSYCHOLOGIQUE
   • Optimal : €15k (minimise insatisfaction)
   • Stratégie : Flexibilité selon taille entreprise (ABC)
"""
    
    print(synthese)
    
    # ---- EXPORT JSON ----
    output = {
        'timestamp': datetime.now().isoformat(),
        'version': '1.0',
        'tgc_event': 'Sustainable Digital Challenge 2024',
        'modules_actifs': [
            'PropositionDeValeur',
            'SegmentationClients',
            'MatriceRSE',
            'NegociationCommerciale',
            'VeilleStrategique',
            'AnalysePEStelSWOT',
            'CalculPrixPsychologique'
        ],
        'apis_recommandees': {
            'veille': ['NewsAPI', 'SerpAPI'],
            'sentiment': ['Hugging Face', 'TextBlob'],
            'nlp': ['spaCy', 'Rake-NLTK'],
            'donnees': ['pandas', 'scikit-learn', 'NumPy']
        }
    }
    
    print("\n" + "="*64)
    print("✅ TGC Commerce Suite exécutée avec succès!")
    print(f"📅 Timestamp : {output['timestamp']}")
    print(f"📦 Modules actifs : {len(output['modules_actifs'])}")
    print("="*64 + "\n")
    
    return output


if __name__ == '__main__':
    resultat = main()
    
    # Export JSON pour intégration
    with open('tgc_rapport_synthese.json', 'w', encoding='utf-8') as f:
        json.dump(resultat, f, indent=2, ensure_ascii=False)
    print("💾 Rapport JSON exporté : tgc_rapport_synthese.json")
