"""
pricing_plans.py — Plans tarifaires BiziApp + Landing neuromarketing
Neuromarketing : ancrage prix, rareté, réciprocité, preuve sociale, identité
Plans : Demo gratuit · Starter 39€/mois · Pro 89€/mois + Annuel -30%
RGPD compliant · SVG illustrations (pas d'emojis)
"""

import streamlit as st
import datetime

# ── SVG icons (no emojis, no external requests) ──────────────────────────────
SVG_CHECK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="11" fill="#44C1BA"/><path d="M7 12l4 4 6-7" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SVG_CROSS = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="11" fill="#C6ECD9"/><path d="M8 8l8 8M16 8l-8 8" stroke="#339999" stroke-width="2" stroke-linecap="round"/></svg>'
SVG_STAR  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="#44C1BA"><polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/></svg>'
SVG_BOLT  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" fill="#44C1BA" stroke="#267371" stroke-width="1.5" stroke-linejoin="round"/></svg>'
SVG_LOCK  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="3" y="11" width="18" height="11" rx="2" fill="#C6ECD9" stroke="#267371" stroke-width="1.5"/><path d="M7 11V7a5 5 0 0110 0v4" stroke="#267371" stroke-width="1.5" stroke-linecap="round"/></svg>'
SVG_GIFT  = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="10" width="18" height="12" rx="1" fill="#C6ECD9" stroke="#267371" stroke-width="1.5"/><rect x="1" y="6" width="22" height="5" rx="1" fill="#44C1BA" stroke="#267371" stroke-width="1.5"/><path d="M12 6V22M12 6c0 0-2-4 0-5s2 5 0 5M12 6c0 0 2-4 0-5s-2 5 0 5" stroke="white" stroke-width="1.5" stroke-linecap="round"/></svg>'
SVG_ARROW = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M12 5l7 7-7 7" stroke="#44C1BA" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SVG_TIMER = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="13" r="8" stroke="#B83D4B" stroke-width="1.5"/><path d="M12 9v4l3 3" stroke="#B83D4B" stroke-width="1.5" stroke-linecap="round"/><path d="M9 2h6" stroke="#B83D4B" stroke-width="1.5" stroke-linecap="round"/></svg>'
SVG_USER  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" fill="#C6ECD9" stroke="#267371" stroke-width="1.5"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="#267371" stroke-width="1.5" stroke-linecap="round"/></svg>'
SVG_CHART = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="3" y="14" width="4" height="7" rx="1" fill="#44C1BA"/><rect x="10" y="9" width="4" height="12" rx="1" fill="#267371"/><rect x="17" y="4" width="4" height="17" rx="1" fill="#0B2221"/></svg>'

# ── Plans ─────────────────────────────────────────────────────────────────────
PLANS = {
    "demo": {
        "name": "Demo",
        "subtitle": "Testez tous les outils, sans carte bancaire",
        "monthly": 0,
        "annual": 0,
        "color": "#339999",
        "badge": "Gratuit",
        "badge_color": "#C6ECD9",
        "features": [
            ("Analyse SWOT basique", True),
            ("1 secteur d'activité", True),
            ("Personas (2 profils)", True),
            ("Résultats limités (50%)", True),
            ("Filigrane sur les exports", True),
            ("Support communauté", True),
            ("Analyse PESTEL complète", False),
            ("14 modules stratégiques", False),
            ("Export PDF/JSON", False),
            ("Données live (news, Sirene)", False),
            ("Plan d'action 180j", False),
            ("Intelligence concurrentielle", False),
        ],
        "cta": "Commencer gratuitement",
        "cta_style": "secondary",
    },
    "starter": {
        "name": "Starter",
        "subtitle": "Pour les dirigeants qui veulent aller vite et bien",
        "monthly": 39,
        "annual": 27,  # 30% de réduction
        "color": "#44C1BA",
        "badge": "Populaire",
        "badge_color": "#44C1BA",
        "popular": True,
        "features": [
            ("14 modules stratégiques complets", True),
            ("SWOT · PESTEL · QQOQCCP · Porter", True),
            ("Personas + Customer Journey", True),
            ("Plan marketing personnalisé", True),
            ("SEO / GEO 2025", True),
            ("Export PDF + JSON", True),
            ("Données live Sirene + News", True),
            ("Support email 48h", True),
            ("Rapport gratuit après inscription", True),
            ("Analyses illimitées", False),
            ("Intelligence concurrentielle avancée", False),
            ("Chatbot IA intégré", False),
        ],
        "cta": "Commencer l'essai 7j gratuit",
        "cta_style": "primary",
    },
    "pro": {
        "name": "Pro",
        "subtitle": "Pour les dirigeants qui pilotent vraiment leur croissance",
        "monthly": 89,
        "annual": 62,  # 30% de réduction
        "color": "#0B2221",
        "badge": "Complet",
        "badge_color": "#0B2221",
        "features": [
            ("Tout Starter inclus", True),
            ("Analyses illimitées", True),
            ("Intelligence concurrentielle avancée", True),
            ("Chatbot IA stratégique", True),
            ("Veille temps réel (news, trends)", True),
            ("Porter 5 Forces + Ansoff", True),
            ("Séquences email complètes", True),
            ("Social Media Strategy", True),
            ("Pricing Strategy avancée", True),
            ("Export PDF personnalisé + logo", True),
            ("Support prioritaire 4h", True),
            ("Accès API BiziApp", True),
        ],
        "cta": "Commencer Pro — 7j gratuit",
        "cta_style": "primary",
    },
}

