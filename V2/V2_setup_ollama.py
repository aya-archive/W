#!/usr/bin/env python3
"""
V2 Ollama Setup Script
Setup script to install and configure Ollama with SmolLM 360M model
"""

import subprocess
import sys
import requests
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ Ollama is installed: {result.stdout.strip()}")
            return True
        else:
            logger.warning("⚠️ Ollama command failed")
            return False
    except FileNotFoundError:
        logger.warning("⚠️ Ollama not found in PATH")
        return False

def install_ollama():
    """Install Ollama"""
    logger.info("🚀 Installing Ollama...")
    
    try:
        # Download and install Ollama
        if sys.platform == "darwin":  # macOS
            logger.info("📥 Downloading Ollama for macOS...")
            subprocess.run([
                "curl", "-fsSL", "https://ollama.ai/install.sh", "|", "sh"
            ], shell=True, check=True)
        elif sys.platform == "linux":
            logger.info("📥 Downloading Ollama for Linux...")
            subprocess.run([
                "curl", "-fsSL", "https://ollama.ai/install.sh", "|", "sh"
            ], shell=True, check=True)
        else:
            logger.error("❌ Unsupported platform. Please install Ollama manually from https://ollama.ai")
            return False
        
        logger.info("✅ Ollama installation completed")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install Ollama: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Installation error: {e}")
        return False

def start_ollama_service():
    """Start Ollama service"""
    logger.info("🚀 Starting Ollama service...")
    
    try:
        # Start Ollama in background
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for service to start
        logger.info("⏳ Waiting for Ollama service to start...")
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    logger.info("✅ Ollama service is running")
                    return True
            except:
                time.sleep(1)
        
        logger.error("❌ Ollama service failed to start")
        return False
        
    except Exception as e:
        logger.error(f"❌ Failed to start Ollama service: {e}")
        return False

def install_smollm_model():
    """Install SmolLM 360M model"""
    logger.info("📥 Installing SmolLM 360M model...")
    
    try:
        # Pull the model
        result = subprocess.run([
            "ollama", "pull", "smolllm:360m"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ SmolLM 360M model installed successfully")
            return True
        else:
            logger.error(f"❌ Failed to install model: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Model installation error: {e}")
        return False

def test_ollama_integration():
    """Test Ollama integration"""
    logger.info("🧪 Testing Ollama integration...")
    
    try:
        # Test API connection
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            logger.error("❌ Ollama API not responding")
            return False
        
        # Check if model is available
        models = response.json().get("models", [])
        model_names = [model["name"] for model in models]
        
        if "smolllm:360m" in model_names:
            logger.info("✅ SmolLM 360M model is available")
            return True
        else:
            logger.error(f"❌ SmolLM 360M model not found. Available models: {model_names}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🤖 V2 AURA - Ollama Setup")
    print("=" * 50)
    print("Setting up Ollama with SmolLM 360M model for V2 AURA platform")
    print("=" * 50)
    
    # Step 1: Check if Ollama is installed
    logger.info("🔍 Checking Ollama installation...")
    if not check_ollama_installed():
        logger.info("📥 Ollama not found. Installing...")
        if not install_ollama():
            logger.error("❌ Failed to install Ollama. Please install manually from https://ollama.ai")
            return False
    else:
        logger.info("✅ Ollama is already installed")
    
    # Step 2: Start Ollama service
    logger.info("🚀 Starting Ollama service...")
    if not start_ollama_service():
        logger.error("❌ Failed to start Ollama service")
        return False
    
    # Step 3: Install SmolLM model
    logger.info("📥 Installing SmolLM 360M model...")
    if not install_smollm_model():
        logger.error("❌ Failed to install SmolLM model")
        return False
    
    # Step 4: Test integration
    logger.info("🧪 Testing integration...")
    if not test_ollama_integration():
        logger.error("❌ Integration test failed")
        return False
    
    print("\n🎉 Ollama setup completed successfully!")
    print("✅ Ollama service is running on localhost:11434")
    print("✅ SmolLM 360M model is ready")
    print("✅ V2 AURA platform can now use local AI")
    print("\n🚀 You can now start the V2 AURA app with: python3 V2_working_app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
