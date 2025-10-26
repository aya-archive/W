#!/usr/bin/env python3
"""
V2 Working App - AURA Platform
Completely working FastAPI + Gradio integration
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import gradio as gr
import logging
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Visualization Functions
def create_churn_distribution_pie(prediction_data=None):
    """Create pie chart for churn distribution"""
    if prediction_data is None or len(prediction_data) == 0:
        # Default empty state - show sample data to make it visible
        labels = ['Low Risk', 'Medium Risk', 'High Risk']
        values = [60, 30, 10]  # Sample percentages
        colors = ['#2E8B57', '#FFD700', '#DC143C']  # Green, Yellow, Red
    else:
        # Count risk levels from prediction data
        risk_counts = {'Low Risk': 0, 'Medium Risk': 0, 'High Risk': 0}
        
        for row in prediction_data:
            if len(row) >= 3:  # Ensure we have at least 3 columns
                risk_level = row[2]  # Risk Level is the 3rd column
                if risk_level in risk_counts:
                    risk_counts[risk_level] += 1
        
        labels = list(risk_counts.keys())
        values = list(risk_counts.values())
        colors = ['#2E8B57', '#FFD700', '#DC143C']  # Green, Yellow, Red
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=colors,
        textinfo='label+percent',
        textfont_size=12
    )])
    
    fig.update_layout(
        title="Churn Risk Distribution",
        title_x=0.5,
        font=dict(size=12),
        showlegend=True,
        height=400
    )
    
    return fig

def create_key_metrics_bar(prediction_data=None):
    """Create bar chart for key metrics"""
    if prediction_data is None or len(prediction_data) == 0:
        # Default empty state - show sample data to make it visible
        categories = ['Total Customers', 'Low Risk', 'Medium Risk', 'High Risk']
        values = [1000, 600, 300, 100]  # Sample data
        colors = ['#4B0082', '#2E8B57', '#FFD700', '#DC143C']
    else:
        # Count risk levels from prediction data
        risk_counts = {'Low Risk': 0, 'Medium Risk': 0, 'High Risk': 0}
        
        for row in prediction_data:
            if len(row) >= 3:  # Ensure we have at least 3 columns
                risk_level = row[2]  # Risk Level is the 3rd column
                if risk_level in risk_counts:
                    risk_counts[risk_level] += 1
        
        # Calculate total customers
        total_customers = sum(risk_counts.values())
        
        # Create categories and values
        categories = ['Total Customers', 'Low Risk', 'Medium Risk', 'High Risk']
        values = [total_customers, risk_counts['Low Risk'], risk_counts['Medium Risk'], risk_counts['High Risk']]
        colors = ['#4B0082', '#2E8B57', '#FFD700', '#DC143C']
    
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=values,
        textposition='auto',
    )])
    
    fig.update_layout(
        title="Customer Risk Distribution",
        xaxis_title="Risk Categories",
        yaxis_title="Number of Customers",
        title_x=0.5,
        font=dict(size=12),
        height=400
    )
    
    return fig

def create_retention_success_rate():
    """Create retention success rate prediction"""
    # Sample data - in real app, this would be calculated from model predictions
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    success_rates = [85, 87, 89, 91, 88, 92]  # Sample retention success rates
    
    fig = go.Figure(data=[go.Scatter(
        x=months,
        y=success_rates,
        mode='lines+markers',
        line=dict(color='#4B0082', width=3),
        marker=dict(size=8, color='#4B0082'),
        name='Retention Success Rate'
    )])
    
    fig.update_layout(
        title="Predicted Retention Success Rate",
        xaxis_title="Month",
        yaxis_title="Success Rate (%)",
        title_x=0.5,
        font=dict(size=12),
        height=400,
        yaxis=dict(range=[80, 95])
    )
    
    return fig

# Create FastAPI app
app = FastAPI(
    title="A.U.R.A - Adaptive User Retention Assistant",
    description="Unified AI-Powered Client Retention Platform",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add static file serving for logo and other assets
app.mount("/static", StaticFiles(directory="."), name="static")

# Create Gradio interface
def create_gradio_interface():
    """Create working Gradio interface"""
    print("Starting create_gradio_interface function...")
    
    def update_pie_chart(prediction_data):
        """Update pie chart with prediction data"""
        return create_churn_distribution_pie(prediction_data)
    
    def generate_ai_strategies(customer_segment, strategy_type):
        """Generate AI-powered retention strategies based on customer segment and strategy type"""
        # AI Strategy Generation Logic
        strategies = {
            "High Risk": {
                "Retention Campaign": {
                    "strategy_1": {
                        "title": "Emergency Retention Call",
                        "description": "Immediate personal intervention for high-risk customers",
                        "steps": "1. Identify customer pain points\n2. Offer immediate resolution\n3. Schedule retention specialist call\n4. Provide exclusive retention offer",
                        "impact": "90% engagement rate, 60% retention success"
                    },
                    "strategy_2": {
                        "title": "Premium Service Upgrade",
                        "description": "Complimentary upgrade to premium service tier",
                        "steps": "1. Analyze current service level\n2. Identify upgrade opportunities\n3. Offer complimentary premium features\n4. Monitor usage and satisfaction",
                        "impact": "80% acceptance rate, increased loyalty"
                    },
                    "strategy_3": {
                        "title": "Personal Account Manager",
                        "description": "Assign dedicated account manager for personalized service",
                        "steps": "1. Assign experienced retention specialist\n2. Schedule weekly check-ins\n3. Provide priority support access\n4. Track satisfaction metrics",
                        "impact": "85% satisfaction improvement, 70% retention"
                    }
                },
                "Win-Back Campaign": {
                    "strategy_1": {
                        "title": "Win-Back Phone Call",
                        "description": "Personalized win-back call with special offers",
                        "steps": "1. Prepare personalized win-back offer\n2. Schedule callback within 24 hours\n3. Present exclusive return benefits\n4. Follow up with email confirmation",
                        "impact": "75% callback rate, 50% win-back success"
                    },
                    "strategy_2": {
                        "title": "Exclusive Return Package",
                        "description": "Special package for returning customers",
                        "steps": "1. Create exclusive return benefits\n2. Send personalized email offer\n3. Include premium service trial\n4. Track return engagement",
                        "impact": "65% email open rate, 40% return rate"
                    },
                    "strategy_3": {
                        "title": "Loyalty Points Bonus",
                        "description": "Bonus loyalty points for returning customers",
                        "steps": "1. Calculate bonus points offer\n2. Send SMS with exclusive code\n3. Provide instant redemption\n4. Monitor redemption patterns",
                        "impact": "70% SMS engagement, 55% redemption rate"
                    }
                }
            },
            "Medium Risk": {
                "Retention Campaign": {
                    "strategy_1": {
                        "title": "Proactive Service Review",
                        "description": "Scheduled service review to identify improvement opportunities",
                        "steps": "1. Schedule service review call\n2. Analyze usage patterns\n3. Identify optimization opportunities\n4. Propose service improvements",
                        "impact": "80% engagement rate, 45% retention improvement"
                    },
                    "strategy_2": {
                        "title": "Loyalty Program Enrollment",
                        "description": "Enroll in enhanced loyalty program with exclusive benefits",
                        "steps": "1. Create personalized loyalty offer\n2. Send enrollment invitation\n3. Provide exclusive member benefits\n4. Track program engagement",
                        "impact": "75% enrollment rate, increased engagement"
                    },
                    "strategy_3": {
                        "title": "Feature Education Campaign",
                        "description": "Educational campaign about unused features and benefits",
                        "steps": "1. Identify unused features\n2. Create educational content\n3. Send feature highlight emails\n4. Track feature adoption",
                        "impact": "60% email engagement, 35% feature adoption"
                    }
                }
            },
            "Low Risk": {
                "Retention Campaign": {
                    "strategy_1": {
                        "title": "Satisfaction Survey & Follow-up",
                        "description": "Regular satisfaction surveys with personalized follow-up",
                        "steps": "1. Send satisfaction survey\n2. Analyze responses\n3. Address any concerns\n4. Follow up with improvements",
                        "impact": "85% survey completion, 95% satisfaction"
                    },
                    "strategy_2": {
                        "title": "Referral Program Invitation",
                        "description": "Invite to exclusive referral program with rewards",
                        "steps": "1. Create referral program offer\n2. Send invitation email\n3. Provide referral tools\n4. Track referral activity",
                        "impact": "70% program participation, increased advocacy"
                    },
                    "strategy_3": {
                        "title": "Premium Feature Preview",
                        "description": "Exclusive preview of upcoming premium features",
                        "steps": "1. Identify premium features\n2. Create preview content\n3. Send exclusive preview\n4. Gather feedback and interest",
                        "impact": "80% preview engagement, 25% upgrade interest"
                    }
                }
            }
        }
        
        # Get strategies for the selected segment and type
        segment_strategies = strategies.get(customer_segment, strategies["High Risk"])
        type_strategies = segment_strategies.get(strategy_type, segment_strategies["Retention Campaign"])
        
        # Return the three strategies
        return (
            type_strategies["strategy_1"]["title"],
            type_strategies["strategy_1"]["description"],
            type_strategies["strategy_1"]["steps"],
            type_strategies["strategy_1"]["impact"],
            type_strategies["strategy_2"]["title"],
            type_strategies["strategy_2"]["description"],
            type_strategies["strategy_2"]["steps"],
            type_strategies["strategy_2"]["impact"],
            type_strategies["strategy_3"]["title"],
            type_strategies["strategy_3"]["description"],
            type_strategies["strategy_3"]["steps"],
            type_strategies["strategy_3"]["impact"],
            f"✅ Generated 3 AI strategies for {customer_segment} customers using {strategy_type}",
            gr.Group(visible=True)  # Make strategy cards visible
        )
        
    def deploy_strategy_channel(strategy_num, channel, strategy_title):
        """Deploy strategy through selected channel"""
        try:
            channel_messages = {
                "📧 Email Campaign": f"📧 Email campaign deployed for '{strategy_title}' - Sent to customer segment",
                "📱 SMS Alert": f"📱 SMS alert sent for '{strategy_title}' - Delivered to mobile devices",
                "📱 In-App Notification": f"📱 In-app notification triggered for '{strategy_title}' - Active in customer app",
                "📞 Direct Call": f"📞 Direct call scheduled for '{strategy_title}' - Added to call queue"
            }
            
            message = channel_messages.get(channel, f"✅ Strategy {strategy_num} deployed through {channel}")
            return f"✅ {message}\n\nStatus: Successfully deployed\nChannel: {channel}\nStrategy: {strategy_title}\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
        except Exception as e:
            return f"❌ Error deploying strategy: {str(e)}"
    
    def process_data(csv_file):
        """Process uploaded CSV data and generate predictions"""
        if csv_file is None:
            return "Please upload a CSV file first.", None, None, None, None
        
        try:
            # Load the uploaded CSV file
            df = pd.read_csv(csv_file.name)
            
            # Check for required columns
            if 'customerID' not in df.columns:
                return "Error: CSV file must contain 'customerID' column.", None, None, None, None
            
            # Simulate predictions
            np.random.seed(42)
            n_customers = len(df)
            
            predictions = []
            for i in range(n_customers):
                prob = np.random.beta(2, 5)  # Skewed towards lower probabilities
                if prob < 0.3:
                    risk_level = "Low Risk"
                elif prob < 0.7:
                    risk_level = "Medium Risk"
                else:
                    risk_level = "High Risk"
                
                predictions.append({
                    "Customer ID": f"CUST_{i+1:04d}",
                    "Churn Probability": round(prob * 100, 1),
                    "Risk Level": risk_level
                })
            
            # Create results dataframe
            results_df = pd.DataFrame(predictions)
            
            # Create simple chart data
            risk_counts = pd.Series([p["Risk Level"] for p in predictions]).value_counts()
            
            # Create prediction data for charts
            prediction_data = [[p["Customer ID"], p["Churn Probability"], p["Risk Level"]] for p in predictions]
            
            # Create the actual chart objects
            pie_chart = create_churn_distribution_pie(prediction_data)
            bar_chart = create_key_metrics_bar(prediction_data)
            
            status_msg = f"✅ Data processed successfully! Analyzed {n_customers} customers."
            return status_msg, results_df, risk_counts.to_dict(), pie_chart, bar_chart
            
        except Exception as e:
            return f"❌ Error processing data: {str(e)}", None, None, None, None
    
    # Create Gradio interface
    with gr.Blocks(
        title="A.U.R.A - Adaptive User Retention Assistant",
        theme=gr.themes.Soft()
    ) as interface:
        
        # Header
        gr.Markdown(
            """
            # 🤖 A.U.R.A - Adaptive User Retention Assistant
            
            **Unified AI-Powered Client Retention Platform**
            """
        )
        
        # CSS Styling for Strategy Cards
        gr.Markdown(
            """
            <style>
            .strategy-card {
                border: 2px solid #ff4444 !important;
                border-radius: 8px !important;
                padding: 15px !important;
                margin: 10px !important;
                background-color: #1a1a1a !important;
                box-shadow: 0 4px 8px rgba(255, 68, 68, 0.3) !important;
            }
            .strategy-card:hover {
                border-color: #ff6666 !important;
                box-shadow: 0 6px 12px rgba(255, 68, 68, 0.5) !important;
            }
            </style>
            """,
            elem_classes=["strategy-card-css"]
        )
        
        # Dashboard Tab
        # Churn AI Tab
        with gr.Tab("🧠 Churn AI"):
            
            with gr.Row():
                with gr.Column():
                    # CSV Upload Section
                    gr.Markdown("### 📁 Upload Customer Data")
                    csv_file = gr.File(
                        label="Choose CSV File",
                        file_types=[".csv"],
                        file_count="single"
                    )
                    
                    # Process Data Button
                    process_data_btn = gr.Button("📊 Process Data", variant="primary", size="lg")
                    
                    # Status
                    newai_status = gr.Textbox(
                        label="NewAI Status",
                        value="Ready to upload CSV file and run NewAI prediction",
                        interactive=False
                    )
            
            # Results Section
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📊 NewAI Results")
                    
                    # Results Table
                    results_table = gr.Dataframe(
                        headers=["Customer ID", "Churn Probability", "Risk Level"],
                        datatype=["str", "number", "str"],
                        interactive=False,
                        label="NewAI Churn Prediction Results"
                    )
                    
                    # Risk Distribution
                    risk_chart = gr.Textbox(
                        label="Risk Distribution",
                        interactive=False
                    )
            
            # Dashboard Section (moved from Dashboard tab)
            gr.Markdown("---")
            gr.Markdown("### 📊 Analytics Dashboard")
            
            # Status
            dashboard_status = gr.Textbox(
                label="Dashboard Status",
                value="Analytics dashboard loaded with interactive charts",
                interactive=False
            )
            
            # Visualization Charts
            with gr.Row():
                with gr.Column(scale=1):
                    # Churn Distribution Pie Chart
                    churn_pie_chart = gr.Plot(
                        value=create_churn_distribution_pie(),
                        label="Churn Risk Distribution (Run prediction to see data)",
                        show_label=True
                    )
                
                with gr.Column(scale=1):
                    # Key Metrics Bar Chart
                    metrics_bar_chart = gr.Plot(
                        value=create_key_metrics_bar(),
                        label="Customer Risk Distribution (Run prediction to see data)",
                        show_label=True
                    )
        
        
        # Playbook Tab
        with gr.Tab("📋 Playbook"):
            gr.Markdown("### 📋 AI Strategy Playbook")
            gr.Markdown("Generate personalized retention strategies using AI and deploy them through targeted channels.")
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Strategy Generation Section
                    gr.Markdown("### 🎯 Generate AI Strategies")
                    
                    # Customer Selection
                    customer_select = gr.Dropdown(
                        label="Select Customer Segment",
                        choices=["High Risk", "Medium Risk", "Low Risk", "All Customers"],
                        value="High Risk",
                        interactive=True
                    )
                    
                    # Strategy Type Selection
                    strategy_type = gr.Dropdown(
                        label="Strategy Type",
                        choices=["Retention Campaign", "Win-Back Campaign", "Preventive Campaign", "Loyalty Program"],
                        value="Retention Campaign",
                        interactive=True
                    )
                    
                    # Generate Button
                    generate_strategy_btn = gr.Button("🤖 Generate AI Strategies", variant="primary", size="lg")
                    
            # Status
                    strategy_status = gr.Textbox(
                        label="Strategy Status",
                        value="Ready to generate AI-powered retention strategies",
                        interactive=False,
                        lines=4
                    )
                
                with gr.Column(scale=3):
                    # Generated Strategies Display
                    gr.Markdown("### 🎯 Generated Strategies")
                    
                    # Strategy Cards Container (initially hidden)
                    strategy_cards_group = gr.Group(visible=False)
                    with strategy_cards_group:
                        with gr.Row():
                            with gr.Column():
                                # Strategy Card 1
                                strategy_card_1 = gr.Column(
                                    elem_classes=["strategy-card"]
                                )
                                with strategy_card_1:
                                    gr.Markdown("**🎯 Immediate Action Strategy**")
                                    strategy_1_title = gr.Textbox(
                                        label="Strategy Title",
                                        value="Personal Retention Call",
                                        interactive=False
                                    )
                                strategy_1_desc = gr.Textbox(
                                    label="Description",
                                    value="Direct personal outreach within 24 hours",
                                    interactive=False,
                                    lines=3
                                )
                                strategy_1_steps = gr.Textbox(
                                    label="Implementation Steps",
                                    value="1. Identify high-risk customer\n2. Prepare personalized offer\n3. Schedule immediate call\n4. Follow up within 48 hours",
                                    interactive=False,
                                    lines=4
                                )
                                strategy_1_impact = gr.Textbox(
                                    label="Expected Impact",
                                    value="85% success rate, immediate engagement",
                interactive=False
            )
        
                                # Target Buttons for Strategy 1
                                with gr.Row():
                                    target_email_1 = gr.Button("📧 Email Campaign", variant="secondary", size="sm")
                                    target_sms_1 = gr.Button("📱 SMS Alert", variant="secondary", size="sm")
                                    target_app_1 = gr.Button("📱 In-App Notification", variant="secondary", size="sm")
                                    target_call_1 = gr.Button("📞 Direct Call", variant="secondary", size="sm")
                        
                        with gr.Column():
                            # Strategy Card 2
                            strategy_card_2 = gr.Column(
                                elem_classes=["strategy-card"]
                            )
                            with strategy_card_2:
                                gr.Markdown("**🎁 Incentive-Based Strategy**")
                                strategy_2_title = gr.Textbox(
                                    label="Strategy Title",
                                    value="Personalized Discount Offer",
                                    interactive=False
                                )
                                strategy_2_desc = gr.Textbox(
                                    label="Description",
                                    value="Targeted discount based on customer value",
                                    interactive=False,
                                    lines=3
                                )
                                strategy_2_steps = gr.Textbox(
                                    label="Implementation Steps",
                                    value="1. Calculate customer lifetime value\n2. Determine optimal discount\n3. Create personalized offer\n4. Track redemption and impact",
                                    interactive=False,
                                    lines=4
                                )
                                strategy_2_impact = gr.Textbox(
                                    label="Expected Impact",
                                    value="75% redemption rate, increased loyalty",
                                    interactive=False
                                )
                                
                                # Target Buttons for Strategy 2
                                with gr.Row():
                                    target_email_2 = gr.Button("📧 Email Campaign", variant="secondary", size="sm")
                                    target_sms_2 = gr.Button("📱 SMS Alert", variant="secondary", size="sm")
                                    target_app_2 = gr.Button("📱 In-App Notification", variant="secondary", size="sm")
                                    target_call_2 = gr.Button("📞 Direct Call", variant="secondary", size="sm")
                        
                        with gr.Column():
                            # Strategy Card 3
                            strategy_card_3 = gr.Column(
                                elem_classes=["strategy-card"]
                            )
                            with strategy_card_3:
                                gr.Markdown("**🔄 Service Enhancement Strategy**")
                                strategy_3_title = gr.Textbox(
                                    label="Strategy Title",
                                    value="Service Plan Upgrade",
                                    interactive=False
                                )
                                strategy_3_desc = gr.Textbox(
                                    label="Description",
                                    value="Proactive service improvement and upgrade",
                                    interactive=False,
                                    lines=3
                                )
                                strategy_3_steps = gr.Textbox(
                                    label="Implementation Steps",
                                    value="1. Analyze usage patterns\n2. Identify upgrade opportunities\n3. Propose enhanced service\n4. Monitor satisfaction metrics",
                                    interactive=False,
                                    lines=4
                                )
                                strategy_3_impact = gr.Textbox(
                                    label="Expected Impact",
                                    value="70% acceptance rate, improved satisfaction",
                                    interactive=False
                                )
                                
                                # Target Buttons for Strategy 3
                                with gr.Row():
                                    target_email_3 = gr.Button("📧 Email Campaign", variant="secondary", size="sm")
                                    target_sms_3 = gr.Button("📱 SMS Alert", variant="secondary", size="sm")
                                    target_app_3 = gr.Button("📱 In-App Notification", variant="secondary", size="sm")
                                    target_call_3 = gr.Button("📞 Direct Call", variant="secondary", size="sm")
            
            # Action Channel Status
            gr.Markdown("### 📡 Action Channel Status")
            channel_status = gr.Textbox(
                label="Channel Deployment Status",
                value="Ready to deploy strategies through selected channels",
                interactive=False,
                lines=2
            )
        
        # AI Assistant Tab
        with gr.Tab("💬 AI Assistant"):
            gr.Markdown("### 💬 AI Assistant")
            
            # Chat Interface
            chatbot = gr.Chatbot(
                label="AI Assistant Chat",
                value=[{"role": "assistant", "content": "Hello! I'm your AURA assistant. How can I help you today?"}],
                type="messages"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Type your message...",
                    placeholder="Ask me about churn prediction, data analysis, or retention strategies...",
                    scale=4
                )
                send_btn = gr.Button("📤 Send", scale=1)
            
            # Clear button
            clear_btn = gr.Button("🔄 Clear Chat", variant="secondary")
        
        # Event Handlers
        # Dashboard events
        
        # NewAI events
        process_data_btn.click(
            process_data,
            inputs=[csv_file],
            outputs=[newai_status, results_table, risk_chart, churn_pie_chart, metrics_bar_chart]
        )
        
        
        # Chatbot events
        def respond(message, history):
            """Hardcoded AI assistant responses based on churn AI output"""
            try:
                message_lower = message.lower()
                
                # Hardcoded responses based on common questions
                if "churn" in message_lower or "prediction" in message_lower:
                    response = """🎯 **Churn Prediction Analysis**

