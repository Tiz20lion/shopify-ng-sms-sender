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

    # Conditional content for authenticated shop users vs landing page
    status_banner_html = ""
    features_grid_html = ""
    landing_page_html = ""
    footer_html = ""
    header_html = ""
    
    if not shop:
        # Landing page for direct visitors
        landing_page_html = """
                <div class="landing-hero">
                    <div class="hero-content">
                        <h1 class="hero-title">Automate SMS Notifications for Your Shopify Store</h1>
                        <p class="hero-subtitle">Send instant order confirmations and fulfillment updates to your Nigerian customers using Termii's reliable SMS platform.</p>
                        <div class="hero-features">
                            <div class="hero-feature">
                                <svg class="hero-icon" viewBox="0 0 24 24">
                                    <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                                </svg>
                                <span>Instant Delivery</span>
                            </div>
                            <div class="hero-feature">
                                <svg class="hero-icon" viewBox="0 0 24 24">
                                    <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                                </svg>
                                <span>Nigeria Optimized</span>
                            </div>
                            <div class="hero-feature">
                                <svg class="hero-icon" viewBox="0 0 24 24">
                                    <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                                </svg>
                                <span>Easy Setup</span>
                            </div>
                        </div>
                        <a href="https://github.com/Tiz20lion/shopify-ng-sms-sender" target="_blank" rel="noopener noreferrer" class="get-started-btn hero-cta">
                            Get Started
                            <svg class="btn-arrow" viewBox="0 0 24 24" width="20" height="20">
                                <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </a>
                    </div>
                    
                    <div class="dashboard-preview">
                        <div class="preview-badge">Live Dashboard</div>
                        <video autoplay loop muted playsinline preload="auto" class="dashboard-image" poster="/attached_assets/dashboard-preview.png">
                            <source src="/attached_assets/lv_0_20251105133946_1762346574066.mp4" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                    </div>
                </div>
                
                <div class="benefits-section scroll-reveal">
                    <h2>Trusted by Top Nigerian Startups</h2>
                    <div class="logo-grid">
                        <div class="logo-cell">
                            <img src="https://res.cloudinary.com/termii-inc/image/upload/v1757823028/termii-new-website/2025%20website/k728pgu4seejcxrszbj3.svg" class="company-logo" alt="Company logo">
                        </div>
                        <div class="logo-cell">
                            <img src="https://res.cloudinary.com/termii-inc/image/upload/v1757823029/termii-new-website/2025%20website/uipur5zwqxu1svigdpuo.svg" class="company-logo" alt="Company logo">
                        </div>
                        <div class="logo-cell">
                            <img src="https://res.cloudinary.com/termii-inc/image/upload/v1757816523/termii-new-website/2025%20website/almjqolkafjopwsvae6n.svg" class="company-logo" alt="Company logo">
                        </div>
                        <div class="logo-cell">
                            <img src="https://res.cloudinary.com/termii-inc/image/upload/v1757823706/termii-new-website/2025%20website/mvnxsu6wbfjyb3mzh0un.svg" class="company-logo" alt="Company logo">
                        </div>
                        <div class="logo-cell">
                            <img src="https://res.cloudinary.com/termii-inc/image/upload/v1757823337/termii-new-website/2025%20website/nzjy0ixv3nbtw7yokrhf.svg" class="company-logo" alt="Company logo">
                        </div>
                        <div class="logo-cell">
                            <img src="https://res.cloudinary.com/termii-inc/image/upload/v1757823337/termii-new-website/2025%20website/p26wmqdlddwbeth2htor.svg" class="company-logo" alt="Company logo">
                        </div>
                    </div>
                </div>
                
                <div class="phone-mockup-section scroll-reveal">
                    <div class="section-content">
                        <div class="text-content">
                            <h2 class="section-title">Test SMS Instantly</h2>
                            <p class="section-description">Send test messages to verify your Termii integration is working perfectly before going live with customer notifications.</p>
                            <ul class="feature-list">
                                <li class="feature-item">
                                    <svg class="check-icon" viewBox="0 0 24 24">
                                        <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                                    </svg>
                                    <span>Instant delivery to Nigerian numbers</span>
                                </li>
                                <li class="feature-item">
                                    <svg class="check-icon" viewBox="0 0 24 24">
                                        <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                                    </svg>
                                    <span>Real-time message preview</span>
                                </li>
                                <li class="feature-item">
                                    <svg class="check-icon" viewBox="0 0 24 24">
                                        <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                                    </svg>
                                    <span>Automatic phone formatting</span>
                                </li>
                            </ul>
                        </div>
                        <div class="mockup-phone">
                            <div class="phone-display">
                                <div class="phone-camera"></div>
                                <video autoplay loop muted playsinline preload="auto" class="phone-video lazy-video" data-src="/attached_assets/Testing_page_Phone_mockup_compressed.mp4">
                                    <source data-src="/attached_assets/Testing_page_Phone_mockup_compressed.mp4" type="video/mp4">
                                </video>
                            </div>
                        </div>
                    </div>
                    <div class="section-cta">
                        <a href="https://github.com/Tiz20lion/shopify-ng-sms-sender" target="_blank" rel="noopener noreferrer" class="get-started-btn">
                            Get Started
                            <svg class="btn-arrow" viewBox="0 0 24 24" width="20" height="20">
                                <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </a>
                    </div>
                </div>
                
                <div class="phone-mockup-section scroll-reveal">
                    <div class="section-content">
                        <div class="mockup-phone">
                            <div class="phone-display">
                                <div class="phone-camera"></div>
                                <video autoplay loop muted playsinline preload="auto" class="phone-video lazy-video" data-src="/attached_assets/Settings_page_Phone_mockup_compressed.mp4">
                                    <source data-src="/attached_assets/Settings_page_Phone_mockup_compressed.mp4" type="video/mp4">
                                </video>
                            </div>
                        </div>
                        <div class="text-content">
                            <h2 class="section-title">Customize Your Messages</h2>
                            <p class="section-description">Personalize SMS templates for order confirmations and fulfillment updates with dynamic variables and your brand voice.</p>
                            <ul class="feature-list">
                                <li class="feature-item">
                                    <svg class="check-icon" viewBox="0 0 24 24">
                                        <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                                    </svg>
                                    <span>Dynamic variables (name, order #, total)</span>
                                </li>
                                <li class="feature-item">
                                    <svg class="check-icon" viewBox="0 0 24 24">
                                        <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                                    </svg>
                                    <span>Clickable variable tags</span>
                                </li>
                                <li class="feature-item">
                                    <svg class="check-icon" viewBox="0 0 24 24">
                                        <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                                    </svg>
                                    <span>Live character count</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="section-cta">
                        <a href="https://github.com/Tiz20lion/shopify-ng-sms-sender" target="_blank" rel="noopener noreferrer" class="get-started-btn">
                            Get Started
                            <svg class="btn-arrow" viewBox="0 0 24 24" width="20" height="20">
                                <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </a>
                    </div>
                </div>
                
                <div class="reviews-section scroll-reveal">
                    <h2>Here's what top companies are saying about Termii</h2>
                    <div class="reviews-track">
                        <div class="review-card">
                            <div class="stars">★★★★★</div>
                            <p class="review-text">We recently had the pleasure of using Termii, and I was thoroughly impressed! The OTP process was smooth and efficient, making it easy to get started and integrate. The team was responsive and maintained decent communication throughout, keeping us informed about progress.</p>
                            <div class="reviewer">
                                <div class="company">Afriex</div>
                                <div class="name">Abayomi</div>
                            </div>
                        </div>
                        <div class="review-card">
                            <div class="stars">★★★★★</div>
                            <p class="review-text">The experience has been great and it has helped us in business scalability. The prompt customer support and responses to our complaints and inquiries, has also made it easy for us to conduct our business efficiently.</p>
                            <div class="reviewer">
                                <div class="company">Indicina</div>
                                <div class="name">Eseoghene Onojafe</div>
                            </div>
                        </div>
                        <div class="review-card">
                            <div class="stars">★★★★★</div>
                            <p class="review-text">Termii Webtech Limited has proven to be more than just a service provider; it is a strategic partner in enabling Grooming Centre's mission of financial inclusion through technology. Their consistency in service delivery and responsiveness continues to support our goals.</p>
                            <div class="reviewer">
                                <div class="company">Grooming Centre</div>
                                <div class="name">Chinedu</div>
                            </div>
                        </div>
                        <div class="review-card">
                            <div class="stars">★★★★★</div>
                            <p class="review-text">Termii has been an exceptional CPaaS partner for our organization's SMS communication. Their dedicated support team consistently provides swift assistance and timely updates on any service interruptions, ensuring minimal downtime.</p>
                            <div class="reviewer">
                                <div class="company">Babban Gona</div>
                                <div class="name">Rehoboth</div>
                            </div>
                        </div>
                        <div class="review-card">
                            <div class="stars">★★★★★</div>
                            <p class="review-text">Crust MFB has been using Termii to send out campaigns, bulk SMS, and receive OTPs, and it's been such a great experience. From the start, I noticed how easy and convenient the platform is to use. Everything feels well organized and straightforward.</p>
                            <div class="reviewer">
                                <div class="company">CRUST MFB</div>
                                <div class="name">Jon Fitzgerald</div>
                            </div>
                        </div>
                        <div class="review-card">
                            <div class="stars">★★★★★</div>
                            <p class="review-text">We recently had the pleasure of using Termii, and I was thoroughly impressed! The OTP process was smooth and efficient, making it easy to get started and integrate. The team was responsive and maintained decent communication throughout, keeping us informed about progress.</p>
                            <div class="reviewer">
                                <div class="company">Afriex</div>
                                <div class="name">Abayomi</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="faq-section scroll-reveal">
                    <h2>Frequently Asked Questions</h2>
                    <div class="faq-container">
                        <div class="faq-item">
                            <button class="faq-question">
                                <span>How do I install this app on my Shopify store?</span>
                                <svg class="faq-icon" viewBox="0 0 24 24" width="20" height="20">
                                    <path d="M19 13H5v-2h14v2z" fill="currentColor"/>
                                </svg>
                            </button>
                            <div class="faq-answer">
                                <p>Clone the repository, set up your Termii API credentials and Shopify app credentials in the environment variables, then deploy the app. Full setup instructions are available in the README file.</p>
                            </div>
                        </div>
                        
                        <div class="faq-item">
                            <button class="faq-question">
                                <span>What SMS messages are sent automatically?</span>
                                <svg class="faq-icon" viewBox="0 0 24 24" width="20" height="20">
                                    <path d="M19 13H5v-2h14v2z" fill="currentColor"/>
                                </svg>
                            </button>
                            <div class="faq-answer">
                                <p>The app automatically sends two types of SMS: order confirmation when a new order is created, and fulfillment updates when an order is shipped. Both messages are fully customizable with dynamic variables.</p>
                            </div>
                        </div>
                        
                        <div class="faq-item">
                            <button class="faq-question">
                                <span>Does this work for Nigerian phone numbers only?</span>
                                <svg class="faq-icon" viewBox="0 0 24 24" width="20" height="20">
                                    <path d="M19 13H5v-2h14v2z" fill="currentColor"/>
                                </svg>
                            </button>
                            <div class="faq-answer">
                                <p>Yes, this app is optimized for Nigerian customers using Termii's reliable SMS platform. Termii provides excellent coverage and delivery rates for all Nigerian mobile networks.</p>
                            </div>
                        </div>
                        
                        <div class="faq-item">
                            <button class="faq-question">
                                <span>Can I customize the SMS templates?</span>
                                <svg class="faq-icon" viewBox="0 0 24 24" width="20" height="20">
                                    <path d="M19 13H5v-2h14v2z" fill="currentColor"/>
                                </svg>
                            </button>
                            <div class="faq-answer">
                                <p>Absolutely! You can customize both order confirmation and fulfillment SMS templates through the Settings page. Use dynamic variables like {{{{customer_name}}}}, {{{{order_number}}}}, and {{{{total_price}}}} to personalize your messages.</p>
                            </div>
                        </div>
                        
                        <div class="faq-item">
                            <button class="faq-question">
                                <span>How much does it cost to send SMS?</span>
                                <svg class="faq-icon" viewBox="0 0 24 24" width="20" height="20">
                                    <path d="M19 13H5v-2h14v2z" fill="currentColor"/>
                                </svg>
                            </button>
                            <div class="faq-answer">
                                <p>SMS costs are based on Termii's pricing for Nigerian numbers. You'll need a Termii account with credits. Check Termii's current pricing at termii.com for the most up-to-date rates.</p>
                            </div>
                        </div>
                        
                        <div class="faq-item">
                            <button class="faq-question">
                                <span>Is there a free trial or demo available?</span>
                                <svg class="faq-icon" viewBox="0 0 24 24" width="20" height="20">
                                    <path d="M19 13H5v-2h14v2z" fill="currentColor"/>
                                </svg>
                            </button>
                            <div class="faq-answer">
                                <p>The app itself is open-source and free to use. You can test SMS sending using the built-in Test page before going live. You'll only pay for SMS credits through your Termii account.</p>
                            </div>
                        </div>
                    </div>
                </div>
        """
    
    if shop:
        # Header section for authenticated store owners only
        header_html = """
            <div class="header">
                <h1>SMS Notifications for Shopify</h1>
                <div class="subtitle">Automate SMS notifications for your Nigerian customers. Send order confirmations and fulfillment updates using Termii's reliable SMS platform.</div>
            </div>
        """
        
        # Footer section for authenticated store owners only
        footer_html = """
                <div class="developer-cta">
                    <div class="developer-info">
                        <h3>Built with ❤️ for Nigerian Shopify Developers</h3>
                        <p>Developed by <strong>Tiz Lion AI</strong></p>
                    </div>
                    <div class="support-section">
                        <p class="support-text">Need help? Questions?</p>
                        <div class="support-icons">
                            <a href="https://github.com/Tiz20lion/shopify-ng-sms-sender/issues" target="_blank" class="support-icon" title="Report Issues">
                                <svg viewBox="0 0 24 24">
                                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                                </svg>
                                <span>Report</span>
                            </a>
                            <a href="https://www.youtube.com/@TizLionAI" target="_blank" class="support-icon" title="Watch Tutorials">
                                <svg viewBox="0 0 24 24">
                                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
                                </svg>
                                <span>Tutorials</span>
                            </a>
                            <a href="https://github.com/Tiz20lion/shopify-ng-sms-sender" target="_blank" class="support-icon" title="Star on GitHub">
                                <svg viewBox="0 0 24 24">
                                    <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                                </svg>
                                <span>Star</span>
                            </a>
                        </div>
                    </div>
                </div>
        """
        
        status_banner_html = f"""<div class="status-banner">
                    <svg class="icon secured-icon" viewBox="0 0 32 32">
                        <defs>
                            <clipPath id="checkClip">
                                <rect x="0" y="0" width="32" height="32"/>
                            </clipPath>
                        </defs>
                        
                        <!-- Outer shield circle -->
                        <circle cx="16" cy="16" r="15" 
                                fill="none" 
                                stroke="#1a1a1a" 
                                stroke-width="2" 
                                stroke-dasharray="94.2" 
                                stroke-dashoffset="94.2"
                                class="shield-circle"
                                transform="rotate(-90 16 16)"/>
                        
                        <!-- Inner security shield -->
                        <path d="M16 4 L24 8 L24 16 C24 22 16 26 16 26 C16 26 8 22 8 16 L8 8 L16 4 Z" 
                              fill="#1a1a1a" 
                              fill-opacity="0.05"
                              stroke="#1a1a1a" 
                              stroke-width="1.5"
                              class="security-shield"/>
                        
                        <!-- Animated checkmark -->
                        <g clip-path="url(#checkClip)">
                            <path d="M12 16 L15 19 L20 13" 
                                  fill="none" 
                                  stroke="#1a1a1a" 
                                  stroke-width="2.5" 
                                  stroke-linecap="round" 
                                  stroke-linejoin="round"
                                  stroke-dasharray="12"
                                  stroke-dashoffset="12"
                                  class="checkmark"/>
                        </g>
                        
                        <!-- Pulse effect -->
                        <circle cx="16" cy="16" r="15" 
                                fill="none" 
                                stroke="#1a1a1a" 
                                stroke-width="1" 
                                stroke-opacity="0.2"
                                class="pulse-ring"/>
                    </svg>
                    <div class="content">
                        <h3>App Successfully Connected</h3>
                        <p>Your Shopify app is running and ready to send SMS notifications to your customers.</p>
                    </div>
                </div>"""
        
        features_grid_html = f"""<div class="features-grid">
                    <div class="feature-card">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                        </svg>
                        <h3>SMS Testing</h3>
                        <p>Test your SMS configuration to ensure Termii integration is working correctly with Nigerian phone numbers.</p>
                        <a href="/test-simple/sms?shop={shop}" class="btn" id="testSmsLink">Test SMS Sender</a>
                    </div>

                    <div class="feature-card">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.44,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
                        </svg>
                        <h3>Configuration</h3>
                        <p>Set up your SMS templates for order confirmations and fulfillment notifications. Customize messages to match your brand.</p>
                        <a href="/admin/settings?shop={shop}" class="btn" id="settingsLink">Configure Settings</a>
                    </div>

                    <div class="feature-card">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,16.5L6.5,12L7.91,10.59L11,13.67L16.59,8.09L18,9.5L11,16.5Z"/>
                        </svg>
                        <h3>Automation</h3>
                        <p>Automatic SMS notifications are sent when orders are created and fulfilled. No manual intervention required.</p>
                        <a href="/admin/settings?shop={shop}" class="btn">View Settings</a>
                    </div>
                </div>"""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="referrer" content="no-referrer-when-downgrade">
        <title>SMS Notifications for Shopify</title>
        <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
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
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 0;
            }}

            /* Mobile-first header */
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
            .header .subtitle {{
                font-size: 0.9rem;
                color: #666;
                font-weight: 400;
                max-width: 100%;
                margin: 0 auto;
                line-height: 1.4;
            }}

            /* Mobile-first content */
            .content {{
                padding: 20px 16px;
                margin: 0 auto;
            }}

            /* Minimalist status section */
            .status-banner {{
                text-align: center;
                padding: 24px 16px;
                margin-bottom: 32px;
                background: transparent;
                border: none;
            }}
            .status-banner .icon {{
                width: 40px;
                height: 40px;
                margin: 0 auto 16px auto;
                display: block;
            }}
            
            /* Secured icon animations */
            .secured-icon .shield-circle {{
                animation: drawCircle 2s ease-out forwards;
                animation-delay: 0.3s;
            }}
            
            .secured-icon .security-shield {{
                opacity: 0;
                animation: fadeInShield 0.8s ease-out forwards;
                animation-delay: 1s;
            }}
            
            .secured-icon .checkmark {{
                animation: drawCheck 1.2s ease-out forwards;
                animation-delay: 1.5s;
            }}
            
            .secured-icon .pulse-ring {{
                animation: pulseRing 3s ease-in-out infinite;
                animation-delay: 2.5s;
            }}
            
            @keyframes drawCircle {{
                from {{
                    stroke-dashoffset: 94.2;
                }}
                to {{
                    stroke-dashoffset: 0;
                }}
            }}
            
            @keyframes fadeInShield {{
                from {{
                    opacity: 0;
                    transform: scale(0.8);
                }}
                to {{
                    opacity: 1;
                    transform: scale(1);
                }}
            }}
            
            @keyframes drawCheck {{
                from {{
                    stroke-dashoffset: 12;
                }}
                to {{
                    stroke-dashoffset: 0;
                }}
            }}
            
            @keyframes pulseRing {{
                0% {{
                    stroke-opacity: 0.3;
                    transform: scale(1);
                }}
                50% {{
                    stroke-opacity: 0.1;
                    transform: scale(1.1);
                }}
                100% {{
                    stroke-opacity: 0.3;
                    transform: scale(1);
                }}
            }}
            .status-banner .content {{
                text-align: center;
                max-width: 500px;
                margin: 0 auto;
            }}
            .status-banner h3 {{
                font-size: 1rem;
                font-weight: 600;
                margin-bottom: 6px;
                color: #1a1a1a;
                letter-spacing: -0.02em;
            }}
            .status-banner h3::after {{
                content: ' ✓';
                color: #1a1a1a;
                font-size: 0.85rem;
            }}
            .status-banner p {{
                color: #666;
                font-size: 0.8rem;
                line-height: 1.4;
                font-weight: 400;
            }}

            /* Mobile-first features grid - 2 columns on mobile */
            .features-grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 12px;
                margin-bottom: 24px;
            }}
            .feature-card {{
                background: white;
                border: 1px solid #e5e5e5;
                border-radius: 8px;
                padding: 16px;
                text-align: center;
                transition: all 0.2s ease;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .feature-card:hover {{
                transform: translateY(-1px);
                box-shadow: 0 3px 8px rgba(0,0,0,0.12);
                border-color: #1a1a1a;
            }}
            .feature-card .icon {{
                width: 32px;
                height: 32px;
                margin: 0 auto 10px;
                fill: #1a1a1a;
            }}
            .feature-card h3 {{
                font-size: 0.95rem;
                font-weight: 600;
                margin-bottom: 8px;
                color: #1a1a1a;
            }}
            .feature-card p {{
                color: #666;
                font-size: 0.75rem;
                line-height: 1.4;
                margin-bottom: 12px;
            }}
            .feature-card .btn {{
                display: inline-block;
                padding: 8px 16px;
                background: #1a1a1a;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 500;
                font-size: 0.75rem;
                transition: all 0.2s ease;
            }}
            .feature-card .btn:hover {{
                background: #333;
                transform: translateY(-1px);
            }}

            /* Mobile-first stats section - 2 columns */
            .stats-section {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-bottom: 24px;
            }}
            .stat-item {{
                background: white;
                border: 1px solid #e5e5e5;
                border-radius: 8px;
                padding: 14px;
                text-align: center;
                transition: all 0.2s ease;
            }}
            .stat-item:hover {{
                transform: translateY(-1px);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-color: #1a1a1a;
            }}
            .stat-item .icon {{
                width: 24px;
                height: 24px;
                margin: 0 auto 8px;
                fill: #1a1a1a;
            }}
            .stat-item .label {{
                font-size: 0.75rem;
                color: #666;
                font-weight: 500;
            }}

            /* Mobile-first developer CTA */
            .developer-cta {{
                background: #1a1a1a;
                color: white;
                border-radius: 6px;
                padding: 16px 12px;
                text-align: center;
                margin-bottom: 24px;
                border: 1px solid #333;
            }}
            .developer-info h3 {{
                font-size: 0.9rem;
                font-weight: 600;
                margin-bottom: 4px;
                color: white;
                line-height: 1.2;
            }}
            .developer-info p {{
                font-size: 0.75rem;
                margin-bottom: 12px;
                opacity: 0.95;
                line-height: 1.3;
            }}

            /* Support section - minimal design */
            .support-section {{
                padding-top: 12px;
                margin-top: 12px;
            }}
            .support-text {{
                font-size: 0.75rem;
                margin-bottom: 12px;
                color: #999;
                text-align: center;
            }}
            .support-icons {{
                display: flex;
                justify-content: center;
                gap: 20px;
            }}
            .support-icon {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 4px;
                text-decoration: none;
                transition: all 0.3s ease;
                -webkit-tap-highlight-color: transparent;
            }}
            .support-icon svg {{
                width: 28px;
                height: 28px;
                fill: white;
                transition: all 0.3s ease;
            }}
            .support-icon span {{
                font-size: 0.65rem;
                color: #999;
                transition: all 0.3s ease;
            }}
            .support-icon:hover svg {{
                fill: #999;
                transform: scale(1.1);
            }}
            .support-icon:hover span {{
                color: white;
            }}
            .support-icon:active {{
                transform: scale(0.95);
            }}

            /* Tablet styles - Keep compact mobile design */
            @media (min-width: 480px) {{
                .content {{
                    padding: 24px 20px;
                }}
                .header {{
                    padding: 32px 20px;
                }}
                .header h1 {{
                    font-size: 1.5rem;
                }}
                .header .subtitle {{
                    font-size: 0.9rem;
                }}
                .status-banner {{
                    padding: 20px 16px;
                    margin-bottom: 24px;
                }}
                .status-banner .icon {{
                    width: 36px;
                    height: 36px;
                    margin-bottom: 12px;
                }}
                .status-banner h3 {{
                    font-size: 1rem;
                }}
                .status-banner p {{
                    font-size: 0.8rem;
                }}
                .features-grid {{
                    grid-template-columns: repeat(2, 1fr);
                    gap: 12px;
                }}
                .stats-section {{
                    grid-template-columns: repeat(4, 1fr);
                    gap: 10px;
                }}
                .developer-cta {{
                    padding: 20px 16px;
                }}
                .support-icons {{
                    gap: 28px;
                }}
                .support-icon svg {{
                    width: 32px;
                    height: 32px;
                }}
            }}

            /* Desktop styles - Maintain compact design */
            @media (min-width: 768px) {{
                .content {{
                    padding: 32px 24px;
                }}
                .header {{
                    padding: 40px 24px;
                }}
                .header h1 {{
                    font-size: 1.75rem;
                }}
                .status-banner {{
                    padding: 24px 20px;
                    margin-bottom: 28px;
                }}
                .status-banner .icon {{
                    width: 40px;
                    height: 40px;
                    margin-bottom: 14px;
                }}
                .status-banner h3 {{
                    font-size: 1.1rem;
                    margin-bottom: 8px;
                }}
                .status-banner p {{
                    font-size: 0.85rem;
                }}
                .features-grid {{
                    grid-template-columns: repeat(3, 1fr);
                    gap: 16px;
                    margin-bottom: 28px;
                }}
                .stats-section {{
                    grid-template-columns: repeat(4, 1fr);
                    gap: 12px;
                    margin-bottom: 28px;
                }}
                .developer-cta {{
                    padding: 24px 20px;
                    margin-bottom: 32px;
                }}
                .developer-info h3 {{
                    font-size: 1rem;
                }}
                .developer-info p {{
                    font-size: 0.8rem;
                    margin-bottom: 16px;
                }}
                .support-icons {{
                    gap: 36px;
                }}
                .support-icon svg {{
                    width: 36px;
                    height: 36px;
                }}
                .support-icon span {{
                    font-size: 0.7rem;
                }}
            }}

            /* Large desktop styles */
            @media (min-width: 1024px) {{
                .header .subtitle {{
                    max-width: 600px;
                }}
            }}

            /* Touch-friendly improvements */
            @media (hover: none) and (pointer: coarse) {{
                .feature-card .btn,
                .developer-link,
                .support-link {{
                    min-height: 48px;
                }}
            }}

            /* High DPI improvements */
            @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {{
                .status-banner,
                .feature-card,
                .stat-item,
                .developer-cta {{
                    border-width: 0.5px;
                }}
            }}

            /* Landing Page Styles */
            .landing-hero {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 2rem;
                margin-bottom: 3rem;
                align-items: center;
            }}

            .hero-content {{
                opacity: 0;
                animation: fadeInUp 0.8s ease-out 0.2s forwards;
            }}

            .hero-title {{
                font-size: 1.75rem;
                font-weight: 700;
                line-height: 1.2;
                margin-bottom: 0.75rem;
                color: #1a1a1a;
            }}

            .hero-subtitle {{
                font-size: 0.95rem;
                line-height: 1.6;
                color: #666;
                margin-bottom: 1.5rem;
            }}

            .hero-features {{
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }}

            .hero-feature {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.85rem;
                color: #1a1a1a;
            }}

            .hero-icon {{
                width: 18px;
                height: 18px;
                fill: #1a1a1a;
                flex-shrink: 0;
            }}
            
            /* Get Started Button */
            .get-started-btn {{
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.75rem 1.5rem;
                background: #1a1a1a;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 0.875rem;
                transition: all 0.3s ease;
                border: 2px solid #1a1a1a;
                margin-top: 1.25rem;
            }}
            
            .get-started-btn:hover {{
                background: white;
                color: #1a1a1a;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }}
            
            .get-started-btn .btn-arrow {{
                transition: transform 0.3s ease;
                width: 18px;
                height: 18px;
            }}
            
            .get-started-btn:hover .btn-arrow {{
                transform: translateX(4px);
            }}
            
            .section-cta {{
                display: flex;
                justify-content: center;
                margin-top: 1.5rem;
                padding: 0.75rem 0;
            }}
            
            /* FAQ Section */
            .faq-section {{
                max-width: 700px;
                margin: 3rem auto 4rem;
                padding: 0 1rem;
            }}
            
            .faq-section h2 {{
                font-size: 1.5rem;
                font-weight: 700;
                text-align: center;
                margin-bottom: 2rem;
                color: #1a1a1a;
            }}
            
            .faq-container {{
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
            }}
            
            .faq-item {{
                border: 1px solid #e5e5e5;
                border-radius: 8px;
                overflow: hidden;
                background: white;
                transition: all 0.3s ease;
            }}
            
            .faq-item:hover {{
                border-color: #1a1a1a;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            }}
            
            .faq-question {{
                width: 100%;
                padding: 1rem 1.25rem;
                background: white;
                border: none;
                text-align: left;
                font-size: 0.95rem;
                font-weight: 600;
                color: #1a1a1a;
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 1rem;
                transition: background 0.2s ease;
            }}
            
            .faq-question:hover {{
                background: #f9f9f9;
            }}
            
            .faq-question span {{
                flex: 1;
            }}
            
            .faq-icon {{
                flex-shrink: 0;
                transition: transform 0.3s ease;
            }}
            
            .faq-item.active .faq-icon {{
                transform: rotate(180deg);
            }}
            
            .faq-answer {{
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.3s ease, padding 0.3s ease;
            }}
            
            .faq-item.active .faq-answer {{
                max-height: 500px;
                padding: 0 1.25rem 1.25rem;
            }}
            
            .faq-answer p {{
                margin: 0;
                font-size: 0.9rem;
                line-height: 1.6;
                color: #666;
            }}

            .dashboard-preview {{
                position: relative;
                opacity: 0;
                transform: translateX(50px) rotateY(-5deg);
                animation: flyIn 1s ease-out 0.5s forwards;
                perspective: 1000px;
            }}

            .preview-badge {{
                position: absolute;
                top: -12px;
                left: 50%;
                transform: translateX(-50%);
                background: #1a1a1a;
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.7rem;
                font-weight: 600;
                z-index: 10;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}

            .dashboard-image {{
                width: 100%;
                height: auto;
                border-radius: 12px;
                border: 1px solid #e5e5e5;
                box-shadow: 0 20px 60px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                display: block;
                object-fit: cover;
            }}

            .dashboard-image:hover {{
                transform: translateY(-5px);
                box-shadow: 0 25px 70px rgba(0,0,0,0.15);
            }}
            
            video.dashboard-image {{
                cursor: default;
            }}
            
            video.dashboard-image::-webkit-media-controls {{
                display: none !important;
            }}
            
            video.dashboard-image::-webkit-media-controls-enclosure {{
                display: none !important;
            }}
            
            video.dashboard-image::-webkit-media-controls-panel {{
                display: none !important;
            }}

            .benefits-section {{
                margin-top: 3rem;
            }}
            
            .benefits-section.scroll-reveal {{
                opacity: 0;
                transform: translateY(50px);
            }}
            
            .benefits-section.scroll-reveal.revealed {{
                opacity: 1;
                transform: translateY(0);
            }}

            .benefits-section h2 {{
                font-size: 1.25rem;
                font-weight: 700;
                text-align: center;
                margin-bottom: 1.5rem;
                color: #1a1a1a;
            }}

            .logo-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 0;
                width: 100%;
            }}

            .logo-cell {{
                border: 0.8px solid rgba(229, 229, 229, 0.8);
                padding: 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 80px;
                background: white;
                transition: all 0.3s ease;
            }}

            .logo-cell:hover {{
                background: rgba(0, 0, 0, 0.02);
                border-color: rgba(26, 26, 26, 0.2);
            }}

            .company-logo {{
                max-height: 48px;
                max-width: 100%;
                object-fit: contain;
                filter: grayscale(100%) opacity(0.7);
                transition: all 0.3s ease;
            }}

            .logo-cell:hover .company-logo {{
                filter: grayscale(0%) opacity(1);
            }}
            
            /* Reviews Section */
            .reviews-section {{
                margin: 4rem 0;
                padding: 2rem 0;
                overflow: hidden;
            }}
            
            .reviews-section h2 {{
                font-size: 1.5rem;
                font-weight: 700;
                text-align: center;
                margin-bottom: 2rem;
                color: #1a1a1a;
            }}
            
            .reviews-track {{
                display: flex;
                gap: 1.5rem;
                animation: scrollLeft 40s linear infinite;
                width: max-content;
            }}
            
            .reviews-track:hover {{
                animation-play-state: paused;
            }}
            
            .review-card {{
                background: #fff;
                border: 1px solid #e5e5e5;
                border-radius: 8px;
                padding: 1.5rem;
                min-width: 350px;
                max-width: 350px;
                flex-shrink: 0;
                transition: all 0.3s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }}
            
            .review-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.1);
                border-color: #d4d4d4;
            }}
            
            .stars {{
                color: #1a1a1a;
                font-size: 1rem;
                margin-bottom: 1rem;
                letter-spacing: 2px;
            }}
            
            .review-text {{
                font-size: 0.9rem;
                line-height: 1.6;
                color: #4a4a4a;
                margin-bottom: 1rem;
                min-height: 140px;
            }}
            
            .reviewer {{
                border-top: 1px solid #f0f0f0;
                padding-top: 1rem;
            }}
            
            .company {{
                font-weight: 700;
                font-size: 0.95rem;
                color: #1a1a1a;
                margin-bottom: 0.25rem;
            }}
            
            .name {{
                font-size: 0.85rem;
                color: #666;
            }}
            
            @keyframes scrollLeft {{
                0% {{
                    transform: translateX(0);
                }}
                100% {{
                    transform: translateX(-50%);
                }}
            }}

            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            @keyframes flyIn {{
                0% {{
                    opacity: 0;
                    transform: translateX(50px) rotateY(-15deg) scale(0.95);
                }}
                60% {{
                    transform: translateX(-5px) rotateY(2deg) scale(1.01);
                }}
                100% {{
                    opacity: 1;
                    transform: translateX(0) rotateY(0) scale(1);
                }}
            }}

            /* Phone Mockup Section */
            .phone-mockup-section {{
                margin-top: 2rem;
                padding: 1.5rem 0;
                background: linear-gradient(to bottom, transparent, rgba(0,0,0,0.02), transparent);
            }}
            
            .section-content {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 1.5rem;
                align-items: center;
                justify-items: center;
            }}
            
            .text-content {{
                text-align: center;
            }}
            
            .section-title {{
                font-size: 1.4rem;
                font-weight: 700;
                margin-bottom: 0.6rem;
                color: #1a1a1a;
                letter-spacing: -0.02em;
            }}
            
            .section-description {{
                font-size: 0.85rem;
                color: #666;
                line-height: 1.5;
                margin-bottom: 1rem;
            }}
            
            .feature-list {{
                list-style: none;
                padding: 0;
                margin: 0;
                display: inline-block;
                text-align: left;
            }}
            
            .feature-item {{
                display: flex;
                align-items: center;
                gap: 0.6rem;
                margin-bottom: 0.5rem;
                font-size: 0.8rem;
                color: #1a1a1a;
            }}
            
            .check-icon {{
                width: 16px;
                height: 16px;
                fill: #1a1a1a;
                flex-shrink: 0;
            }}
            
            /* Phone Mockup - Samsung S25 Ultra Style with Realistic Angled Bezel */
            .mockup-phone {{
                width: 220px;
                height: 450px;
                position: relative;
                background: linear-gradient(135deg, #c8c8c8 0%, #a0a0a0 100%);
                border-radius: 28px;
                padding: 8px;
                box-shadow: 
                    inset 0 3px 6px rgba(255,255,255,0.6),
                    inset 0 -3px 6px rgba(0,0,0,0.5),
                    0 15px 45px rgba(0,0,0,0.35);
                transition: all 0.4s ease;
            }}
            
            .mockup-phone::before {{
                content: '';
                position: absolute;
                top: 5px;
                left: 5px;
                right: 5px;
                bottom: 5px;
                background: linear-gradient(135deg, #2a2a2a 0%, #0a0a0a 100%);
                border-radius: 23px;
                box-shadow: 
                    inset 0 2px 8px rgba(0,0,0,0.7),
                    inset 0 -1px 4px rgba(255,255,255,0.1);
                z-index: 0;
            }}
            
            .mockup-phone:hover {{
                transform: translateY(-8px) scale(1.02);
                box-shadow: 
                    inset 0 3px 6px rgba(255,255,255,0.6),
                    inset 0 -3px 6px rgba(0,0,0,0.5),
                    0 20px 60px rgba(0,0,0,0.45);
            }}
            
            .phone-display {{
                position: relative;
                width: calc(100% - 10px);
                height: calc(100% - 10px);
                margin: 5px;
                background: #fff;
                border-radius: 18px;
                overflow: hidden;
                z-index: 1;
                box-shadow: 
                    0 0 0 1px rgba(0,0,0,0.1),
                    inset 0 1px 2px rgba(0,0,0,0.05);
            }}
            
            .phone-camera {{
                position: absolute;
                top: 12px;
                left: 50%;
                transform: translateX(-50%);
                background: radial-gradient(circle at 30% 30%, #5a6b7d, #2d3748);
                height: 8px;
                width: 8px;
                border-radius: 50%;
                box-shadow: 
                    inset 0 1px 3px rgba(0,0,0,0.7),
                    0 0 0 1px rgba(0,0,0,0.3),
                    0 1px 2px rgba(0,0,0,0.3);
                z-index: 10;
            }}
            
            .phone-video {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}
            
            /* Loading state for lazy videos */
            .lazy-video {{
                background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            }}
            
            .lazy-video::after {{
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 40px;
                height: 40px;
                border: 3px solid #ddd;
                border-top-color: #1a1a1a;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
            }}
            
            @keyframes spin {{
                to {{ transform: translate(-50%, -50%) rotate(360deg); }}
            }}
            
            /* Scroll Reveal Animation */
            .scroll-reveal {{
                opacity: 0;
                transform: translateY(50px);
                transition: opacity 0.8s ease, transform 0.8s ease;
            }}
            
            .scroll-reveal.revealed {{
                opacity: 1;
                transform: translateY(0);
            }}

            /* Mobile-first responsive design */
            @media (max-width: 767px) {{
                .landing-hero {{
                    padding: 2rem 0 1.5rem;
                    gap: 2rem;
                }}
                
                .hero-title {{
                    font-size: 1.5rem;
                    line-height: 1.3;
                    margin-bottom: 0.75rem;
                }}
                
                .hero-subtitle {{
                    font-size: 0.875rem;
                    line-height: 1.5;
                    margin-bottom: 1.25rem;
                }}
                
                .hero-features {{
                    gap: 0.6rem;
                }}
                
                .hero-feature {{
                    font-size: 0.8rem;
                }}
                
                .hero-icon {{
                    width: 16px;
                    height: 16px;
                }}
                
                .hero-cta {{
                    margin-top: 1.25rem;
                }}
                
                .dashboard-preview {{
                    margin-top: 0.5rem;
                }}
                
                .preview-badge {{
                    font-size: 0.65rem;
                    padding: 0.2rem 0.6rem;
                }}
                
                .dashboard-image {{
                    border-radius: 8px;
                }}
                
                .phone-mockup-section {{
                    padding: 1.5rem 0;
                }}
                
                .section-content {{
                    gap: 1.5rem;
                    align-items: center;
                    justify-content: center;
                }}
                
                .mockup-phone {{
                    width: 180px;
                    height: 370px;
                    padding: 6px;
                    border-radius: 24px;
                    margin: 0 auto;
                }}
                
                .mockup-phone::before {{
                    top: 3px;
                    left: 3px;
                    right: 3px;
                    bottom: 3px;
                    border-radius: 21px;
                }}
                
                .phone-display {{
                    width: calc(100% - 8px);
                    height: calc(100% - 8px);
                    margin: 4px;
                    border-radius: 16px;
                }}
                
                .phone-camera {{
                    top: 10px;
                    height: 6px;
                    width: 6px;
                }}
                
                .section-title {{
                    font-size: 1.25rem;
                }}
                
                .section-description {{
                    font-size: 0.9rem;
                }}
                
                .feature-list {{
                    gap: 0.5rem;
                }}
                
                .feature-item {{
                    font-size: 0.85rem;
                }}
                
                .benefits-section {{
                    margin: 2rem 0;
                    padding: 1rem 0;
                }}
                
                .benefits-section h2 {{
                    font-size: 1.25rem;
                    margin-bottom: 1.5rem;
                }}
                
                .logo-cell {{
                    padding: 0.75rem 0.5rem;
                    min-height: 70px;
                }}
                
                .company-logo {{
                    max-height: 36px;
                }}
                
                .reviews-section {{
                    margin: 2rem 0;
                    padding: 1rem 0;
                }}
                
                .reviews-section h2 {{
                    font-size: 1.3rem;
                    margin-bottom: 1.5rem;
                }}
                
                .reviews-track {{
                    gap: 1rem;
                }}
                
                .review-card {{
                    min-width: 260px;
                    max-width: 260px;
                    padding: 1rem;
                }}
                
                .review-text {{
                    font-size: 0.85rem;
                    min-height: 110px;
                }}
                
                .stars {{
                    font-size: 0.9rem;
                    margin-bottom: 0.75rem;
                }}
                
                .company {{
                    font-size: 0.9rem;
                }}
                
                .name {{
                    font-size: 0.8rem;
                }}
                
                .get-started-btn {{
                    padding: 0.65rem 1.25rem;
                    font-size: 0.8rem;
                    margin-top: 1rem;
                    gap: 0.35rem;
                }}
                
                .get-started-btn .btn-arrow {{
                    width: 16px;
                    height: 16px;
                }}
                
                .section-cta {{
                    margin-top: 1.25rem;
                    padding: 0.5rem 0;
                }}
                
                .faq-section {{
                    margin: 2rem auto 3rem;
                    padding: 0 1rem;
                }}
                
                .faq-section h2 {{
                    font-size: 1.3rem;
                    margin-bottom: 1.5rem;
                }}
                
                .faq-container {{
                    gap: 0.6rem;
                }}
                
                .faq-question {{
                    padding: 0.875rem 1rem;
                    font-size: 0.875rem;
                }}
                
                .faq-answer p {{
                    font-size: 0.85rem;
                }}
            }}

            /* Tablet and up */
            @media (min-width: 768px) {{
                .landing-hero {{
                    grid-template-columns: 1fr 1fr;
                    gap: 3rem;
                }}

                .hero-title {{
                    font-size: 2.25rem;
                }}

                .hero-subtitle {{
                    font-size: 1.05rem;
                }}

                .logo-grid {{
                    grid-template-columns: repeat(3, 1fr);
                }}
                
                .section-content {{
                    grid-template-columns: 1fr 1fr;
                    gap: 2.5rem;
                }}
                
                .text-content {{
                    text-align: left;
                }}
                
                .section-title {{
                    font-size: 1.6rem;
                }}
            }}

            /* Desktop */
            @media (min-width: 1024px) {{
                .hero-title {{
                    font-size: 2.5rem;
                }}
                
                .section-title {{
                    font-size: 1.75rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {header_html}

            <div class="content">
                {landing_page_html}
                
                {status_banner_html}

                {features_grid_html}

                <div class="stats-section">
                    <div class="stat-item">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M12,2C13.1,2 14,2.9 14,4C14,5.1 13.1,6 12,6C10.9,6 10,5.1 10,4C10,2.9 10.9,2 12,2M21,9V7L15,1H5C3.89,1 3,1.89 3,3V21A2,2 0 0,0 5,23H19A2,2 0 0,0 21,21V9M19,9H14V4H19V9Z"/>
                        </svg>
                        <div class="label">Ready to Deploy</div>
                    </div>
                    <div class="stat-item">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M13,9H18.5L13,3.5V9M6,2H14L20,8V20A2,2 0 0,1 18,22H6C4.89,22 4,21.1 4,20V4C4,2.89 4.89,2 6,2M15,18V16H6V18H15M18,14V12H6V14H18Z"/>
                        </svg>
                        <div class="label">Instant Notifications</div>
                    </div>
                    <div class="stat-item">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z"/>
                        </svg>
                        <div class="label">Nigeria Optimized</div>
                    </div>
                    <div class="stat-item">
                        <svg class="icon" viewBox="0 0 24 24">
                            <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,7C13.4,7 14.8,8.6 14.8,10V11.5C15.4,11.5 16,12.4 16,13V16C16,17.4 15.4,18 14.8,18H9.2C8.6,18 8,17.4 8,16V13C8,12.4 8.6,11.5 9.2,11.5V10C9.2,8.6 10.6,7 12,7M12,8.2C11.2,8.2 10.5,8.7 10.5,10V11.5H13.5V10C13.5,8.7 12.8,8.2 12,8.2Z"/>
                        </svg>
                        <div class="label">Secure & Reliable</div>
                    </div>
                </div>

                {footer_html}
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

                console.log('Home page - detected shop:', shop);

                // Save shop to localStorage for future use
                if (shop && shop !== '' && shop !== 'null') {{
                    try {{
                        localStorage.setItem('shopify_shop_domain', shop);
                    }} catch (e) {{
                        console.warn('Could not save to localStorage:', e);
                    }}
                }}

                const settingsLinks = [
                    document.getElementById('settingsLink')
                ];
                const testSmsLinks = [
                    document.getElementById('testSmsLink')
                ];

                // Get host parameter from current URL
                const host = urlParams.get('host');

                if (shop && shop !== '' && shop !== 'null') {{
                    settingsLinks.forEach(link => {{
                        if (link) {{
                            const baseUrl = link.getAttribute('href').split('?')[0];
                            let settingsUrl = `${{baseUrl}}?shop=${{encodeURIComponent(shop)}}`;
                            if (host) {{
                                settingsUrl += `&host=${{encodeURIComponent(host)}}`;
                            }}
                            link.href = settingsUrl;
                        }}
                    }});

                    testSmsLinks.forEach(link => {{
                        if (link) {{
                            const baseUrl = link.getAttribute('href').split('?')[0];
                            link.href = `${{baseUrl}}?shop=${{shop}}`;
                        }}
                    }});
                }} else {{
                    console.warn('Shop not found, links may not work');
                }}
            }})();

            // Scroll Reveal Animation using Intersection Observer
            (function() {{
                const revealElements = document.querySelectorAll('.scroll-reveal');
                
                if ('IntersectionObserver' in window) {{
                    const observer = new IntersectionObserver((entries) => {{
                        entries.forEach(entry => {{
                            if (entry.isIntersecting) {{
                                entry.target.classList.add('revealed');
                                observer.unobserve(entry.target);
                            }}
                        }});
                    }}, {{
                        threshold: 0.15,
                        rootMargin: '0px 0px -50px 0px'
                    }});
                    
                    revealElements.forEach(element => {{
                        observer.observe(element);
                    }});
                }} else {{
                    // Fallback for browsers that don't support Intersection Observer
                    revealElements.forEach(element => {{
                        element.classList.add('revealed');
                    }});
                }}
            }})();

            // Optimized Lazy Video Loading - Start loading videos BEFORE they come into view
            (function() {{
                const lazyVideos = document.querySelectorAll('.lazy-video');
                
                if ('IntersectionObserver' in window) {{
                    const videoObserver = new IntersectionObserver((entries) => {{
                        entries.forEach(entry => {{
                            if (entry.isIntersecting) {{
                                const video = entry.target;
                                const source = video.querySelector('source');
                                
                                // Load video source
                                if (source && source.dataset.src) {{
                                    source.src = source.dataset.src;
                                    video.load();
                                    
                                    // Try to play when loaded
                                    video.addEventListener('loadeddata', () => {{
                                        video.play().catch(e => console.log('Autoplay prevented:', e));
                                    }});
                                }}
                                
                                // Remove lazy class and stop observing
                                video.classList.remove('lazy-video');
                                videoObserver.unobserve(video);
                            }}
                        }});
                    }}, {{
                        // Start loading 800px BEFORE video comes into view
                        rootMargin: '800px 0px 800px 0px',
                        threshold: 0
                    }});
                    
                    lazyVideos.forEach(video => {{
                        videoObserver.observe(video);
                    }});
                }} else {{
                    // Fallback: load all videos immediately
                    lazyVideos.forEach(video => {{
                        const source = video.querySelector('source');
                        if (source && source.dataset.src) {{
                            source.src = source.dataset.src;
                            video.load();
                        }}
                    }});
                }}
            }})();
            
            // FAQ Accordion
            (function() {{
                const faqItems = document.querySelectorAll('.faq-item');
                
                faqItems.forEach(item => {{
                    const question = item.querySelector('.faq-question');
                    
                    question.addEventListener('click', () => {{
                        // Close other open items
                        faqItems.forEach(otherItem => {{
                            if (otherItem !== item && otherItem.classList.contains('active')) {{
                                otherItem.classList.remove('active');
                            }}
                        }});
                        
                        // Toggle current item
                        item.classList.toggle('active');
                    }});
                }});
            }})();
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