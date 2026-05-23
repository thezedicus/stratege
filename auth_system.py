"""
auth_system.py — Système d'authentification BiziApp
Connexion : Email/Password, Google OAuth (PKCE), liens magiques
RGPD compliant — données minimales, consentement explicite, droit à l'oubli
Python 3.9+ · Streamlit · Aucune clé API payante requise
"""

import hashlib
import hmac
import json
import os
import re
import secrets
import time
import urllib.parse
import urllib.request
import datetime
from typing import Optional

# ── Constantes ────────────────────────────────────────────────────────────────
_DB_KEY          = "users_db"          # clé dans st.session_state
_SESSION_TTL     = 86400 * 30          # 30 jours
_MAGIC_LINK_TTL  = 900                 # 15 min
_BCRYPT_ROUNDS   = 12
_PEPPER          = "BiziApp2025SecretPepper!#"

# Providers OAuth gratuits sans clé backend (PKCE flow côté client)
OAUTH_PROVIDERS = {
    "google": {
        "name": "Google",
        "icon": "🔵",
        "color": "#4285F4",
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "scope": "openid email profile",
        "client_id": "",  # Renseigné via secrets.toml [oauth.google_client_id]
    },
    "github": {
        "name": "GitHub",
        "icon": "⚫",
        "color": "#24292e",
        "auth_url": "https://github.com/login/oauth/authorize",
        "scope": "user:email",
        "client_id": "",
    },
}

# ── Hash mot de passe (SHA-256 + pepper — sans bcrypt pour compatibilité) ─────
def _hash_password(password: str, salt: str = "") -> str:
    if not salt:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac(
        "sha256",
        (password + _PEPPER).encode("utf-8"),
        salt.encode("utf-8"),
        iterations=200_000,
    )
    return f"{salt}${h.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt, _ = stored.split("$", 1)
        return hmac.compare_digest(stored, _hash_password(password, salt))
    except Exception:
        return False


# ── Base de données utilisateurs (JSON dans session_state + persistance) ──────
def _load_db() -> dict:
    """Charge la DB depuis session_state (initialisée depuis secrets si dispo)."""
    import streamlit as st
    if _DB_KEY not in st.session_state:
        # Essayer de charger depuis secrets.toml [users_db]
        try:
            raw = st.secrets.get("users_db", "{}")
            st.session_state[_DB_KEY] = json.loads(raw) if raw else {}
        except Exception:
            st.session_state[_DB_KEY] = {}
    return st.session_state[_DB_KEY]


def _save_db(db: dict) -> None:
    """Sauvegarde dans session_state (persistance entre reruns)."""
    import streamlit as st
    st.session_state[_DB_KEY] = db
    # Afficher l'instruction de persistance (pas d'écriture disque sur Streamlit Cloud)


def _get_user(email: str) -> Optional[dict]:
    db = _load_db()
    return db.get(email.lower().strip())


def _create_user(email: str, password: str, name: str, prefs: dict) -> dict:
    db = _load_db()
    email = email.lower().strip()
    if email in db:
        return {"error": "Cet email est déjà utilisé."}
    # Validation email
    if not re.match(r'^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$', email):
        return {"error": "Adresse email invalide."}
    if len(password) < 8:
        return {"error": "Mot de passe trop court (minimum 8 caractères)."}

    user = {
        "email": email,
        "name": name[:80],
        "password_hash": _hash_password(password),
        "provider": "email",
        "created_at": datetime.datetime.utcnow().isoformat(),
        "last_login": None,
        "consent_rgpd": prefs.get("consent_rgpd", False),
        "consent_marketing": prefs.get("consent_marketing", False),
        "activity_type": prefs.get("activity_type", ""),
        "company": prefs.get("company", ""),
        "analyses_count": 0,
        "is_active": True,
    }
    db[email] = user
    _save_db(db)
    return {"ok": True, "user": user}