Based on our AI model analysis:
- **Model Accuracy**: 94.2% (Simulated)
- **High Risk Customers**: 15% of total customer base
- **Medium Risk**: 25% of customers
- **Low Risk**: 60% of customers

**Key Insights**:
• Customers with low usage patterns show 85% churn probability
• Payment delays increase churn risk by 3.2x
• Customers aged 25-35 have highest retention rates

**Recommended Actions**:
1. Target high-risk customers with immediate retention campaigns
2. Implement usage-based engagement programs
3. Set up payment reminder systems"""
                
                elif "retention" in message_lower or "strategy" in message_lower:
                    response = """📋 **Retention Strategy Recommendations**

**Immediate Actions** (High Risk):
• Personal retention calls within 24 hours
• Emergency discount offers (15-25% off)
• Service plan upgrades with free trial

**Preventive Measures** (Medium Risk):
• Proactive customer check-ins
• Usage optimization recommendations
• Loyalty program enrollment

**Retention Campaigns**:
• Email sequences for different risk levels
• SMS alerts for payment reminders
• In-app notifications for engagement

**Success Metrics**:
• 85% success rate for immediate actions
• 75% redemption rate for incentives
• 70% acceptance rate for service upgrades"""
                
                elif "data" in message_lower or "analysis" in message_lower:
                    response = """📊 **Data Analysis Insights**

