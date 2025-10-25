#!/usr/bin/env python3
"""
V2 Local AI Model - Ollama SmolLM 360M Integration
Lightweight local AI model using Ollama SmolLM 360M for the V2 AURA platform
"""

import requests
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class V2OllamaAI:
    """V2 Ollama AI Model - SmolLM 360M Integration"""
    
    def __init__(self, model_name: str = "smolllm:360m", ollama_url: str = "http://localhost:11434"):
        """Initialize V2 Ollama AI"""
        self.name = "V2 AURA Assistant"
        self.version = "2.0.0"
        self.model_type = "Ollama SmolLM 360M"
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.api_url = f"{ollama_url}/api"
        
        # Conversation context
        self.conversation_history = []
        self.user_preferences = {}
        
        # System prompt for AURA context
        self.system_prompt = """You are the V2 AURA (Adaptive User Retention Assistant) AI. You help users with:

1. Churn prediction and customer retention strategies
2. Data analysis and CSV file processing guidance
3. Platform navigation and feature explanations
4. Analytics interpretation and insights
5. Customer retention best practices

You are knowledgeable about:
- Machine learning models for churn prediction
- Customer data analysis and preprocessing
- Retention strategies and customer lifecycle management
- Business analytics and key performance indicators
- The V2 AURA platform features and capabilities

Always provide helpful, accurate, and actionable advice. Be concise but informative. If you don't know something, say so and suggest where the user might find the information."""
        
        # Check if Ollama is running
        self._check_ollama_status()
        
        logger.info("✅ V2 Ollama AI initialized successfully")
    
    def _check_ollama_status(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                
                if self.model_name in model_names:
                    logger.info(f"✅ Ollama model '{self.model_name}' is available")
                    return True
                else:
                    logger.warning(f"⚠️ Model '{self.model_name}' not found. Available models: {model_names}")
                    logger.info("💡 To install SmolLM 360M, run: ollama pull smolllm:360m")
                    return False
            else:
                logger.error(f"❌ Ollama API not responding: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            logger.error("❌ Cannot connect to Ollama. Make sure Ollama is running on localhost:11434")
            logger.info("💡 Start Ollama with: ollama serve")
            return False
        except Exception as e:
            logger.error(f"❌ Error checking Ollama status: {e}")
            return False
    
    def process_message(self, message: str) -> str:
        """
        Process user message and generate response using Ollama
        
        Args:
            message: User input message
            
        Returns:
            AI response string
        """
        try:
            # Add to conversation history
            self.conversation_history.append({
                "timestamp": datetime.now(),
                "user": message,
                "ai": None
            })
            
            # Generate response using Ollama
            response = self._generate_ollama_response(message)
            
            # Add response to history
            self.conversation_history[-1]["ai"] = response
            
            logger.info(f"✅ V2 Ollama AI processed message: {message[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
            return "I apologize, but I encountered an error processing your message. Please try again."
    
    def _generate_ollama_response(self, message: str) -> str:
        """Generate response using Ollama SmolLM 360M"""
        try:
            # Prepare the conversation context
            conversation_context = self._build_conversation_context()
            
            # Prepare the prompt
            full_prompt = f"{self.system_prompt}\n\n{conversation_context}\n\nUser: {message}\n\nAssistant:"
            
            # Call Ollama API
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            }
            
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "I couldn't generate a response. Please try again.")
            else:
                logger.error(f"❌ Ollama API error: {response.status_code}")
                return "I'm having trouble connecting to the AI model. Please make sure Ollama is running."
                
        except requests.exceptions.Timeout:
            logger.error("❌ Ollama request timeout")
            return "The AI model is taking too long to respond. Please try again."
        except requests.exceptions.ConnectionError:
            logger.error("❌ Cannot connect to Ollama")
            return "I cannot connect to the AI model. Please make sure Ollama is running on localhost:11434."
        except Exception as e:
            logger.error(f"❌ Error generating Ollama response: {e}")
            return "I encountered an error while processing your request. Please try again."
    
    def _build_conversation_context(self) -> str:
        """Build conversation context from recent history"""
        if not self.conversation_history:
            return ""
        
        # Get last 3 exchanges for context
        recent_history = self.conversation_history[-3:]
        context_parts = []
        
        for exchange in recent_history:
            if exchange["user"] and exchange["ai"]:
                context_parts.append(f"User: {exchange['user']}")
                context_parts.append(f"Assistant: {exchange['ai']}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def get_conversation_summary(self) -> Dict:
        """Get conversation summary"""
        return {
            "total_messages": len(self.conversation_history),
            "recent_topics": [msg["user"][:50] for msg in self.conversation_history[-5:]],
            "ai_name": self.name,
            "version": self.version,
            "model": self.model_name
        }
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        logger.info("🔄 V2 Ollama AI conversation reset")
    
    def get_ai_info(self) -> Dict:
        """Get AI model information"""
        return {
            "name": self.name,
            "version": self.version,
            "model_type": self.model_type,
            "model_name": self.model_name,
            "ollama_url": self.ollama_url,
            "capabilities": [
                "Churn prediction guidance",
                "Data analysis assistance", 
                "Retention strategy advice",
                "Platform navigation help",
                "Analytics interpretation",
                "Natural language processing",
                "Context-aware responses"
            ],
            "knowledge_areas": [
                "churn_prediction",
                "data_analysis", 
                "retention_strategies",
                "platform_guidance",
                "analytics_insights",
                "customer_lifecycle"
            ],
            "conversation_count": len(self.conversation_history),
            "ollama_status": self._check_ollama_status()
        }
    
    def test_connection(self) -> Dict:
        """Test Ollama connection and model availability"""
        try:
            # Test basic connection
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code != 200:
                return {"status": "error", "message": f"Ollama API not responding: {response.status_code}"}
            
            # Check model availability
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if self.model_name in model_names:
                return {
                    "status": "success", 
                    "message": f"Ollama is running and model '{self.model_name}' is available",
                    "available_models": model_names
                }
            else:
                return {
                    "status": "warning",
                    "message": f"Model '{self.model_name}' not found. Available: {model_names}",
                    "available_models": model_names,
                    "install_command": f"ollama pull {self.model_name}"
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "message": "Cannot connect to Ollama. Make sure it's running on localhost:11434",
                "start_command": "ollama serve"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection test failed: {str(e)}"
            }

# Global AI instance
v2_ollama_ai = V2OllamaAI()

def get_local_ai() -> V2OllamaAI:
    """Get the global V2 Ollama AI instance"""
    return v2_ollama_ai