# ── CSS Pricing ───────────────────────────────────────────────────────────────
PRICING_CSS = """
<style>
.pricing-section{padding:24px 0 40px}
.pricing-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0}
@media(max-width:900px){.pricing-grid{grid-template-columns:1fr}}
.pricing-card{background:white;border-radius:20px;padding:28px 24px;border:2px solid #C6ECD9;
  position:relative;transition:transform .25s cubic-bezier(.34,1.56,.64,1),box-shadow .25s}
.pricing-card:hover{transform:translateY(-6px);box-shadow:0 20px 48px rgba(68,193,186,.18)}
.pricing-card.popular{border-color:#44C1BA;box-shadow:0 8px 32px rgba(68,193,186,.2)}
.pricing-card.pro-card{background:linear-gradient(135deg,#0B2221 0%,#267371 100%);border-color:#44C1BA}
.pricing-badge{position:absolute;top:-12px;left:50%;transform:translateX(-50%);
  border-radius:50px;padding:4px 16px;font-size:.72rem;font-weight:800;white-space:nowrap;
  letter-spacing:.06em;text-transform:uppercase}
.pricing-name{font-size:1.3rem;font-weight:900;margin-bottom:4px}
.pricing-sub{font-size:.78rem;line-height:1.5;margin-bottom:20px;opacity:.8}
.pricing-price{margin-bottom:6px}
.pricing-amount{font-size:2.8rem;font-weight:900;line-height:1}
.pricing-period{font-size:.8rem;opacity:.7;font-weight:500}
.pricing-annual-note{font-size:.72rem;margin-bottom:20px;font-weight:600}
.pricing-feature{display:flex;align-items:center;gap:9px;padding:6px 0;
  border-bottom:1px solid rgba(0,0,0,.04);font-size:.82rem}
.pricing-feature:last-child{border-bottom:none}
.pricing-cta{width:100%;padding:13px;border-radius:12px;font-weight:800;font-size:.92rem;
  cursor:pointer;border:none;margin-top:20px;transition:all .2s;letter-spacing:.02em}
.pricing-cta-primary{background:linear-gradient(135deg,#44C1BA,#267371);color:white}
.pricing-cta-primary:hover{transform:scale(1.02);box-shadow:0 6px 20px rgba(68,193,186,.4)}
.pricing-cta-secondary{background:transparent;color:#267371;border:2px solid #C6ECD9!important}
.pricing-cta-secondary:hover{border-color:#44C1BA!important;background:#F7FBF4}
.anchor-box{background:linear-gradient(135deg,#FDF0F2,#F7EEF0);border:1.5px solid #B83D4B;
  border-radius:14px;padding:18px 20px;margin-bottom:24px;text-align:center}
.anchor-consultant{font-size:1.6rem;font-weight:900;color:#B83D4B;text-decoration:line-through}
.anchor-biziapp{font-size:1.4rem;font-weight:900;color:#267371}
.rarity-bar{background:linear-gradient(135deg,#0B2221,#267371);border-radius:10px;
  padding:12px 18px;color:white;display:flex;align-items:center;gap:12px;margin:16px 0}
.rarity-progress{flex:1;height:8px;background:rgba(255,255,255,.2);border-radius:99px;overflow:hidden}
.rarity-fill{height:100%;background:#44C1BA;border-radius:99px;width:73%}
.annual-toggle{display:flex;align-items:center;justify-content:center;gap:12px;margin:16px 0}
.annual-badge{background:#44C1BA;color:white;border-radius:50px;padding:3px 12px;
  font-size:.72rem;font-weight:800;animation:pulseRing 2.5s infinite}
.guarantee-strip{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;
  margin:16px 0;font-size:.76rem;color:#267371;font-weight:600}
</style>
"""