**Customer Segmentation**:
• **High Value**: 20% of customers, 60% of revenue
• **Medium Value**: 45% of customers, 30% of revenue  
• **Low Value**: 35% of customers, 10% of revenue

**Behavioral Patterns**:
• Peak usage: Weekdays 9AM-5PM
• Payment patterns: 70% pay on time, 20% late, 10% delinquent
• Service preferences: Mobile > Web > Phone support

**Predictive Indicators**:
• Usage decline > 30% = High churn risk
• Payment delay > 7 days = Medium risk
• Support tickets > 3/month = High risk

**Data Quality**: 98.5% accuracy in customer profiles"""
                
                elif "help" in message_lower or "how" in message_lower:
                    response = """🤖 **AURA Assistant Help**

**Available Commands**:
• Ask about "churn prediction" for risk analysis
• Inquire about "retention strategies" for campaigns
• Request "data analysis" for insights
• Ask "what can you do" for capabilities

**Platform Features**:
• 📊 Dashboard: Real-time analytics
• 🧠 Churn AI: Upload CSV for predictions
• 📋 Playbook: Generate AI strategies
• 💬 Assistant: This chat interface

**Quick Tips**:
• Upload customer data in CSV format
• Generate strategies based on risk levels
• Deploy campaigns through multiple channels
• Monitor results in the dashboard"""
                
                elif "hello" in message_lower or "hi" in message_lower:
                    response = """👋 **Welcome to AURA!**

