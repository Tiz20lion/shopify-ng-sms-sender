import re
from typing import Optional


def format_phone_for_termii(phone: str, default_country_code: Optional[str] = None) -> str:
    """
    Format phone number for Termii API (international format without leading +).
    
    Args:
        phone: Phone number in various formats (with/without country code, with/without +)
        default_country_code: Default country code to use if missing (e.g., "234" for Nigeria)
    
    Returns:
        Formatted phone number in international format without + (e.g., "2349118462627")
    
    Examples:
        format_phone_for_termii("+2349118462627") -> "2349118462627"
        format_phone_for_termii("09118462627", "234") -> "2349118462627"
        format_phone_for_termii("2349118462627") -> "2349118462627"
    """
    if not phone:
        raise ValueError("Phone number cannot be empty")
    
    phone = phone.strip()
    
    # Remove common non-digit characters except digits
    phone = re.sub(r'[^\d]', '', phone)
    
    if not phone:
        raise ValueError("Phone number contains no digits")
    
    # If phone starts with country code, use as is
    if default_country_code and not phone.startswith(default_country_code):
        # Add default country code if missing
        if len(phone) < 10:
            raise ValueError(f"Phone number too short: {phone}")
        phone = default_country_code + phone.lstrip('0')
    elif not phone.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
        # If it doesn't start with a digit 1-9, might be invalid
        if default_country_code and not phone.startswith(default_country_code):
            phone = default_country_code + phone.lstrip('0')
    
    return phone

