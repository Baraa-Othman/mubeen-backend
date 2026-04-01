import json
import logging
from fastapi import HTTPException, Request

import firebase_admin
from firebase_admin import auth, credentials

from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Firebase initialisation ───────────────────────────────────────────────────
# On Render/cloud: set FIREBASE_CREDENTIALS_JSON env var to the full JSON string
# (copy-paste the entire serviceAccountKey.json content as a single env var).
# Locally: keep serviceAccountKey.json on disk and set FIREBASE_CREDENTIALS_PATH.
if settings.FIREBASE_CREDENTIALS_JSON:
    _cred = credentials.Certificate(json.loads(settings.FIREBASE_CREDENTIALS_JSON))
else:
    _cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)

firebase_admin.initialize_app(_cred)


def verify_firebase_token(request: Request) -> str:
    """
    Extract and verify the Firebase ID token from the Authorization header.

    Returns the uid of the authenticated user.
    Raises HTTP 401 if the token is missing or invalid.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        logger.warning("Missing or malformed Authorization header")
        raise HTTPException(status_code=401, detail="رمز التحقق غير صالح")

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        decoded = auth.verify_id_token(token)
        uid: str = decoded["uid"]
        logger.info("Authenticated user: %s", uid)
        return uid
    except Exception as exc:
        logger.warning("Token verification failed: %s", exc)
        raise HTTPException(status_code=401, detail="رمز التحقق غير صالح")
