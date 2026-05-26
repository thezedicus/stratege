"""
pages/2_Nouveau_Projet.py — Wizard de création de projet BiziApp
Onglet indépendant · Étapes guidées · 100% gratuit
"""
import streamlit as st
import json, re, hashlib, datetime

st.set_page_config(
    page_title="Nouveau Projet — BiziApp",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""<style>
:root{--teal:#44C1BA;--jade:#267371;--dark:#0B2221;--light:#F7FBF4;--card:#C6ECD9;--accent:#393DAC}
body,html{font-family:system-ui,-apple-system,sans-serif;background:var(--light)}
.wiz-step{background:white;border-radius:16px;border:2px solid var(--card);padding:28px 24px;margin-bottom:20px}
.wiz-step.active{border-color:var(--teal);box-shadow:0 0 0 4px rgba(68,193,186,.12)}
.wiz-step.done{border-color:var(--jade);background:#F7FBF4}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;
  border-radius:50%;background:var(--teal);color:white;font-weight:800;font-size:.9rem;margin-right:12px;flex-shrink:0}
.step-num.done{background:var(--jade)}
.step-title{font-size:1.05rem;font-weight:700;color:var(--dark)}
.kw-tag{display:inline-block;background:var(--card);color:var(--jade);border-radius:50px;
  padding:4px 14px;margin:3px;font-size:.8rem;font-weight:600;border:1.5px solid var(--teal)}
.progress-wiz{height:6px;background:#C6ECD9;border-radius:99px;margin:16px 0}
.progress-fill-wiz{height:100%;background:linear-gradient(90deg,#44C1BA,#267371);border-radius:99px;transition:width .4s ease}
.result-card{background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:18px;padding:26px;margin-top:16px}
.insight-box{background:white;border-left:4px solid var(--teal);border-radius:0 12px 12px 0;padding:14px 18px;margin-bottom:10px}
</style>""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;padding-bottom:16px;border-bottom:2px solid #C6ECD9;margin-bottom:24px">
  <div style="width:46px;height:46px;border-radius:12px;background:linear-gradient(135deg,#44C1BA,#267371);
    display:flex;align-items:center;justify-content:center;font-size:1.4rem">🚀</div>
  <div>
    <div style="font-size:1.5rem;font-weight:900;color:#0B2221">Créer un nouveau projet</div>
    <div style="font-size:.82rem;color:#339999;font-weight:600">Wizard guidé · 5 étapes · Analyse instantanée</div>
  </div>
  <div style="margin-left:auto">
    <a href="/" style="background:#C6ECD9;color:#267371;border-radius:50px;padding:8px 18px;font-size:.8rem;font-weight:700;text-decoration:none">← Retour BiziApp</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
def _ss(k, default=None):
    if k not in st.session_state:
        st.session_state[k] = default
    return st.session_state[k]

_ss("wiz_step", 1)
_ss("wiz_project_name", "")
_ss("wiz_keywords", [])
_ss("wiz_activity", "ecommerce")
_ss("wiz_goal", "sales")
_ss("wiz_budget", 200)
_ss("wiz_website", "")
_ss("wiz_maturity", "launched")
_ss("wiz_target", "")
_ss("wiz_usp", "")
_ss("wiz_done", False)

current_step = st.session_state["wiz_step"]
total_steps  = 5

# ── PROGRESS BAR ──────────────────────────────────────────────────────────────
pct = int((current_step - 1) / total_steps * 100)
st.markdown(f"""
<div style="display:flex;justify-content:space-between;font-size:.76rem;color:#339999;font-weight:600;margin-bottom:4px">
  <span>Étape {current_step} sur {total_steps}</span><span>{pct}% complété</span>
</div>
<div class="progress-wiz"><div class="progress-fill-wiz" style="width:{pct}%"></div></div>
""", unsafe_allow_html=True)

# ── ÉTAPES ────────────────────────────────────────────────────────────────────

# ── ÉTAPE 1 : Infos de base ────────────────────────────────────────────────────
with st.container():
    done1 = current_step > 1
    active1 = current_step == 1
    cls1 = "wiz-step done" if done1 else ("wiz-step active" if active1 else "wiz-step")
    num_cls = "step-num done" if done1 else "step-num"
    st.markdown(f"""<div class="{cls1}">
      <div style="display:flex;align-items:center;margin-bottom:16px">
        <span class="{num_cls}">{'✓' if done1 else '1'}</span>
        <span class="step-title">Informations de base du projet</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if active1:
        st.markdown("**Donnez un nom à votre projet :**")
        proj_name = st.text_input("Nom du projet", value=st.session_state["wiz_project_name"],
                                   placeholder="Ex: Ma Boutique Bio, SaaS RH, Cabinet Conseil...")
        c1, c2 = st.columns(2)
        with c1:
            activity = st.selectbox("Type d'activité", [
                "ecommerce","saas","service","consulting","content","other"
            ], index=["ecommerce","saas","service","consulting","content","other"].index(st.session_state["wiz_activity"]),
            format_func=lambda x: {
                "ecommerce":"🛍️ E-commerce","saas":"💻 SaaS / Tech",
                "service":"🔧 Prestataire de services","consulting":"🧠 Conseil & consulting",
                "content":"📱 Créateur de contenu","other":"🏢 Autre secteur"
            }.get(x, x))
        with c2:
            goal = st.selectbox("Objectif principal", [
                "sales","leads","notoriete","retention","lancement"
            ], format_func=lambda x: {
                "sales":"💰 Vendre / générer du CA","leads":"🎯 Générer des leads",
                "notoriete":"📣 Développer la notoriété","retention":"💙 Fidéliser les clients",
                "lancement":"🚀 Lancer un nouveau produit"
            }.get(x, x))
        website = st.text_input("URL de votre site (optionnel)", value=st.session_state["wiz_website"],
                                placeholder="https://monsite.fr")
        if st.button("Continuer →", type="primary", use_container_width=True):
            if proj_name.strip():
                st.session_state["wiz_project_name"] = proj_name.strip()
                st.session_state["wiz_activity"]     = activity
                st.session_state["wiz_goal"]         = goal
                st.session_state["wiz_website"]      = website
                st.session_state["wiz_step"]         = 2
                st.rerun()
            else:
                st.error("Donnez un nom à votre projet pour continuer.")

# ── ÉTAPE 2 : Mots-clés métier ────────────────────────────────────────────────
if current_step >= 2:
    done2 = current_step > 2
    active2 = current_step == 2
    cls2 = "wiz-step done" if done2 else ("wiz-step active" if active2 else "wiz-step")
    num_cls2 = "step-num done" if done2 else "step-num"
    st.markdown(f"""<div class="{cls2}">
      <div style="display:flex;align-items:center;margin-bottom:{'16px' if active2 else '0'}">
        <span class="{num_cls2}">{'✓' if done2 else '2'}</span>
        <span class="step-title">Mots-clés liés à votre business</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if active2:
        st.markdown("""
> 🎯 **Les mots-clés** définissent votre univers sémantique.
> Ils serviront à personnaliser toute votre stratégie : SEO, personas, contenu, ads.
""")
        st.markdown("**Entrez vos mots-clés métier (séparés par des virgules ou Entrée) :**")
        kw_input = st.text_area(
            "Mots-clés",
            placeholder="Ex: formation en ligne, coach business, productivité, freelance, startup...",
            height=100,
            help="Minimum 3 mots-clés recommandés pour une analyse complète"
        )
        # Suggestions automatiques par secteur
        SUGGESTIONS = {
            "ecommerce": ["boutique en ligne","livraison rapide","paiement sécurisé","avis clients","meilleur prix"],
            "saas": ["logiciel","abonnement","API","automatisation","dashboard","intégration"],
            "service": ["devis gratuit","expertise","sur-mesure","satisfaction client","professionnel"],
            "consulting": ["stratégie","conseil","diagnostic","transformation","performance","ROI"],
            "content": ["créateur","audience","monétisation","engagement","newsletter","YouTube"],
            "other": ["qualité","innovation","service client","expertise","solution"],
        }
        act = st.session_state["wiz_activity"]
        sugg = SUGGESTIONS.get(act, [])
        st.markdown("**Suggestions pour votre secteur (cliquez pour ajouter) :**")
        sugg_cols = st.columns(min(5, len(sugg)))
        for col, s in zip(sugg_cols, sugg):
            with col:
                if st.button(s, key=f"sugg_{s}"):
                    existing = kw_input or ""
                    kw_input = existing + (", " if existing else "") + s
        c_back2, c_next2 = st.columns([1, 3])
        with c_back2:
            if st.button("← Retour"):
                st.session_state["wiz_step"] = 1
                st.rerun()
        with c_next2:
            if st.button("Continuer →", type="primary", use_container_width=True):
                _sep_pat = re.compile(r"[,;\s]+")
                kws = [k.strip() for k in _sep_pat.split(kw_input) if k.strip() and len(k.strip()) >= 2]
                if len(kws) >= 1:
                    st.session_state["wiz_keywords"] = kws[:20]
                    st.session_state["wiz_step"] = 3
                    st.rerun()
                else:
                    st.warning("Entrez au moins 1 mot-clé pour continuer.")
    elif done2:
        kws_saved = st.session_state.get("wiz_keywords", [])
        tags_html = "".join(f'<span class="kw-tag">{k}</span>' for k in kws_saved[:10])
        st.markdown(f'<div style="padding:8px 0 0 46px">{tags_html}</div>', unsafe_allow_html=True)

# ── ÉTAPE 3 : Budget & maturité ────────────────────────────────────────────────
if current_step >= 3:
    done3 = current_step > 3
    active3 = current_step == 3
    cls3 = "wiz-step done" if done3 else ("wiz-step active" if active3 else "wiz-step")
    num_cls3 = "step-num done" if done3 else "step-num"
    st.markdown(f"""<div class="{cls3}">
      <div style="display:flex;align-items:center;margin-bottom:{'16px' if active3 else '0'}">
        <span class="{num_cls3}">{'✓' if done3 else '3'}</span>
        <span class="step-title">Budget marketing & maturité</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if active3:
        c1, c2 = st.columns(2)
        with c1:
            budget = st.slider("Budget marketing mensuel (€)", 10, 2000,
                               st.session_state["wiz_budget"], step=10)
            st.markdown(f"<div style='text-align:center;font-size:1.2rem;font-weight:800;color:#44C1BA'>{budget} €/mois</div>", unsafe_allow_html=True)
        with c2:
            maturity = st.radio("Maturité du projet", [
                "idea","inprogress","launched"
            ], format_func=lambda x: {
                "idea":"💡 Idée / Concept","inprogress":"🔨 En cours de lancement","launched":"🚀 Déjà lancé"
            }.get(x, x), index=["idea","inprogress","launched"].index(st.session_state["wiz_maturity"]))
        c_back3, c_next3 = st.columns([1, 3])
        with c_back3:
            if st.button("← Retour", key="back3"):
                st.session_state["wiz_step"] = 2
                st.rerun()
        with c_next3:
            if st.button("Continuer →", type="primary", use_container_width=True, key="next3"):
                st.session_state["wiz_budget"]   = budget
                st.session_state["wiz_maturity"] = maturity
                st.session_state["wiz_step"]     = 4
                st.rerun()

# ── ÉTAPE 4 : Cible & USP ──────────────────────────────────────────────────────
if current_step >= 4:
    done4 = current_step > 4
    active4 = current_step == 4
    cls4 = "wiz-step done" if done4 else ("wiz-step active" if active4 else "wiz-step")
    num_cls4 = "step-num done" if done4 else "step-num"
    st.markdown(f"""<div class="{cls4}">
      <div style="display:flex;align-items:center;margin-bottom:{'16px' if active4 else '0'}">
        <span class="{num_cls4}">{'✓' if done4 else '4'}</span>
        <span class="step-title">Cible clients & proposition de valeur</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if active4:
        target = st.text_area("Décrivez votre cible client idéale",
            placeholder="Ex: Dirigeants de TPE entre 35-55 ans, freelances tech, e-commerçants débutants...",
            height=80, value=st.session_state["wiz_target"])
        usp = st.text_area("Votre proposition de valeur unique (USP)",
            placeholder="Ex: Le seul outil qui génère un plan complet en 10 minutes sans expertise marketing...",
            height=80, value=st.session_state["wiz_usp"])
        st.info("💡 **Astuce** : Une bonne USP répond à : Qu'est-ce que tu fais, pour qui, et pourquoi c'est différent ?")
        c_back4, c_next4 = st.columns([1, 3])
        with c_back4:
            if st.button("← Retour", key="back4"):
                st.session_state["wiz_step"] = 3
                st.rerun()
        with c_next4:
            if st.button("Continuer →", type="primary", use_container_width=True, key="next4"):
                st.session_state["wiz_target"] = target
                st.session_state["wiz_usp"]    = usp
                st.session_state["wiz_step"]   = 5
                st.rerun()

# ── ÉTAPE 5 : Analyse & résultat ──────────────────────────────────────────────
if current_step >= 5:
    done5 = st.session_state.get("wiz_done", False)
    active5 = current_step == 5
    cls5 = "wiz-step done" if done5 else "wiz-step active"
    num_cls5 = "step-num done" if done5 else "step-num"
    st.markdown(f"""<div class="{cls5}">
      <div style="display:flex;align-items:center;margin-bottom:16px">
        <span class="{num_cls5}">{'✓' if done5 else '5'}</span>
        <span class="step-title">Récapitulatif & Analyse instantanée</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if active5 or done5:
        # Récapitulatif
        proj   = st.session_state.get("wiz_project_name","")
        act    = st.session_state.get("wiz_activity","")
        goal   = st.session_state.get("wiz_goal","")
        budget = st.session_state.get("wiz_budget",200)
        kws    = st.session_state.get("wiz_keywords",[])
        target = st.session_state.get("wiz_target","")
        usp    = st.session_state.get("wiz_usp","")
        mat    = st.session_state.get("wiz_maturity","launched")
        url    = st.session_state.get("wiz_website","")

        st.markdown(f"""
<div class="result-card">
  <div style="font-size:1.2rem;font-weight:900;margin-bottom:14px">🎯 Projet : {proj}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">
    <div style="background:rgba(255,255,255,.08);border-radius:10px;padding:12px">
      <div style="font-size:.65rem;color:#44C1BA;font-weight:700;text-transform:uppercase;margin-bottom:5px">Activité</div>
      <div style="font-size:.88rem">{act}</div>
    </div>
    <div style="background:rgba(255,255,255,.08);border-radius:10px;padding:12px">
      <div style="font-size:.65rem;color:#44C1BA;font-weight:700;text-transform:uppercase;margin-bottom:5px">Objectif</div>
      <div style="font-size:.88rem">{goal}</div>
    </div>
    <div style="background:rgba(255,255,255,.08);border-radius:10px;padding:12px">
      <div style="font-size:.65rem;color:#44C1BA;font-weight:700;text-transform:uppercase;margin-bottom:5px">Budget</div>
      <div style="font-size:.88rem">{budget} €/mois</div>
    </div>
    <div style="background:rgba(255,255,255,.08);border-radius:10px;padding:12px">
      <div style="font-size:.65rem;color:#44C1BA;font-weight:700;text-transform:uppercase;margin-bottom:5px">Maturité</div>
      <div style="font-size:.88rem">{mat}</div>
    </div>
  </div>
  <div style="margin-bottom:10px">
    <div style="font-size:.65rem;color:#44C1BA;font-weight:700;text-transform:uppercase;margin-bottom:6px">Mots-clés ({len(kws)})</div>
    {''.join(f'<span style="background:rgba(68,193,186,.25);color:white;border-radius:50px;padding:2px 10px;margin:2px;display:inline-block;font-size:.75rem">{k}</span>' for k in kws[:12])}
  </div>
</div>
""", unsafe_allow_html=True)

        # Analyse instantanée des mots-clés
        if kws:
            st.markdown("### 📊 Analyse de vos mots-clés")
            _INTENT_MAP = {
                "acheter":"transactionnel","commander":"transactionnel","prix":"transactionnel",
                "avis":"informationnel","meilleur":"informationnel","comparatif":"informationnel",
                "comment":"informationnel","guide":"informationnel","qu'est":"informationnel",
                "formation":"commercial","cours":"commercial","apprendre":"commercial",
                "service":"commercial","agence":"commercial","freelance":"commercial",
            }
            for kw in kws[:8]:
                kw_lower = kw.lower()
                intent = next((v for k,v in _INTENT_MAP.items() if k in kw_lower), "navigational")
                intent_color = {"transactionnel":"#44C1BA","informationnel":"#393DAC",
                               "commercial":"#267371","navigational":"#339999"}.get(intent,"#339999")
                diff = "Facile" if len(kw) > 12 else "Modéré" if len(kw) > 6 else "Élevé"
                diff_color = {"Facile":"#267371","Modéré":"#44C1BA","Élevé":"#B83D4B"}.get(diff,"#339999")
                volume_est = {"transactionnel": "500-2K","informationnel":"1K-10K",
                              "commercial":"200-1K","navigational":"100-500"}.get(intent,"N/A")
                st.markdown(f"""
<div class="insight-box">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <div style="font-weight:700;color:#0B2221;font-size:.9rem">🔑 {kw}</div>
    <div style="display:flex;gap:8px">
      <span style="background:{intent_color};color:white;border-radius:50px;padding:2px 10px;font-size:.68rem;font-weight:700">{intent}</span>
      <span style="background:{diff_color};color:white;border-radius:50px;padding:2px 10px;font-size:.68rem;font-weight:700">{diff}</span>
    </div>
  </div>
  <div style="font-size:.75rem;color:#339999;margin-top:4px">Volume estimé : {volume_est} recherches/mois</div>
</div>
""", unsafe_allow_html=True)

        # Recommandations personnalisées
        st.markdown("### 💡 Recommandations personnalisées")
        reco_map = {
            "ecommerce": ["Lancez Google Shopping dès votre premier mois", "Optimisez vos fiches produits avec les mots-clés identifiés", "Mettez en place un programme d'avis clients (trust = conversion)"],
            "saas":      ["Créez une page de comparaison vs concurrents (fort pour SEO)", "Lancez un essai gratuit 14j pour réduire la friction", "Investissez en content marketing technique (HubSpot model)"],
            "service":   ["Référencez-vous sur Google My Business (gratuit, fort impact local)", "Créez une page résultats/cas clients avec chiffres concrets", "Lancez une newsletter hebdo expertise pour fidéliser"],
            "consulting":["Publiez 1 article LinkedIn expert/semaine minimum", "Créez votre newsletter avec Beehiiv ou Substack (gratuit)", "Positionnez-vous sur 1 niche précise plutôt que généraliste"],
            "content":   ["Analysez vos 3 meilleurs contenus et doublez la cadence sur ce format", "Lancez une newsletter payante sur votre meilleur sujet", "Collaborez avec 2-3 créateurs complémentaires pour croître"],
            "other":     ["Définissez 1 canal d'acquisition prioritaire et maîtrisez-le à fond", "Collectez 10 témoignages clients et affichez-les partout", "Testez un budget pub de 50€ sur Google avant d'investir plus"],
        }
        recos = reco_map.get(act, reco_map["other"])
        for i, r in enumerate(recos, 1):
            st.markdown(f"**{i}.** {r}")

        # Actions
        c_back5, c_analyse, c_restart = st.columns([1, 2, 1])
        with c_back5:
            if st.button("← Retour", key="back5"):
                st.session_state["wiz_step"] = 4
                st.rerun()
        with c_analyse:
            if st.button("🎯 Lancer l'analyse complète dans BiziApp", type="primary", use_container_width=True):
                # Pré-remplir les params dans session_state pour BiziApp
                st.session_state["prefill_activity"] = act
                st.session_state["prefill_goal"]     = goal
                st.session_state["prefill_budget"]   = budget
                st.session_state["prefill_maturity"] = mat
                st.session_state["prefill_website"]  = url
                st.session_state["wiz_done"]         = True
                st.success("✅ Paramètres transmis ! Retournez sur la page principale pour lancer l'analyse complète.")
        with c_restart:
            if st.button("🔄 Nouveau projet"):
                for k in ["wiz_step","wiz_project_name","wiz_keywords","wiz_activity","wiz_goal",
                          "wiz_budget","wiz_website","wiz_maturity","wiz_target","wiz_usp","wiz_done"]:
                    st.session_state.pop(k, None)
                st.rerun()

        # Export JSON du projet
        project_export = {
            "nom": proj, "activite": act, "objectif": goal,
            "budget_mensuel": budget, "maturite": mat,
            "mots_cles": kws, "cible": target, "usp": usp,
            "website": url,
            "cree_le": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "version": "BiziApp v3.2",
        }
        st.download_button(
            "⬇️ Télécharger mon projet (JSON)",
            data=json.dumps(project_export, ensure_ascii=False, indent=2),
            file_name=f"projet_{re.sub(r'[^a-z0-9]', '_', proj.lower()[:30])}.json",
            mime="application/json",
        )
