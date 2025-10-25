#!/usr/bin/env python3
"""
A.U.R.A App Launcher
Runs the Gradio app with Churn Prediction integration
"""

import subprocess
import sys
import time
import os

def main():
    """Main launcher function"""
    print("🤖 A.U.R.A - Adaptive User Retention Assistant")
    print("=" * 60)
    print("🚀 Starting A.U.R.A App with Churn Prediction...")
    print("")
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found!")
        print("Please ensure the app.py file exists in the current directory.")
        sys.exit(1)
    
    print("✅ Found app.py")
    print("🧠 Churn Prediction tab integrated")
    print("📊 Features available:")
    print("   • Interactive Dashboard")
    print("   • AI Chatbot Assistant")
    print("   • Risk Analysis")
    print("   • Forecasting")
    print("   • Churn Prediction (NEW)")
    print("")
    print("🌐 Starting Gradio app...")
    print("Access at: http://localhost:7865")
    print("")
    print("🛑 Press Ctrl+C to stop the app")
    print("=" * 60)
    
    try:
        # Run the app
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 A.U.R.A app stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    main()
