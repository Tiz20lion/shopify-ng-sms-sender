"""
Simple SMS test endpoint without complex JavaScript to verify backend works.
"""

import os
import logging
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from app.services.termii import TermiiService
from app.utils.phone_formatter import format_phone_for_termii
# Settings are now in .env, not per-shop

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/test-simple", tags=["test-simple"])


def get_shop_domain_from_request(request: Request) -> str:
    """Extract shop domain from request for settings lookup."""
    shop_domain = request.headers.get("X-Shopify-Shop-Domain")
    if shop_domain:
        return shop_domain
    
    shop_domain = request.query_params.get("shop", "")
    if shop_domain:
        return shop_domain
    
    referer = request.headers.get("referer", "")
    if referer:
        import re
        from urllib.parse import unquote
        match = re.search(r'[?&]shop=([^&]+)', referer)
        if match:
            shop_domain = unquote(match.group(1))
            if shop_domain:
                return shop_domain
        if ".myshopify.com" in referer:
            match = re.search(r'https://([^/]+\.myshopify\.com)', referer)
            if match:
                return match.group(1)
    
    return ""


@router.get("/sms", response_class=HTMLResponse)
async def simple_test_sms_page(request: Request):
    """Simple test page for sending SMS - uses basic form submission."""
    shop_domain = get_shop_domain_from_request(request)
    logger.info(f"Simple test SMS page - Shop domain: '{shop_domain}'")
    
    # Check Termii configuration from environment
    termii_api_key = os.getenv("TERMII_API_KEY", "").strip()
    termii_sender_id = os.getenv("TERMII_SENDER_ID", "").strip()
    termii_configured = bool(termii_api_key and termii_sender_id)
    
    settings_status = ""
    if termii_configured:
        settings_status = f'<div style="background: #e3fcef; padding: 12px; border-radius: 4px; margin-bottom: 20px;"><strong>✓ Termii Configured</strong><br>Sender ID: {termii_sender_id}</div>'
    else:
        settings_status = '<div style="background: #fef2f2; padding: 12px; border-radius: 4px; margin-bottom: 20px; color: #d72c0d;"><strong>⚠ Termii Not Configured</strong><br>Please add TERMII_API_KEY and TERMII_SENDER_ID to your .env file.</div>'
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simple SMS Test</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 600px;
                margin: 40px auto;
                padding: 20px;
                background: #f6f6f7;
            }}
            .container {{
                background: white;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            h1 {{ color: #202223; margin-top: 0; }}
            .form-group {{ margin-bottom: 20px; }}
            label {{
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
                color: #202223;
            }}
            input, textarea {{
                width: 100%;
                padding: 10px;
                border: 1px solid #c9cccf;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }}
            textarea {{ min-height: 100px; resize: vertical; }}
            .help-text {{
                font-size: 12px;
                color: #6d7175;
                margin-top: 4px;
            }}
            button {{
                padding: 12px 24px;
                background: #008060;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                cursor: pointer;
                font-size: 14px;
                width: 100%;
            }}
            button:hover {{ background: #006e52; }}
            .back-link {{
                display: inline-block;
                margin-top: 20px;
                color: #008060;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 Simple SMS Test</h1>
            <p>Basic form to test SMS sending (no JavaScript required)</p>
            
            {settings_status}
            
            <form method="POST" action="/test-simple/sms?shop={shop_domain}">
                <div class="form-group">
                    <label for="phone">Phone Number *</label>
                    <input 
                        type="text" 
                        id="phone" 
                        name="phone" 
                        placeholder="2349118462627"
                        required
                    >
                    <div class="help-text">International format without + (e.g., 2349118462627)</div>
                </div>
                
                <div class="form-group">
                    <label for="message">Message *</label>
                    <textarea 
                        id="message" 
                        name="message" 
                        placeholder="Enter your test message..."
                        required
                    >Hi, this is a test message from Termii SMS!</textarea>
                    <div class="help-text">Maximum 160 characters for standard SMS</div>
                </div>
                
                <button type="submit">Send Test SMS</button>
            </form>
            
            <a href="/?shop={shop_domain}" class="back-link">← Back to Home</a>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


@router.post("/sms", response_class=HTMLResponse)
async def send_simple_test_sms(
    request: Request,
    phone: str = Form(...),
    message: str = Form(...)
):
    """Send test SMS and return HTML response."""
    try:
        logger.info(f"Simple test SMS - Phone: {phone}, Message length: {len(message)}")
        
        # Get shop domain
        shop_domain = get_shop_domain_from_request(request)
        logger.info(f"Shop domain: '{shop_domain}'")
        
        # Get Termii credentials from environment
        termii_api_key = os.getenv("TERMII_API_KEY", "").strip()
        termii_sender_id = os.getenv("TERMII_SENDER_ID", "").strip()
        
        if not termii_api_key or not termii_sender_id:
            raise HTTPException(
                status_code=400,
                detail="TERMII_API_KEY or TERMII_SENDER_ID not configured in .env file"
            )
        
        # Format phone and send SMS
        formatted_phone = format_phone_for_termii(phone)
        logger.info(f"Formatted phone: {formatted_phone}")
        
        termii_base_url = os.getenv("TERMII_BASE_URL", "https://v3.api.termii.com")
        termii_service = TermiiService(api_key=termii_api_key, base_url=termii_base_url)
        
        result = await termii_service.send_sms(
            to=formatted_phone,
            message=message,
            sender_id=termii_sender_id,
            channel="generic"
        )
        
        logger.info(f"SMS sent successfully: {result}")
        
        message_id = result.get('message_id') or result.get('messageId')
        
        # Return success page
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SMS Sent Successfully</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 600px;
                    margin: 40px auto;
                    padding: 20px;
                    background: #f6f6f7;
                }}
                .container {{
                    background: white;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                .success {{
                    background: #e3fcef;
                    color: #008060;
                    padding: 15px;
                    border-radius: 4px;
                    margin-bottom: 20px;
                    border-left: 4px solid #008060;
                }}
                .details {{
                    background: #f6f6f7;
                    padding: 15px;
                    border-radius: 4px;
                    margin-bottom: 20px;
                }}
                pre {{
                    margin: 0;
                    font-size: 12px;
                    overflow-x: auto;
                }}
                a {{
                    display: inline-block;
                    margin-top: 10px;
                    color: #008060;
                    text-decoration: none;
                }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success">
                    <h2 style="margin: 0 0 10px 0;">✓ SMS Sent Successfully!</h2>
                    <p style="margin: 0;">Your test SMS has been sent via Termii.</p>
                </div>
                
                <div class="details">
                    <strong>Details:</strong><br>
                    <strong>Phone:</strong> {formatted_phone}<br>
                    <strong>Message ID:</strong> {message_id}<br>
                    <strong>Sender ID:</strong> {termii_sender_id}<br><br>
                    <strong>Full Response:</strong>
                    <pre>{result}</pre>
                </div>
                
                <a href="/test-simple/sms?shop={shop_domain}">← Send Another SMS</a><br>
                <a href="/?shop={shop_domain}">← Back to Home</a>
            </div>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html_content)
        
    except ValueError as e:
        logger.error(f"Error: {e}")
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 600px;
                    margin: 40px auto;
                    padding: 20px;
                }}
                .error {{
                    background: #fef2f2;
                    color: #d72c0d;
                    padding: 15px;
                    border-radius: 4px;
                    border-left: 4px solid #d72c0d;
                }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>Error Sending SMS</h2>
                <p>{str(e)}</p>
                <a href="/test-simple/sms?shop={shop_domain}">← Try Again</a>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=400)
        
    except Exception as e:
        logger.error(f"Error sending SMS: {e}")
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 600px;
                    margin: 40px auto;
                    padding: 20px;
                }}
                .error {{
                    background: #fef2f2;
                    color: #d72c0d;
                    padding: 15px;
                    border-radius: 4px;
                    border-left: 4px solid #d72c0d;
                }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>Error Sending SMS</h2>
                <p>{str(e)}</p>
                <a href="/test-simple/sms?shop={shop_domain}">← Try Again</a>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)

