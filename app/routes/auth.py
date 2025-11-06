import os
import logging
import secrets
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import RedirectResponse
import httpx
from dotenv import load_dotenv
from app.services.shopify import save_shop_token

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])

SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")
SHOPIFY_SCOPES = os.getenv("SHOPIFY_SCOPES", "read_orders,read_customers")
APP_URL = os.getenv("APP_URL", "http://localhost:8000")


# In-memory storage for OAuth state (for CSRF protection)
# Format: {state: shop_domain}
_oauth_states: dict[str, str] = {}


@router.get("")
async def initiate_oauth(request: Request, shop: str = Query(...)):
    """
    Initiate Shopify OAuth flow.
    
    Args:
        shop: Shop domain (e.g., "myshop.myshopify.com")
    """
    if not SHOPIFY_API_KEY or not SHOPIFY_API_SECRET:
        raise HTTPException(status_code=500, detail="Shopify API credentials not configured")
    
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = shop
    
    # Build OAuth URL
    redirect_uri = f"{APP_URL}/api/auth/callback"
    auth_url = (
        f"https://{shop}/admin/oauth/authorize"
        f"?client_id={SHOPIFY_API_KEY}"
        f"&scope={SHOPIFY_SCOPES}"
        f"&redirect_uri={redirect_uri}"
        f"&state={state}"
    )
    
    logger.info(f"Initiating OAuth for shop: {shop}")
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def oauth_callback(
    request: Request,
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    shop: Optional[str] = Query(None),
    hmac: Optional[str] = Query(None)
):
    """
    Handle Shopify OAuth callback and exchange code for access token.
    """
    if not code or not state or not shop or not hmac:
        raise HTTPException(status_code=400, detail="Missing required OAuth parameters")
    
    # Verify state (CSRF protection)
    if state not in _oauth_states or _oauth_states[state] != shop:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")
    
    # Clean up state
    _oauth_states.pop(state, None)
    
    # Exchange code for access token
    redirect_uri = f"{APP_URL}/api/auth/callback"
    token_url = f"https://{shop}/admin/oauth/access_token"
    
    payload = {
        "client_id": SHOPIFY_API_KEY,
        "client_secret": SHOPIFY_API_SECRET,
        "code": code
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(token_url, json=payload)
            response.raise_for_status()
            
            token_data = response.json()
            access_token = token_data.get("access_token")
            
            if not access_token:
                raise HTTPException(status_code=500, detail="Failed to obtain access token")
            
            # Save access token for this shop
            save_shop_token(shop, access_token)
            
            logger.info(f"OAuth completed successfully for shop: {shop}")
            
            # Redirect to admin settings page
            admin_url = f"https://{shop}/admin/apps/{SHOPIFY_API_KEY}/settings"
            return RedirectResponse(url=admin_url)
            
    except httpx.HTTPStatusError as e:
        logger.error(f"OAuth token exchange failed: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=500, detail="Failed to exchange OAuth code for token")
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during OAuth callback")

