import time
import json
import base64
import hmac
import hashlib
from typing import Optional, Dict, Any
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES, ADMIN_EMAIL, ADMIN_PASSWORD

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def _base64url_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def create_access_token(payload: dict, expires_minutes: int = JWT_EXPIRE_MINUTES) -> str:
    """Generates a secure Base64 HMAC-SHA256 Signed JWT Access Token."""
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    now = int(time.time())
    
    token_data = payload.copy()
    token_data.update({
        "iat": now,
        "exp": now + (expires_minutes * 60)
    })
    
    encoded_header = _base64url_encode(json.dumps(header).encode('utf-8'))
    encoded_payload = _base64url_encode(json.dumps(token_data).encode('utf-8'))
    
    signature_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
    signature = hmac.new(JWT_SECRET.encode('utf-8'), signature_input, hashlib.sha256).digest()
    encoded_signature = _base64url_encode(signature)
    
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def decode_access_token(token: str) -> Optional[dict]:
    """Verifies HMAC signature and expiration date of JWT Token."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
            
        encoded_header, encoded_payload, encoded_signature = parts
        
        # Verify signature
        signature_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
        expected_sig = hmac.new(JWT_SECRET.encode('utf-8'), signature_input, hashlib.sha256).digest()
        actual_sig = _base64url_decode(encoded_signature)
        
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
            
        # Parse payload
        payload_bytes = _base64url_decode(encoded_payload)
        payload = json.loads(payload_bytes.decode('utf-8'))
        
        # Check expiry
        if payload.get("exp") and int(time.time()) > payload["exp"]:
            return None
            
        return payload
    except Exception as e:
        print(f"Token decoding error: {e}")
        return None

def verify_admin_credentials(email: str, password: str) -> Optional[dict]:
    """Validates admin email and password."""
    if email.strip().lower() == ADMIN_EMAIL.strip().lower() and password == ADMIN_PASSWORD:
        return {
            "email": ADMIN_EMAIL,
            "name": "System Administrator",
            "role": "admin"
        }
    return None
