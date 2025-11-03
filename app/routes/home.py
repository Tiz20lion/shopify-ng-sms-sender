import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["home"])

SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")


@router.get("/", response_class=HTMLResponse)
async def app_home(request: Request):
    """
    Main app home page for embedded Shopify app.
    This page loads in the Shopify admin iframe.
    """
    # Get shop domain from query params (Shopify adds this)
    shop = request.query_params.get("shop", "")
    host = request.headers.get("host", "localhost:8000")
    
    # Extract host for App Bridge
    api_key = SHOPIFY_API_KEY or ""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Termii SMS Notifications</title>
        <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
        <script>
            // Set header to bypass ngrok browser warning (for free ngrok tier)
            // This ensures all fetch requests include the header to skip the warning page
            if (typeof fetch !== 'undefined') {{
                const originalFetch = window.fetch;
                window.fetch = function(...args) {{
                    if (args[1]) {{
                        args[1].headers = args[1].headers || {{}};
                        args[1].headers['ngrok-skip-browser-warning'] = 'true';
                    }} else {{
                        args[1] = {{ headers: {{ 'ngrok-skip-browser-warning': 'true' }} }};
                    }}
                    return originalFetch.apply(this, args);
                }};
            }}
            
            // Also set for XMLHttpRequest
            if (typeof XMLHttpRequest !== 'undefined') {{
                const originalOpen = XMLHttpRequest.prototype.open;
                const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
                
                XMLHttpRequest.prototype.open = function(method, url, ...rest) {{
                    this._url = url;
                    return originalOpen.apply(this, [method, url, ...rest]);
                }};
                
                XMLHttpRequest.prototype.setRequestHeader = function(name, value) {{
                    // Ensure ngrok header is always set
                    if (name.toLowerCase() === 'ngrok-skip-browser-warning') {{
                        return originalSetRequestHeader.apply(this, [name, value]);
                    }}
                    const result = originalSetRequestHeader.apply(this, [name, value]);
                    // Set ngrok header after setting other headers
                    try {{
                        originalSetRequestHeader.call(this, 'ngrok-skip-browser-warning', 'true');
                    }} catch (e) {{
                        // Header might already be set, ignore
                    }}
                    return result;
                }};
            }}
        </script>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                margin: 0;
                padding: 20px;
                background: #f6f6f7;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #202223;
                margin-top: 0;
            }}
            .status {{
                padding: 15px;
                background: #e3fcef;
                border-left: 4px solid #008060;
                border-radius: 4px;
                margin: 20px 0;
            }}
            .info {{
                background: #f6f6f7;
                padding: 15px;
                border-radius: 4px;
                margin: 20px 0;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background: #008060;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 20px;
                margin-right: 10px;
                font-weight: 500;
                transition: background 0.2s;
            }}
            .button:hover {{
                background: #006e52;
            }}
            .button.secondary {{
                background: #5c6ac4;
            }}
            .button.secondary:hover {{
                background: #4c54b2;
            }}
            .button-group {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 20px;
            }}
            ul {{
                line-height: 1.8;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 Termii SMS Notifications</h1>
            
            <div class="status">
                <strong>✅ App is running successfully!</strong>
                <p>Your Shopify app is connected and ready to send SMS notifications.</p>
            </div>
            
            <div class="info">
                <h3>Getting Started</h3>
                <ol>
                    <li><strong>Test SMS Sender:</strong> First, test your SMS configuration to ensure Termii is working correctly.</li>
                    <li><strong>Configure Settings:</strong> Set up your SMS templates for order confirmations and fulfillments.</li>
                    <li><strong>Test with Real Orders:</strong> Create a test order to verify SMS notifications are working.</li>
                </ol>
                
                <div class="button-group">
                    <a href="/test-simple/sms?shop={shop}" class="button" id="testSmsLink">📱 Test SMS Sender</a>
                    <a href="/admin/settings?shop={shop}" class="button secondary" id="settingsLink">⚙️ Configure Settings</a>
                </div>
            </div>
            
            <div class="info">
                <h3>Features</h3>
                <ul>
                    <li>✅ Automatic SMS notifications when orders are created</li>
                    <li>✅ SMS notifications when orders are fulfilled</li>
                    <li>✅ Customizable SMS templates with order and customer data</li>
                    <li>✅ Easy-to-use admin settings interface</li>
                </ul>
            </div>
            
            <div class="info">
                <h3>Need Help?</h3>
                <p>Check the README.md file in your project for detailed setup instructions and troubleshooting tips.</p>
            </div>
        </div>
        
        <script>
            // Initialize App Bridge
            if (typeof window.shopify !== 'undefined') {{
                console.log('App Bridge initialized');
            }}
            
            // Ensure settings link includes shop parameter and save to localStorage
            (function() {{
                const urlParams = new URLSearchParams(window.location.search);
                let shop = urlParams.get('shop');
                
                // Fallback to server-provided shop
                if (!shop || shop === '') {{
                    shop = '{shop}';
                }}
                
                // Try App Bridge session as fallback
                if ((!shop || shop === '' || shop === 'null') && typeof shopify !== 'undefined' && shopify?.session?.shop) {{
                    shop = shopify.session.shop;
                }}
                
                console.log('Home page - detected shop:', shop);
                
                // Save shop to localStorage for future use
                if (shop && shop !== '' && shop !== 'null') {{
                    try {{
                        localStorage.setItem('shopify_shop_domain', shop);
                    }} catch (e) {{
                        console.warn('Could not save to localStorage:', e);
                    }}
                }}
                
                   const settingsLink = document.getElementById('settingsLink');
                   const testSmsLink = document.getElementById('testSmsLink');
                   
                   // Get host parameter from current URL
                   const urlParams = new URLSearchParams(window.location.search);
                   const host = urlParams.get('host');
                   
                   if (shop && shop !== '' && shop !== 'null') {{
                       if (settingsLink) {{
                           const baseUrl = settingsLink.getAttribute('href').split('?')[0];
                           let settingsUrl = `${{baseUrl}}?shop=${{encodeURIComponent(shop)}}`;
                           if (host) {{
                               settingsUrl += `&host=${{encodeURIComponent(host)}}`;
                           }}
                           settingsLink.href = settingsUrl;
                           console.log('Updated settings link to:', settingsUrl);
                           console.log('Host parameter included:', !!host);
                       }}
                       if (testSmsLink) {{
                           const baseUrl = testSmsLink.getAttribute('href').split('?')[0];
                           testSmsLink.href = `${{baseUrl}}?shop=${{shop}}`;
                           console.log('Updated test SMS link to:', testSmsLink.href);
                       }}
                   }} else {{
                       console.warn('Shop not found, links may not work');
                   }}
            }})();
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