def render_countdown():
    """Compte à rebours dynamique (neuromarketing : rareté temporelle)."""
    now = datetime.datetime.now()
    end_of_month = (now.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
    delta = end_of_month - now
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    return f"{delta.days}j {hours:02d}h {minutes:02d}m"


def render_pricing_page(billing="monthly", on_plan_select=None):
    """
    Affiche la page pricing complète avec neuromarketing maximal.
    billing: 'monthly' | 'annual'
    on_plan_select: callback(plan_name)
    """
    st.markdown(PRICING_CSS, unsafe_allow_html=True)

    # ── Ancrage prix (neuromarketing : référence haute → le nôtre semble low) ──
    st.markdown(f"""
<div class="anchor-box">
  <div style="font-size:.78rem;color:#B83D4B;font-weight:700;text-transform:uppercase;
    letter-spacing:.08em;margin-bottom:8px">Ce qu'un consultant stratégique vous coûterait</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap">
    <div>
      <div class="anchor-consultant">5 000€ / diagnostic</div>
      <div style="font-size:.72rem;color:#B83D4B">Cabinet conseil classique</div>
    </div>
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
      <path d="M5 12h14M12 5l7 7-7 7" stroke="#44C1BA" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    <div>
      <div class="anchor-biziapp">dès 39€ / mois</div>
      <div style="font-size:.72rem;color:#267371;font-weight:600">BiziApp — résultat identique</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Rareté + FOMO ─────────────────────────────────────────────────────────
    _countdown = render_countdown()
    st.markdown(f"""
<div class="rarity-bar">
  {SVG_TIMER}
  <div style="flex:1">
    <div style="font-size:.76rem;font-weight:700;margin-bottom:4px">
      Offre de lancement — 30% de réduction se termine dans {_countdown}
    </div>
    <div class="rarity-progress"><div class="rarity-fill"></div></div>
  </div>
  <div style="font-size:.72rem;color:#44C1BA;font-weight:700;white-space:nowrap">73 / 100 places</div>
</div>
""", unsafe_allow_html=True)

    # ── Toggle mensuel / annuel ────────────────────────────────────────────────
    _billing_choice = st.radio(
        "", ["Mensuel", "Annuel (-30%)"],
        horizontal=True, index=1 if billing == "annual" else 0,
        label_visibility="collapsed", key="billing_toggle"
    )
    is_annual = "Annuel" in _billing_choice

    # ── Grille de prix ─────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]

    for col, (plan_id, plan) in zip(cols, PLANS.items()):
        price = plan["annual"] if is_annual else plan["monthly"]
        is_popular = plan.get("popular", False)
        is_pro = plan_id == "pro"
        text_color = "white" if is_pro else "#0B2221"
        sub_color  = "rgba(255,255,255,.75)" if is_pro else "#339999"
        feature_border = "rgba(255,255,255,.1)" if is_pro else "rgba(0,0,0,.04)"

        with col:
            features_html = "".join(
                f'<div class="pricing-feature" style="border-bottom:1px solid {feature_border}">'
                f'{SVG_CHECK if ok else SVG_CROSS}'
                f'<span style="color:{text_color if ok else "#9CA3AF"};{"" if ok else "opacity:.6"}'
                f';font-weight:{"600" if ok else "400"}">{feat}</span>'
                f'</div>'
                for feat, ok in plan["features"]
            )

            annual_note = f'<div class="pricing-annual-note" style="color:{"#44C1BA" if is_pro else "#267371"}">Facturation annuelle — économisez {plan["monthly"] * 12 - price * 12}€/an</div>' if is_annual and price > 0 else '<div class="pricing-annual-note" style="color:#339999">Facturation mensuelle — résiliable à tout moment</div>' if price > 0 else '<div class="pricing-annual-note" style="color:#339999">Accès permanent · Sans carte bancaire</div>'

            st.markdown(f"""
<div class="pricing-card {'popular' if is_popular else ''} {'pro-card' if is_pro else ''}"
  style="{'background:linear-gradient(135deg,#0B2221 0%,#267371 100%)' if is_pro else ''}">
  <div class="pricing-badge"
    style="background:{plan['badge_color']};color:{'white' if is_pro else 'white' if is_popular else '#267371'}">
    {plan['badge']}
  </div>
  <div class="pricing-name" style="color:{text_color}">{plan['name']}</div>
  <div class="pricing-sub" style="color:{sub_color}">{plan['subtitle']}</div>
  <div class="pricing-price">
    <span class="pricing-amount" style="color:{text_color}">
      {'Gratuit' if price == 0 else f'{price}€'}
    </span>
    {f'<span class="pricing-period" style="color:{sub_color}">/mois</span>' if price > 0 else ''}
  </div>
  {annual_note}
  <div style="margin:0 0 4px">
    {features_html}
  </div>
</div>
""", unsafe_allow_html=True)

            # Bouton CTA (Streamlit natif pour les callbacks)
            btn_label = plan["cta"]
            btn_type = "primary" if plan["cta_style"] == "primary" else "secondary"
            if st.button(btn_label, key=f"plan_{plan_id}", type=btn_type, use_container_width=True):
                if on_plan_select:
                    on_plan_select(plan_id)
                else:
                    st.session_state["selected_plan"] = plan_id
                    st.rerun()

    # ── Garanties micro (neuromarketing : réduction du risque) ─────────────────
    st.markdown("""
<div class="guarantee-strip">
  <span>Remboursé sous 30j sans question</span>
  <span>|</span>
  <span>Résiliation en 1 clic</span>
  <span>|</span>
  <span>Données hebergées en France</span>
  <span>|</span>
  <span>Conforme RGPD</span>
</div>
""", unsafe_allow_html=True)

    # ── Preuve sociale (neuromarketing) ────────────────────────────────────────
    st.markdown(f"""
<div style="background:#F7FBF4;border-radius:14px;padding:20px 24px;border:1.5px solid #C6ECD9;margin-top:16px">
  <div style="font-size:.78rem;font-weight:700;color:#267371;text-align:center;margin-bottom:14px;text-transform:uppercase;letter-spacing:.06em">
    Ils ont remplace leur cabinet conseil par BiziApp
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">
    <div style="background:white;border-radius:12px;padding:14px;border:1px solid #C6ECD9">
      <div style="display:flex;gap:4px;margin-bottom:6px">{SVG_STAR*5}</div>
      <div style="font-size:.76rem;color:#0B2221;line-height:1.5;font-style:italic">
        "Je gerai 11 salaries et je n'avais pas de strategie claire. BiziApp m'en a fait une en 10 minutes. Maintenant j'ai un cap."
      </div>
      <div style="font-size:.68rem;color:#339999;margin-top:8px;font-weight:600">Thomas D. — Dirigeant, Lyon</div>
    </div>
    <div style="background:white;border-radius:12px;padding:14px;border:1px solid #C6ECD9">
      <div style="display:flex;gap:4px;margin-bottom:6px">{SVG_STAR*5}</div>
      <div style="font-size:.76rem;color:#0B2221;line-height:1.5;font-style:italic">
        "J'ai montre le plan BiziApp a ma banque pour mon financement. Ils ont trouve ca tres professionnel. Le pret a ete accepte."
      </div>
      <div style="font-size:.68rem;color:#339999;margin-top:8px;font-weight:600">Sarah M. — Freelance, Paris</div>
    </div>
    <div style="background:white;border-radius:12px;padding:14px;border:1px solid #C6ECD9">
      <div style="display:flex;gap:4px;margin-bottom:6px">{SVG_STAR*5}</div>
      <div style="font-size:.76rem;color:#0B2221;line-height:1.5;font-style:italic">
        "J'utilise BiziApp Pro avant chaque client. Gain de temps enorme, mes presentations sont percutantes."
      </div>
      <div style="font-size:.68rem;color:#339999;margin-top:8px;font-weight:600">Marc R. — Consultant, Bordeaux</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Reciprocite (rapport gratuit) ─────────────────────────────────────────
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#0B2221,#267371);border-radius:14px;
  padding:18px 24px;margin-top:16px;display:flex;align-items:center;gap:16px;color:white">
  {SVG_GIFT}
  <div style="flex:1">
    <div style="font-weight:800;font-size:.9rem;margin-bottom:3px">Rapport offert apres inscription</div>
    <div style="font-size:.76rem;opacity:.8">Analyse de votre secteur (valeur 200€) offerte avec tout compte cree aujourd'hui</div>
  </div>
  <div style="font-size:1.1rem;font-weight:900;color:#44C1BA;white-space:nowrap">+200€ offerts</div>
</div>
""", unsafe_allow_html=True)
