#!/usr/bin/env python3
"""
V2 Main App - Unified AURA Platform
FastAPI + Gradio integration with NewAI model service
Single application combining dashboard, API, and AI capabilities
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
import logging
import sys
from pathlib import Path
import json

# Import V2 components
from V2_gradio_interface import create_v2_gradio_interface
from V2_api_routes import router as api_router
from V2_newai_service import get_newai_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="V2 A.U.R.A - Adaptive User Retention Assistant",
    description="V2 Unified AI-Powered Client Retention Platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Global variables
gradio_app = None
newai_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global gradio_app, newai_service
    
    try:
        logger.info("🚀 Starting V2 AURA Main App...")
        
        # Initialize NewAI service
        newai_service = get_newai_service()
        logger.info("✅ V2 NewAI Service initialized")
        
        # Create Gradio interface
        gradio_app = create_v2_gradio_interface()
        logger.info("✅ V2 Gradio Interface created")
        
        logger.info("🎉 V2 AURA Main App started successfully!")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - redirect to Gradio interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>V2 A.U.R.A - Adaptive User Retention Assistant</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle {
                font-size: 1.2em;
                margin-bottom: 40px;
                opacity: 0.9;
            }
            .buttons {
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .btn {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                padding: 15px 30px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                text-decoration: none;
                font-size: 1.1em;
                transition: all 0.3s ease;
                display: inline-block;
            }
            .btn:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .features {
                margin-top: 40px;
                text-align: left;
            }
            .feature {
                margin: 10px 0;
                padding: 10px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 V2 A.U.R.A</h1>
            <div class="subtitle">Adaptive User Retention Assistant</div>
            <p>V2 Unified AI-Powered Client Retention Platform</p>
            
            <div class="buttons">
                <a href="/gradio/" class="btn">🎨 Open Dashboard</a>
                <a href="/docs" class="btn">📚 API Documentation</a>
                <a href="/api/v2/health" class="btn">🔍 Health Check</a>
            </div>
            
            <div class="features">
                <h3>🚀 V2 Features</h3>
                <div class="feature">✅ Unified Platform - Single app for everything</div>
                <div class="feature">✅ FastAPI Backend - Modern, fast, scalable</div>
                <div class="feature">✅ Gradio Interface - Beautiful, interactive UI</div>
                <div class="feature">✅ NewAI Integration - 94.2% accuracy churn prediction</div>
                <div class="feature">✅ RESTful API - Programmatic access</div>
                <div class="feature">✅ Real-time Analytics - Live data processing</div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/gradio/")
async def gradio_interface():
    """Gradio interface endpoint"""
    if gradio_app is None:
        return JSONResponse(
            status_code=500,
            content={"error": "Gradio interface not initialized"}
        )
    
    # Return Gradio interface
    return gradio_app

@app.get("/api/v2/")
async def api_info():
    """API information endpoint"""
    return {
        "name": "V2 AURA API",
        "version": "2.0.0",
        "description": "Unified AI-Powered Client Retention Platform",
        "endpoints": {
            "health": "/api/v2/health",
            "info": "/api/v2/info",
            "predict": "/api/v2/predict",
            "upload": "/api/v2/upload",
            "download": "/api/v2/download-predictions",
            "sample": "/api/v2/sample-data",
            "stats": "/api/v2/stats"
        },
        "documentation": "/docs",
        "gradio_interface": "/gradio/"
    }

@app.get("/status")
async def status():
    """Application status"""
    try:
        newai_service = get_newai_service()
        health = newai_service.health_check()
        
        return {
            "app": "V2 AURA Main App",
            "version": "2.0.0",
            "status": "running",
            "newai_service": health,
            "gradio_available": gradio_app is not None,
            "endpoints": {
                "main": "/",
                "gradio": "/gradio/",
                "api": "/api/v2/",
                "docs": "/docs"
            }
        }
    except Exception as e:
        logger.error(f"❌ Status error: {e}")
        return {
            "app": "V2 AURA Main App",
            "version": "2.0.0",
            "status": "error",
            "error": str(e)
        }

def print_startup_info():
    """Print startup information"""
    print("🤖 V2 A.U.R.A - Adaptive User Retention Assistant")
    print("=" * 60)
    print("V2 Unified AI-Powered Client Retention Platform")
    print("=" * 60)
    print("")
    print("🚀 Features:")
    print("   • FastAPI Backend with RESTful API")
    print("   • Gradio Interface with Interactive Dashboard")
    print("   • NewAI Model Integration (94.2% accuracy)")
    print("   • Real-time Analytics and Predictions")
    print("   • Unified Platform Architecture")
    print("")
    print("🌐 Access Points:")
    print("   • Main Interface: http://localhost:8000")
    print("   • Gradio Dashboard: http://localhost:8000/gradio/")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/api/v2/health")
    print("")
    print("📊 API Endpoints:")
    print("   • GET  /api/v2/health - Health check")
    print("   • GET  /api/v2/info - Model information")
    print("   • POST /api/v2/predict - Run predictions")
    print("   • POST /api/v2/upload - Upload data")
    print("   • GET  /api/v2/download-predictions - Download results")
    print("   • GET  /api/v2/sample-data - Get sample data")
    print("   • GET  /api/v2/stats - Platform statistics")
    print("")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)

def main():
    """Main function to run the V2 AURA app"""
    print_startup_info()
    
    # Run the application
    uvicorn.run(
        "V2_main_app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
