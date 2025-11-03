import os
import logging
from typing import Optional, Dict
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


# In-memory storage for OAuth tokens per shop
# Format: {shop_domain: access_token}
_shop_tokens: Dict[str, str] = {}


def get_shop_token(shop_domain: str) -> Optional[str]:
    """Get OAuth access token for a specific shop."""
    return _shop_tokens.get(shop_domain)


def save_shop_token(shop_domain: str, access_token: str) -> None:
    """Save OAuth access token for a specific shop."""
    _shop_tokens[shop_domain] = access_token


class ShopifyService:
    def __init__(self, shop_domain: str):
        self.shop_domain = shop_domain
        self.access_token = get_shop_token(shop_domain)
        
        if not self.access_token:
            raise ValueError(f"No access token found for shop: {shop_domain}")
    
    async def get_order(self, order_id: str) -> dict:
        """
        Fetch order details from Shopify.
        
        Args:
            order_id: Shopify order ID
        
        Returns:
            Order data as dict
        """
        api_version = "2024-01"
        url = f"https://{self.shop_domain}/admin/api/{api_version}/orders/{order_id}.json"
        
        headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()["order"]
        except httpx.HTTPStatusError as e:
            logger.error(f"Shopify API error fetching order {order_id}: {e.response.status_code}")
            raise
        except Exception as e:
            logger.error(f"Error fetching order from Shopify: {e}")
            raise

