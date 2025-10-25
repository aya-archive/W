#!/usr/bin/env python3
"""
V2 AURA Launcher - Easy way to start the V2 AURA app
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch V2 AURA app"""
    print("🚀 Starting V2 A.U.R.A - Adaptive User Retention Assistant")
    print("=" * 60)
    
    # Change to V2 directory
    v2_dir = Path(__file__).parent / "V2"
    os.chdir(v2_dir)
    
    print(f"📁 Working directory: {v2_dir}")
    print("🌐 Starting V2 AURA app on http://localhost:8001")
    print("📊 Gradio interface: http://localhost:8001/gradio/")
    print("=" * 60)
    print("Press Ctrl+C to stop the app")
    print()
    
    try:
        # Start the V2 app
        subprocess.run([sys.executable, "V2_working_app.py"])
    except KeyboardInterrupt:
        print("\n🛑 V2 AURA app stopped")
    except Exception as e:
        print(f"❌ Error starting V2 AURA app: {e}")

if __name__ == "__main__":
    main()