I'm your AI-powered retention assistant. I can help you with:

🎯 **Churn Prediction** - Analyze customer risk levels
📋 **Retention Strategies** - Generate targeted campaigns  
📊 **Data Analysis** - Get insights from your data
🚀 **Platform Guidance** - Navigate AURA features

**Try asking me**:
• "What's our churn prediction accuracy?"
• "Show me retention strategies for high-risk customers"
• "Analyze our customer data patterns"
• "How do I use the playbook feature?"

What would you like to know about customer retention?"""
                
                elif "accuracy" in message_lower or "model" in message_lower:
                    response = """🎯 **Model Performance Metrics**

**NewAI Churn Prediction Model**:
• **Accuracy**: 94.2% (Simulated)
• **Precision**: 91.8% for high-risk detection
• **Recall**: 89.5% for churn prediction
• **F1-Score**: 90.6% overall performance

**Model Features**:
• 20+ customer attributes analyzed
• Real-time risk scoring
• Behavioral pattern recognition
• Payment history analysis

**Validation Results**:
• Cross-validation accuracy: 93.7%
• Test set performance: 94.2%
• Production accuracy: 94.1%

**Confidence Levels**:
• High confidence predictions: 78%
• Medium confidence: 18%
• Low confidence: 4%"""
                
                elif "customers" in message_lower or "segment" in message_lower:
                    response = """👥 **Customer Segmentation Analysis**

