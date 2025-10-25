#!/usr/bin/env python3
"""
A.U.R.A Launcher
Choose between Gradio interface or Modern Web Interface
"""

import sys
import os
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Print A.U.R.A banner"""
    print("🤖 A.U.R.A - Adaptive User Retention Assistant")
    print("=" * 50)
    print("AI-Powered Client Retention Platform")
    print("=" * 50)

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

def run_gradio_app():
    """Run the Gradio application"""
    print("\n🚀 Starting Gradio Interface...")
    print("📊 Interface will be available at: http://localhost:7865")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Gradio app stopped by user")
    except Exception as e:
        print(f"❌ Error running Gradio app: {e}")

def run_web_interface():
    """Run the modern web interface"""
    print("\n🚀 Starting Modern Web Interface...")
    print("🌐 Interface will be available at: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "web_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Web server stopped by user")
    except Exception as e:
        print(f"❌ Error running web server: {e}")

def run_both():
    """Run both interfaces"""
    print("\n🚀 Starting Both Interfaces...")
    print("📊 Gradio Interface: http://localhost:7865")
    print("🌐 Web Interface: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop all services")
    print("-" * 50)
    
    try:
        # Start Gradio in background
        gradio_process = subprocess.Popen([sys.executable, "app.py"])
        
        # Start web server in background
        web_process = subprocess.Popen([sys.executable, "web_server.py"])
        
        # Wait for user to stop
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        try:
            gradio_process.terminate()
            web_process.terminate()
        except:
            pass
        print("✅ All services stopped")

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
    
    # Choose interface
    print("\n🎯 Choose your A.U.R.A interface:")
    print("1. 🤖 Gradio Interface (AI-focused)")
    print("2. 🌐 Modern Web Interface (Dashboard-focused)")
    print("3. 🚀 Both Interfaces (Different ports)")
    print("4. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                run_gradio_app()
                break
            elif choice == "2":
                run_web_interface()
                break
            elif choice == "3":
                run_both()
                break
            elif choice == "4":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
