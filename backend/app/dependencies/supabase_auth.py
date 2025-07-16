import httpx
from jose import jwt, JWTError
from fastapi import Request, HTTPException
from jose import jwk
from jose.utils import base64url_decode

JWKS_URL = "https://rszyavogpjiwodgpdare.supabase.co/auth/v1/.well-known/jwks.json"  # your actual URL

_jwks_cache = None  # memory cache

async def get_jwks():
    global _jwks_cache
    if _jwks_cache:
        return _jwks_cache

    async with httpx.AsyncClient() as client:
        response = await client.get(JWKS_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Could not fetch JWKS")
        _jwks_cache = response.json()
        return _jwks_cache

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]

    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]
        alg = unverified_header["alg"]

        jwks = await get_jwks()
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

        if not key:
            raise HTTPException(status_code=401, detail="Key not found in JWKS")

        public_key = jwk.construct(key)
        message, encoded_sig = token.rsplit('.', 1)
        decoded_sig = base64url_decode(encoded_sig.encode())

        if not public_key.verify(message.encode(), decoded_sig):
            raise HTTPException(status_code=401, detail="Invalid token signature")

        payload = jwt.decode(token, public_key.to_pem(), algorithms=[alg], audience=None)
        return payload

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")
