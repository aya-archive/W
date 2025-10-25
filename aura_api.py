#!/usr/bin/env python3
"""
A.U.R.A API Server
Provides complete A.U.R.A functionality using HTTP server (same tech stack as NewAI API)
Duplicates main Gradio components without using Gradio
"""

import json
import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import logging
import io
import base64

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple settings for the app
class Settings:
    PROJECT_VERSION = "1.0.0"

settings = Settings()

# Global variables for data storage
customer_data = pd.DataFrame()
data_loaded = False

def load_aura_data():
    """Load A.U.R.A data from pipeline or generate sample data."""
    global customer_data, data_loaded
    
    # Generate sample data
    np.random.seed(42)
    n_customers = 500
    
    customer_data = pd.DataFrame({
        'customer_id': [f'CUST_{i:04d}' for i in range(1, n_customers + 1)],
        'name': [f'Customer {i}' for i in range(1, n_customers + 1)],
        'segment': np.random.choice(['SMB', 'Medium-Value', 'High-Value'], n_customers, p=[0.5, 0.3, 0.2]),
        'subscription_plan': np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], n_customers, p=[0.3, 0.4, 0.2, 0.1]),
        'current_health_score': np.clip(np.random.normal(60, 20, n_customers), 0, 100),
        'churn_risk_level': np.random.choice(['Low', 'Medium', 'High'], n_customers, p=[0.6, 0.3, 0.1]),
        'total_lifetime_revenue': np.random.lognormal(8, 1, n_customers),
        'engagement_score': np.random.uniform(0, 1, n_customers),
        'days_since_last_engagement': np.random.randint(1, 90, n_customers),
        'total_support_tickets_lifetime': np.random.poisson(3, n_customers)
    })
    
    data_loaded = True
    return "✅ Sample data generated successfully!"

def validate_csv_data(df):
    """Validate uploaded CSV data."""
    errors = []
    
    # Check if dataframe is empty
    if df.empty:
        errors.append("CSV file is empty")
        return {'valid': False, 'errors': errors}
    
    # Check for required columns (flexible requirements)
    required_columns = ['customer_id']  # Only customer_id is strictly required
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Check for data types
    if 'customer_id' in df.columns:
        if df['customer_id'].isna().any():
            errors.append("customer_id column contains missing values")
    
    # Check for duplicate customer IDs
    if 'customer_id' in df.columns:
        duplicates = df['customer_id'].duplicated().sum()
        if duplicates > 0:
            errors.append(f"Found {duplicates} duplicate customer IDs")
    
    return {'valid': len(errors) == 0, 'errors': errors}

def process_uploaded_data(df):
    """Process uploaded CSV data."""
    # Clean the data
    df_clean = df.copy()
    
    # Handle missing values
    df_clean = df_clean.fillna('Unknown')
    
    # Ensure customer_id is string
    if 'customer_id' in df_clean.columns:
        df_clean['customer_id'] = df_clean['customer_id'].astype(str)
    
    return df_clean

def generate_forecast(metric_type, periods):
    """Generate forecasts using simple trend analysis."""
    if not data_loaded or customer_data.empty:
        return None, "No data loaded. Please load data first."
    
    try:
        # Create sample time series data for demonstration
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
        
        if metric_type == "Revenue":
            values = np.random.lognormal(8, 1, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 1000
        elif metric_type == "Engagement":
            values = np.random.uniform(0, 1, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 30) * 0.2
        else:  # Customer Count
            values = np.random.normal(500, 50, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 100
        
        # Create forecast data
        forecast_dates = pd.date_range(start='2024-01-02', periods=int(periods), freq='D')
        forecast_values = values[-1] + np.random.normal(0, values.std() * 0.1, int(periods))
        
        # Create visualization
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=values, mode='lines', name='Historical', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=forecast_dates, y=forecast_values, mode='lines', name='Forecast', line=dict(color='red', dash='dash')))
        fig.update_layout(title=f"{metric_type} Forecast", xaxis_title="Date", yaxis_title=metric_type)
        
        # Generate insights
        current_value = values[-1]
        forecasted_value = forecast_values[-1]
        growth_rate = ((forecasted_value - current_value) / current_value) * 100
        
        insights_text = f"""
        **Forecast Insights for {metric_type}:**
        
        - **Forecast Periods:** {int(periods)} days
        - **Growth Rate:** {growth_rate:.2f}%
        - **Current Value:** {current_value:.2f}
        - **Forecasted Value:** {forecasted_value:.2f}
        
        **Recommendations:**
        - Monitor trend changes closely
        - Adjust strategies based on forecast accuracy
        - Consider seasonal patterns in planning
        """
        
        return fig, insights_text
        
    except Exception as e:
        logger.error(f"Forecast generation failed: {e}")
        return None, f"❌ Forecast generation failed: {str(e)}"

