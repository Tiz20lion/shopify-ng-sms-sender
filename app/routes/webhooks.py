import os
import json
import logging
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import Response
from dotenv import load_dotenv
from app.services.webhook_verifier import verify_shopify_webhook
from app.services.termii import TermiiService
from app.models.templates import get_templates
from app.utils.phone_formatter import format_phone_for_termii

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

# Webhook signing secret from Shopify Admin → Settings → Notifications → Webhooks
# This is the 64-character secret shown at the bottom of the webhooks page
# Different from the app's API secret (client secret) in Partner Dashboard
SHOPIFY_WEBHOOK_SECRET = os.getenv("SHOPIFY_WEBHOOK_SECRET", "").strip()
# Fallback to SHOPIFY_API_SECRET for backward compatibility
if not SHOPIFY_WEBHOOK_SECRET:
    SHOPIFY_WEBHOOK_SECRET = os.getenv("SHOPIFY_API_SECRET", "").strip()

# Termii configuration from environment variables (global, not per-shop)
TERMII_API_KEY = os.getenv("TERMII_API_KEY", "").strip()
TERMII_SENDER_ID = os.getenv("TERMII_SENDER_ID", "").strip()
TERMII_BASE_URL = os.getenv("TERMII_BASE_URL", "https://v3.api.termii.com").strip()


def render_template(template: str, context: dict) -> str:
    """
    Simple template rendering for SMS messages.
    Replaces {{variable_name}} with values from context.
    """
    result = template
    for key, value in context.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result


