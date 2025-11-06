<div align="center">

#  Shopify NG SMS Sender

**Automate SMS notifications for your Nigerian Shopify store using Termii API**

Send order confirmations and fulfillment updates to your customers via SMS - built specifically for Nigerian e-commerce developers.

---

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi)
![Shopify](https://img.shields.io/badge/Shopify-App-95BF47?style=flat-square&logo=shopify)
![Termii](https://img.shields.io/badge/Termii-SMS-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

</div>

## 📱 Live Demo

<div align="center">

![App Demo](attached_assets/app-demo.gif)

*app demonstration - Modern SaaS landing page with interactive features and responsive design*

</div>

## 🎯 Overview

This FastAPI-based Shopify app automatically sends SMS notifications to Nigerian customers when they:
- ✅ Place an order (Order Confirmation)
- 📦 Receive order fulfillment updates (Shipping Notifications)

Built with **Termii API** for reliable SMS delivery across Nigerian networks.

### Why This Tool?

- 🇳🇬 **Nigeria-focused**: Optimized for Nigerian phone numbers and networks
- 🚀 **Easy Setup**: Get running in under 10 minutes
- 🎨 **Customizable**: Edit SMS templates to match your brand
- 💰 **Cost-effective**: Uses Termii's affordable Nigerian SMS rates
- 🔒 **Secure**: Built-in webhook verification, OAuth, and shop whitelist protection

## 📚 Documentation

For detailed information about the system architecture, UI/UX decisions, technical implementations, and external dependencies, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Quick Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `example.env` to `.env` and add your credentials:

```env
# Shopify App (from Partner Dashboard → Apps → Your App → Configuration)
SHOPIFY_API_KEY=your_client_id
SHOPIFY_API_SECRET=your_client_secret

# Webhook Secret (from Shopify Admin → Settings → Notifications → Webhooks)
SHOPIFY_WEBHOOK_SECRET=your_64_char_webhook_secret

SHOPIFY_SCOPES=read_orders,read_customers,read_fulfillments

# Termii SMS
TERMII_API_KEY=your_termii_api_key
TERMII_BASE_URL=https://v3.api.termii.com
TERMII_SENDER_ID=your_sender_id

# Tunnel URL
APP_URL=https://tizlionai.com

# Security: Shop Whitelist (Optional - Recommended for Production)
# Comma-separated list of authorized shop domains
# Leave empty during initial setup, then add your shop(s) to restrict access
ALLOWED_SHOPS=yourstore.myshopify.com,anotherstore.myshopify.com
```

### 3. Start Tunnel

**Cloudflare (Recommended)**
```bash
cloudflared tunnel --url http://localhost:8000
```

**ngrok (Alternative)**
```bash
ngrok http 8000
```

### 4. Configure Shopify App

1. Go to [Shopify Partner Dashboard](https://partners.shopify.com)
2. Navigate to: **Apps → Your App → Configuration**
3. Set URLs:
   - **App URL**: `https://your-tunnel-url`
   - **Redirect URL**: `https://your-tunnel-url/api/auth/callback`
4. Copy Client ID and Client Secret to `.env`

### 5. Setup Webhooks

1. Install app: `https://your-tunnel-url/api/auth?shop=yourstore.myshopify.com`
2. Go to Shopify Admin: **Settings → Notifications → Webhooks**
3. Create two webhooks:
   - **Order creation** → `https://your-tunnel-url/webhooks/orders/create` (API 2025-10)
   - **Order fulfillment** → `https://your-tunnel-url/webhooks/orders/fulfilled` (API 2025-10)
4. Copy the 64-character **webhook signing secret** shown at bottom to `SHOPIFY_WEBHOOK_SECRET` in `.env`

### 6. Run App

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Usage

1. **Configure Settings**: Go to Shopify Admin → Apps → SMS Notifications
2. **Add Termii credentials** and customize SMS templates
3. **Test SMS**: Use the test page at `https://your-tunnel-url/test-simple/sms`
4. **Create test order** in Shopify to verify automation

## 🔐 Security Features

### Shop Whitelist Protection

Prevent unauthorized shops from accessing your app and incurring SMS costs:

1. **Set ALLOWED_SHOPS** environment variable with your authorized shop domain(s)
2. Only whitelisted shops can access admin features (settings, SMS testing)
3. Works seamlessly with Shopify's embedded iframe - no URL editing needed

**Example:**
```env
# Single shop
ALLOWED_SHOPS=yourstore.myshopify.com

# Multiple shops
ALLOWED_SHOPS=shop1.myshopify.com,shop2.myshopify.com,shop3.myshopify.com
```

**Note:** Leave empty during initial setup. Once configured, only whitelisted shops will have access to admin features.

## SMS Templates

Available variables:
- `{{customer_name}}` - Customer first name
- `{{order_number}}` - Order number (e.g., #1001)
- `{{total_price}}` - Order total (order confirmation only)

**Default Templates:**
```
Order Confirmation:
Hi {{customer_name}}, your order #{{order_number}} has been confirmed. Total: {{total_price}}. Thank you!

Fulfillment:
Hi {{customer_name}}, your order #{{order_number}} has been shipped and will arrive soon!
```

## Troubleshooting

### Webhooks Failing (401 Error)
- Ensure `SHOPIFY_WEBHOOK_SECRET` matches the secret in Shopify Admin webhooks page
- Delete and recreate webhooks if you changed the secret
- Check logs for HMAC verification details

### SMS Not Sending
- Verify Termii API key and sender ID are correct
- Ensure Termii account has sufficient balance
- Check phone numbers are in international format (no `+` prefix)
- Use `generic` channel for transactional messages

### App Not Loading
- Verify tunnel is running and accessible
- Check redirect URLs match exactly in Partner Dashboard
- Ensure app is installed: `https://your-tunnel-url/api/auth?shop=yourstore.myshopify.com`

### Access Denied (403 Forbidden)
- Check if `ALLOWED_SHOPS` is set and includes your shop domain
- Ensure shop domain is in correct format: `yourstore.myshopify.com`
- For multiple shops, use comma-separated list without spaces
- Leave `ALLOWED_SHOPS` empty during initial setup/testing

### Save Button Hangs ("Saving...")
- This is due to Shopify's embedded app security
- **Fixed**: The app now uses App Bridge's `authenticatedFetch()`
- Hard refresh the page (`Ctrl+Shift+R` or `Cmd+Shift+R`)
- Check browser console for "App Bridge authenticated fetch initialized"

## Project Structure

```
shopify-ng-sms-sender/
├── app/
│   ├── main.py              # FastAPI app
│   ├── routes/
│   │   ├── auth.py          # OAuth
│   │   ├── webhooks.py      # Webhook handlers
│   │   ├── admin.py         # Settings API
│   │   ├── admin_ui.py      # Settings UI page
│   │   ├── home.py          # Home page
│   │   └── test_simple.py   # Test SMS page
│   ├── services/
│   │   ├── termii.py        # SMS service
│   │   ├── shopify.py       # Shopify API client
│   │   └── webhook_verifier.py  # HMAC verification
│   ├── models/
│   │   ├── settings.py      # Settings model
│   │   └── templates.py     # Template storage
│   ├── utils/
│   │   └── phone_formatter.py  # Phone number formatting
│   └── templates.json.example  # Template example (copy to templates.json)
├── extensions/
│   └── admin-ui/            # Shopify Admin UI Extension
├── example.env              # Environment template
├── shopify.app.toml         # Shopify app configuration
├── requirements.txt        # Python dependencies
├── ARCHITECTURE.md         # System architecture and design documentation
└── LICENSE                 # MIT License
```

## API Endpoints

- `GET /api/auth?shop={shop}` - Install app
- `POST /webhooks/orders/create` - Order creation
- `POST /webhooks/orders/fulfilled` - Order fulfillment
- `GET /api/settings` - Get settings
- `POST /api/settings` - Update settings
- `GET /test-simple/sms` - Test SMS

## 🤝 Support & Community

Need help? Have questions?

- 📺 [Watch tutorials on YouTube](https://www.youtube.com/@TizLionAI)
- 🐛 [Report issues](https://github.com/Tiz20lion/shopify-ng-sms-sender/issues)
- ⭐ [Star this repo](https://github.com/Tiz20lion/shopify-ng-sms-sender) if you find it useful!

## 📄 License

MIT License - feel free to use this for your projects!

---

<div align="center">

**Built with ❤️ for Nigerian Shopify Developers**

**Developed by [Tiz Lion AI](https://github.com/Tiz20lion)**

[YouTube](https://www.youtube.com/@TizLionAI) • [LinkedIn](https://www.linkedin.com/in/olajide-azeez-a2133a258) • [GitHub](https://github.com/Tiz20lion)

</div>