def analyze_customer_risk(customer_id):
    """Analyze customer risk using simple scoring."""
    if not data_loaded or customer_data.empty:
        return "No data loaded. Please load data first."
    
    if not customer_id:
        return "Please enter a customer ID."
    
    try:
        # Find customer
        customer = customer_data[customer_data['customer_id'] == customer_id]
        if customer.empty:
            return f"Customer {customer_id} not found."
        
        customer_info = customer.iloc[0]
        
        # Simple risk analysis
        health_score = customer_info.get('current_health_score', 50)
        churn_risk = customer_info.get('churn_risk_level', 'Medium')
        engagement = customer_info.get('engagement_score', 0.5)
        days_since_engagement = customer_info.get('days_since_last_engagement', 30)
        
        # Calculate composite risk score
        risk_score = 0
        if churn_risk == 'High':
            risk_score += 0.4
        elif churn_risk == 'Medium':
            risk_score += 0.2
        
        if health_score < 30:
            risk_score += 0.3
        elif health_score < 50:
            risk_score += 0.2
        
        if engagement < 0.3:
            risk_score += 0.2
        
        if days_since_engagement > 60:
            risk_score += 0.1
        
        # Determine risk level
        if risk_score > 0.7:
            risk_level = "Critical"
        elif risk_score > 0.5:
            risk_level = "High"
        elif risk_score > 0.3:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        analysis_text = f"""
        ## Customer Risk Analysis: {customer_info['name']}
        
        **Customer ID:** {customer_info['customer_id']}
        **Risk Level:** {risk_level}
        **Risk Score:** {risk_score:.3f}
        **Confidence:** High
        
        **Key Risk Factors:**
        - Churn Risk Level: {churn_risk} ({0.4 if churn_risk == 'High' else 0.2 if churn_risk == 'Medium' else 0.0:.3f})
        - Health Score: {health_score} ({0.3 if health_score < 30 else 0.2 if health_score < 50 else 0.0:.3f})
        - Engagement Score: {engagement:.3f} ({0.2 if engagement < 0.3 else 0.0:.3f})
        - Days Since Engagement: {days_since_engagement} ({0.1 if days_since_engagement > 60 else 0.0:.3f})
        
        **Priority:** {'Critical' if risk_level == 'Critical' else 'High' if risk_level == 'High' else 'Medium'}
        **Timeline:** {'Immediate' if risk_level in ['Critical', 'High'] else '1-2 weeks'}
        **Expected Outcome:** {'High retention probability' if risk_level == 'Low' else 'Moderate retention probability' if risk_level == 'Medium' else 'Low retention probability'}
        
        **Recommended Actions:**
        - Schedule immediate customer success call
        - Provide personalized retention offer
        - Assign dedicated account manager
        - Monitor engagement metrics daily
        
        **Required Resources:**
        - Customer Success Manager
        - Retention Specialist
        - Marketing team for campaigns
        """
        
        return analysis_text
        
    except Exception as e:
        logger.error(f"Risk analysis failed: {e}")
        return f"❌ Risk analysis failed: {str(e)}"

