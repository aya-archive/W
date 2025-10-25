# 🤖 A.U.R.A - Adaptive User Retention Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-green.svg)](https://gradio.app)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-aya--archive%2FAURAAI-blue.svg)](https://github.com/aya-archive/AURAAI)

> **AI-Powered Client Retention Platform with NewAI Churn Prediction Integration**

A.U.R.A is a comprehensive AI-powered platform designed to help businesses analyze client data, predict churn risk, and implement effective retention strategies. The platform combines modern web interfaces, machine learning models, and intelligent chatbots to provide actionable insights for client retention.

## 🌟 **Key Features**

### 🎯 **Core Capabilities**
- **🤖 AI-Powered Analysis**: Advanced machine learning for churn prediction
- **📊 Interactive Dashboards**: Real-time data visualization and insights
- **💬 Intelligent Chatbot**: Natural language processing for data queries
- **📈 Forecasting**: Revenue and engagement predictions
- **🎯 Risk Assessment**: Customer risk analysis and prioritization
- **📋 Data Management**: CSV upload, processing, and export functionality

### 🧠 **NewAI Integration**
- **Churn Prediction Model**: Advanced ML model for customer churn prediction
- **Risk Classification**: Low/Medium/High risk customer categorization
- **Probability Scoring**: 0-100% churn probability for each customer
- **Feature Analysis**: Demographics, usage patterns, contract information
- **API Integration**: RESTful API for model predictions

### 🌐 **Multi-Interface Support**
- **Modern Web Interface**: Beautiful, responsive dashboard with tab navigation
- **Gradio Interface**: AI-focused interface for data analysis
- **REST API**: Programmatic access to all features
- **Multi-Service Architecture**: Scalable, modular design

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8 or higher
- pip package manager

### **Installation**
```bash
# Clone the repository
git clone https://github.com/aya-archive/AURAAI.git
cd AURAAI

# Install dependencies
pip install -r requirements.txt
```

### **Launch Options**

#### **Option 1: Complete Platform (Recommended)**
```bash
python3 launch_complete.py
```
Choose "All Services" for complete functionality.

#### **Option 2: Individual Services**
```bash
# Web Interface with NewAI tab
python3 web_server.py

# Gradio Interface
python3 app.py

# NewAI API Server
python3 newai_api.py
```

### **Access Points**
- **🌐 Web Interface**: http://localhost:8080
- **🤖 Gradio Interface**: http://localhost:7865
- **🧠 NewAI API**: http://localhost:8081

## 📊 **Platform Components**

### **🌐 Web Interface**
- **Tab Navigation**: Dashboard, NewAI, Data Management
- **Interactive Charts**: Risk distribution, forecasting, engagement
- **AI Chatbot**: Natural language processing for data queries
- **Real-time Updates**: Live data refresh and analysis
- **Responsive Design**: Works on all devices

### **🤖 Gradio Interface**
- **AI Chatbot**: Intelligent assistant for data analysis
- **Risk Analysis**: Customer risk assessment and scoring
- **Forecasting**: Revenue and engagement predictions
- **Data Pipeline**: Automated data processing and validation
- **Decision Engine**: Rule-based retention strategies

### **🧠 NewAI Integration**
- **Churn Prediction**: Advanced ML model for customer churn
- **Risk Classification**: Automated risk level assignment
- **Feature Analysis**: Comprehensive customer data analysis
- **API Endpoints**: RESTful API for model predictions
- **Data Export**: CSV export of predictions and insights

## 🎯 **Usage Examples**

### **Web Interface**
1. **Access Dashboard**: Navigate to http://localhost:8080
2. **Upload Data**: Use the Data Management tab to upload CSV files
3. **Run Analysis**: Use the NewAI tab for churn prediction
4. **Chat with AI**: Ask questions about your data using the chatbot
5. **Export Results**: Download predictions and insights

