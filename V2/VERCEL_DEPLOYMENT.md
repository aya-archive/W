# 🚀 Deploy AURA to Vercel

## Prerequisites
1. Install Vercel CLI: `npm i -g vercel`
2. Create a Vercel account at https://vercel.com
3. Login: `vercel login`

## Deployment Steps

### 1. Prepare Your App
```bash
cd V2
# Make sure all dependencies are in requirements-vercel.txt
pip freeze > requirements-vercel.txt
```

### 2. Deploy to Vercel
```bash
# Initialize Vercel project
vercel

# Deploy
vercel --prod
```

### 3. Environment Variables (if needed)
Set these in Vercel dashboard:
- `PYTHON_VERSION=3.9`
- Any API keys or secrets your app needs

## Important Notes

### ⚠️ Limitations:
- **File Uploads**: Vercel has limits on file upload size (4.5MB)
- **Model Files**: Large ML models may need external storage
- **Memory**: Serverless functions have memory limits
- **Cold Starts**: First request may be slower

### 🔧 Optimizations:
1. **Use smaller models** or external model hosting
2. **Optimize file sizes** for uploads
3. **Consider model caching** strategies
4. **Use Vercel's edge functions** for better performance

### 📁 File Structure:
```
V2/
├── api/
│   └── index.py          # Vercel serverless function
├── V2_working_app.py     # Your main app
├── vercel.json           # Vercel configuration
├── requirements-vercel.txt
└── .vercelignore
```

## Alternative: Railway or Render
If Vercel doesn't work well, consider:
- **Railway**: Better for Python apps with persistent storage
- **Render**: Good for FastAPI + Gradio apps
- **Heroku**: Traditional but reliable for Python apps

## Testing Locally
```bash
# Test Vercel build locally
vercel dev
```

## Troubleshooting
- Check Vercel function logs in dashboard
- Ensure all dependencies are in requirements-vercel.txt
- Verify file paths are correct
- Test with smaller datasets first
