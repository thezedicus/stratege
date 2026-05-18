#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLES D'UTILISATION - TGC SUSTAINABLE COMMERCE SUITE v1.0

Copier-coller ces exemples pour intégrer le script dans vos projets.
"""

# ============================================================================
# IMPORT
# ============================================================================
from tgc_sustainable_commerce_suite import (
    PropositionDeValeur,
    SegmentationClients,
    MatriceRSE,
    NegociationCommerciale,
    VeilleStrategique,
    AnalysePEStelSWOT,
    CalculPrixPsychologique
)
from datetime import datetime


# ============================================================================
# EXEMPLE 1 : PROPOSITION DE VALEUR PERSONNALISÉE
# ============================================================================

def exemple_proposition_valeur():
    """
    Créer une proposition de valeur pour votre produit/service.
    """
    print("\n" + "="*70)
    print("EXEMPLE 1 : PROPOSITION DE VALEUR")
    print("="*70)
    
    # Créer proposition personnalisée
    pv = PropositionDeValeur(
        nom_entreprise="Mon Entreprise",
        produit="Mon Produit/Service",
        public_cible="Mes clients cibles"
    )
    
    # Définir le slogan (idéalement 7 mots max)
    pv.definir_slogan("Slogan court et mémorable")
    
    # Ajouter les 4 dimensions de valeur
    pv.ajouter_dimension('fonctionnelle', 'Performance, gain de temps, facilité')
    pv.ajouter_dimension('economique', 'Prix compétitif, ROI positif, économies')
    pv.ajouter_dimension('emotionnelle', 'Confiance, fierté, plaisir, sécurité')
    pv.ajouter_dimension('symbolique', 'Image, statut, appartenance, identité')
    
    # Ajouter points de différenciation vs concurrence
    pv.ajouter_differenciateur('Avantage unique 1')
    pv.ajouter_differenciateur('Avantage unique 2')
    pv.ajouter_differenciateur('Avantage unique 3')
    
    # Générer rapport
    print(pv.generer_rapport())
    
    return pv


# ============================================================================
# EXEMPLE 2 : SEGMENTATION CLIENTS RFM
# ============================================================================

def exemple_segmentation_clients():
    """
    Analyser votre portefeuille clients avec RFM + Pareto 80/20.
    """
    print("\n" + "="*70)
    print("EXEMPLE 2 : SEGMENTATION CLIENTS RFM")
    print("="*70)
    
    # Créer instance segmentation
    seg = SegmentationClients()
    
    # Ajouter vos clients réels (id, nom, date dernier achat, nb achats, montant total)
    clients_data = [
        ('CLI001', 'Client Premium A', '2024-05-15', 15, 150000),
        ('CLI002', 'Client Premium B', '2024-05-10', 12, 120000),
        ('CLI003', 'Client Standard 1', '2024-04-20', 6, 45000),
        ('CLI004', 'Client Standard 2', '2024-04-15', 5, 40000),
        ('CLI005', 'Client Faible 1', '2024-02-01', 2, 10000),
        ('CLI006', 'Client Faible 2', '2024-01-15', 1, 5000),
    ]
    
    for cid, nom, date, nb, montant in clients_data:
        seg.ajouter_client(cid, nom, date, nb, montant)
    
    # Générer rapport RFM + ABC
    print(seg.generer_rapport_segmentation())
    
    # Récupérer données pour utilisation
    rfm = seg.calculer_rfm()
    abc = seg.segmentation_abc()
    
    print("\n📊 ANALYSE DÉTAILLÉE")
    print(f"Segment A : {abc['A']}")
    print(f"Segment B : {abc['B']}")
    print(f"Segment C : {abc['C']}")
    
    return seg


# ============================================================================
# EXEMPLE 3 : AUDIT RSE ISO 26000
# ============================================================================

def exemple_audit_rse():
    """
    Évaluer maturité RSE de votre entreprise (ISO 26000).
    """
    print("\n" + "="*70)
    print("EXEMPLE 3 : AUDIT RSE ISO 26000")
    print("="*70)
    
    # Créer matrice RSE
    rse = MatriceRSE("Mon Entreprise")
    
    # Évaluer maturité par dimension (1=débutant, 5=leader)
    # À adapter selon votre situation réelle
    rse.evaluer_maturite('economique', 3)      # À améliorer
    rse.evaluer_maturite('social', 2)          # Action prioritaire
    rse.evaluer_maturite('environnemental', 4) # Bon niveau
    
    # Générer rapport
    print(rse.generer_rapport_rse())
    
    # Recommandations par dimension
    print("\n💡 RECOMMANDATIONS")
    print("- ÉCONOMIQUE    : Renforcer rentabilité et innovation")
    print("- SOCIAL        : Augmenter bien-être et formation salarié")
    print("- ENVIRONNEMENTAL : Maintenir excellence niveau 4+")
    
    return rse


# ============================================================================
# EXEMPLE 4 : PRÉPARATION NÉGOCIATION COMMERCIALE
# ============================================================================

def exemple_negociation():
    """
    Préparer une négociation commerciale (prix, contrat, partenariat).
    """
    print("\n" + "="*70)
    print("EXEMPLE 4 : NÉGOCIATION COMMERCIALE")
    print("="*70)
    
    # Créer session négociation
    nego = NegociationCommerciale(
        nom_nego="Négociation Contrat 2024",
        partie_a="Mon Entreprise",
        partie_b="Client/Partenaire"
    )
    
    # Définir BATNA (Plan B si pas accord)
    nego.definir_batna('A', 'Situation actuelle ou autre client')
    nego.definir_batna('B', 'Partenaire concurrent')
    
    # Définir ZOPA (Zone d'accord possible)
    nego.definir_zopa(
        prix_min=10000,   # Minimum acceptable
        prix_max=50000    # Maximum offert
    )
    
    # Générer rapport stratégique
    print(nego.generer_rapport_nego())
    
    # Tactiques SONCAS pour argumentation
    print("\n💬 TACTIQUES D'ARGUMENTATION (SONCAS)")
    soncas_arguments = {
        'S': 'Sécurité    : "Partenariat stable et sécurisé"',
        'O': 'Orgueil     : "Leader de l\'industrie, innovant"',
        'N': 'Nouveauté   : "Solution dernière génération"',
        'C': 'Confort     : "Implémentation facile, ROI rapide"',
        'A': 'Argent      : "Meilleur ROI du marché"',
        'S2': 'Sympathie  : "Partenaire de confiance depuis X ans"'
    }
    
    for code, arg in soncas_arguments.items():
        print(f"  ✓ {arg}")
    
    return nego


# ============================================================================
# EXEMPLE 5 : VEILLE STRATÉGIQUE & GREENWASHING
# ============================================================================

def exemple_veille():
    """
    Monitorer articles/communications pour détecter greenwashing.
    """
    print("\n" + "="*70)
    print("EXEMPLE 5 : VEILLE STRATÉGIQUE & DÉTECTION GREENWASHING")
    print("="*70)
    
    # Créer système veille
    veille = VeilleStrategique()
    
    # Ajouter articles à analyser
    articles_test = [
        {
            'titre': 'Entreprise X lance initiative "Green"',
            'contenu': 'Nous sommes 100% écologique et vert durable',
            'source': 'Communication Presse',
            'date': '2024-05-15'
        },
        {
            'titre': 'Entreprise Y labellisée ISO 14001',
            'contenu': 'Certifiée ISO 14001 depuis 2022, audit annuel validé',
            'source': 'Rapport RSE officiel',
            'date': '2024-05-14'
        },
    ]
    
    for article in articles_test:
        veille.ajouter_article(
            titre=article['titre'],
            contenu=article['contenu'],
            source=article['source'],
            date=article['date']
        )
    
    # Générer rapport veille
    print(veille.generer_rapport_veille())
    
    return veille


# ============================================================================
# EXEMPLE 6 : ANALYSE PESTEL + SWOT
# ============================================================================

def exemple_strategie():
    """
    Effectuer diagnostic stratégique complet (PESTEL + SWOT).
    """
    print("\n" + "="*70)
    print("EXEMPLE 6 : ANALYSE STRATÉGIQUE (PESTEL + SWOT)")
    print("="*70)
    
    # Créer analyse stratégique
    strat = AnalysePEStelSWOT("Plan Stratégique 2024-2025")
    
    # PESTEL - Environnement externe
    strat.ajouter_pestel('P', 'Lois Grenelle II, AGEC, plan vigilance en vigueur')
    strat.ajouter_pestel('E', 'Économie stable, croissance RSE, inflation réduite')
    strat.ajouter_pestel('S', 'Demande croissante consommateurs RSE, engagement')
    strat.ajouter_pestel('T', 'IA sentiment analysis, APIs libres, monitoring IA')
    strat.ajouter_pestel('E2', 'Cible carbone neutral 2030, pression réglementaire')
    strat.ajouter_pestel('L', 'RGPD, DPEF, transparence données clients')
    
    # SWOT - Analyse interne
    strat.ajouter_swot('forces', 'Équipe talentueuse et RSE sensibilisée')
    strat.ajouter_swot('forces', 'Portefeuille clients premium')
    strat.ajouter_swot('faiblesses', 'Budget communication limité')
    strat.ajouter_swot('faiblesses', 'Visibilité faible vs géants du secteur')
    strat.ajouter_swot('opportunites', 'Croissance événements RSE')
    strat.ajouter_swot('opportunites', 'Partenariats stratégiques possibles')
    strat.ajouter_swot('menaces', 'Événements RSE concurrents émergents')
    strat.ajouter_swot('menaces', 'Volatilité engagement post-crise')
    
    # Générer rapport
    print(strat.generer_rapport_strategique())
    
    return strat


# ============================================================================
# EXEMPLE 7 : CALCUL PRIX PSYCHOLOGIQUE
# ============================================================================

def exemple_prix():
    """
    Déterminer prix optimal via courbe d'insatisfaction cumulative.
    """
    print("\n" + "="*70)
    print("EXEMPLE 7 : CALCUL PRIX PSYCHOLOGIQUE")
    print("="*70)
    
    # Créer analyseur prix
    prix = CalculPrixPsychologique()
    
    # Ajouter tests de prix (réels ou sondage clients)
    # Format : (prix testé, nombre de clients insatisfaits à ce prix)
    tests_prix = [
        (5000, 150),    # Très bas : clients pensent "trop bon pour être vrai"
        (10000, 95),
        (15000, 45),    # Optimal estimé
        (20000, 60),
        (25000, 120),   # Très cher : clients rejettent
        (30000, 180),
    ]
    
    for prix_test, insatisfaits in tests_prix:
        prix.ajouter_point_test(prix_test, insatisfaits)
    
    # Générer rapport
    print(prix.generer_rapport_prix())
    
    # Recommandation
    optimal = prix.calculer_prix_optimal()
    print(f"\n💰 RECOMMANDATION TARIFAIRE")
    print(f"Prix optimal : €{optimal['prix_optimal']:,.0f}")
    print(f"Marge de sécurité : ±€2,000 possibles")
    
    return prix


# ============================================================================
# EXEMPLE 8 : WORKFLOW COMPLET TGC 2024
# ============================================================================

def workflow_tgc_complet():
    """
    Workflow complet pour préparer Sustainable Digital Challenge 2024.
    """
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*15 + "WORKFLOW COMPLET - TGC SDC 2024" + " "*22 + "║")
    print("╚" + "═"*68 + "╝\n")
    
    # Étape 1 : Proposition de valeur
    print("\n📍 ÉTAPE 1 : Proposition de Valeur")
    pv = PropositionDeValeur(
        'TGC', 'Sustainable Digital Challenge 2024', 
        'Entreprises socio-responsables'
    )
    pv.definir_slogan('Leader du numérique durable')
    pv.ajouter_dimension('fonctionnelle', 'Événement + recrutement 12 entreprises')
    pv.ajouter_dimension('economique', 'Accès talentspour RSE, ROI mesurable')
    pv.ajouter_dimension('emotionnelle', 'Impact CO2 positif, fierté changement')
    pv.ajouter_dimension('symbolique', 'Visibilité leadership RSE, innovation')
    print("✓ Proposition définie\n")
    
    # Étape 2 : Segmentation clients
    print("📍 ÉTAPE 2 : Segmentation Portefeuille")
    seg = SegmentationClients()
    clients_tgc = [
        ('SNCF', 'SNCF', '2024-05-15', 5, 50000),
        ('Blablacar', 'BlaBlaCar', '2024-04-20', 3, 25000),
        ('GroupeInd', 'Groupe Industriel', '2024-05-01', 12, 120000),
        ('PME1', 'PME Tech', '2024-02-10', 8, 15000),
        ('Startup1', 'Startup', '2024-01-05', 1, 5000),
    ]
    for cid, nom, date, nb, montant in clients_tgc:
        seg.ajouter_client(cid, nom, date, nb, montant)
    abc = seg.segmentation_abc()
    print(f"✓ Segment A (priorité rétention) : {len(abc['A'])} clients")
    print(f"✓ Segment B (développement)      : {len(abc['B'])} clients")
    print(f"✓ Segment C (automation)         : {len(abc['C'])} clients\n")
    
    # Étape 3 : RSE
    print("📍 ÉTAPE 3 : Maturité RSE")
    rse = MatriceRSE('TGC')
    rse.evaluer_maturite('economique', 4)
    rse.evaluer_maturite('social', 3)
    rse.evaluer_maturite('environnemental', 5)
    print("✓ Score RSE : 4.0/5 (Leader)\n")
    
    # Étape 4 : Négociation
    print("📍 ÉTAPE 4 : Stratégie Sponsoring")
    nego = NegociationCommerciale('Sponsoring SDC', 'TGC', 'SNCF')
    nego.definir_batna('A', 'Événement réduit, partenariats minimaux')
    nego.definir_batna('B', 'Sponsoring concurrent, intégration faible')
    nego.definir_zopa(15000, 35000)
    print("✓ ZOPA définie : €15k-€35k")
    print("✓ Tactiques SONCAS préparées\n")
    
    # Étape 5 : Veille
    print("📍 ÉTAPE 5 : Monitoring Greenwashing")
    veille = VeilleStrategique()
    print("✓ Système veille initié\n")
    
    # Étape 6 : PESTEL + SWOT
    print("📍 ÉTAPE 6 : Diagnostic Stratégique")
    strat = AnalysePEStelSWOT('Plan TGC 2024')
    strat.ajouter_swot('forces', 'Positionnement unique RSE + Tech')
    strat.ajouter_swot('menaces', 'Événements concurrents émergents')
    print("✓ Diagnostic complété\n")
    
    # Étape 7 : Prix
    print("📍 ÉTAPE 7 : Tarification Partenariats")
    prix = CalculPrixPsychologique()
    prix.ajouter_point_test(10000, 120)
    prix.ajouter_point_test(15000, 45)
    prix.ajouter_point_test(25000, 100)
    optimal = prix.calculer_prix_optimal()
    print(f"✓ Prix optimal : €{optimal['prix_optimal']:,.0f}\n")
    
    # Résumé exécutif
    print("\n" + "="*70)
    print("✅ WORKFLOW COMPLET EXÉCUTÉ AVEC SUCCÈS")
    print("="*70)
    print(f"""
OBJECTIFS 2024 :
- 12 entreprises recrutées
- 1,000+ nouveaux abonnés LinkedIn
- Score RSE 4.0+ maintenu
- Sponsorings à €15k-€35k
- 0 greenwashing détecté
- Impact CO2 mesuré et publié

PROCHAINES ÉTAPES :
1. Valider auprès de comité direction
2. Lancer campagne communication LinkedIn
3. Initier négociations Segment A
4. Déployer monitoring greenwashing
5. Mesurer KPIs post-événement
""")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*10 + "EXEMPLES D'UTILISATION - TGC COMMERCE SUITE v1.0" + " "*8 + "║")
    print("╚" + "═"*68 + "╝\n")
    
    # Exécuter tous les exemples
    pv = exemple_proposition_valeur()
    seg = exemple_segmentation_clients()
    rse = exemple_audit_rse()
    nego = exemple_negociation()
    veille = exemple_veille()
    strat = exemple_strategie()
    prix = exemple_prix()
    
    # Workflow complet
    workflow_tgc_complet()
    
    print("\n✨ Tous les exemples exécutés avec succès!")
    print("📚 Consultez README.md pour plus d'informations")
    print("📧 Questions ? Intégrez dans vos scripts personnels\n")
