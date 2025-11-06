import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
from app.middleware.auth import require_admin_access

load_dotenv()

router = APIRouter(prefix="/admin", tags=["admin-ui"])

SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY", "")


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, _auth: bool = Depends(require_admin_access)):
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
        <div class="status-banner success">
            <svg class="icon" viewBox="0 0 24 24">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
            </svg>
            <div>
                <h3>Termii is Configured</h3>
                <p>Sender ID: <strong>{termii_sender_id}</strong><br>Termii API credentials are configured in your server's .env file</p>
            </div>
        </div>
        '''
    else:
        termii_status_banner = '''
        <div class="status-banner warning">
            <svg class="icon" viewBox="0 0 24 24">
                <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
            </svg>
            <div>
                <h3>Termii Not Configured</h3>
                <p>Please add <code>TERMII_API_KEY</code> and <code>TERMII_SENDER_ID</code> to your server's .env file</p>
            </div>
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
        <meta name="referrer" content="no-referrer-when-downgrade">
        <title>Settings - SMS Notifications</title>
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
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                min-height: 100vh;
            }}

            .app-container {{
                min-height: 100vh;
            }}

            /* Header */
            .header {{
                padding: 24px 16px;
                text-align: center;
                background: #1a1a1a;
                border-bottom: 1px solid rgba(0,0,0,0.2);
            }}
            .header h1 {{
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 8px;
                color: #ffffff;
                letter-spacing: -0.02em;
            }}
            .header .subtitle {{
                font-size: 0.9rem;
                color: rgba(255,255,255,0.7);
                font-weight: 400;
                max-width: 100%;
                margin: 0 auto;
                line-height: 1.5;
            }}

            /* Content */
            .content {{
                padding: 20px 16px;
                max-width: 900px;
                margin: 0 auto;
            }}

            /* Status banners */
            .status-banner {{
                display: flex;
                align-items: flex-start;
                gap: 12px;
                padding: 16px;
                background: rgba(255,255,255,0.9);
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: 6px;
                margin-bottom: 24px;
                backdrop-filter: blur(10px);
                box-shadow: 0 2px 8px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
            }}
            .status-banner.success {{
                border-color: rgba(26,26,26,0.15);
                background: rgba(255,255,255,0.95);
            }}
            .status-banner.warning {{
                border-color: rgba(245,158,11,0.2);
                background: rgba(255,255,255,0.95);
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
            .status-banner code {{
                background: rgba(26, 26, 26, 0.08);
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'SF Mono', Monaco, monospace;
                font-size: 0.8rem;
                color: #1a1a1a;
            }}
            .status-banner strong {{
                color: #1a1a1a;
                font-weight: 600;
            }}

            /* Settings grid */
            .settings-grid {{
                display: grid;
                gap: 20px;
                margin-bottom: 24px;
            }}
            
            /* Form card */
            .form-card {{
                background: rgba(255,255,255,0.9);
                border: 1px solid rgba(0,0,0,0.08);
                border-radius: 6px;
                padding: 20px;
                transition: all 0.2s ease;
                backdrop-filter: blur(10px);
                box-shadow: 0 2px 8px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
            }}
            .form-card:focus-within {{
                border-color: rgba(26,26,26,0.2);
                box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.1);
            }}
            .form-card h3 {{
                font-size: 1.1rem;
                font-weight: 700;
                margin-bottom: 10px;
                color: #1a1a1a;
                letter-spacing: -0.01em;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .form-card .description {{
                font-size: 0.85rem;
                color: #666;
                margin-bottom: 20px;
                line-height: 1.5;
            }}

            /* Form groups */
            .form-group {{
                margin-bottom: 18px;
            }}
            .form-group:last-child {{
                margin-bottom: 0;
            }}
            label {{
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #1a1a1a;
                font-size: 0.85rem;
                letter-spacing: -0.01em;
            }}
            textarea {{
                width: 100%;
                padding: 12px 14px;
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: 6px;
                font-size: 0.9rem;
                font-family: inherit;
                min-height: 100px;
                resize: vertical;
                transition: all 0.2s ease;
                background: rgba(255,255,255,0.9);
                color: #1a1a1a;
                backdrop-filter: blur(10px);
            }}
            textarea:hover {{
                border-color: rgba(0,0,0,0.15);
            }}
            textarea:focus {{
                outline: none;
                border-color: #1a1a1a;
                box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.08);
                background: rgba(255,255,255,0.95);
            }}
            .help-text {{
                font-size: 0.75rem;
                color: #666;
                margin-top: 6px;
                line-height: 1.4;
            }}
            
            /* Variable tags */
            .variable-tags {{
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-top: 8px;
            }}
            .variable-tag {{
                display: inline-block;
                padding: 4px 10px;
                background: rgba(0,0,0,0.05);
                border: 1px solid rgba(0,0,0,0.08);
                border-radius: 4px;
                font-size: 0.75rem;
                font-family: 'SF Mono', Monaco, monospace;
                color: #1a1a1a;
                cursor: pointer;
                transition: all 0.2s ease;
            }}
            .variable-tag:hover {{
                background: rgba(0,0,0,0.08);
                border-color: rgba(0,0,0,0.15);
                transform: translateY(-1px);
            }}

            /* Button styles */
            .btn {{
                display: inline-block;
                padding: 14px 20px;
                background: #1a1a1a;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 700;
                font-size: 0.9rem;
                text-decoration: none;
                cursor: pointer;
                transition: all 0.2s ease;
                text-align: center;
                width: 100%;
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
            .btn:disabled {{
                background: #ccc;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }}

            /* Message styles */
            .message {{
                padding: 16px;
                border-radius: 6px;
                margin-bottom: 20px;
                font-size: 0.9rem;
                display: none;
                border: 1px solid;
                backdrop-filter: blur(10px);
                animation: slideIn 0.3s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
            }}
            .message.success {{
                background: rgba(255,255,255,0.95);
                color: #1a1a1a;
                border-color: rgba(26,26,26,0.15);
            }}
            .message.error {{
                background: rgba(255,255,255,0.95);
                color: #666;
                border-color: rgba(245,158,11,0.2);
            }}
            @keyframes slideIn {{
                from {{
                    opacity: 0;
                    transform: translateY(-10px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            /* Back link */
            .back-link {{
                display: inline-block;
                color: #666;
                text-decoration: none;
                font-size: 0.9rem;
                margin-top: 24px;
                transition: all 0.2s ease;
            }}
            .back-link:hover {{
                color: #1a1a1a;
            }}

            /* Mobile responsive */
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
                .form-card {{
                    padding: 16px;
                }}
                .settings-grid {{
                    gap: 16px;
                    margin-bottom: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="header">
                <h1>Settings</h1>
                <p class="subtitle">Configure your SMS notifications and templates</p>
            </div>

            <div class="content">
                <div id="message" class="message"></div>

                <!-- Termii Configuration Status -->
                {termii_status_banner}

                <!-- SMS Templates -->
                <div class="settings-grid">
                    <div class="form-card">
                        <h3>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                            </svg>
                            Order Confirmation Template
                        </h3>
                        <p class="description">Sent automatically when a customer places an order</p>

                        <form id="settingsForm">
                            <div class="form-group">
                                <label for="order_confirmation_template">Template Message</label>
                                <textarea id="order_confirmation_template" name="order_confirmation_template" placeholder="Hi {{{{customer_name}}}}, your order #{{{{order_number}}}} has been confirmed...">Hi {{{{customer_name}}}}, your order #{{{{order_number}}}} has been confirmed. Total: {{{{total_price}}}}. Thank you for your purchase!</textarea>
                                <div class="help-text">Click a variable below to insert it:</div>
                                <div class="variable-tags">
                                    <span class="variable-tag" onclick="insertVariable('order_confirmation_template', '{{{{customer_name}}}}')">{{{{customer_name}}}}</span>
                                    <span class="variable-tag" onclick="insertVariable('order_confirmation_template', '{{{{order_number}}}}')">{{{{order_number}}}}</span>
                                    <span class="variable-tag" onclick="insertVariable('order_confirmation_template', '{{{{total_price}}}}')">{{{{total_price}}}}</span>
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="fulfillment_template">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                                        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                                        <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                                        <line x1="12" y1="22.08" x2="12" y2="12"></line>
                                    </svg>
                                    Fulfillment Template
                                </label>
                                <textarea id="fulfillment_template" name="fulfillment_template" placeholder="Hi {{{{customer_name}}}}, your order #{{{{order_number}}}} has been shipped...">Hi {{{{customer_name}}}}, your order #{{{{order_number}}}} has been shipped and will arrive soon!</textarea>
                                <div class="help-text">Click a variable below to insert it:</div>
                                <div class="variable-tags">
                                    <span class="variable-tag" onclick="insertVariable('fulfillment_template', '{{{{customer_name}}}}')">{{{{customer_name}}}}</span>
                                    <span class="variable-tag" onclick="insertVariable('fulfillment_template', '{{{{order_number}}}}')">{{{{order_number}}}}</span>
                                </div>
                            </div>

                            <button type="submit" class="btn" id="saveButton">Save Templates</button>
                        </form>
                    </div>
                </div>

                <a href="/?shop={shop}" class="back-link" id="backToHomeLink">← Back to Home</a>
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
            
            // Function to insert variable at cursor position
            window.insertVariable = function(textareaId, variable) {{
                const textarea = document.getElementById(textareaId);
                const cursorPos = textarea.selectionStart;
                const textBefore = textarea.value.substring(0, cursorPos);
                const textAfter = textarea.value.substring(cursorPos);
                
                textarea.value = textBefore + variable + textAfter;
                textarea.focus();
                
                // Set cursor position after inserted variable
                const newCursorPos = cursorPos + variable.length;
                textarea.setSelectionRange(newCursorPos, newCursorPos);
            }};

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
                
                // Scroll to top to see the notification
                window.scrollTo({{
                    top: 0,
                    behavior: 'smooth'
                }});
                
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