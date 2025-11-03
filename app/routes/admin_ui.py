import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/admin", tags=["admin-ui"])

SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY", "")


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """
    Settings page for customizing SMS templates.
    Termii credentials are configured in .env file (not editable here).
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Get shop domain and host parameter
    shop = request.query_params.get("shop", "")
    host_param = request.query_params.get("host", "")
    
    # If host not in query params, try to extract from referer
    if not host_param:
        referer = request.headers.get("referer", "")
        if referer:
            import re
            # Extract host from referer URL query params
            match = re.search(r'[?&]host=([^&]+)', referer)
            if match:
                from urllib.parse import unquote
                host_param = unquote(match.group(1))
                logger.info(f"Host extracted from referer: '{host_param[:30]}...'")
    
    logger.info(f"Shop from query params: '{shop}'")
    logger.info(f"Final host parameter: '{host_param[:30] if host_param else 'NOT PROVIDED'}...'")

    
    # Also try to extract shop from referer URL query params
    if not shop:
        referer = request.headers.get("referer", "")
        logger.info(f"Referer header: '{referer[:200] if referer else 'None'}'")
        if referer:
            import re
            from urllib.parse import unquote
            # Try to extract shop from referer URL query string
            match = re.search(r'[?&]shop=([^&]+)', referer)
            if match:
                shop = unquote(match.group(1))
                logger.info(f"Shop extracted from referer query: '{shop}'")
            # Also try to extract from referer domain
            if not shop and ".myshopify.com" in referer:
                match = re.search(r'https://([^/]+\.myshopify\.com)', referer)
                if match:
                    shop = match.group(1)
                    logger.info(f"Shop extracted from referer domain: '{shop}'")
    
    logger.info(f"Final shop domain determined: '{shop}'")
    
    # Check Termii configuration from environment
    termii_api_key = os.getenv("TERMII_API_KEY", "").strip()
    termii_sender_id = os.getenv("TERMII_SENDER_ID", "").strip()
    termii_configured = bool(termii_api_key and termii_sender_id)
    
    # Log for debugging
    logger.info(f"SHOPIFY_API_KEY loaded: {bool(SHOPIFY_API_KEY)}, length: {len(SHOPIFY_API_KEY) if SHOPIFY_API_KEY else 0}")
    
    # Create status banner
    if termii_configured:
        termii_status_banner = f'''
        <div class="banner banner-success">
            <div style="font-weight: 600; margin-bottom: 4px;">✓ Termii is Configured</div>
            <div style="font-size: 13px;">Sender ID: <strong>{termii_sender_id}</strong></div>
            <div style="font-size: 12px; margin-top: 4px; opacity: 0.8;">Termii API credentials are configured in your server's .env file</div>
        </div>
        '''
    else:
        termii_status_banner = '''
        <div class="banner banner-warning">
            <div style="font-weight: 600; margin-bottom: 4px;">⚠ Termii Not Configured</div>
            <div style="font-size: 13px; margin-top: 4px;">Please add <code>TERMII_API_KEY</code> and <code>TERMII_SENDER_ID</code> to your server's .env file</div>
        </div>
        '''
    
    # Pass shop domain to JavaScript (properly escaped)
    if shop:
        shop_js = f'"{shop}"'  # Wrap in quotes for JavaScript string
    else:
        shop_js = 'null'  # Use null instead of empty string
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Settings - Termii SMS Notifications</title>
        <script>
            // For embedded Shopify apps with server-side OAuth sessions,
            // we use regular fetch - the backend manages authentication via cookies/sessions
            console.log('🔐 Authentication: Using session-based auth (managed by backend OAuth)');
            
            // Enhanced fetch with better error handling and ngrok compatibility
            async function authenticatedFetch(url, options = {{}}) {{
                // Add headers for ngrok and JSON
                options.headers = {{
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true',
                    ...options.headers
                }};
                
                try {{
                    const response = await fetch(url, options);
                    return response;
                }} catch (error) {{
                    console.error('🔴 Fetch error:', error);
                    throw error;
                }}
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
            .section {{
                margin-bottom: 30px;
            }}
            .section-title {{
                font-size: 16px;
                font-weight: 600;
                color: #202223;
                margin-bottom: 16px;
            }}
            .banner {{
                padding: 16px;
                border-radius: 8px;
                margin-bottom: 24px;
                border-left: 4px solid;
            }}
            .banner-success {{
                background: #e3fcef;
                color: #008060;
                border-color: #008060;
            }}
            .banner-warning {{
                background: #fff4e6;
                color: #c05717;
                border-color: #c05717;
            }}
            .banner code {{
                background: rgba(0,0,0,0.1);
                padding: 2px 6px;
                border-radius: 3px;
                font-family: monospace;
                font-size: 12px;
            }}
            .form-group {{
                margin-bottom: 20px;
            }}
            label {{
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
                color: #202223;
                font-size: 14px;
            }}
            textarea {{
                width: 100%;
                padding: 10px;
                border: 1px solid #c9cccf;
                border-radius: 4px;
                font-size: 14px;
                font-family: inherit;
                min-height: 100px;
                resize: vertical;
                box-sizing: border-box;
            }}
            .help-text {{
                font-size: 12px;
                color: #6d7175;
                margin-top: 6px;
            }}
            .button {{
                padding: 12px 24px;
                background: #008060;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
                cursor: pointer;
                font-size: 14px;
            }}
            .button:hover {{
                background: #006e52;
            }}
            .button:disabled {{
                background: #c9cccf;
                cursor: not-allowed;
            }}
            .message {{
                padding: 12px;
                border-radius: 4px;
                margin-bottom: 20px;
                display: none;
            }}
            .message.success {{
                background: #e3fcef;
                color: #008060;
                border-left: 4px solid #008060;
            }}
            .message.error {{
                background: #fef2f2;
                color: #d72c0d;
                border-left: 4px solid #d72c0d;
            }}
            .info-box {{
                background: #f6f6f7;
                padding: 12px 16px;
                border-radius: 4px;
                font-size: 13px;
                color: #6d7175;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚙️ Settings - Termii SMS Notifications</h1>
            
            <div id="message" class="message"></div>
            
            <!-- Termii Configuration Status -->
            <div class="section">
                <div class="section-title">Termii Configuration</div>
                {termii_status_banner}
            </div>
            
            <!-- SMS Templates -->
            <div class="section">
                <div class="section-title">SMS Templates</div>
                <div class="info-box">
                    📝 Customize the SMS messages sent to customers. Templates are saved per-shop and persist across server restarts.
                </div>
                
                <form id="settingsForm">
                    <div class="form-group">
                        <label for="order_confirmation_template">Order Confirmation Template</label>
                        <textarea id="order_confirmation_template" name="order_confirmation_template">Hi {{{{customer_name}}}}, your Backwoods order #{{{{order_number}}}} has been confirmed. Total: {{{{total_price}}}}. Thank you for your purchase!</textarea>
                        <div class="help-text">Available variables: {{{{customer_name}}}}, {{{{order_number}}}}, {{{{total_price}}}}</div>
                    </div>
                    
                    <div class="form-group">
                        <label for="fulfillment_template">Fulfillment Template</label>
                        <textarea id="fulfillment_template" name="fulfillment_template">Hi {{{{customer_name}}}}, your order #{{{{order_number}}}} has been shipped and will arrive soon!</textarea>
                        <div class="help-text">Available variables: {{{{customer_name}}}}, {{{{order_number}}}}</div>
                    </div>
                    
                    <button type="submit" class="button" id="saveButton">Save Templates</button>
                </form>
            </div>
            
            <div style="margin-top: 30px;">
                <a href="/?shop={shop}" style="color: #008060; text-decoration: none;" id="backToHomeLink">← Back to Home</a>
            </div>
        </div>
        
        <script>
            // Get shop domain from multiple sources
            function getShopDomain() {{
                let shopDomain = {shop_js};
                
                if (!shopDomain) {{
                    const urlParams = new URLSearchParams(window.location.search);
                    shopDomain = urlParams.get('shop');
                }}
                
                if (!shopDomain) {{
                    try {{
                        const referrer = document.referrer;
                        if (referrer) {{
                            const referrerParams = new URLSearchParams(referrer.split('?')[1] || '');
                            shopDomain = referrerParams.get('shop');
                        }}
                    }} catch (e) {{}}
                }}
                
                if (!shopDomain) {{
                    try {{
                        const referrer = document.referrer;
                        const match = referrer.match(/https:\\/\\/([^/]+\\.myshopify\\.com)/);
                        if (match) {{
                            shopDomain = match[1];
                        }}
                    }} catch (e) {{}}
                }}
                
                if (shopDomain && !shopDomain.includes('.myshopify.com')) {{
                    shopDomain = `${{shopDomain}}.myshopify.com`;
                }}
                
                if (shopDomain) {{
                    try {{
                        localStorage.setItem('shopify_shop_domain', shopDomain);
                    }} catch (e) {{}}
                }}
                
                return shopDomain || '';
            }}
            
            let shop = getShopDomain();
            console.log('🏪 Shop domain detected:', shop);
            
            const form = document.getElementById('settingsForm');
            const messageDiv = document.getElementById('message');
            const saveButton = document.getElementById('saveButton');
            
            if (!shop) {{
                console.error('❌ Shop domain detection failed');
                messageDiv.className = 'message error';
                messageDiv.style.display = 'block';
                messageDiv.innerHTML = 'Unable to determine shop domain. Cannot save settings.';
                form.style.pointerEvents = 'none';
                form.style.opacity = '0.6';
            }} else {{
                window.currentShop = shop;
                const backLink = document.getElementById('backToHomeLink');
                if (backLink) backLink.href = `/?shop=${{shop}}`;
            }}
            
            // Load existing templates
            async function loadSettings() {{
                if (!shop) return;
                
                try {{
                    const response = await authenticatedFetch(`/api/settings?shop=${{encodeURIComponent(shop)}}`);
                    
                    if (response.ok) {{
                        const data = await response.json();
                        console.log('✅ Templates loaded:', data);
                        
                        document.getElementById('order_confirmation_template').value = data.order_confirmation_template || '';
                        document.getElementById('fulfillment_template').value = data.fulfillment_template || '';
                    }} else {{
                        console.warn('⚠️ Could not load existing templates (may not exist yet)');
                    }}
                }} catch (error) {{
                    console.error('❌ Error loading templates:', error);
                }}
            }}
            
            // Show message
            function showMessage(text, type) {{
                messageDiv.textContent = text;
                messageDiv.className = `message ${{type}}`;
                messageDiv.style.display = 'block';
                setTimeout(() => {{
                    messageDiv.style.display = 'none';
                }}, 5000);
            }}
            
            // Save templates
            form.addEventListener('submit', async (e) => {{
                e.preventDefault();
                
                let currentShop = window.currentShop || shop || getShopDomain();
                
                if (!currentShop) {{
                    showMessage('Unable to determine shop domain. Cannot save templates.', 'error');
                    return;
                }}
                
                saveButton.disabled = true;
                saveButton.textContent = 'Saving...';
                
                const formData = {{
                    order_confirmation_template: document.getElementById('order_confirmation_template').value,
                    fulfillment_template: document.getElementById('fulfillment_template').value
                }};
                
                console.log('💾 Saving templates for shop:', currentShop);
                console.log('📝 Form data:', formData);
                
                try {{
                    const apiUrl = `/api/settings?shop=${{encodeURIComponent(currentShop)}}`;
                    console.log('🚀 POST URL:', apiUrl);
                    
                    // Add timeout to prevent infinite hanging
                    const controller = new AbortController();
                    const timeoutId = setTimeout(() => controller.abort(), 15000);
                    
                    const response = await authenticatedFetch(apiUrl, {{
                        method: 'POST',
                        body: JSON.stringify(formData),
                        signal: controller.signal
                    }});
                    
                    clearTimeout(timeoutId);
                    
                    console.log('📡 Response status:', response.status);
                    
                    saveButton.disabled = false;
                    saveButton.textContent = 'Save Templates';
                    
                    if (response.ok) {{
                        const result = await response.json();
                        console.log('✅ Templates saved successfully:', result);
                        showMessage('Templates saved successfully!', 'success');
                        await loadSettings();
                    }} else {{
                        let errorMessage = 'Failed to save templates';
                        try {{
                            const error = await response.json();
                            errorMessage = error.detail || error.message || errorMessage;
                            console.error('❌ Error response:', error);
                        }} catch (e) {{
                            const text = await response.text();
                            console.error('❌ Error response (non-JSON):', text);
                            errorMessage = text || errorMessage;
                        }}
                        showMessage(errorMessage, 'error');
                    }}
                }} catch (error) {{
                    console.error('❌ Exception saving templates:', error);
                    console.error('🔍 Error name:', error.name);
                    console.error('💬 Error message:', error.message);
                    
                    saveButton.disabled = false;
                    saveButton.textContent = 'Save Templates';
                    
                    let errorMsg = 'Error saving templates';
                    if (error.name === 'AbortError') {{
                        errorMsg = 'Request timed out after 15 seconds. Please check your connection and try again.';
                    }} else if (error.message) {{
                        errorMsg = `Error: ${{error.message}}`;
                    }}
                    
                    showMessage(errorMsg, 'error');
                }}
            }});
            
            // Load templates on page load
            loadSettings();
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)
