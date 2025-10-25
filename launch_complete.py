#!/usr/bin/env python3
"""
A.U.R.A Complete Launcher
Launches all A.U.R.A services including NewAI integration
"""

import sys
import os
import subprocess
import time
import threading
from pathlib import Path

def print_banner():
    """Print A.U.R.A banner"""
    print("🤖 A.U.R.A - Adaptive User Retention Assistant")
    print("=" * 60)
    print("AI-Powered Client Retention Platform with NewAI Integration")
    print("=" * 60)

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import gradio
        import pandas
        import plotly
        print("✅ Required packages are available")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def start_web_interface():
    """Start the web interface server"""
    print("🌐 Starting Web Interface Server...")
    try:
        subprocess.Popen([sys.executable, "web_server.py"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        print("✅ Web Interface: http://localhost:8080")
        return True
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        return False

def start_gradio_interface():
    """Start the Gradio interface"""
    print("🤖 Starting Gradio Interface...")
    try:
        subprocess.Popen([sys.executable, "app.py"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        print("✅ Gradio Interface: http://localhost:7865")
        return True
    except Exception as e:
        print(f"❌ Error starting Gradio interface: {e}")
        return False

def start_newai_api():
    """Start the NewAI API server"""
    print("🧠 Starting NewAI API Server...")
    try:
        subprocess.Popen([sys.executable, "newai_api.py"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        print("✅ NewAI API: http://localhost:8081")
        return True
    except Exception as e:
        print(f"❌ Error starting NewAI API: {e}")
        return False

def run_all_services():
    """Run all A.U.R.A services"""
    print("\n🚀 Starting All A.U.R.A Services...")
    print("-" * 60)
    
    services = []
    
    # Start Web Interface
    if start_web_interface():
        services.append("Web Interface")
    
    # Start Gradio Interface
    if start_gradio_interface():
        services.append("Gradio Interface")
    
    # Start NewAI API
    if start_newai_api():
        services.append("NewAI API")
    
    print(f"\n✅ Started {len(services)} services:")
    for service in services:
        print(f"   • {service}")
    
    print("\n🌐 Access Points:")
    print("   • Web Interface: http://localhost:8080")
    print("   • Gradio Interface: http://localhost:7865")
    print("   • NewAI API: http://localhost:8081")
    
    print("\n📊 Features Available:")
    print("   • Interactive Dashboard with Tabs")
    print("   • AI Chatbot Assistant")
    print("   • Risk Analysis & Forecasting")
    print("   • NewAI Churn Prediction Model")
    print("   • Data Management & Export")
    
    print("\n🛑 Press Ctrl+C to stop all services")
    print("=" * 60)
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        print("✅ All services stopped")

def run_web_only():
    """Run only the web interface"""
    print("\n🌐 Starting Web Interface Only...")
    print("-" * 60)
    
    if start_web_interface():
        print("\n✅ Web Interface started successfully!")
        print("🌐 Access: http://localhost:8080")
        print("📊 Features: Dashboard, AI Chat, NewAI Integration")
        print("\n🛑 Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Web interface stopped")

def run_gradio_only():
    """Run only the Gradio interface"""
    print("\n🤖 Starting Gradio Interface Only...")
    print("-" * 60)
    
    if start_gradio_interface():
        print("\n✅ Gradio Interface started successfully!")
        print("🤖 Access: http://localhost:7865")
        print("📊 Features: AI Chat, Data Analysis, Forecasting")
        print("\n🛑 Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Gradio interface stopped")

def run_newai_only():
    """Run only the NewAI API"""
    print("\n🧠 Starting NewAI API Only...")
    print("-" * 60)
    
    if start_newai_api():
        print("\n✅ NewAI API started successfully!")
        print("🧠 Access: http://localhost:8081")
        print("📊 Features: Churn Prediction, Risk Analysis")
        print("\n🛑 Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 NewAI API stopped")

def main():
    """Main launcher function"""
    print_banner()
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Error: app.py not found. Please run from the AURA directory.")
        sys.exit(1)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Choose service configuration
    print("\n🎯 Choose your A.U.R.A configuration:")
    print("1. 🚀 All Services (Recommended)")
    print("2. 🌐 Web Interface Only")
    print("3. 🤖 Gradio Interface Only")
    print("4. 🧠 NewAI API Only")
    print("5. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                run_all_services()
                break
            elif choice == "2":
                run_web_only()
                break
            elif choice == "3":
                run_gradio_only()
                break
            elif choice == "4":
                run_newai_only()
                break
            elif choice == "5":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
