import os
import logging
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from app.models.templates import ShopTemplates, get_templates, save_templates
from app.middleware.auth import require_admin_access

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["admin"])


def get_shop_domain_from_request(request: Request) -> Optional[str]:
    """
    Extract shop domain from request headers.
    Shopify sends X-Shopify-Shop-Domain header in authenticated requests.
    """
    shop_domain = request.headers.get("X-Shopify-Shop-Domain")
    if not shop_domain:
        # Fallback: try to get from query params (for testing)
        shop_domain = request.query_params.get("shop")
    return shop_domain


class SettingsResponse(BaseModel):
    """Response model for settings - includes Termii status from env and templates."""
    termii_configured: bool
    termii_sender_id: str  # Show sender ID (not secret)
    order_confirmation_template: str
    fulfillment_template: str


class SettingsUpdateRequest(BaseModel):
    """Request model for updating settings - only templates."""
    order_confirmation_template: str
    fulfillment_template: str


@router.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "API is reachable"}


@router.get("/settings")
async def get_settings_endpoint(request: Request, _auth: bool = Depends(require_admin_access)):
    """
    Get current settings for the authenticated shop.
    Returns Termii configuration status from environment and templates for the shop.
    """
    shop_domain = get_shop_domain_from_request(request)
    
    if not shop_domain:
        raise HTTPException(status_code=400, detail="Shop domain is required")
    
    # Check Termii configuration from environment
    termii_api_key = os.getenv("TERMII_API_KEY", "").strip()
    termii_sender_id = os.getenv("TERMII_SENDER_ID", "").strip()
    termii_configured = bool(termii_api_key and termii_sender_id)
    
    # Get templates for this shop (returns defaults if not found)
    templates = get_templates(shop_domain)
    
    return SettingsResponse(
        termii_configured=termii_configured,
        termii_sender_id=termii_sender_id if termii_configured else "",
        order_confirmation_template=templates.order_confirmation,
        fulfillment_template=templates.fulfillment
    )


@router.post("/settings")
async def update_settings_endpoint(request: Request, settings_data: SettingsUpdateRequest, _auth: bool = Depends(require_admin_access)):
    """
    Update SMS templates for the authenticated shop.
    Termii credentials are configured globally in .env file.
    """
    logger.info("=" * 80)
    logger.info("POST /api/settings - REQUEST RECEIVED")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Query params: {dict(request.query_params)}")
    logger.info(f"Body data: {settings_data.dict()}")
    
    shop_domain = get_shop_domain_from_request(request)
    logger.info(f"Shop domain extracted: {shop_domain}")
    
    if not shop_domain:
        logger.error("Shop domain is missing - returning 400")
        raise HTTPException(status_code=400, detail="Shop domain is required")
    
    try:
        logger.info(f"Creating ShopTemplates object...")
        templates = ShopTemplates(
            order_confirmation=settings_data.order_confirmation_template,
            fulfillment=settings_data.fulfillment_template
        )
        
        logger.info(f"Saving templates to file for shop: {shop_domain}")
        save_templates(shop_domain, templates)
        
        logger.info(f"✓ Templates successfully saved for shop: {shop_domain}")
        logger.info("=" * 80)
        
        return {"message": "Templates saved successfully", "shop": shop_domain}
        
    except Exception as e:
        logger.error(f"ERROR updating templates: {e}", exc_info=True)
        logger.error("=" * 80)
        raise HTTPException(status_code=400, detail=f"Invalid templates: {str(e)}")