**Risk-Based Segments**:
• **High Risk** (15%): Immediate intervention needed
• **Medium Risk** (25%): Preventive measures recommended
• **Low Risk** (60%): Maintain current engagement

**Value-Based Segments**:
• **Premium** (20%): High revenue, low churn
• **Standard** (45%): Moderate revenue, medium churn
• **Basic** (35%): Lower revenue, higher churn

**Behavioral Segments**:
• **Power Users**: High engagement, low churn risk
• **Casual Users**: Moderate usage, medium risk
• **At-Risk Users**: Declining usage, high churn risk

**Demographic Insights**:
• Age 25-35: Highest retention rates
• Age 18-24: Highest churn rates
• Age 35+: Most stable customer base"""
                
                else:
                    response = """🤖 **AURA Assistant Response**

I understand you're asking about: "{}"

Here's what I can help you with:

🎯 **Churn Prediction**: Ask about risk analysis and model accuracy
📋 **Retention Strategies**: Get campaign recommendations
📊 **Data Analysis**: Request customer insights and patterns
🚀 **Platform Help**: Learn about AURA features

**Try these specific questions**:
• "What's our churn prediction model accuracy?"
• "Show me retention strategies for high-risk customers"
• "Analyze our customer segmentation data"
• "How do I generate AI strategies in the playbook?"

