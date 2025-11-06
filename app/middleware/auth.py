import os
from fastapi import Request, HTTPException
from typing import Optional

ALLOWED_SHOPS = os.getenv("ALLOWED_SHOPS", "")


def get_shop_from_request(request: Request) -> str:
    """Extract shop domain from request query parameters."""
    return request.query_params.get("shop", "").strip()


def verify_shop_access(request: Request) -> bool:
    """
    Check if the requesting shop is in the allowed shops list.
    Shop is extracted from the 'shop' query parameter sent by Shopify.
    """
    if not ALLOWED_SHOPS:
        # If no whitelist is configured, allow all shops (for initial setup)
        return True
    
    # Get the shop from the request
    shop = get_shop_from_request(request)
    if not shop:
        # No shop parameter provided
        return False
    
    # Parse allowed shops (comma-separated list)
    allowed_shops_list = [s.strip().lower() for s in ALLOWED_SHOPS.split(",") if s.strip()]
    
    # Check if shop is in whitelist
    return shop.lower() in allowed_shops_list


def require_admin_access(request: Request):
    """Dependency that requires shop to be whitelisted"""
    if not verify_shop_access(request):
        shop = get_shop_from_request(request)
        if not shop:
            raise HTTPException(
                status_code=403,
                detail="Access denied. Shop parameter is required."
            )
        raise HTTPException(
            status_code=403,
            detail=f"Access denied. Shop '{shop}' is not authorized to access this app."
        )
    return True
