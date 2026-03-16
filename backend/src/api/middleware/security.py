from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import hashlib
import hmac
import time
from typing import Optional
import jwt
from ...core.config import settings

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

class SecurityMiddleware:
    """Security enhancements middleware"""
    
    def __init__(self, app):
        self.app = app
        
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
            
        request = Request(scope, receive)
        
        # Add security headers
        headers = [
            (b"content-type", b"application/json"),
            (b"x-content-type-options", b"nosniff"),
            (b"x-frame-options", b"DENY"),
            (b"x-xss-protection", b"1; mode=block"),
            (b"strict-transport-security", b"max-age=31536000; includeSubDomains"),
            (b"referrer-policy", b"strict-origin-when-cross-origin"),
        ]
        
        # Add CORS headers if needed
        origin = request.headers.get("origin")
        if origin and origin in settings.ALLOWED_ORIGINS:
            headers.append((b"access-control-allow-origin", origin.encode()))
            
        # Continue with request
        await self.app(scope, receive, send)

# API Key authentication
class APIKeyAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization")
            
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            
        if not self.verify_api_key(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid API key")
            
        return credentials
        
    def verify_api_key(self, api_key: str) -> bool:
        # Verify API key against stored keys
        return api_key in settings.API_KEYS

# Request signing
def sign_request(payload: dict, secret: str) -> str:
    """Sign request payload for integrity"""
    message = json.dumps(payload, sort_keys=True).encode()
    signature = hmac.new(
        secret.encode(),
        message,
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_signature(payload: dict, signature: str, secret: str) -> bool:
    """Verify request signature"""
    expected = sign_request(payload, secret)
    return hmac.compare_digest(signature, expected)

# Input sanitization
def sanitize_input(data: any) -> any:
    """Sanitize input to prevent injection"""
    if isinstance(data, str):
        # Remove any potentially dangerous characters
        dangerous = ['<', '>', '&', '"', "'", ';', '`', '$', '{', '}']
        for char in dangerous:
            data = data.replace(char, f"&#{ord(char)};")
        return data
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    else:
        return data