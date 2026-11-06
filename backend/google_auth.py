"""Google sign-in: verify the ID token the app receives from Google, using Google's published signing keys.

The app (web or Android) gets a signed ID token from Google and sends it here. We check the signature, that it was
issued for OUR client id, that it has not expired, and that the email is verified. Nothing here trusts the app's word.
Configuration (environment):
  GOOGLE_CLIENT_IDS   comma-separated OAuth client ids we accept as the token audience (the "Web client" id first)
  GOOGLE_JWKS_URL     optional, defaults to Google's key set (only overridden in tests)
"""
import os
from typing import List, Optional

import jwt
from jwt import PyJWKClient

JWKS_URL = os.environ.get("GOOGLE_JWKS_URL", "https://www.googleapis.com/oauth2/v3/certs")
ISSUERS = ["https://accounts.google.com", "accounts.google.com"]

_client: Optional[PyJWKClient] = None


def client_ids() -> List[str]:
    return [x.strip() for x in os.environ.get("GOOGLE_CLIENT_IDS", "").split(",") if x.strip()]


def jwks_client() -> PyJWKClient:
    global _client
    if _client is None:
        _client = PyJWKClient(JWKS_URL, cache_keys=True, lifespan=3600)
    return _client


def verify_id_token(token: str, audiences: List[str], keys=None) -> dict:
    """Return the verified claims, or raise ValueError with a safe message."""
    if not audiences:
        raise ValueError("Google sign-in is not set up")
    try:
        signing_key = (keys or jwks_client()).get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token, signing_key.key,
            algorithms=["RS256"],               # never accept HS256 or "none" here
            audience=audiences,
            options={"require": ["exp", "iat", "aud", "iss", "sub"]},
            leeway=30,
        )
    except jwt.PyJWTError:
        raise ValueError("Google sign-in could not be verified")
    if claims.get("iss") not in ISSUERS:  # PyJWT 2.8 takes only one issuer, and Google uses two spellings
        raise ValueError("Google sign-in could not be verified")
    email = (claims.get("email") or "").strip().lower()
    if not email or claims.get("email_verified") not in (True, "true"):
        raise ValueError("Your Google email is not verified")
    claims["email"] = email
    return claims