### **AI Chatbot Commands**
- "Show me high-risk customers"
- "Generate revenue forecast for next quarter"
- "Analyze customer engagement patterns"
- "Run NewAI churn prediction model"
- "Export customer data with risk scores"

### **NewAI Model**
- **Input**: Customer demographics, service usage, contract info
- **Output**: Churn probability (0-100%), risk level (Low/Medium/High)
- **Features**: 20+ customer attributes analyzed
- **Accuracy**: 94.2% prediction accuracy

## 📁 **Project Structure**

```
A.U.R.A/
├── 📱 Main Applications
│   ├── app.py                    # Gradio interface
│   ├── web_interface.html       # Modern web dashboard
│   ├── web_server.py            # Web server
│   └── launch_complete.py       # Complete launcher
├── 🧠 NewAI Integration
│   ├── newai_integration.py     # NewAI model integration
│   └── newai_api.py             # NewAI API server
├── 📦 Core Components
│   ├── src/
│   │   ├── config/              # Configuration management
│   │   ├── data_pipeline/       # Data processing
│   │   └── models/              # AI/ML models
├── 📋 Documentation
│   ├── README.md                # This file
│   ├── INTERFACE_GUIDE.md       # Web interface guide
│   ├── NEWAI_INTEGRATION.md     # NewAI integration guide
│   └── GITHUB_SETUP.md          # GitHub setup guide
├── ⚙️ Configuration
│   ├── requirements.txt         # Dependencies
│   └── public/                  # PWA assets
└── 📊 Data & Logs
    ├── data/                    # Data directories
    └── logs/                    # System logs
```

## 🔧 **API Endpoints**

### **NewAI API (Port 8081)**
- `GET /api/newai/info` - Model information
- `GET /api/newai/predict` - Run churn predictions
- `POST /api/newai/upload` - Upload customer data
- `GET /api/newai/health` - Health check

### **Web Interface (Port 8080)**
- Interactive dashboard with real-time data
- AI chatbot for natural language queries
- Data management and export functionality
- NewAI integration with churn prediction

## 📊 **Sample Data**

The platform includes comprehensive sample data:
- **1000+ Customer Records**: Realistic client data
- **Risk Distribution**: Low/Medium/High risk classification
- **Churn Probabilities**: 0-100% risk scores
- **Customer Attributes**: Demographics, usage, billing, contracts
- **Engagement Metrics**: Interaction scores and patterns

## 🎨 **Screenshots**

### **Web Interface Dashboard**
- Modern, responsive design with tab navigation
- Interactive charts and visualizations
- AI chatbot integration
- Real-time data updates

### **NewAI Churn Prediction**
- Model performance metrics
- Risk distribution charts
- Customer prediction table
- Individual customer analysis

### **Gradio Interface**
- AI chatbot for data queries
- Risk analysis and forecasting
- Data pipeline management
- Decision engine insights

## 🤝 **Contributing**

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Gradio**: For the amazing AI interface framework
- **Plotly**: For interactive data visualizations
- **Pandas**: For data manipulation and analysis
- **Scikit-learn**: For machine learning capabilities
- **NewAI**: For the churn prediction model

## 📞 **Support**

- **Documentation**: Check the guides in the `/docs` directory
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join the community discussions
- **Email**: Contact the development team

## 🚀 **Roadmap**

### **Upcoming Features**
- [ ] Advanced ML models for different industries
- [ ] Real-time data streaming integration
- [ ] Mobile app for on-the-go analysis
- [ ] Advanced visualization options
- [ ] Multi-language support
- [ ] Cloud deployment options

### **Recent Updates**
- ✅ NewAI churn prediction integration
- ✅ Modern web interface with tab navigation
- ✅ REST API for programmatic access
- ✅ Comprehensive documentation
- ✅ Multi-service architecture

---

**Built with ❤️ by the A.U.R.A Team**

*Empowering businesses with AI-driven client retention strategies*# AURAAI