@router.post("/orders/create")
async def handle_order_create(
    request: Request, 
    x_shopify_hmac_sha256: str = Header(..., alias="X-Shopify-Hmac-Sha256"),
    x_shopify_shop_domain: str = Header(None, alias="X-Shopify-Shop-Domain")
):
    """
    Handle order creation webhook.
    Sends order confirmation SMS to customer.
    """
    if not SHOPIFY_WEBHOOK_SECRET:
        logger.error("Shopify webhook secret not configured")
        raise HTTPException(status_code=500, detail="Server configuration error")
    
    # Get raw body for HMAC verification (must read once)
    raw_body = await request.body()
    
    # Log for debugging
    logger.info(f"Webhook received - Body length: {len(raw_body)} bytes, HMAC header: {x_shopify_hmac_sha256[:20]}...")
    logger.info(f"SHOPIFY_WEBHOOK_SECRET configured: {bool(SHOPIFY_WEBHOOK_SECRET)}, length: {len(SHOPIFY_WEBHOOK_SECRET) if SHOPIFY_WEBHOOK_SECRET else 0}")
    
    # Verify webhook signature
    if not verify_shopify_webhook(SHOPIFY_WEBHOOK_SECRET, raw_body, x_shopify_hmac_sha256):
        logger.warning("Webhook HMAC verification failed for orders/create")
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    # Parse JSON payload from raw body (already read)
    try:
        order = json.loads(raw_body.decode('utf-8'))
    except Exception as e:
        logger.error(f"Failed to parse webhook JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Get shop domain from header or order data
    shop_domain = x_shopify_shop_domain or order.get("myshopify_domain", "")
    
    if not shop_domain:
        logger.warning("Missing shop domain in webhook")
        return Response(status_code=200)
    
    logger.info(f"Processing order/create webhook for shop: {shop_domain}, order ID: {order.get('id')}")
    
    # Check Termii configuration (global from .env)
    if not TERMII_API_KEY or not TERMII_SENDER_ID:
        logger.error("Termii not configured in environment variables. Check TERMII_API_KEY and TERMII_SENDER_ID in .env")
        return Response(status_code=200)
    
    # Get SMS templates for this shop
    templates = get_templates(shop_domain)
    
    # Extract customer phone number (handle case where customer might be None)
    customer = order.get("customer") or {}
    phone = customer.get("phone") or order.get("phone") or order.get("billing_address", {}).get("phone")
    
    if not phone:
        logger.info(f"No phone number found for order {order.get('id')} on shop {shop_domain}")
        return Response(status_code=200)
    
    try:
        # Format phone number
        logger.info(f"Formatting phone number: {phone}")
        formatted_phone = format_phone_for_termii(phone)
        logger.info(f"Formatted phone number: {formatted_phone}")
        
        # Prepare template context
        customer_name = customer.get("first_name", "Customer") or "Customer"
        order_number = order.get("order_number") or order.get("name", "N/A")
        total_price = order.get("total_price", "0")
        currency = order.get("currency", "")
        
        context = {
            "customer_name": customer_name,
            "order_number": order_number,
            "total_price": f"{currency} {total_price}" if currency else total_price
        }
        
        # Render SMS template
        message = render_template(templates.order_confirmation, context)
        logger.info(f"SMS message: {message[:100]}...")
        
        # Send SMS
        termii_service = TermiiService(
            api_key=TERMII_API_KEY,
            base_url=TERMII_BASE_URL
        )
        
        result = await termii_service.send_sms(
            to=formatted_phone,
            message=message,
            sender_id=TERMII_SENDER_ID,
            channel="generic"
        )
        
        logger.info(f"Order confirmation SMS sent to {formatted_phone} for order {order_number}. Response: {result}")
        
    except Exception as e:
        logger.error(f"Error sending order confirmation SMS for order {order.get('id')}: {e}", exc_info=True)
        # Return 200 OK even if SMS fails (to prevent webhook retries)
    
    return Response(status_code=200)


@router.post("/orders/fulfilled")
async def handle_order_fulfilled(
    request: Request, 
    x_shopify_hmac_sha256: str = Header(..., alias="X-Shopify-Hmac-Sha256"),
    x_shopify_shop_domain: str = Header(None, alias="X-Shopify-Shop-Domain")
):
    """
    Handle order fulfillment webhook.
    Sends fulfillment notification SMS to customer.
    """
    if not SHOPIFY_WEBHOOK_SECRET:
        logger.error("Shopify webhook secret not configured")
        raise HTTPException(status_code=500, detail="Server configuration error")
    
    # Get raw body for HMAC verification (must read once)
    raw_body = await request.body()
    
    # Log for debugging
    logger.info(f"Webhook received - Body length: {len(raw_body)} bytes, HMAC header: {x_shopify_hmac_sha256[:20]}...")
    logger.info(f"SHOPIFY_WEBHOOK_SECRET configured: {bool(SHOPIFY_WEBHOOK_SECRET)}, length: {len(SHOPIFY_WEBHOOK_SECRET) if SHOPIFY_WEBHOOK_SECRET else 0}")
    
    # Verify webhook signature
    if not verify_shopify_webhook(SHOPIFY_WEBHOOK_SECRET, raw_body, x_shopify_hmac_sha256):
        logger.warning("Webhook HMAC verification failed for orders/fulfilled")
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    # Parse JSON payload from raw body (already read)
    try:
        order = json.loads(raw_body.decode('utf-8'))
    except Exception as e:
        logger.error(f"Failed to parse webhook JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Get shop domain from header or order data
    shop_domain = x_shopify_shop_domain or order.get("myshopify_domain", "")
    
    if not shop_domain:
        logger.warning("Missing shop domain in webhook")
        return Response(status_code=200)
    
    logger.info(f"Processing order/fulfilled webhook for shop: {shop_domain}, order ID: {order.get('id')}")
    
    # Check Termii configuration (global from .env)
    if not TERMII_API_KEY or not TERMII_SENDER_ID:
        logger.error("Termii not configured in environment variables. Check TERMII_API_KEY and TERMII_SENDER_ID in .env")
        return Response(status_code=200)
    
    # Get SMS templates for this shop
    templates = get_templates(shop_domain)
    
    # Extract customer phone number (handle case where customer might be None)
    customer = order.get("customer") or {}
    phone = customer.get("phone") or order.get("phone") or order.get("billing_address", {}).get("phone")
    
    if not phone:
        logger.info(f"No phone number found for fulfilled order {order.get('id')} on shop {shop_domain}")
        return Response(status_code=200)
    
    try:
        # Format phone number
        logger.info(f"Formatting phone number: {phone}")
        formatted_phone = format_phone_for_termii(phone)
        logger.info(f"Formatted phone number: {formatted_phone}")
        
        # Prepare template context
        customer_name = customer.get("first_name", "Customer") or "Customer"
        order_number = order.get("order_number") or order.get("name", "N/A")
        
        # Get tracking info if available
        fulfillments = order.get("fulfillments", [])
        tracking_number = ""
        tracking_url = ""
        if fulfillments:
            tracking_number = fulfillments[0].get("tracking_number", "")
            tracking_url = fulfillments[0].get("tracking_url", "")
        
        context = {
            "customer_name": customer_name,
            "order_number": order_number,
            "tracking_number": tracking_number,
            "tracking_url": tracking_url
        }
        
        # Render SMS template
        message = render_template(templates.fulfillment, context)
        logger.info(f"SMS message: {message[:100]}...")
        
        # Send SMS
        termii_service = TermiiService(
            api_key=TERMII_API_KEY,
            base_url=TERMII_BASE_URL
        )
        
        result = await termii_service.send_sms(
            to=formatted_phone,
            message=message,
            sender_id=TERMII_SENDER_ID,
            channel="generic"
        )
        
        logger.info(f"Fulfillment SMS sent to {formatted_phone} for order {order_number}. Response: {result}")
        
    except Exception as e:
        logger.error(f"Error sending fulfillment SMS for order {order.get('id')}: {e}", exc_info=True)
        # Return 200 OK even if SMS fails (to prevent webhook retries)
    
    return Response(status_code=200)

