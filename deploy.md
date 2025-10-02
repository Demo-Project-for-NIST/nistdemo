# NIST AI Risk Management Toolkit - Deployment Guide

## Quick Deploy to Render (5 minutes)

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub account

### 2. Deploy Web Service
- Click "New" → "Web Service"
- Connect your GitHub repository
- Configure settings:
  - **Name**: `nist-ai-risk-toolkit`
  - **Branch**: `main`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn src.api:app --host 0.0.0.0 --port $PORT`
  - **Instance Type**: Free

### 3. Deploy Static Site (Dashboard)
- Click "New" → "Static Site"
- Connect same repository
- Configure settings:
  - **Name**: `nist-ai-dashboard`
  - **Branch**: `main`
  - **Publish Directory**: `examples`

### 4. Update Dashboard URL
In `examples/visual_dashboard.html`, update line 177:
```javascript
: 'https://YOUR-SERVICE-NAME.onrender.com';
```

### 5. Test Deployment
- Visit: `https://your-service.onrender.com`
- Check API: `https://your-service.onrender.com/docs`
- Test Dashboard: `https://your-dashboard.onrender.com`

## Demo URLs (Update these after deployment)
- **Main Demo**: https://nist-ai-risk-toolkit.onrender.com
- **API Docs**: https://nist-ai-risk-toolkit.onrender.com/docs
- **Dashboard**: https://nist-ai-dashboard.onrender.com

## For NIST Evaluation
The system will be immediately accessible at the above URLs. 
No installation or setup required - ready for immediate testing.

## Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
uvicorn src.api:app --reload --port 8001

# Open dashboard
open examples/visual_dashboard.html
```

## System Status
- ✅ Mathematical framework implemented
- ✅ Six risk factors (95-point total)
- ✅ CSF 2.0 category mapping
- ✅ Action plans with NIST references
- ✅ Economic stress integration
- ⚠️ Requires empirical validation

## Contact
For technical questions or NIST collaboration:
[Your contact information]