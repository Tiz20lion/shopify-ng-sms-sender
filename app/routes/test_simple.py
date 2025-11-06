"""
Simple SMS test endpoint without complex JavaScript to verify backend works.
"""

import os
import logging
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from app.services.termii import TermiiService
from app.utils.phone_formatter import format_phone_for_termii
from app.middleware.auth import require_admin_access
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
async def simple_test_sms_page(request: Request, _auth: bool = Depends(require_admin_access)):
    """Simple test page for sending SMS - uses basic form submission."""
    shop_domain = get_shop_domain_from_request(request)
    logger.info(f"Simple test SMS page - Shop domain: '{shop_domain}'")

    # Check Termii configuration from environment
    termii_api_key = os.getenv("TERMII_API_KEY", "").strip()
    termii_sender_id = os.getenv("TERMII_SENDER_ID", "").strip()
    termii_configured = bool(termii_api_key and termii_sender_id)

    settings_status = ""
    if termii_configured:
        settings_status = f'''<div class="status-banner success">
                    <svg class="icon" viewBox="0 0 24 24">
                        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                    </svg>
                    <div>
                        <h3>Termii Configured</h3>
                        <p>Ready to send SMS notifications. Sender ID: {termii_sender_id}</p>
                    </div>
                </div>'''
    else:
        settings_status = '''<div class="status-banner warning">
                    <svg class="icon" viewBox="0 0 24 24">
                        <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                    </svg>
                    <div>
                        <h3>Termii Not Configured</h3>
                        <p>Please add TERMII_API_KEY and TERMII_SENDER_ID to your .env file to enable SMS functionality.</p>
                    </div>
                </div>'''

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="referrer" content="no-referrer-when-downgrade">
        <title>SMS Test - SMS Notifications</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #ffffff;
                background-size: 20px 20px;
                background-image: 
                    linear-gradient(to right, rgba(0,0,0,0.03) 1px, transparent 1px),
                    linear-gradient(to bottom, rgba(0,0,0,0.03) 1px, transparent 1px);
                color: #1a1a1a;
                line-height: 1.5;
                min-height: 100vh;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
            }}
            .app-container {{
                min-height: 100vh;
            }}
            .header {{
                padding: 24px 16px;
                text-align: center;
                border-bottom: 1px solid rgba(0,0,0,0.08);
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
            }}
            .header h1 {{
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 8px;
                color: #1a1a1a;
                letter-spacing: -0.02em;
            }}
            .header p {{
                font-size: 0.9rem;
                color: #666;
                margin: 0;
            }}
            .content {{
                padding: 20px 16px;
                max-width: 420px;
                margin: 0 auto;
            }}
            .status-banner {{
                display: flex;
                align-items: flex-start;
                gap: 12px;
                padding: 16px;
                background: rgba(255,255,255,0.8);
                border: 1px solid rgba(0,0,0,0.06);
                border-radius: 6px;
                margin-bottom: 24px;
                backdrop-filter: blur(10px);
            }}
            .status-banner.success {{
                background: rgba(255,255,255,0.9);
                border-color: rgba(26,26,26,0.1);
            }}
            .status-banner.warning {{
                background: rgba(255,255,255,0.9);
                border-color: rgba(245,158,11,0.2);
            }}
            .status-banner .icon {{
                width: 20px;
                height: 20px;
                fill: #1a1a1a;
                flex-shrink: 0;
                margin-top: 2px;
            }}
            .status-banner.warning .icon {{
                fill: #f59e0b;
            }}
            .status-banner h3 {{
                font-size: 1rem;
                font-weight: 700;
                margin-bottom: 6px;
                color: #1a1a1a;
                letter-spacing: -0.01em;
            }}
            .status-banner p {{
                font-size: 0.85rem;
                color: #555;
                line-height: 1.4;
            }}
            .form-section {{
                margin-bottom: 24px;
            }}
            .form-group {{
                margin-bottom: 20px;
            }}
            .form-group label {{
                display: block;
                margin-bottom: 6px;
                font-weight: 600;
                color: #1a1a1a;
                font-size: 0.85rem;
                letter-spacing: -0.01em;
            }}
            .form-group input,
            .form-group textarea {{
                width: 100%;
                padding: 12px 14px;
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: 6px;
                font-size: 0.9rem;
                background: rgba(255,255,255,0.9);
                color: #1a1a1a;
                transition: all 0.2s ease;
                backdrop-filter: blur(10px);
            }}
            .form-group input:focus,
            .form-group textarea:focus {{
                outline: none;
                border-color: #1a1a1a;
                box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.08);
                background: rgba(255,255,255,0.95);
            }}
            .form-group textarea {{
                min-height: 100px;
                resize: vertical;
            }}
            .help-text {{
                font-size: 0.75rem;
                color: #666;
                margin-top: 4px;
                line-height: 1.3;
            }}
            .btn {{
                display: inline-block;
                padding: 14px 20px;
                background: #1a1a1a;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 700;
                font-size: 0.9rem;
                text-align: center;
                border: none;
                cursor: pointer;
                width: 100%;
                transition: all 0.2s ease;
                letter-spacing: -0.01em;
            }}
            .btn:hover {{
                background: #333;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
            .btn:active {{
                transform: translateY(0);
            }}
            .back-link {{
                display: inline-block;
                margin-top: 24px;
                color: #666;
                text-decoration: none;
                font-size: 0.9rem;
            }}
            .back-link:hover {{
                color: #1a1a1a;
            }}
            @media (max-width: 640px) {{
                body {{
                    background-size: 16px 16px;
                }}
                .header {{
                    padding: 20px 16px;
                }}
                .header h1 {{
                    font-size: 1.4rem;
                }}
                .content {{
                    padding: 16px 12px;
                }}
                .status-banner {{
                    padding: 14px;
                    margin-bottom: 20px;
                }}
                .form-group input,
                .form-group textarea {{
                    padding: 12px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="header">
                <h1>SMS Test</h1>
                <p>Test your SMS configuration with Nigerian phone numbers</p>
            </div>
            
            <div class="content">
                {settings_status}

                <div class="form-section">
                    <form method="POST" action="/test-simple/sms?shop={shop_domain}" id="smsForm">
                        <div class="form-group">
                            <label for="phone">Phone Number</label>
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
                            <label for="message">Message</label>
                            <textarea 
                                id="message" 
                                name="message" 
                                placeholder="Enter your test message..."
                                required
                            >Hi, this is a test message from your Shopify store!</textarea>
                            <div class="help-text">Maximum 160 characters for standard SMS</div>
                        </div>

                        <button type="submit" class="btn">Send Test SMS</button>
                    </form>
                </div>

                <a href="/?shop={shop_domain}" class="back-link">← Back to Dashboard</a>
            </div>
        </div>
        
        <!--Start of Tawk.to Script-->
        <script type="text/javascript">
        var Tawk_API=Tawk_API||{{}}, Tawk_LoadStart=new Date();
        (function(){{
        var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
        s1.async=true;
        s1.src='https://embed.tawk.to/690b95aae10d0719502aea91/1j9ak193c';
        s1.charset='UTF-8';
        s1.setAttribute('crossorigin','*');
        s0.parentNode.insertBefore(s1,s0);
        }})();
        </script>
        <!--End of Tawk.to Script-->
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)


@router.post("/sms", response_class=HTMLResponse)
async def send_simple_test_sms(
    request: Request,
    phone: str = Form(...),
    message: str = Form(...),
    _auth: bool = Depends(require_admin_access)
):
    """Send test SMS and return HTML response."""
    shop_domain = ""

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
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background-color: #ffffff;
                    background-size: 20px 20px;
                    background-image: 
                        linear-gradient(to right, rgba(0,0,0,0.03) 1px, transparent 1px),
                        linear-gradient(to bottom, rgba(0,0,0,0.03) 1px, transparent 1px);
                    color: #1a1a1a;
                    line-height: 1.5;
                    min-height: 100vh;
                    -webkit-text-size-adjust: 100%;
                    -ms-text-size-adjust: 100%;
                }}
                .app-container {{
                    min-height: 100vh;
                }}
                .header {{
                    padding: 24px 16px;
                    text-align: center;
                    border-bottom: 1px solid rgba(0,0,0,0.08);
                    background: rgba(255,255,255,0.95);
                    backdrop-filter: blur(10px);
                }}
                .header h1 {{
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin-bottom: 8px;
                    color: #1a1a1a;
                    letter-spacing: -0.02em;
                }}
                .content {{
                    padding: 20px 16px;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .success-banner {{
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                    padding: 16px;
                    background: rgba(255,255,255,0.95);
                    border: 1px solid rgba(26,26,26,0.15);
                    border-radius: 6px;
                    margin-bottom: 24px;
                    backdrop-filter: blur(10px);
                }}
                .success-banner .icon {{
                    width: 24px;
                    height: 24px;
                    fill: #1a1a1a;
                    flex-shrink: 0;
                    margin-top: 2px;
                }}
                .success-banner h2 {{
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin-bottom: 6px;
                    color: #1a1a1a;
                    letter-spacing: -0.01em;
                }}
                .success-banner p {{
                    font-size: 0.9rem;
                    color: #555;
                    line-height: 1.4;
                    margin: 0;
                }}
                .details-section {{
                    background: rgba(255,255,255,0.9);
                    border: 1px solid rgba(0,0,0,0.08);
                    border-radius: 6px;
                    padding: 16px;
                    margin-bottom: 24px;
                    backdrop-filter: blur(10px);
                }}
                .details-section h3 {{
                    font-size: 0.85rem;
                    font-weight: 700;
                    margin-bottom: 12px;
                    color: #1a1a1a;
                    letter-spacing: -0.01em;
                    text-transform: uppercase;
                }}
                .detail-row {{
                    display: flex;
                    margin-bottom: 8px;
                    font-size: 0.9rem;
                }}
                .detail-label {{
                    font-weight: 600;
                    color: #1a1a1a;
                    min-width: 100px;
                }}
                .detail-value {{
                    color: #555;
                    word-break: break-all;
                }}
                .response-box {{
                    background: rgba(240,240,240,0.8);
                    border: 1px solid rgba(0,0,0,0.06);
                    border-radius: 4px;
                    padding: 12px;
                    margin-top: 12px;
                    overflow-x: auto;
                }}
                .response-box pre {{
                    margin: 0;
                    font-size: 0.75rem;
                    color: #333;
                    font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Courier New', monospace;
                    line-height: 1.4;
                }}
                .link-group {{
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }}
                .link {{
                    display: inline-block;
                    color: #666;
                    text-decoration: none;
                    font-size: 0.9rem;
                    transition: all 0.2s ease;
                }}
                .link:hover {{
                    color: #1a1a1a;
                    transform: translateX(-2px);
                }}
                @media (max-width: 640px) {{
                    body {{
                        background-size: 16px 16px;
                    }}
                    .header {{
                        padding: 20px 16px;
                    }}
                    .header h1 {{
                        font-size: 1.4rem;
                    }}
                    .content {{
                        padding: 16px 12px;
                    }}
                    .detail-row {{
                        flex-direction: column;
                        gap: 2px;
                    }}
                    .detail-label {{
                        min-width: auto;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="app-container">
                <div class="header">
                    <h1>SMS Sent Successfully</h1>
                </div>
                
                <div class="content">
                    <div class="success-banner">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                        </svg>
                        <div>
                            <h2>✓ SMS Sent Successfully!</h2>
                            <p>Your test SMS has been sent via Termii.</p>
                        </div>
                    </div>

                    <div class="details-section">
                        <h3>Details</h3>
                        <div class="detail-row">
                            <span class="detail-label">Phone:</span>
                            <span class="detail-value">{formatted_phone}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Message ID:</span>
                            <span class="detail-value">{message_id}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Sender ID:</span>
                            <span class="detail-value">{termii_sender_id}</span>
                        </div>
                        
                        <div class="response-box">
                            <strong style="font-size: 0.8rem; color: #1a1a1a;">Full Response:</strong>
                            <pre>{result}</pre>
                        </div>
                    </div>

                    <div class="link-group">
                        <a href="/test-simple/sms?shop={shop_domain}" class="link">← Send Another SMS</a>
                        <a href="/?shop={shop_domain}" class="link">← Back to Home</a>
                    </div>
                </div>
            </div>
            
            <!--Start of Tawk.to Script-->
            <script type="text/javascript">
            var Tawk_API=Tawk_API||{{}}, Tawk_LoadStart=new Date();
            (function(){{
            var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
            s1.async=true;
            s1.src='https://embed.tawk.to/690b95aae10d0719502aea91/1j9ak193c';
            s1.charset='UTF-8';
            s1.setAttribute('crossorigin','*');
            s0.parentNode.insertBefore(s1,s0);
            }})();
            </script>
            <!--End of Tawk.to Script-->
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
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: white;
                    color: #1a1a1a;
                    line-height: 1.6;
                    min-height: 100vh;
                }}
                .app-container {{ min-height: 100vh; }}
                .header {{
                    padding: 32px 16px;
                    text-align: center;
                    border-bottom: 1px solid #e5e5e5;
                }}
                .header h1 {{
                    font-size: 1.75rem;
                    font-weight: 600;
                    margin-bottom: 12px;
                    color: #1a1a1a;
                }}
                .content {{
                    padding: 24px 16px;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .status-banner {{
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                    padding: 20px;
                    background: #f9f9f9;
                    border: 1px solid #666;
                    border-radius: 8px;
                    margin-bottom: 32px;
                }}
                .status-banner .icon {{
                    width: 20px;
                    height: 20px;
                    fill: #666;
                    flex-shrink: 0;
                    margin-top: 2px;
                }}
                .status-banner h3 {{
                    font-size: 1.1rem;
                    font-weight: 600;
                    margin-bottom: 8px;
                    color: #1a1a1a;
                }}
                .status-banner p {{
                    font-size: 0.9rem;
                    color: #666;
                    line-height: 1.4;
                }}
                .btn-link {{
                    display: inline-block;
                    padding: 12px 20px;
                    background: #1a1a1a;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 0.9rem;
                    transition: all 0.2s ease;
                    text-align: center;
                }}
                .btn-link:hover {{
                    background: #333;
                    transform: translateY(-1px);
                }}
            </style>
        </head>
        <body>
            <div class="app-container">
                <div class="header">
                    <h1>Error</h1>
                </div>
                <div class="content">
                    <div class="status-banner">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                        </svg>
                        <div>
                            <h3>Error Sending SMS</h3>
                            <p>{str(e)}</p>
                        </div>
                    </div>
                    <a href="/test-simple/sms?shop={shop_domain}" class="btn-link">Try Again</a>
                </div>
            </div>
            
            <!--Start of Tawk.to Script-->
            <script type="text/javascript">
            var Tawk_API=Tawk_API||{{}}, Tawk_LoadStart=new Date();
            (function(){{
            var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
            s1.async=true;
            s1.src='https://embed.tawk.to/690b95aae10d0719502aea91/1j9ak193c';
            s1.charset='UTF-8';
            s1.setAttribute('crossorigin','*');
            s0.parentNode.insertBefore(s1,s0);
            }})();
            </script>
            <!--End of Tawk.to Script-->
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
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: white;
                    color: #1a1a1a;
                    line-height: 1.6;
                    min-height: 100vh;
                }}
                .app-container {{ min-height: 100vh; }}
                .header {{
                    padding: 32px 16px;
                    text-align: center;
                    border-bottom: 1px solid #e5e5e5;
                }}
                .header h1 {{
                    font-size: 1.75rem;
                    font-weight: 600;
                    margin-bottom: 12px;
                    color: #1a1a1a;
                }}
                .content {{
                    padding: 24px 16px;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .status-banner {{
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                    padding: 20px;
                    background: #f9f9f9;
                    border: 1px solid #666;
                    border-radius: 8px;
                    margin-bottom: 32px;
                }}
                .status-banner .icon {{
                    width: 20px;
                    height: 20px;
                    fill: #666;
                    flex-shrink: 0;
                    margin-top: 2px;
                }}
                .status-banner h3 {{
                    font-size: 1.1rem;
                    font-weight: 600;
                    margin-bottom: 8px;
                    color: #1a1a1a;
                }}
                .status-banner p {{
                    font-size: 0.9rem;
                    color: #666;
                    line-height: 1.4;
                }}
                .btn-link {{
                    display: inline-block;
                    padding: 12px 20px;
                    background: #1a1a1a;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 0.9rem;
                    transition: all 0.2s ease;
                    text-align: center;
                }}
                .btn-link:hover {{
                    background: #333;
                    transform: translateY(-1px);
                }}
            </style>
        </head>
        <body>
            <div class="app-container">
                <div class="header">
                    <h1>Error</h1>
                </div>
                <div class="content">
                    <div class="status-banner">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                        </svg>
                        <div>
                            <h3>Error Sending SMS</h3>
                            <p>{str(e)}</p>
                        </div>
                    </div>
                    <a href="/test-simple/sms?shop={shop_domain}" class="btn-link">Try Again</a>
                </div>
            </div>
            
            <!--Start of Tawk.to Script-->
            <script type="text/javascript">
            var Tawk_API=Tawk_API||{{}}, Tawk_LoadStart=new Date();
            (function(){{
            var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
            s1.async=true;
            s1.src='https://embed.tawk.to/690b95aae10d0719502aea91/1j9ak193c';
            s1.charset='UTF-8';
            s1.setAttribute('crossorigin','*');
            s0.parentNode.insertBefore(s1,s0);
            }})();
            </script>
            <!--End of Tawk.to Script-->
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)