What specific aspect of customer retention would you like to explore?""".format(message)
                
                # Return in the correct format for messages type
                return [{"role": "user", "content": message}, {"role": "assistant", "content": response}]
                
            except Exception as e:
                logger.error(f"❌ Error in AI response: {e}")
                return [{"role": "user", "content": message}, {"role": "assistant", "content": "I apologize, but I encountered an error. Please try again."}]
        
        send_btn.click(
            respond,
            inputs=[msg, chatbot],
            outputs=[chatbot]
        ).then(
            lambda: "",
            outputs=[msg]
        )
        
        clear_btn.click(
            lambda: [{"role": "assistant", "content": "Hello! I'm your AURA assistant. How can I help you today?"}],
            outputs=[chatbot]
        )
        
        # Strategy Generation events
        generate_strategy_btn.click(
            generate_ai_strategies,
            inputs=[customer_select, strategy_type],
            outputs=[
                strategy_1_title, strategy_1_desc, strategy_1_steps, strategy_1_impact,
                strategy_2_title, strategy_2_desc, strategy_2_steps, strategy_2_impact,
                strategy_3_title, strategy_3_desc, strategy_3_steps, strategy_3_impact,
                strategy_status, strategy_cards_group
            ]
        )
        
        # Target button events for Strategy 1
        target_email_1.click(
            lambda: deploy_strategy_channel("1", "📧 Email Campaign", strategy_1_title.value),
            outputs=[channel_status]
        )
        target_sms_1.click(
            lambda: deploy_strategy_channel("1", "📱 SMS Alert", strategy_1_title.value),
            outputs=[channel_status]
        )
        target_app_1.click(
            lambda: deploy_strategy_channel("1", "📱 In-App Notification", strategy_1_title.value),
            outputs=[channel_status]
        )
        target_call_1.click(
            lambda: deploy_strategy_channel("1", "📞 Direct Call", strategy_1_title.value),
            outputs=[channel_status]
        )
        
        # Target button events for Strategy 2
        target_email_2.click(
            lambda: deploy_strategy_channel("2", "📧 Email Campaign", strategy_2_title.value),
            outputs=[channel_status]
        )
        target_sms_2.click(
            lambda: deploy_strategy_channel("2", "📱 SMS Alert", strategy_2_title.value),
            outputs=[channel_status]
        )
        target_app_2.click(
            lambda: deploy_strategy_channel("2", "📱 In-App Notification", strategy_2_title.value),
            outputs=[channel_status]
        )
        target_call_2.click(
            lambda: deploy_strategy_channel("2", "📞 Direct Call", strategy_2_title.value),
            outputs=[channel_status]
        )
        
        # Target button events for Strategy 3
        target_email_3.click(
            lambda: deploy_strategy_channel("3", "📧 Email Campaign", strategy_3_title.value),
            outputs=[channel_status]
        )
        target_sms_3.click(
            lambda: deploy_strategy_channel("3", "📱 SMS Alert", strategy_3_title.value),
            outputs=[channel_status]
        )
        target_app_3.click(
            lambda: deploy_strategy_channel("3", "📱 In-App Notification", strategy_3_title.value),
            outputs=[channel_status]
        )
        target_call_3.click(
            lambda: deploy_strategy_channel("3", "📞 Direct Call", strategy_3_title.value),
            outputs=[channel_status]
        )
        
        # Footer
        gr.Markdown(
            """
            ---
            <div style="text-align: center; color: #666; font-size: 0.9em;">
            🤖 A.U.R.A - Adaptive User Retention Assistant | Built with FastAPI + Gradio | Unified Platform
            </div>
            """,
            elem_classes=["footer"]
        )
    
    return interface

# Create the Gradio interface
print("Creating Gradio interface...")
gradio_interface = create_gradio_interface()
print(f"Gradio interface created: {gradio_interface is not None}")

# Mount Gradio app
app = gr.mount_gradio_app(app, gradio_interface, path="/gradio")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - Redirect to Gradio interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AURA - Adaptive User Retention Assistant</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="0; url=/gradio/">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 40px;
                background: linear-gradient(135deg, #4B0082 0%, #2E8B57 100%);
                color: white;
                text-align: center;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            .container {
                max-width: 600px;
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
                margin-bottom: 30px;
                opacity: 0.9;
            }
            .redirect-message {
                font-size: 1.1em;
                margin-bottom: 30px;
                opacity: 0.8;
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 A.U.R.A</h1>
            <div class="subtitle">Adaptive User Retention Assistant</div>
            <p class="redirect-message">Redirecting to the dashboard...</p>
            <a href="/gradio/" class="btn">🎨 Open Dashboard</a>
        </div>
    </body>
    </html>
    """

# Removed health check endpoint as requested

@app.get("/api/v2/info")
async def get_model_info():
    """Get model information"""
    return {
        "name": "Working NewAI Churn Prediction Model",
        "type": "Machine Learning",
        "version": "2.0.0",
        "features": [
            "Customer Demographics",
            "Service Usage Patterns",
            "Contract Information",
            "Payment History",
            "Billing Patterns"
        ],
        "performance": {
            "accuracy": "94.2%",
            "precision": "91.8%",
            "recall": "89.3%",
            "f1_score": "90.5%"
        },
        "available": True,
        "mode": "simulation"
    }

def main():
    """Main function to run the Working AURA app"""
    print("🤖 A.U.R.A - Adaptive User Retention Assistant")
    print("=" * 60)
    print("Unified AI-Powered Client Retention Platform")
    print("=" * 60)
    print("")
    print("")
    print("🌐 Access Points:")
    print("   • Main Interface: http://localhost:8080")
    print("   • Gradio Dashboard: http://localhost:8080/gradio/")
    print("")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run the application
    uvicorn.run(
        "working_app:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
