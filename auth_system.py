"""
auth_system.py — Authentification BiziApp v5.4
Email/Password robuste + session persistante
Sans OAuth externe (client_id requis cote serveur — non disponible sur Streamlit Cloud gratuit)
RGPD compliant
"""

import hashlib, hmac, json, re, secrets, time, datetime
from typing import Optional

_DB_KEY         = "users_db"
_SESSION_TTL    = 86400 * 30   # 30 jours
_PEPPER         = "BiziApp2025SecretPepper!#xZ9"
_MAX_ATTEMPTS   = 5
_LOCKOUT_SEC    = 300  # 5 min lockout apres trop d echecs


# ── Hash mot de passe ───────────────────────────────────────────────────────
def _hash_pw(password: str, salt: str = "") -> str:
    if not salt:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac(
        "sha256",
        (password + _PEPPER).encode("utf-8"),
        salt.encode("utf-8"),
        iterations=100_000,
    )
    return f"{salt}${h.hex()}"

def _verify_pw(password: str, stored: str) -> bool:
    try:
        salt, _ = stored.split("$", 1)
        return hmac.compare_digest(stored, _hash_pw(password, salt))
    except Exception:
        return False


# ── Base de donnees en session_state ────────────────────────────────────────
def _load_db() -> dict:
    import streamlit as st
    if _DB_KEY not in st.session_state:
        try:
            raw = st.secrets.get("users_db", "{}")
            st.session_state[_DB_KEY] = json.loads(raw) if isinstance(raw, str) else (raw if isinstance(raw, dict) else {})
        except Exception:
            st.session_state[_DB_KEY] = {}
    return st.session_state[_DB_KEY]

def _save_db(db: dict) -> None:
    import streamlit as st
    st.session_state[_DB_KEY] = db


# ── Validation ──────────────────────────────────────────────────────────────
def _valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", email.strip()))

def _valid_pw(pw: str) -> tuple:
    """Retourne (ok, message)."""
    if len(pw) < 8:
        return False, "Minimum 8 caracteres"
    if not re.search(r"[0-9]", pw):
        return False, "Au moins 1 chiffre requis"
    return True, ""


# ── CRUD utilisateurs ────────────────────────────────────────────────────────
def _get_user(email: str) -> Optional[dict]:
    return _load_db().get(email.lower().strip())

def create_user(email: str, password: str, name: str, prefs: dict = None) -> dict:
    db = _load_db()
    email = email.lower().strip()
    if not _valid_email(email):
        return {"error": "Adresse email invalide."}
    pw_ok, pw_msg = _valid_pw(password)
    if not pw_ok:
        return {"error": f"Mot de passe invalide : {pw_msg}."}
    if email in db:
        return {"error": "Cet email est deja utilise. Connectez-vous."}
    user = {
        "email":              email,
        "name":               (name or email.split("@")[0])[:80],
        "password_hash":      _hash_pw(password),
        "provider":           "email",
        "created_at":         datetime.datetime.utcnow().isoformat(),
        "last_login":         None,
        "consent_rgpd":       bool((prefs or {}).get("consent_rgpd", True)),
        "consent_marketing":  bool((prefs or {}).get("consent_marketing", False)),
        "activity_type":      (prefs or {}).get("activity_type", ""),
        "company":            (prefs or {}).get("company", ""),
        "analyses_count":     0,
        "is_active":          True,
        "failed_attempts":    0,
        "locked_until":       0,
    }
    db[email] = user
    _save_db(db)
    return {"ok": True, "user": user}

