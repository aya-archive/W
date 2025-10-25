# 🤖 V2 AURA - Ollama SmolLM 360M Integration

## Overview

V2 AURA now integrates with Ollama using the SmolLM 360M model for local AI assistance. This provides a balance of small size (~360MB) and usable performance for the AI assistant.

## 🚀 Quick Setup

### 1. Install Ollama

#### macOS
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Windows
Download from: https://ollama.ai/download

### 2. Start Ollama Service
```bash
ollama serve
```

### 3. Install SmolLM 360M Model
```bash
ollama pull smolllm:360m
```

### 4. Test Integration
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Test V2 AURA AI
curl http://localhost:8000/api/v2/ai-test
```

## 🔧 Automated Setup

Use the provided setup script:

```bash
python3 V2_setup_ollama.py
```

This script will:
- ✅ Check if Ollama is installed
- ✅ Install Ollama if needed
- ✅ Start Ollama service
- ✅ Install SmolLM 360M model
- ✅ Test integration

## 🌐 API Endpoints

### AI Information
```bash
GET /api/v2/ai-info
```
Returns AI model information and capabilities.

### AI Connection Test
```bash
GET /api/v2/ai-test
```
Tests Ollama connection and model availability.

## 🧠 AI Capabilities

The SmolLM 360M model provides:

- **Churn Prediction Guidance**: Expert advice on customer retention
- **Data Analysis Assistance**: Help with CSV uploads and processing
- **Retention Strategy Advice**: Personalized recommendations
- **Platform Navigation Help**: Guide users through V2 features
- **Analytics Interpretation**: Explain metrics and insights
- **Natural Language Processing**: Context-aware responses
- **Conversation Memory**: Remembers chat history

## 📊 Model Specifications

- **Model**: SmolLM 360M
- **Size**: ~360MB
- **Performance**: Balanced speed and quality
- **Context**: Conversation-aware responses
- **Local**: Runs entirely on your machine

## 🚀 Usage

### Start V2 AURA with Ollama
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start V2 AURA
python3 V2_working_app.py
```

### Access AI Assistant
1. Go to http://localhost:8000/gradio/
2. Click on "💬 V2 AI Assistant" tab
3. Chat with the AI assistant

## 🔍 Troubleshooting

### Ollama Not Running
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Install SmolLM 360M
ollama pull smolllm:360m
```

### Connection Issues
```bash
# Test V2 AURA AI connection
curl http://localhost:8000/api/v2/ai-test

# Check Ollama status
curl http://localhost:11434/api/tags
```

## 🎯 Benefits of SmolLM 360M

- **Small Size**: Only ~360MB download
- **Fast Inference**: Quick response times
- **Local Privacy**: No data sent to external services
- **Good Performance**: Balanced quality for most tasks
- **Easy Setup**: Simple installation and configuration

## 🔄 Fallback Mode

If Ollama is not available, the V2 AURA platform will:
- ✅ Continue to work normally
- ✅ Show connection error in AI Assistant
- ✅ Provide instructions to install Ollama
- ✅ Maintain all other functionality

## 🎉 Ready to Use!

Your V2 AURA platform now has:
- ✅ **Local AI Assistant** (SmolLM 360M)
- ✅ **Privacy-First** (no external API calls)
- ✅ **Fast Responses** (local inference)
- ✅ **Context Awareness** (conversation memory)
- ✅ **Easy Setup** (automated installation)

**Start chatting with your local AI assistant!** 🚀✨
