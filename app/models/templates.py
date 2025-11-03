"""
Template storage for SMS messages.
Templates are stored per-shop in a JSON file for persistence.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Path to templates file
TEMPLATES_FILE = Path(__file__).parent.parent / "templates.json"


class ShopTemplates(BaseModel):
    """SMS templates for a shop."""
    order_confirmation: str = Field(
        default="Hi {{customer_name}}, your order #{{order_number}} has been confirmed. Total: {{total_price}}. Thank you!",
        description="Template for order confirmation SMS"
    )
    fulfillment: str = Field(
        default="Hi {{customer_name}}, your order #{{order_number}} has been shipped and will arrive soon!",
        description="Template for fulfillment SMS"
    )


def _load_templates_file() -> Dict[str, dict]:
    """Load templates from JSON file."""
    if not TEMPLATES_FILE.exists():
        return {}
    
    try:
        with open(TEMPLATES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading templates file: {e}")
        return {}


def _save_templates_file(data: Dict[str, dict]) -> None:
    """Save templates to JSON file."""
    try:
        with open(TEMPLATES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Templates saved to {TEMPLATES_FILE}")
    except Exception as e:
        logger.error(f"Error saving templates file: {e}")
        raise


def get_templates(shop_domain: str) -> ShopTemplates:
    """
    Get templates for a specific shop.
    Returns default templates if none exist.
    """
    all_templates = _load_templates_file()
    shop_data = all_templates.get(shop_domain, {})
    
    return ShopTemplates(
        order_confirmation=shop_data.get("order_confirmation", ShopTemplates().order_confirmation),
        fulfillment=shop_data.get("fulfillment", ShopTemplates().fulfillment)
    )


def save_templates(shop_domain: str, templates: ShopTemplates) -> None:
    """Save templates for a specific shop."""
    all_templates = _load_templates_file()
    
    all_templates[shop_domain] = {
        "order_confirmation": templates.order_confirmation,
        "fulfillment": templates.fulfillment
    }
    
    _save_templates_file(all_templates)
    logger.info(f"Templates saved for shop: {shop_domain}")


def delete_templates(shop_domain: str) -> None:
    """Delete templates for a specific shop."""
    all_templates = _load_templates_file()
    
    if shop_domain in all_templates:
        del all_templates[shop_domain]
        _save_templates_file(all_templates)
        logger.info(f"Templates deleted for shop: {shop_domain}")

