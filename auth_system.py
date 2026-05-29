"""
auth_system.py — Authentification BiziApp v5.4
Methodes : Email/Password + Streamlit Cloud OAuth (Google) + Mode demo
RGPD compliant — donnees minimales, session locale uniquement
"""

import hashlib
import hmac
import json
import re
import secrets
import time
import datetime
import urllib.parse
import urllib.request
from typing import Optional

# ── Constantes ─────────────────────────────────────────────────────────────
_DB_KEY      = "users_db"
_SESSION_TTL = 86400 * 30   # 30 jours
_OTP_TTL     = 600          # 10 min
_PEPPER      = "BiziApp2025SecretPepper!#"

# ── Hash mot de passe (PBKDF2-SHA256) ──────────────────────────────────────
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


# ── Base de donnees (session_state) ────────────────────────────────────────
def _load_db() -> dict:
    import streamlit as st
    if _DB_KEY not in st.session_state:
        try:
            raw = st.secrets.get("users_db", "{}")
            st.session_state[_DB_KEY] = json.loads(raw) if raw else {}
        except Exception:
            st.session_state[_DB_KEY] = {}
    return st.session_state[_DB_KEY]


def _save_db(db: dict) -> None:
    import streamlit as st
    st.session_state[_DB_KEY] = db


def _get_user(email: str) -> Optional[dict]:
    return _load_db().get(email.lower().strip())


def _create_user(email: str, password: str, name: str, prefs: dict) -> dict:
    db = _load_db()
    email = email.lower().strip()
    if email in db:
        return {"error": "Cet email est deja utilise."}
    if not re.match(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$", email):
        return {"error": "Adresse email invalide."}
    if len(password) < 6:
        return {"error": "Mot de passe trop court (minimum 6 caracteres)."}
    user = {
        "email": email,
        "name": name[:80],
        "password_hash": _hash_password(password),
        "provider": "email",
        "created_at": datetime.datetime.utcnow().isoformat(),
        "last_login": None,
        "consent_rgpd": prefs.get("consent_rgpd", True),
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
        return {"error": "Ce compte a ete desactive."}
    if user.get("provider") != "email":
        prov = user.get("provider", "")
        return {"error": f"Ce compte utilise la connexion {prov}."}
    if not _verify_password(password, user.get("password_hash", "")):
        return {"error": "Email ou mot de passe incorrect."}
    db = _load_db()
    db[email.lower()]["last_login"] = datetime.datetime.utcnow().isoformat()
    _save_db(db)
    return {"ok": True, "user": user}


def _oauth_user_upsert(email: str, name: str, provider: str) -> dict:
    """Cree ou met a jour un utilisateur OAuth."""
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
        "consent_rgpd": True,
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
    db = _load_db()
    email = email.lower().strip()
    if email in db:
        del db[email]
        _save_db(db)
        return True
    return False


# ── OTP (code 6 chiffres) pour connexion sans mot de passe ─────────────────
def generate_otp(email: str) -> str:
    """Genere un code OTP 6 chiffres valide 10 min."""
    import streamlit as st
    code = str(secrets.randbelow(900000) + 100000)
    if "_otps" not in st.session_state:
        st.session_state["_otps"] = {}
    st.session_state["_otps"][email.lower()] = {
        "code": code,
        "expires": time.time() + _OTP_TTL,
    }
    return code


def verify_otp(email: str, code: str) -> bool:
    """Verifie un code OTP."""
    import streamlit as st
    otps = st.session_state.get("_otps", {})
    data = otps.get(email.lower())
    if not data:
        return False
    if time.time() > data.get("expires", 0):
        return False
    return hmac.compare_digest(str(data["code"]), str(code).strip())


# ── Session ─────────────────────────────────────────────────────────────────
def get_current_user() -> Optional[dict]:
    """Retourne l utilisateur connecte ou None."""
    import streamlit as st
    # Methode 1 : session normale
    session = st.session_state.get("_user_session")
    if session and time.time() < session.get("expires", 0):
        return session.get("user")
    # Methode 2 : Streamlit Cloud OAuth natif (st.user)
    try:
        u = st.experimental_user
        if u and u.get("email") and u.get("is_logged_in", False):
            email = u["email"]
            name  = u.get("name", email.split("@")[0])
            result = _oauth_user_upsert(email, name, "streamlit_oauth")
            if result.get("ok"):
                set_session(result["user"])
                return result["user"]
    except Exception:
        pass
    return None


def set_session(user: dict) -> None:
    import streamlit as st
    st.session_state["_user_session"] = {
        "user": user,
        "expires": time.time() + _SESSION_TTL,
    }
    st.session_state["_run"] = False  # reset pour forcer re-analyse


def logout() -> None:
    import streamlit as st
    for key in ["_user_session", "_run", "_cache_key", "_analysis",
                "_site_data_cache", "_otps"]:
        st.session_state.pop(key, None)


def increment_analysis_count(email: str) -> None:
    db = _load_db()
    if email in db:
        db[email]["analyses_count"] = db[email].get("analyses_count", 0) + 1
        _save_db(db)


# ── OAuth URL (Google/GitHub via PKCE) ──────────────────────────────────────
def build_oauth_url(provider: str, redirect_uri: str = "") -> str:
    """Construit l URL OAuth. Necessite un client_id dans secrets.toml."""
    import streamlit as st

    PROVIDERS = {
        "google": {
            "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "scope": "openid email profile",
        },
        "github": {
            "auth_url": "https://github.com/login/oauth/authorize",
            "scope": "user:email",
        },
        "microsoft": {
            "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
            "scope": "openid email profile",
        },
    }

    cfg = PROVIDERS.get(provider)
    if not cfg:
        return ""

    client_id = ""
    try:
        client_id = (st.secrets.get("oauth") or {}).get(f"{provider}_client_id", "")
    except Exception:
        pass

    if not client_id:
        return ""

    state = secrets.token_hex(16)
    st.session_state[f"_oauth_state_{provider}"] = state

    params = {
        "client_id":     client_id,
        "redirect_uri":  redirect_uri or "https://biziapp.streamlit.app",
        "response_type": "code",
        "scope":         cfg["scope"],
        "state":         state,
    }
    if provider == "google":
        params["access_type"] = "online"

    return cfg["auth_url"] + "?" + urllib.parse.urlencode(params)


# ── Connexion demomode (sans compte) ────────────────────────────────────────
def get_demo_user() -> dict:
    """Retourne un utilisateur de demonstration."""
    return {
        "email":          "demo@biziapp.fr",
        "name":           "Visiteur",
        "provider":       "demo",
        "analyses_count": 0,
        "is_active":      True,
        "created_at":     datetime.datetime.utcnow().isoformat(),
    }