def process_customer_batch():
    """Process all customers using simple risk analysis."""
    if not data_loaded or customer_data.empty:
        return pd.DataFrame(), "No data loaded. Please load data first."
    
    try:
        # Process customer batch with simple risk analysis
        results = []
        
        for _, customer in customer_data.iterrows():
            health_score = customer.get('current_health_score', 50)
            churn_risk = customer.get('churn_risk_level', 'Medium')
            engagement = customer.get('engagement_score', 0.5)
            days_since_engagement = customer.get('days_since_last_engagement', 30)
            
            # Calculate risk score
            risk_score = 0
            if churn_risk == 'High':
                risk_score += 0.4
            elif churn_risk == 'Medium':
                risk_score += 0.2
            
            if health_score < 30:
                risk_score += 0.3
            elif health_score < 50:
                risk_score += 0.2
            
            if engagement < 0.3:
                risk_score += 0.2
            
            if days_since_engagement > 60:
                risk_score += 0.1
            
            # Determine risk level
            if risk_score > 0.7:
                risk_level = "Critical"
            elif risk_score > 0.5:
                risk_level = "High"
            elif risk_score > 0.3:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            results.append({
                'customer_id': customer['customer_id'],
                'name': customer['name'],
                'risk_level': risk_level,
                'risk_score': risk_score,
                'health_score': health_score,
                'churn_risk': churn_risk,
                'engagement_score': engagement,
                'priority': 'Critical' if risk_level == 'Critical' else 'High' if risk_level == 'High' else 'Medium'
            })
        
        results_df = pd.DataFrame(results)
        
        # Generate summary
        total_customers = len(results_df)
        high_risk = len(results_df[results_df['risk_level'].isin(['High', 'Critical'])])
        critical_priority = len(results_df[results_df['priority'] == 'Critical'])
        avg_risk_score = results_df['risk_score'].mean()
        
        risk_distribution = results_df['risk_level'].value_counts().to_dict()
        priority_distribution = results_df['priority'].value_counts().to_dict()
        
        summary_text = f"""
        **Decision Engine Summary:**
        
        - **Total Customers:** {total_customers:,}
        - **High Risk:** {high_risk:,}
        - **Critical Priority:** {critical_priority:,}
        - **Average Risk Score:** {avg_risk_score:.3f}
        
        **Risk Distribution:**
        {chr(10).join(f"- {level}: {count}" for level, count in risk_distribution.items())}
        
        **Priority Distribution:**
        {chr(10).join(f"- {priority}: {count}" for priority, count in priority_distribution.items())}
        
        **Key Insights:**
        - {high_risk} customers require immediate attention
        - Focus on {critical_priority} critical priority customers first
        - Average risk score indicates overall customer health
        - Consider proactive retention strategies for medium-risk customers
        """
        
        return results_df, summary_text
        
    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
        return pd.DataFrame(), f"❌ Batch processing failed: {str(e)}"

def chat_with_aura(message, history):
    """AI chatbot for A.U.R.A with natural language processing."""
    if not message.strip():
        return history, ""
    
    # Add user message to history
    history.append([message, None])
    
    # Simple AI responses based on keywords
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        response = "Hello! I'm A.U.R.A, your AI retention assistant. I can help you analyze customer data, predict churn risk, and develop retention strategies. What would you like to know?"
    
    elif any(word in message_lower for word in ['churn', 'retention', 'risk']):
        response = "I can help you analyze churn risk and develop retention strategies. I can:\n\n• Analyze individual customer risk\n• Process customer data batches\n• Generate retention recommendations\n• Provide forecasting insights\n\nWould you like me to analyze your customer data?"
    
    elif any(word in message_lower for word in ['forecast', 'prediction', 'future']):
        response = "I can generate forecasts for:\n\n• Revenue trends\n• Customer engagement\n• Customer count\n• Risk distribution\n\nWhat type of forecast would you like to see?"
    
    elif any(word in message_lower for word in ['data', 'upload', 'csv']):
        response = "I can help you with data management:\n\n• Upload and validate CSV files\n• Process customer data\n• Generate sample data\n• Export results\n\nHave you uploaded your customer data yet?"
    
    elif any(word in message_lower for word in ['help', 'assistance', 'support']):
        response = "I'm here to help! I can assist with:\n\n• Customer risk analysis\n• Churn prediction\n• Retention strategies\n• Data processing\n• Forecasting\n• Data export\n\nWhat specific help do you need?"
    
    else:
        response = "I understand you're asking about: " + message + "\n\nI can help you with customer retention analysis, churn prediction, data processing, and forecasting. Could you be more specific about what you'd like to do?"
    
    # Add AI response to history
    history[-1][1] = response
    
    return history, ""

class AURAAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for A.U.R.A API"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == '/':
                self._handle_dashboard()
            elif self.path == '/api/aura/health':
                self._handle_health()
            elif self.path == '/api/aura/load-data':
                self._handle_load_data()
            elif self.path == '/api/aura/forecast':
                self._handle_forecast()
            elif self.path == '/api/aura/risk-analysis':
                self._handle_risk_analysis()
            elif self.path == '/api/aura/batch-process':
                self._handle_batch_process()
            elif self.path == '/api/aura/chat':
                self._handle_chat()
            else:
                self._send_error(404, "Not Found")
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
            self._send_error(500, f"Internal Server Error: {str(e)}")
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            if self.path == '/api/aura/upload':
                self._handle_upload()
            elif self.path == '/api/aura/chat':
                self._handle_chat()
            else:
                self._send_error(404, "Not Found")
        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self._send_error(500, f"Internal Server Error: {str(e)}")
    
    def _handle_dashboard(self):
        """Serve the main dashboard HTML"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>A.U.R.A - Adaptive User Retention Assistant</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { text-align: center; margin-bottom: 30px; }
                .header h1 { color: #2d3748; margin-bottom: 10px; }
                .header p { color: #718096; font-size: 1.1em; }
                .tabs { display: flex; gap: 10px; margin-bottom: 30px; }
                .tab { padding: 12px 24px; background: #e2e8f0; border: none; border-radius: 8px; cursor: pointer; font-weight: 500; }
                .tab.active { background: #4299e1; color: white; }
                .card { background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .btn { padding: 12px 24px; background: #4299e1; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 500; }
                .btn:hover { background: #3182ce; }
                .btn-secondary { background: #e2e8f0; color: #4a5568; }
                .btn-secondary:hover { background: #cbd5e0; }
                .hidden { display: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 A.U.R.A - Adaptive User Retention Assistant</h1>
                    <p>AI-Powered Client Retention Platform</p>
                </div>
                
                <div class="tabs">
                    <button class="tab active" onclick="showTab('dashboard')">📊 Dashboard</button>
                    <button class="tab" onclick="showTab('analysis')">🔍 Analysis</button>
                    <button class="tab" onclick="showTab('forecast')">📈 Forecast</button>
                    <button class="tab" onclick="showTab('chat')">💬 AI Chat</button>
                </div>
                
                <div id="dashboard-tab" class="tab-content">
                    <div class="card">
                        <h2>📊 Dashboard Overview</h2>
                        <p>Welcome to A.U.R.A! Your AI-powered retention assistant is ready to help you analyze customer data and develop retention strategies.</p>
                        <button class="btn" onclick="loadData()">Load Sample Data</button>
                        <button class="btn btn-secondary" onclick="showTab('analysis')">Start Analysis</button>
                    </div>
                </div>
                
                <div id="analysis-tab" class="tab-content hidden">
                    <div class="card">
                        <h2>🔍 Customer Risk Analysis</h2>
                        <p>Analyze individual customers or process entire batches for risk assessment.</p>
                        <input type="text" id="customer-id" placeholder="Enter Customer ID" style="padding: 8px; margin-right: 10px; border: 1px solid #e2e8f0; border-radius: 4px;">
                        <button class="btn" onclick="analyzeCustomer()">Analyze Customer</button>
                        <button class="btn btn-secondary" onclick="processBatch()">Process All Customers</button>
                    </div>
                </div>
                
                <div id="forecast-tab" class="tab-content hidden">
                    <div class="card">
                        <h2>📈 Forecasting</h2>
                        <p>Generate forecasts for revenue, engagement, and customer metrics.</p>
                        <select id="forecast-metric" style="padding: 8px; margin-right: 10px; border: 1px solid #e2e8f0; border-radius: 4px;">
                            <option value="Revenue">Revenue</option>
                            <option value="Engagement">Engagement</option>
                            <option value="Customer Count">Customer Count</option>
                        </select>
                        <input type="number" id="forecast-periods" placeholder="Periods" value="30" style="padding: 8px; margin-right: 10px; border: 1px solid #e2e8f0; border-radius: 4px;">
                        <button class="btn" onclick="generateForecast()">Generate Forecast</button>
                    </div>
                </div>
                
                <div id="chat-tab" class="tab-content hidden">
                    <div class="card">
                        <h2>💬 AI Chat Assistant</h2>
                        <div id="chat-messages" style="height: 300px; overflow-y: auto; border: 1px solid #e2e8f0; padding: 15px; margin-bottom: 15px; background: #f8f9fa;">
                            <div class="message">🤖 Hello! I'm A.U.R.A, your AI retention assistant. How can I help you today?</div>
                        </div>
                        <div style="display: flex; gap: 10px;">
                            <input type="text" id="chat-input" placeholder="Ask me anything about retention..." style="flex: 1; padding: 8px; border: 1px solid #e2e8f0; border-radius: 4px;">
                            <button class="btn" onclick="sendMessage()">Send</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                function showTab(tabName) {
                    // Hide all tabs
                    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.add('hidden'));
                    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
                    
                    // Show selected tab
                    document.getElementById(tabName + '-tab').classList.remove('hidden');
                    event.target.classList.add('active');
                }
                
                function loadData() {
                    fetch('/api/aura/load-data')
                        .then(response => response.json())
                        .then(data => {
                            alert(data.message);
                        });
                }
                
                function analyzeCustomer() {
                    const customerId = document.getElementById('customer-id').value;
                    if (!customerId) {
                        alert('Please enter a Customer ID');
                        return;
                    }
                    
                    fetch(`/api/aura/risk-analysis?customer_id=${customerId}`)
                        .then(response => response.text())
                        .then(data => {
                            alert(data);
                        });
                }
                
                function processBatch() {
                    fetch('/api/aura/batch-process')
                        .then(response => response.json())
                        .then(data => {
                            alert(data.summary);
                        });
                }
                
                function generateForecast() {
                    const metric = document.getElementById('forecast-metric').value;
                    const periods = document.getElementById('forecast-periods').value;
                    
                    fetch(`/api/aura/forecast?metric=${metric}&periods=${periods}`)
                        .then(response => response.text())
                        .then(data => {
                            alert(data);
                        });
                }
                
                function sendMessage() {
                    const input = document.getElementById('chat-input');
                    const message = input.value.trim();
                    if (!message) return;
                    
                    // Add user message
                    const chatMessages = document.getElementById('chat-messages');
                    chatMessages.innerHTML += `<div class="message" style="text-align: right; color: #4299e1;">👤 ${message}</div>`;
                    
                    // Send to API
                    fetch('/api/aura/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message})
                    })
                    .then(response => response.json())
                    .then(data => {
                        chatMessages.innerHTML += `<div class="message">🤖 ${data.response}</div>`;
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    });
                    
                    input.value = '';
                }
                
                // Allow Enter key in chat
                document.getElementById('chat-input').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def _handle_health(self):
        """Handle health check request"""
        health = {
            "status": "healthy",
            "aura_available": True,
            "version": settings.PROJECT_VERSION
        }
        self._send_json_response(health)
    
    def _handle_load_data(self):
        """Handle load data request"""
        result = load_aura_data()
        response = {"message": result}
        self._send_json_response(response)
    
    def _handle_forecast(self):
        """Handle forecast request"""
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        metric = query_params.get('metric', ['Revenue'])[0]
        periods = int(query_params.get('periods', ['30'])[0])
        
        fig, insights = generate_forecast(metric, periods)
        if fig:
            # Convert plotly figure to HTML
            html_fig = fig.to_html(include_plotlyjs=False, div_id="forecast-chart")
            response = {"chart": html_fig, "insights": insights}
        else:
            response = {"error": insights}
        
        self._send_json_response(response)
    
    def _handle_risk_analysis(self):
        """Handle risk analysis request"""
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        customer_id = query_params.get('customer_id', [''])[0]
        
        result = analyze_customer_risk(customer_id)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))
    
    def _handle_batch_process(self):
        """Handle batch processing request"""
        results_df, summary = process_customer_batch()
        
        if not results_df.empty:
            # Convert results to JSON
            results_json = results_df.to_dict('records')
            response = {
                "results": results_json,
                "summary": summary,
                "total_customers": len(results_df)
            }
        else:
            response = {"error": summary}
        
        self._send_json_response(response)
    
    def _handle_chat(self):
        """Handle chat request"""
        if self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            message = data.get('message', '')
            
            # Simple chat response
            response = chat_with_aura(message, [])
            chat_response = response[0][-1][1] if response[0] else "I'm here to help!"
            
            self._send_json_response({"response": chat_response})
        else:
            self._send_error(405, "Method Not Allowed")
    
    def _handle_upload(self):
        """Handle file upload request"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Parse multipart form data (simplified)
        # In a real implementation, you'd use a proper multipart parser
        response = {"message": "File upload functionality would be implemented here"}
        self._send_json_response(response)
    
    def _send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def _send_error(self, status_code, message):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        error_response = {"error": message}
        self.wfile.write(json.dumps(error_response).encode('utf-8'))

def start_aura_api(port=8082):
    """Start the A.U.R.A API server"""
    try:
        with HTTPServer(("", port), AURAAPIHandler) as httpd:
            print("🤖 A.U.R.A API Server Starting...")
            print("=" * 50)
            print(f"🌐 Server running at: http://localhost:{port}")
            print("📊 Features available:")
            print("   • Interactive Dashboard")
            print("   • Customer Risk Analysis")
            print("   • Forecasting")
            print("   • AI Chat Assistant")
            print("   • Data Processing")
            print("\n🛑 Press Ctrl+C to stop the server")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 A.U.R.A API server stopped by user")
    except Exception as e:
        print(f"❌ Error starting A.U.R.A API server: {e}")

if __name__ == "__main__":
    start_aura_api()