def login_user(email: str, password: str) -> dict:
    email = email.lower().strip()
    user = _get_user(email)
    if not user:
        return {"error": "Email ou mot de passe incorrect."}
    if not user.get("is_active", True):
        return {"error": "Ce compte est desactive."}
    # Lockout
    if time.time() < user.get("locked_until", 0):
        remaining = int(user["locked_until"] - time.time())
        return {"error": f"Compte temporairement bloque. Reessayez dans {remaining}s."}
    if user.get("provider", "email") != "email":
        return {"error": f"Utilisez la connexion par email/mot de passe pour ce compte."}
    if not _verify_pw(password, user.get("password_hash", "")):
        # Incrementer echecs
        db = _load_db()
        db[email]["failed_attempts"] = db[email].get("failed_attempts", 0) + 1
        if db[email]["failed_attempts"] >= _MAX_ATTEMPTS:
            db[email]["locked_until"] = time.time() + _LOCKOUT_SEC
            db[email]["failed_attempts"] = 0
            _save_db(db)
            return {"error": "Trop d echecs. Compte bloque 5 minutes."}
        _save_db(db)
        return {"error": "Email ou mot de passe incorrect."}
    # Succes
    db = _load_db()
    db[email]["last_login"]        = datetime.datetime.utcnow().isoformat()
    db[email]["failed_attempts"]   = 0
    db[email]["locked_until"]      = 0
    _save_db(db)
    return {"ok": True, "user": db[email]}

def login_or_create_social(email: str, name: str, provider: str) -> dict:
    """Connexion/creation via provider social (Google, GitHub…) — simule le callback OAuth."""
    if not email or not _valid_email(email):
        return {"error": "Email invalide."}
    db = _load_db()
    email = email.lower().strip()
    if email in db:
        db[email]["last_login"] = datetime.datetime.utcnow().isoformat()
        db[email]["name"]       = name or db[email]["name"]
        _save_db(db)
        return {"ok": True, "user": db[email]}
    user = {
        "email":             email,
        "name":              (name or email.split("@")[0])[:80],
        "password_hash":     "",
        "provider":          provider,
        "created_at":        datetime.datetime.utcnow().isoformat(),
        "last_login":        datetime.datetime.utcnow().isoformat(),
        "consent_rgpd":      True,
        "consent_marketing": False,
        "activity_type":     "",
        "company":           "",
        "analyses_count":    0,
        "is_active":         True,
        "failed_attempts":   0,
        "locked_until":      0,
    }
    db[email] = user
    _save_db(db)
    return {"ok": True, "user": user}

def delete_user(email: str) -> bool:
    """RGPD — suppression complete."""
    db = _load_db()
    email = email.lower().strip()
    if email in db:
        del db[email]
        _save_db(db)
        return True
    return False

def update_user(email: str, fields: dict) -> bool:
    db = _load_db()
    email = email.lower().strip()
    if email not in db:
        return False
    for k, v in fields.items():
        if k not in ("email", "password_hash"):
            db[email][k] = v
    _save_db(db)
    return True

def change_password(email: str, old_pw: str, new_pw: str) -> dict:
    result = login_user(email, old_pw)
    if "error" in result:
        return result
    pw_ok, pw_msg = _valid_pw(new_pw)
    if not pw_ok:
        return {"error": f"Nouveau mot de passe invalide : {pw_msg}"}
    db = _load_db()
    db[email.lower()]["password_hash"] = _hash_pw(new_pw)
    _save_db(db)
    return {"ok": True}


# ── Session ──────────────────────────────────────────────────────────────────
def get_current_user() -> Optional[dict]:
    import streamlit as st
    session = st.session_state.get("_user_session")
    if not session:
        return None
    if time.time() > session.get("expires", 0):
        st.session_state.pop("_user_session", None)
        return None
    return session.get("user")

def set_session(user: dict) -> None:
    import streamlit as st
    st.session_state["_user_session"] = {
        "user":    user,
        "expires": time.time() + _SESSION_TTL,
    }

def logout() -> None:
    import streamlit as st
    for k in ["_user_session","_run","_cache_key","_analysis","_site_data_cache","bizibot_history","_bizibot_suggs"]:
        st.session_state.pop(k, None)

def increment_analysis_count(email: str) -> None:
    db = _load_db()
    if email in db:
        db[email]["analyses_count"] = db[email].get("analyses_count", 0) + 1
        _save_db(db)

# ── Demo user ─────────────────────────────────────────────────────────────────
def get_demo_user() -> dict:
    return {
        "email":            "demo@biziapp.fr",
        "name":             "Visiteur",
        "provider":         "demo",
        "analyses_count":   0,
        "activity_type":    "",
        "is_active":        True,
    }
