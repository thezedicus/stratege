# ══════════════════════════════════════════════════════════════════════════════
# TAB — NOUVEAU PROJET (wizard indépendant étape par étape)
# ══════════════════════════════════════════════════════════════════════════════

def render_new_project_tab():
    """Wizard création nouveau projet — 6 étapes guidées."""
    import streamlit as st
    import json as _json

    st.markdown("""
<div style="background:linear-gradient(135deg,#0B2221,#267371);color:white;
  border-radius:16px;padding:22px 28px;margin-bottom:24px">
  <div style="font-size:1.3rem;font-weight:900;margin-bottom:6px">🚀 Créer un nouveau projet</div>
  <div style="opacity:.88;font-size:.88rem">Guidé étape par étape · Sauvegardé dans votre session · Export JSON</div>
</div>
""", unsafe_allow_html=True)

    # Initialiser le state du wizard
    if "proj_step" not in st.session_state:
        st.session_state["proj_step"] = 1
    if "proj_data" not in st.session_state:
        st.session_state["proj_data"] = {}

    step = st.session_state["proj_step"]
    proj = st.session_state["proj_data"]

    # Barre de progression
    progress_pct = (step - 1) / 6 * 100
    st.markdown(f"""
<div style="margin-bottom:20px">
  <div style="display:flex;justify-content:space-between;font-size:.75rem;
    color:#339999;font-weight:600;margin-bottom:6px">
    <span>Étape {step} / 6</span><span>{progress_pct:.0f}% complété</span>
  </div>
  <div style="height:6px;background:#C6ECD9;border-radius:99px;overflow:hidden">
    <div style="height:100%;background:linear-gradient(90deg,#44C1BA,#267371);
      border-radius:99px;width:{progress_pct}%;transition:width .4s ease"></div>
  </div>
  <div style="display:flex;gap:6px;margin-top:10px;flex-wrap:wrap">
    {"".join(f'<span style="padding:4px 12px;border-radius:50px;font-size:.7rem;font-weight:700;background:{"#44C1BA" if i+1<step else "#C6ECD9" if i+1==step else "#F2ECD9"};color:{"white" if i+1<=step else "#339999"}">{lbl}</span>'
    for i,lbl in enumerate(["🎯 Concept","🏢 Entreprise","👥 Cible","💰 Budget","🔑 Mots-clés","✅ Résumé"]))}
  </div>
</div>
""", unsafe_allow_html=True)

    # ── ÉTAPE 1 — Concept du projet ──────────────────────────────────────────
    if step == 1:
        st.markdown("### 🎯 Concept du projet")
        st.markdown("*Décrivez votre idée en quelques mots — BiziApp l'analysera pour vous*")

        proj["nom"] = st.text_input("Nom du projet *", value=proj.get("nom",""),
            placeholder="Ex: Ma boutique de cosmétiques bio",
            help="Le nom de votre projet ou entreprise")

        proj["description"] = st.text_area("Description en 2-3 phrases *",
            value=proj.get("description",""),
            placeholder="Ex: Je vends des cosmétiques naturels et biologiques en ligne, ciblant les femmes de 25-45 ans soucieuses de leur santé et de l'environnement.",
            height=100)

        proj["type_projet"] = st.selectbox("Type de projet *",
            ["E-commerce / Boutique en ligne", "SaaS / Logiciel", "Prestation de services",
             "Consulting / Conseil", "Création de contenu", "Autre"],
            index=["E-commerce / Boutique en ligne","SaaS / Logiciel","Prestation de services",
                   "Consulting / Conseil","Création de contenu","Autre"].index(proj.get("type_projet","E-commerce / Boutique en ligne")))

        proj["stade"] = st.radio("Où en êtes-vous ?", 
            ["💡 Idée — je commence à réfléchir",
             "🔨 En cours — j'ai démarré la construction",
             "🚀 Lancé — j'ai déjà des clients"],
            index=["💡 Idée — je commence à réfléchir",
                   "🔨 En cours — j'ai démarré la construction",
                   "🚀 Lancé — j'ai déjà des clients"].index(proj.get("stade","💡 Idée — je commence à réfléchir")))

        c1, c2 = st.columns([1,3])
        with c2:
            if st.button("Étape suivante →", type="primary", use_container_width=True,
                         disabled=not (proj.get("nom") and proj.get("description"))):
                st.session_state["proj_step"] = 2
                st.session_state["proj_data"] = proj
                st.rerun()
        if not proj.get("nom"):
            st.caption("⚠ Remplissez au minimum le nom et la description pour continuer")

    # ── ÉTAPE 2 — Informations entreprise ────────────────────────────────────
    elif step == 2:
        st.markdown("### 🏢 Votre entreprise")

        proj["secteur"] = st.selectbox("Secteur principal *",
            ["Beauté / Cosmétiques", "Mode / Textile", "Alimentation / Épicerie fine",
             "Tech / Informatique", "Santé / Bien-être", "Formation / Education",
             "Immobilier", "Finance / Assurance", "Transport / Logistique",
             "Tourisme / Hôtellerie", "Sport / Loisirs", "Art / Culture",
             "BTP / Construction", "Agriculture / Environnement", "Autre"],
            index=0 if "secteur" not in proj else
                  ["Beauté / Cosmétiques","Mode / Textile","Alimentation / Épicerie fine",
                   "Tech / Informatique","Santé / Bien-être","Formation / Education",
                   "Immobilier","Finance / Assurance","Transport / Logistique",
                   "Tourisme / Hôtellerie","Sport / Loisirs","Art / Culture",
                   "BTP / Construction","Agriculture / Environnement","Autre"].index(proj.get("secteur","Autre")))

        proj["zone_geo"] = st.selectbox("Zone géographique cible",
            ["France entière", "Île-de-France / Paris", "Province — région spécifique",
             "Europe francophone (Belgique, Suisse, Canada)", "International"])

        proj["structure_juridique"] = st.selectbox("Structure juridique",
            ["Non encore définie", "Auto-entrepreneur / Micro-entreprise",
             "SASU / SAS", "EURL / SARL", "Association", "Autre"])

        proj["site_web"] = st.text_input("Site web (si existant)",
            value=proj.get("site_web",""),
            placeholder="https://www.monsite.fr")

        c1, c2, c3 = st.columns([1,1,2])
        with c1:
            if st.button("← Retour", use_container_width=True):
                st.session_state["proj_step"] = 1
                st.session_state["proj_data"] = proj
                st.rerun()
        with c3:
            if st.button("Étape suivante →", type="primary", use_container_width=True):
                st.session_state["proj_step"] = 3
                st.session_state["proj_data"] = proj
                st.rerun()

    # ── ÉTAPE 3 — Cible clients ───────────────────────────────────────────────
    elif step == 3:
        st.markdown("### 👥 Votre cible client")

        proj["type_client"] = st.radio("Type de client principal",
            ["B2C — Particuliers", "B2B — Professionnels", "B2B2C — Les deux"])

        proj["age_cible"] = st.select_slider("Tranche d'âge cible",
            options=["18-24", "25-34", "35-44", "45-54", "55-64", "65+", "Tous âges"],
            value=proj.get("age_cible", "25-34"))

        proj["probleme_resolu"] = st.text_area("Quel problème résolvez-vous ? *",
            value=proj.get("probleme_resolu",""),
            placeholder="Ex: Mes clients manquent de temps pour trouver des cosmétiques naturels de qualité sans additifs chimiques à prix raisonnable.",
            height=90)

        proj["concurrents_connus"] = st.text_input(
            "Principaux concurrents (optionnel)",
            value=proj.get("concurrents_connus",""),
            placeholder="Ex: Aroma-Zone, Melvita, Centifolia")

        proj["avantage_concurrentiel"] = st.text_area(
            "Votre avantage concurrentiel *",
            value=proj.get("avantage_concurrentiel",""),
            placeholder="Ex: Certification bio française, sourcing éthique, packaging 100% recyclable, prix 30% sous le marché.",
            height=80)

        c1, c2, c3 = st.columns([1,1,2])
        with c1:
            if st.button("← Retour", use_container_width=True):
                st.session_state["proj_step"] = 2
                st.session_state["proj_data"] = proj
                st.rerun()
        with c3:
            if st.button("Étape suivante →", type="primary", use_container_width=True,
                         disabled=not (proj.get("probleme_resolu") and proj.get("avantage_concurrentiel"))):
                st.session_state["proj_step"] = 4
                st.session_state["proj_data"] = proj
                st.rerun()

    # ── ÉTAPE 4 — Budget & objectifs ─────────────────────────────────────────
    elif step == 4:
        st.markdown("### 💰 Budget & objectifs")

        proj["budget_mensuel"] = st.slider(
            "Budget marketing mensuel (€)", 0, 5000,
            value=proj.get("budget_mensuel", 200), step=50)

        proj["objectif_principal"] = st.selectbox("Objectif principal (6 mois)",
            ["Ventes / CA — générer du revenu rapidement",
             "Notoriété — faire connaître mon projet",
             "Leads — constituer une base de prospects",
             "Fidélisation — garder mes clients actuels",
             "Levée de fonds — convaincre des investisseurs"])

        proj["ca_cible_6mois"] = st.number_input(
            "CA cible à 6 mois (€)", min_value=0, max_value=1000000,
            value=proj.get("ca_cible_6mois", 10000), step=1000)

        proj["nb_clients_cible"] = st.number_input(
            "Nombre de clients cible à 6 mois", min_value=0, max_value=100000,
            value=proj.get("nb_clients_cible", 100), step=10)

        proj["canaux_prioritaires"] = st.multiselect(
            "Canaux prioritaires",
            ["SEO / Blog", "Google Ads", "Meta / Instagram", "LinkedIn",
             "TikTok", "Email marketing", "Partenariats", "Bouche-à-oreille",
             "Marketplaces", "Presse / RP"],
            default=proj.get("canaux_prioritaires", ["SEO / Blog", "Meta / Instagram"]))

        c1, c2, c3 = st.columns([1,1,2])
        with c1:
            if st.button("← Retour", use_container_width=True):
                st.session_state["proj_step"] = 3
                st.session_state["proj_data"] = proj
                st.rerun()
        with c3:
            if st.button("Étape suivante →", type="primary", use_container_width=True):
                st.session_state["proj_step"] = 5
                st.session_state["proj_data"] = proj
                st.rerun()

    # ── ÉTAPE 5 — Mots-clés SEO ───────────────────────────────────────────────
    elif step == 5:
        st.markdown("### 🔑 Mots-clés de votre business")
        st.markdown("*BiziApp va enrichir vos mots-clés avec des données de recherche réelles*")

        proj["mots_cles_principaux"] = st.text_area(
            "Vos mots-clés principaux (1 par ligne) *",
            value=proj.get("mots_cles_principaux",""),
            placeholder="cosmétiques bio\ncrème naturelle visage\nsoins peau naturels\nbio vegan skincare\nroutine beauté naturelle",
            height=140,
            help="Entrez les termes que vos clients tapent sur Google pour trouver vos produits/services")

        proj["mots_cles_longue_traine"] = st.text_area(
            "Mots-clés longue traîne (phrases complètes)",
            value=proj.get("mots_cles_longue_traine",""),
            placeholder="meilleure crème hydratante naturelle pour peau sèche\ncomment choisir cosmétiques bio sans parabènes\ncosmetique naturel pas cher livraison rapide france",
            height=120,
            help="Les phrases longues ont moins de concurrence et convertissent mieux")

        proj["sujets_blog"] = st.text_area(
            "Idées de sujets d'articles blog",
            value=proj.get("sujets_blog",""),
            placeholder="Top 10 ingrédients naturels pour la peau\nComment lire une étiquette cosmétique bio\nRoutine beauté naturelle pour débutantes",
            height=100)

        # Suggestions automatiques basées sur le secteur
        _sector_suggestions = {
            "Beauté / Cosmétiques": ["cosmétique naturel", "beauté bio", "soins naturels", "vegan skincare"],
            "Tech / Informatique": ["logiciel", "application", "digital", "SaaS", "automatisation"],
            "Alimentation / Épicerie fine": ["épicerie fine", "produits artisanaux", "bio", "local", "terroir"],
            "Formation / Education": ["formation en ligne", "e-learning", "certification", "compétences"],
        }
        suggestions = _sector_suggestions.get(proj.get("secteur",""), [])
        if suggestions:
            st.markdown(f"**💡 Suggestions pour votre secteur :** " + " · ".join(f"`{s}`" for s in suggestions))

        c1, c2, c3 = st.columns([1,1,2])
        with c1:
            if st.button("← Retour", use_container_width=True):
                st.session_state["proj_step"] = 4
                st.session_state["proj_data"] = proj
                st.rerun()
        with c3:
            if st.button("Générer le résumé →", type="primary", use_container_width=True,
                         disabled=not proj.get("mots_cles_principaux")):
                st.session_state["proj_step"] = 6
                st.session_state["proj_data"] = proj
                st.rerun()

    # ── ÉTAPE 6 — Résumé & Export ─────────────────────────────────────────────
    elif step == 6:
        st.markdown("### ✅ Résumé de votre projet")
        st.success("**Projet configuré !** Voici votre fiche stratégique complète.")

        # Affichage résumé
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""
<div class="proof-card" style="margin-bottom:12px">
  <div style="position:relative;z-index:1">
    <div style="font-size:.7rem;color:#44C1BA;font-weight:700;text-transform:uppercase;margin-bottom:10px">IDENTITÉ PROJET</div>
    <div style="font-weight:800;font-size:1.1rem;color:white;margin-bottom:6px">{proj.get("nom","")}</div>
    <div style="font-size:.82rem;color:rgba(255,255,255,.85);margin-bottom:10px">{proj.get("description","")[:150]}</div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      <span style="background:rgba(68,193,186,.3);color:#44C1BA;border-radius:50px;padding:2px 10px;font-size:.7rem;font-weight:700">{proj.get("type_projet","")}</span>
      <span style="background:rgba(68,193,186,.3);color:#44C1BA;border-radius:50px;padding:2px 10px;font-size:.7rem;font-weight:700">{proj.get("secteur","")}</span>
      <span style="background:rgba(68,193,186,.3);color:#44C1BA;border-radius:50px;padding:2px 10px;font-size:.7rem;font-weight:700">{proj.get("zone_geo","")}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        with r2:
            st.metric("Budget mensuel", f"{proj.get('budget_mensuel',0)}€")
            st.metric("CA cible 6 mois", f"{proj.get('ca_cible_6mois',0):,}€")
            st.metric("Clients cible", f"{proj.get('nb_clients_cible',0)}")

        # Mots-clés générés
        kws_raw = proj.get("mots_cles_principaux","").strip().split("\n")
        kws = [k.strip() for k in kws_raw if k.strip()]
        if kws:
            st.markdown("**🔑 Mots-clés validés :**")
            st.markdown(" ".join(f"`{k}`" for k in kws[:15]))

        # Analyse rapide
        budget = proj.get("budget_mensuel", 200)
        ca_cible = proj.get("ca_cible_6mois", 10000)
        roi_estimé = round(ca_cible / max(budget * 6, 1), 1)
        st.info(f"📊 **Analyse rapide** : Budget total 6 mois = **{budget*6:,}€** · CA cible = **{ca_cible:,}€** · ROI estimé = **{roi_estimé}×** · Ticket moyen estimé = **{round(ca_cible/max(proj.get('nb_clients_cible',100),1)):,}€**")

        # Export JSON
        import json as _j, datetime as _dt
        proj["_generated_at"] = _dt.datetime.now().isoformat()
        proj["_version"] = "BiziApp v3.2"
        json_export = _j.dumps(proj, ensure_ascii=False, indent=2)

        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            st.download_button("⬇️ Exporter JSON", json_export,
                file_name=f"projet_{proj.get('nom','biziapp').lower().replace(' ','_')}.json",
                mime="application/json", use_container_width=True)
        with ec2:
            if st.button("🔄 Nouveau projet", use_container_width=True):
                for k in ["proj_step","proj_data"]:
                    st.session_state.pop(k, None)
                st.rerun()
        with ec3:
            if st.button("← Modifier", use_container_width=True):
                st.session_state["proj_step"] = 1
                st.rerun()

        st.divider()
        st.markdown("""
<div style="background:#C6ECD9;border-radius:12px;padding:16px 20px;border-left:4px solid #44C1BA">
  <div style="font-weight:700;color:#0B2221;margin-bottom:6px">🎯 Prochaine étape recommandée</div>
  <div style="font-size:.88rem;color:#267371">
    Utilisez les informations de ce projet dans l'onglet <b>🔍 Diagnostic</b> pour générer votre 
    analyse SWOT complète, vos personas clients et votre plan marketing personnalisé.
  </div>
</div>
""", unsafe_allow_html=True)
