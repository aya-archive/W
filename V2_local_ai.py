#!/usr/bin/env python3
"""
V2 Local AI Model - Mini AI Assistant
Lightweight local AI model for the V2 AURA platform
"""

import re
import random
import logging
from typing import List, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class V2LocalAI:
    """V2 Local AI Model - Mini AI Assistant"""
    
    def __init__(self):
        """Initialize V2 Local AI"""
        self.name = "V2 AURA Assistant"
        self.version = "2.0.0"
        self.model_type = "Local Mini AI"
        
        # Knowledge base for churn prediction and retention
        self.knowledge_base = {
            "churn": {
                "keywords": ["churn", "retention", "customer", "leave", "cancel", "quit"],
                "responses": [
                    "Churn prediction helps identify customers at risk of leaving. Our V2 NewAI model achieves 94.2% accuracy in predicting customer churn.",
                    "To reduce churn, focus on high-value customers, improve customer service, and offer personalized retention strategies.",
                    "Key churn indicators include decreased usage, support ticket frequency, payment delays, and contract renewal patterns.",
                    "Use the NewAI tab to upload your customer data and get personalized churn risk assessments for each customer."
                ]
            },
            "data": {
                "keywords": ["data", "csv", "upload", "file", "analysis", "dataset"],
                "responses": [
                    "Upload your CSV files in the Data Management tab. The system supports customer data with features like demographics, usage patterns, and billing information.",
                    "For best results, ensure your CSV contains columns like customerID, gender, tenure, MonthlyCharges, and TotalCharges.",
                    "The V2 platform can process large datasets and provide real-time analytics and predictions.",
                    "Use the Dashboard tab to view comprehensive analytics and key metrics about your customer base."
                ]
            },
            "model": {
                "keywords": ["model", "ai", "prediction", "accuracy", "algorithm"],
                "responses": [
                    "Our V2 NewAI model achieves 94.2% accuracy in churn prediction. It analyzes 20+ customer attributes to provide risk assessments.",
                    "The model uses advanced machine learning techniques including XGBoost and feature engineering to predict customer behavior.",
                    "Model features include customer demographics, service usage patterns, contract information, payment history, and billing patterns.",
                    "The V2 platform uses simulation mode when the full model isn't available, providing realistic predictions for testing."
                ]
            },
            "retention": {
                "keywords": ["retention", "strategy", "prevent", "keep", "loyalty"],
                "responses": [
                    "Effective retention strategies include personalized offers, proactive customer service, and early intervention for at-risk customers.",
                    "Focus on high-value customers first, as they have the highest impact on revenue retention.",
                    "Implement automated alerts for customers showing early churn signals like decreased engagement or support issues.",
                    "Use the V2 platform's risk assessment to prioritize retention efforts and allocate resources effectively."
                ]
            },
            "analytics": {
                "keywords": ["analytics", "dashboard", "metrics", "insights", "report"],
                "responses": [
                    "The V2 Dashboard provides comprehensive analytics including customer segmentation, risk distribution, and key performance metrics.",
                    "Key metrics to track include total customers, high-risk count, medium-risk count, and average churn probability.",
                    "Use the analytics to identify trends, patterns, and opportunities for improving customer retention.",
                    "The platform provides real-time updates and interactive visualizations for better decision-making."
                ]
            },
            "general": {
                "keywords": ["help", "how", "what", "explain", "guide"],
                "responses": [
                    "I'm your V2 AURA assistant! I can help you with churn prediction, data analysis, retention strategies, and platform guidance.",
                    "Use the Dashboard tab for analytics overview, NewAI tab for predictions, Data Management for file operations, and this chat for assistance.",
                    "The V2 platform combines FastAPI backend, Gradio interface, and NewAI model integration for a unified experience.",
                    "I can explain features, provide guidance, and help you make the most of your customer retention platform."
                ]
            }
        }
        
        # Conversation context
        self.conversation_history = []
        self.user_preferences = {}
        
        logger.info("✅ V2 Local AI initialized successfully")
    
    def process_message(self, message: str) -> str:
        """
        Process user message and generate response
        
        Args:
            message: User input message
            
        Returns:
            AI response string
        """
        try:
            # Clean and normalize input
            message = message.strip().lower()
            
            # Add to conversation history
            self.conversation_history.append({
                "timestamp": datetime.now(),
                "user": message,
                "ai": None
            })
            
            # Determine intent and generate response
            response = self._generate_response(message)
            
            # Add response to history
            self.conversation_history[-1]["ai"] = response
            
            logger.info(f"✅ V2 Local AI processed message: {message[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
            return "I apologize, but I encountered an error processing your message. Please try again."
    
    def _generate_response(self, message: str) -> str:
        """Generate AI response based on message content"""
        
        # Check for specific intents
        intent_scores = {}
        
        for intent, data in self.knowledge_base.items():
            score = 0
            for keyword in data["keywords"]:
                if keyword in message:
                    score += 1
            intent_scores[intent] = score
        
        # Get the best matching intent
        best_intent = max(intent_scores, key=intent_scores.get) if intent_scores else "general"
        
        # Generate contextual response
        if intent_scores[best_intent] > 0:
            # Use specific knowledge base responses
            responses = self.knowledge_base[best_intent]["responses"]
            base_response = random.choice(responses)
        else:
            # Use general responses
            responses = self.knowledge_base["general"]["responses"]
            base_response = random.choice(responses)
        
        # Add contextual enhancements
        enhanced_response = self._enhance_response(base_response, message)
        
        return enhanced_response
    
    def _enhance_response(self, base_response: str, message: str) -> str:
        """Enhance response with contextual information"""
        
        # Add specific guidance based on message content
        enhancements = []
        
        if "upload" in message or "csv" in message:
            enhancements.append("💡 Tip: Make sure your CSV file has a 'customerID' column for best results.")
        
        if "churn" in message:
            enhancements.append("📊 Use the NewAI tab to run predictions on your customer data.")
        
        if "dashboard" in message or "analytics" in message:
            enhancements.append("📈 Check the Dashboard tab for comprehensive analytics and insights.")
        
        if "help" in message or "how" in message:
            enhancements.append("🚀 Explore all tabs to discover the full capabilities of the V2 platform.")
        
        # Combine base response with enhancements
        if enhancements:
            return f"{base_response}\n\n{random.choice(enhancements)}"
        else:
            return base_response
    
    def get_conversation_summary(self) -> Dict:
        """Get conversation summary"""
        return {
            "total_messages": len(self.conversation_history),
            "recent_topics": [msg["user"][:50] for msg in self.conversation_history[-5:]],
            "ai_name": self.name,
            "version": self.version
        }
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        logger.info("🔄 V2 Local AI conversation reset")
    
    def get_ai_info(self) -> Dict:
        """Get AI model information"""
        return {
            "name": self.name,
            "version": self.version,
            "model_type": self.model_type,
            "capabilities": [
                "Churn prediction guidance",
                "Data analysis assistance", 
                "Retention strategy advice",
                "Platform navigation help",
                "Analytics interpretation"
            ],
            "knowledge_areas": list(self.knowledge_base.keys()),
            "conversation_count": len(self.conversation_history)
        }

# Global AI instance
v2_local_ai = V2LocalAI()

def get_local_ai() -> V2LocalAI:
    """Get the global V2 Local AI instance"""
    return v2_local_ai
