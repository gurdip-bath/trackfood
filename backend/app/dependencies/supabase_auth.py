import httpx
from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode
from fastapi import Request, HTTPException
from app.schemas.user import UserJWT
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Updated JWKS URL for new signing keys
JWKS_URL = "https://rszyavogpjiwodgpdare.supabase.co/auth/v1/.well-known/jwks.json"

_jwks_cache = None

async def get_jwks():
    global _jwks_cache
    if _jwks_cache:
        return _jwks_cache

    async with httpx.AsyncClient() as client:
        response = await client.get(JWKS_URL)
        if response.status_code != 200:
            logger.error(f"Failed to fetch JWKS: {response.status_code}")
            raise HTTPException(status_code=500, detail="Could not fetch JWKS")
        _jwks_cache = response.json()
        logger.info(f"JWKS fetched successfully. Keys: {len(_jwks_cache.get('keys', []))}")
        return _jwks_cache

async def get_current_user(request: Request) -> UserJWT:
    auth_header = request.headers.get("Authorization")
    logger.info(f"Auth header present: {bool(auth_header)}")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.error("Missing or invalid Authorization header")
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]
    logger.info(f"Token length: {len(token)}")
    
    try:
        # Get token header to identify key
        unverified_header = jwt.get_unverified_header(token)
        logger.info(f"Token algorithm: {unverified_header.get('alg')}")
        logger.info(f"Token key ID: {unverified_header.get('kid')}")
        
        # Determine verification method based on algorithm
        if unverified_header.get('alg') == 'HS256':
            # Legacy HS256 verification
            from app.core.config import settings
            payload = jwt.decode(
                token, 
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated"
            )
        else:
            # ECC P-256 verification using JWKS
            jwks = await get_jwks()
            key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)
            
            if not key:
                logger.error(f"Key not found in JWKS for kid: {unverified_header['kid']}")
                raise HTTPException(status_code=401, detail="Key not found in JWKS")

            # Construct public key and verify
            public_key = jwk.construct(key)
            payload = jwt.decode(
                token,
                public_key.to_pem(),
                algorithms=[unverified_header.get('alg')],
                audience="authenticated"
            )
        
        logger.info(f"Token decoded successfully")
        email = payload.get("email")
        sub = payload.get("sub")

        if not email:
            logger.error("Email claim missing in token")
            raise HTTPException(status_code=401, detail="Email claim missing in token")

        logger.info(f"User authenticated: {email}")
        return UserJWT(email=email, sub=sub)
    
    except JWTError as e:
        logger.error(f"JWT Error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"JWT Error: {str(e)}")
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")