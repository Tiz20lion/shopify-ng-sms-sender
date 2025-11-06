# Shopify NG SMS Sender

## Overview

This Shopify app automates sending SMS notifications to Nigerian customers via the Termii API. It provides order confirmation and fulfillment updates, aiming to enhance customer communication for Shopify merchants in Nigeria.

## User Preferences

None documented yet.

## System Architecture

The application is built with FastAPI (Python 3.11) and designed as an embedded Shopify app. It integrates with the Termii API for SMS delivery and Shopify's API for order and fulfillment events.

**UI/UX Decisions:**
- **Modern SaaS Landing Page:** Features a hero section with an auto-playing dashboard video, mobile responsiveness, `fadeInUp` and `flyIn` CSS animations, a "Trusted by Top Nigerian Startups" section with grayscale logos that colorize on hover, and static file serving for assets. Includes compact, mobile-optimized "Get Started" CTA buttons after key sections (hero section and both phone mockup sections) that link to the GitHub repository. Hero section is fully optimized for mobile with reduced font sizes, tighter spacing, and compact button layout.
- **Dynamic Header/Footer:** The header is conditionally rendered for authenticated users, and the developer footer is visible only for authenticated store owners.
- **SMS Test Page & Settings Page Redesign:** Both pages adhere to a black/white minimalist brand theme with a consistent grid background. The settings page features a black header with white text, SVG icons, box shadows for depth, enhanced focus states, auto-scroll on template save, clickable variable tags, backdrop blur effects, and slide-in animations for messages.
- **Scroll Reveal Animations:** Utilizes Intersection Observer API for smooth, scroll-triggered animations (fade in and slide up) with a 0.8s ease transition.
- **Company Logo Grid:** "Trusted by Top Nigerian Startups" section displays 6 company logos (Paystack, ByteDance, Moniepoint, Piggyvest, Branch, Chipper) in a 2-column grid on mobile and 3-column grid on desktop. Features grayscale-to-color hover effect. Fully responsive with optimized mobile sizing (36px logo height, compact 0.75rem padding on mobile vs 48px height and 1rem padding on desktop).
- **Phone Mockup Sections:** Compact, interactive Samsung S25 Ultra style mockups showcase the Testing and Settings pages with auto-playing, optimized video demos. These mockups feature dual-layer angled bezels with gradients and inset shadows for realistic depth, and hover animations. Fully responsive with mobile-optimized sizing (180x370px on mobile, 220x450px on desktop).
- **Reviews Section:** "Here's what top companies are saying about Termii" - features animated testimonials from companies like Afriex, Indicina, Grooming Centre, Babban Gona, and CRUST MFB. Cards scroll horizontally in a continuous infinite loop (40s animation). Minimalist card design with 5-star ratings, review text, company name, and reviewer name. Animation pauses on hover for better readability. Fully responsive with smaller cards on mobile (280px) and larger on desktop (350px).
- **FAQ Section:** Minimalist accordion-style FAQ section with 6 common questions about the app (installation, features, pricing, customization). Mobile-first design with black and white branding, smooth expand/collapse animations, hover effects, and one-at-a-time accordion behavior. Fully responsive with optimized spacing and typography for mobile devices.
- **Embedded App Design:** The app loads within an iframe in the Shopify admin interface, eliminating the need for a custom login system as Shopify handles authentication via its OAuth flow.

**Technical Implementations:**
- **FastAPI Backend:** Provides API endpoints for Shopify webhooks, settings management, and SMS testing.
- **SMS Service Integration:** Uses `termii.py` for Termii API interactions.
- **Shopify Integration:** `shopify.py` handles Shopify API client interactions, and `webhook_verifier.py` ensures HMAC verification for incoming webhooks.
- **Security:** Implements shop whitelist security via the `ALLOWED_SHOPS` environment variable to restrict access to admin features to authorized Shopify stores. All webhooks are secured with HMAC verification.
- **Environment Management:** Utilizes `python-dotenv` for managing environment variables.
- **Port Configuration:** Configured to run on port 8000 or any.
- **Dynamic SMS Templates:** Supports variables like `{{customer_name}}`, `{{order_number}}`, and `{{total_price}}`.
- **Tawk.to Live Chat:** Integrated on all pages (landing page, settings page, test SMS page, success/error pages) for customer support before the closing `</body>` tag.

**Feature Specifications:**
- **Order Confirmation SMS:** Triggered by `orders/create` webhook.
- **Fulfillment Update SMS:** Triggered by `orders/fulfilled` webhook.
- **SMS Testing Page:** Allows sending test SMS messages.
- **Settings Page:** For configuring SMS templates and other app settings.

## External Dependencies

- **Shopify API:** For order, customer, and fulfillment data, and webhook integration.
- **Termii API:** For sending SMS notifications to Nigerian phone numbers.
- **Uvicorn:** ASGI server for FastAPI.
- **httpx:** Asynchronous HTTP client.
- **python-dotenv:** For loading environment variables.
- **pydantic:** For data validation and settings management.