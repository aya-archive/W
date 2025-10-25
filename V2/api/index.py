"""
Vercel serverless function for AURA app
This creates a serverless endpoint for your FastAPI + Gradio app
"""

import sys
import os
from pathlib import Path

# Add the V2 directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from V2_working_app import app

# Export the FastAPI app for Vercel
handler = app
