#!/bin/bash

# A.U.R.A GitHub Push Script
# Pushes the complete A.U.R.A project to GitHub

echo "🤖 A.U.R.A - GitHub Push Script"
echo "================================="
echo "Pushing to: https://github.com/aya-archive/AURAAI.git"
echo ""

# Navigate to AURA directory
cd /Users/aya/AURA

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "   Install with: brew install git"
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
fi

# Add remote origin
echo "🔗 Adding remote origin..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/aya-archive/AURAAI.git

# Create .gitignore file
echo "📝 Creating .gitignore file..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Data files (optional)
*.csv
*.pkl
*.pickle

# Temporary files
temp/
tmp/
EOF

# Add all files
echo "📦 Adding all files to git..."
git add .

# Create commit
echo "💾 Creating commit..."
git commit -m "Initial commit: A.U.R.A - Adaptive User Retention Assistant

🤖 A.U.R.A - Complete AI-Powered Retention Platform

Features:
- Modern web interface with tab navigation
- NewAI churn prediction model integration  
- AI chatbot assistant with natural language processing
- Interactive dashboards and visualizations
- Data management and export functionality
- REST API for NewAI model predictions
- Comprehensive documentation and guides
- Multi-service launcher for complete platform

Components:
- Web Interface (HTML/CSS/JavaScript)
- Gradio Interface (Python)
- NewAI Integration (Machine Learning)
- API Server (REST endpoints)
- Documentation (Complete guides)

Ready for deployment!"

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main

# Check if push was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Repository: https://github.com/aya-archive/AURAAI.git"
    echo ""
    echo "📊 Repository Contents:"
    echo "   • Complete A.U.R.A codebase"
    echo "   • Web interface with NewAI integration"
    echo "   • AI chatbot and retention strategies"
    echo "   • Interactive dashboards and visualizations"
    echo "   • REST API for machine learning models"
    echo "   • Comprehensive documentation"
    echo "   • Multi-service launcher"
    echo ""
    echo "🎯 Next Steps:"
    echo "   1. Clone the repository: git clone https://github.com/aya-archive/AURAAI.git"
    echo "   2. Install dependencies: pip install -r requirements.txt"
    echo "   3. Run the platform: python3 launch_complete.py"
    echo "   4. Access at: http://localhost:8080"
    echo ""
    echo "🎉 Your AI-powered retention platform is now on GitHub!"
else
    echo ""
    echo "❌ Failed to push to GitHub."
    echo "Please check your internet connection and GitHub credentials."
    echo "You may need to authenticate with GitHub first."
fi
