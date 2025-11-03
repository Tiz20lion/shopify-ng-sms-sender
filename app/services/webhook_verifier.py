import hmac
import hashlib
import base64
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def verify_shopify_webhook(secret: str, raw_body: bytes, hmac_header: Optional[str]) -> bool:
    """
    Verify Shopify webhook HMAC signature.
    
    According to Shopify documentation:
    - HMAC header is BASE64 encoded (not hex)
    - Use app's client secret (from Partner Dashboard API credentials)
    - Calculate HMAC-SHA256 and encode as base64 for comparison
    
    Args:
        secret: Shopify app client secret (SHOPIFY_API_SECRET from Partner Dashboard)
        raw_body: Raw request body bytes (must be raw, not parsed)
        hmac_header: X-Shopify-Hmac-Sha256 header value (base64 encoded)
    
    Returns:
        True if signature is valid, False otherwise
    """
    if not hmac_header:
        logger.warning("Missing HMAC header in webhook request")
        return False
    
    if not secret:
        logger.error("Shopify API secret is not configured")
        return False
    
    try:
        # Calculate HMAC-SHA256 and encode as BASE64 (not hex!)
        # This matches Shopify's format as per official documentation
        calculated_hmac = base64.b64encode(
            hmac.new(
                secret.encode('utf-8'),
                raw_body,
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        # Compare base64-encoded HMACs using constant-time comparison
        is_valid = hmac.compare_digest(calculated_hmac, hmac_header)
        
        if not is_valid:
            logger.warning("Webhook HMAC verification failed")
            logger.info(f"Expected HMAC (first 20 chars): {calculated_hmac[:20]}...")
            logger.info(f"Received HMAC (first 20 chars): {hmac_header[:20]}...")
            logger.info(f"Secret length: {len(secret)}, Body length: {len(raw_body)} bytes")
            logger.info(f"Secret starts with: {secret[:10] if len(secret) >= 10 else secret}...")
        else:
            logger.info("Webhook HMAC verification successful")
        
        return is_valid
        
    except Exception as e:
        logger.error(f"Error verifying webhook HMAC: {e}", exc_info=True)
        return False

