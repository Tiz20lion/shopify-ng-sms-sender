import os
import logging
from typing import Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class TermiiService:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("TERMII_API_KEY")
        self.base_url = base_url or os.getenv("TERMII_BASE_URL", "https://v3.api.termii.com")
        
        if not self.api_key:
            raise ValueError("Termii API key is required")
    
    async def fetch_sender_ids(self, sender_id: Optional[str] = None, status: Optional[str] = None) -> dict:
        """
        Fetch all sender IDs associated with the account.
        
        Args:
            sender_id: Optional filter by sender ID name
            status: Optional filter by status (active, pending, blocked)
        
        Returns:
            Response dict with list of sender IDs and their status
        
        Raises:
            httpx.HTTPError: If API request fails
            ValueError: If API returns an error
        """
        url = f"{self.base_url}/api/sender-id"
        
        params = {
            "api_key": self.api_key
        }
        
        if sender_id:
            params["sender_id"] = sender_id
        if status:
            params["status"] = status
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params, headers=headers)
                
                # Log the raw response for debugging
                logger.info(f"Termii Sender IDs API response status: {response.status_code}")
                logger.info(f"Termii Sender IDs API response text: {response.text[:500] if response.text else '(empty)'}")  # First 500 chars
                
                # Handle empty response
                if not response.text or response.text.strip() == '':
                    logger.info("Termii API returned empty response - no sender IDs found")
                    return {
                        "content": [],
                        "totalElements": 0,
                        "empty": True
                    }
                
                try:
                    result = response.json()
                except Exception as e:
                    logger.warning(f"Failed to parse JSON response: {e}, raw text: {response.text[:200]}")
                    # If not JSON, might be empty or different format
                    if response.text.strip():
                        result = {"error": response.text}
                    else:
                        return {
                            "content": [],
                            "totalElements": 0,
                            "empty": True
                        }
                
                if result.get("status") == "error":
                    error_message = result.get("message", "Unknown error from Termii API")
                    logger.error(f"Termii API error fetching sender IDs: {error_message}")
                    raise ValueError(f"Termii API Error: {error_message}")
                
                response.raise_for_status()
                return result
                
        except ValueError as e:
            raise
        except httpx.HTTPStatusError as e:
            try:
                error_data = e.response.json()
                error_message = error_data.get("message", f"HTTP {e.response.status_code} error")
                logger.error(f"Termii API HTTP error: {e.response.status_code} - {error_message}")
                raise ValueError(f"Termii API Error: {error_message}")
            except Exception:
                logger.error(f"Termii API HTTP error: {e.response.status_code} - {e.response.text}")
                raise ValueError(f"Termii API HTTP Error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Termii API request error: {e}")
            raise ValueError(f"Network error: Unable to connect to Termii API - {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching sender IDs: {e}")
            raise ValueError(f"Unexpected error: {str(e)}")
    
    async def send_sms(
        self,
        to: str,
        message: str,
        sender_id: str,
        channel: str = "generic",
        message_type: str = "plain"
    ) -> dict:
        """
        Send SMS via Termii API using generic channel for messages.
        
        Args:
            to: Destination phone number in international format (no +, e.g., "2349118462627")
            message: Text message to send
            sender_id: Sender ID (alphanumeric, 3-11 characters)
            channel: Messaging channel - use "generic" for messages (or "dnd" if activated)
            message_type: Message format - "plain", "unicode", or "encrypted"
        
        Returns:
            Response dict with message_id, balance, etc.
        
        Raises:
            httpx.HTTPError: If API request fails
            ValueError: If parameters are invalid
        """
        if not to:
            raise ValueError("Phone number is required")
        if not message:
            raise ValueError("Message content is required")
        if not sender_id:
            raise ValueError("Sender ID is required")
        if channel not in ["dnd", "generic", "whatsapp", "voice"]:
            raise ValueError(f"Invalid channel: {channel}. Must be one of: dnd, generic, whatsapp, voice")
        
        url = f"{self.base_url}/api/sms/send"
        
        payload = {
            "api_key": self.api_key,
            "to": to,
            "from": sender_id,
            "sms": message,
            "type": message_type,
            "channel": channel
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Log the payload for debugging (hide API key)
        debug_payload = {**payload, "api_key": "***HIDDEN***"}
        logger.info(f"Sending SMS to Termii API: URL={url}, Payload={debug_payload}")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                logger.info(f"Termii API HTTP status: {response.status_code}")
                logger.info(f"Termii API response text: {response.text[:500]}")
                
                # Parse response even if status code indicates error
                try:
                    result = response.json()
                    logger.info(f"Termii API JSON response: {result}")
                except Exception:
                    result = {"error": response.text}
                    logger.warning(f"Termii API returned non-JSON response: {response.text[:200]}")
                
                # Check for API-level errors in response body
                if result.get("status") == "error" or result.get("code") not in ["ok", 200, None]:
                    error_message = result.get("message", "Unknown error from Termii API")
                    error_code = result.get("code", "unknown")
                    logger.error(f"Termii API error: {error_code} - {error_message}")
                    logger.error(f"Full error response: {result}")
                    raise ValueError(f"Termii API Error: {error_message}")
                
                # Check HTTP status
                response.raise_for_status()
                
                if result.get("code") == "ok":
                    message_id = result.get('message_id') or result.get('messageId') or result.get('data', {}).get('message_id')
                    logger.info(f"SMS sent successfully to {to}. Message ID: {message_id}")
                    logger.info(f"Full success response: {result}")
                else:
                    logger.warning(f"Termii API returned non-ok status: {result}")
                
                return result
                
        except ValueError as e:
            # Re-raise ValueError (API errors) as-is
            raise
        except httpx.HTTPStatusError as e:
            # Try to extract error message from response
            try:
                error_data = e.response.json()
                error_message = error_data.get("message", f"HTTP {e.response.status_code} error")
                logger.error(f"Termii API HTTP error: {e.response.status_code} - {error_message}")
                raise ValueError(f"Termii API Error: {error_message}")
            except Exception:
                logger.error(f"Termii API HTTP error: {e.response.status_code} - {e.response.text}")
                raise ValueError(f"Termii API HTTP Error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Termii API request error: {e}")
            raise ValueError(f"Network error: Unable to connect to Termii API - {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error sending SMS: {e}")
            raise ValueError(f"Unexpected error: {str(e)}")

