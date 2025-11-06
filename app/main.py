import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.routes import auth, webhooks, admin, admin_ui, home, test_simple

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Shopify Termii SMS Notifications",
    description="Send SMS notifications to customers via Termii when orders are created or fulfilled",
    version="1.0.0"
)

# Mount static files directory for images
app.mount("/attached_assets", StaticFiles(directory="attached_assets"), name="attached_assets")

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)


# Middleware to add headers for embedded iframe and bypass ngrok warning
@app.middleware("http")
async def add_embed_headers(request, call_next):
    # Log all requests for debugging
    logger.info(f"{request.method} {request.url.path} - Query: {dict(request.query_params)}")
    
    # Set header to skip ngrok browser warning (for free ngrok tier)
    # This header must be sent FROM the client, but we'll also set it here for server-side requests
    # For client-side, we need to ensure requests include this header
    
    response = await call_next(request)
    # Allow embedding in iframes (required for embedded Shopify apps)
    # Remove X-Frame-Options if it exists (defaults to DENY which blocks iframes)
    if "X-Frame-Options" in response.headers:
        del response.headers["X-Frame-Options"]
    
    # Get shop domain from query params or headers
    shop = request.query_params.get("shop", "")
    if not shop:
        # Try to extract from referer or other headers
        referer = request.headers.get("referer", "")
        if ".myshopify.com" in referer:
            import re
            match = re.search(r'https://([^/]+\.myshopify\.com)', referer)
            if match:
                shop = match.group(1)
    
    # Set CSP to allow framing from shop domain and Shopify admin
    # Simplified CSP that doesn't block Tawk.to
    if shop:
        frame_ancestors = f"frame-ancestors https://{shop} https://admin.shopify.com"
    else:
        # Fallback: allow all for development
        frame_ancestors = "frame-ancestors *"
    
    # Only set frame-ancestors CSP, don't restrict other sources to avoid blocking Tawk.to
    response.headers["Content-Security-Policy"] = f"{frame_ancestors};"
    
    # Remove X-Frame-Options conflicting header
    if "X-Frame-Options" in response.headers:
        del response.headers["X-Frame-Options"]
    
    return response

# Include routers
app.include_router(home.router)
app.include_router(admin_ui.router)
app.include_router(test_simple.router)
app.include_router(auth.router)
app.include_router(webhooks.router)
app.include_router(admin.router)


@app.get("/api", response_model=dict)
async def api_info():
    """API information endpoint."""
    return {
        "status": "healthy",
        "app": "Shopify Termii SMS Notifications",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)