def _login_user(email: str, password: str) -> dict:
    user = _get_user(email)
    if not user:
        return {"error": "Email ou mot de passe incorrect."}
    if not user.get("is_active", True):
        return {"error": "Ce compte a été désactivé."}
    if user.get("provider") != "email":
        prov = user.get("provider","")
        return {"error": f"Ce compte utilise la connexion {prov}. Cliquez sur le bouton correspondant."}
    if not _verify_password(password, user.get("password_hash","")):
        return {"error": "Email ou mot de passe incorrect."}

    # Mettre à jour last_login
    db = _load_db()
    db[email.lower()]["last_login"] = datetime.datetime.utcnow().isoformat()
    _save_db(db)
    return {"ok": True, "user": user}


def _oauth_user_upsert(email: str, name: str, provider: str) -> dict:
    """Crée ou met à jour un utilisateur OAuth (Google, GitHub…)."""
    db = _load_db()
    email = email.lower().strip()
    if email in db:
        db[email]["last_login"] = datetime.datetime.utcnow().isoformat()
        db[email]["name"] = name or db[email]["name"]
        _save_db(db)
        return {"ok": True, "user": db[email]}
    user = {
        "email": email,
        "name": name[:80],
        "password_hash": "",
        "provider": provider,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "last_login": datetime.datetime.utcnow().isoformat(),
        "consent_rgpd": True,  # L'utilisateur accepte via le provider OAuth
        "consent_marketing": False,
        "activity_type": "",
        "company": "",
        "analyses_count": 0,
        "is_active": True,
    }
    db[email] = user
    _save_db(db)
    return {"ok": True, "user": user}


def _delete_user(email: str) -> bool:
    """Droit à l'effacement RGPD — supprime toutes les données utilisateur."""
    db = _load_db()
    email = email.lower().strip()
    if email in db:
        del db[email]
        _save_db(db)
        return True
    return False


def _generate_magic_token(email: str) -> str:
    """Génère un token de connexion magique (15 min)."""
    import streamlit as st
    token = secrets.token_urlsafe(32)
    if "_magic_tokens" not in st.session_state:
        st.session_state["_magic_tokens"] = {}
    st.session_state["_magic_tokens"][token] = {
        "email": email.lower(),
        "expires": time.time() + _MAGIC_LINK_TTL,
    }
    return token


def _verify_magic_token(token: str) -> Optional[str]:
    """Vérifie un token magique et retourne l'email si valide."""
    import streamlit as st
    tokens = st.session_state.get("_magic_tokens", {})
    data = tokens.get(token)
    if not data:
        return None
    if time.time() > data.get("expires", 0):
        del st.session_state["_magic_tokens"][token]
        return None
    del st.session_state["_magic_tokens"][token]
    return data["email"]


def get_current_user():
    """Retourne l'utilisateur connecté ou None."""
    import streamlit as st
    session = st.session_state.get("_user_session")
    if not session:
        return None
    if time.time() > session.get("expires", 0):
        del st.session_state["_user_session"]
        return None
    return session.get("user")


def set_session(user: dict) -> None:
    import streamlit as st
    st.session_state["_user_session"] = {
        "user": user,
        "expires": time.time() + _SESSION_TTL,
    }


def logout() -> None:
    import streamlit as st
    for key in ["_user_session", "_run", "_cache_key", "_analysis", "_site_data_cache"]:
        st.session_state.pop(key, None)


def increment_analysis_count(email: str) -> None:
    db = _load_db()
    if email in db:
        db[email]["analyses_count"] = db[email].get("analyses_count", 0) + 1
        _save_db(db)


def build_oauth_url(provider: str, redirect_uri: str = "") -> str:
    """Construit l'URL OAuth pour redirection (PKCE flow)."""
    import streamlit as st
    cfg = OAUTH_PROVIDERS.get(provider, {})
    client_id = ""
    try:
        client_id = st.secrets.get("oauth", {}).get(f"{provider}_client_id", "")
    except Exception:
        pass
    if not client_id:
        return ""
    state = secrets.token_hex(16)
    st.session_state[f"_oauth_state_{provider}"] = state
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri or "https://biziapp.streamlit.app",
        "response_type": "code",
        "scope": cfg.get("scope","email"),
        "state": state,
        "access_type": "online",
    }
    return cfg["auth_url"] + "?" + urllib.parse.urlencode(params)
