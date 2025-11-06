from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator


class Settings(BaseModel):
    termii_api_key: str = Field(..., min_length=1, description="Termii API key")
    termii_sender_id: str = Field(..., min_length=3, max_length=11, description="Termii sender ID (alphanumeric)")
    order_confirmation_template: str = Field(
        default="Hi {{customer_name}}, your order #{{order_number}} has been confirmed. Thank you for your purchase!",
        description="SMS template for order confirmation"
    )
    fulfillment_template: str = Field(
        default="Hi {{customer_name}}, your order #{{order_number}} has been shipped and will arrive soon!",
        description="SMS template for order fulfillment"
    )
    
    @field_validator('termii_sender_id')
    @classmethod
    def validate_sender_id(cls, v: str) -> str:
        if not v.replace(' ', '').isalnum():
            raise ValueError("Sender ID must be alphanumeric")
        return v


# In-memory storage for per-shop settings
# Format: {shop_domain: Settings}
_shop_settings: Dict[str, Settings] = {}


def get_settings(shop_domain: str) -> Optional[Settings]:
    """Get settings for a specific shop."""
    return _shop_settings.get(shop_domain)


def save_settings(shop_domain: str, settings: Settings) -> None:
    """Save settings for a specific shop."""
    _shop_settings[shop_domain] = settings


def delete_settings(shop_domain: str) -> None:
    """Delete settings for a specific shop."""
    _shop_settings.pop(shop_domain, None)

