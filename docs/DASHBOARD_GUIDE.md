# Visual Dashboard User Guide

## 🎯 **Fixed: Dashboard Connection Issue**

The visual dashboard connection issue has been resolved! CORS (Cross-Origin Resource Sharing) support has been added to the API server.

## 🌐 **How to Access Your Visual Dashboard**

### Method 1: Using Dashboard Server (Recommended)
```bash
# Terminal 1: Start API server
source venv/bin/activate
uvicorn src.api:app --reload --port 8001

# Terminal 2: Start dashboard server
python serve_dashboard.py --port 8080
```

**Then open:** http://localhost:8080/visual_dashboard.html

### Method 2: Direct File Access
1. Start API server: `uvicorn src.api:app --reload --port 8001`
2. Open `examples/visual_dashboard.html` in your web browser
3. The dashboard should now show: **"API Status: ✅ Connected"**

## ✅ **Dashboard Features You'll See**

### 1. **API Status Indicator**
- ✅ **Green "Connected"** = Dashboard working correctly
- ❌ **Red "Disconnected"** = API server not running

### 2. **AI System Risk Assessment Form**
- **System Name**: Enter any AI system name
- **Model Type**: Choose from dropdown (Random Forest, Neural Network, etc.)
- **Deployment Environment**: AWS, Azure, Google Cloud, On-premise
- **Data Sources**: Comma-separated list
- **Third-Party Libraries**: Comma-separated list

### 3. **Real-Time Results Display**
- **Risk Score**: 0-100 with color coding
- **Risk Level**: Critical (red), High (orange), Medium (yellow), Low (green)
- **NIST CSF Gaps**: Interactive list with severity levels
- **Recommendations**: Actionable remediation steps

### 4. **CSF Risk Mapping Explorer**
- **Dropdown**: 8 AI risk types to explore
- **Live Mapping**: See which NIST CSF categories apply
- **Severity Levels**: Color-coded risk assessment

## 🧪 **Test Your Dashboard**

### Quick Test: Load Example Data
1. Click **"Load Example"** button
2. Click **"Assess Risk"** 
3. You should see:
   - Risk score around 65-85/100
   - Multiple CSF compliance gaps
   - Specific recommendations

### Test CSF Mapping
1. Select **"Training Data Poisoning"** from dropdown
2. Click **"Explore CSF Mapping"**
3. You should see:
   - Risk description
   - 3+ mapped NIST CSF categories
   - Severity levels for each

## 🚨 **Troubleshooting Dashboard Issues**

### If Dashboard Shows "Disconnected"

**1. Check API Server Status:**
```bash
curl http://localhost:8001/health
# Should return: {"status":"healthy","service":"nist-ai-scm-toolkit"}
```

**2. Test Dashboard Connection:**
```bash
python test_dashboard_connection.py
# Should show: "Dashboard Connection Status: READY"
```

**3. Verify CORS Headers:**
```bash
curl -H "Origin: http://localhost:8080" -X OPTIONS http://localhost:8001/health
# Should return: OK with CORS headers
```

### Common Solutions

**Problem**: API Status shows "Disconnected"
**Solution**: 
```bash
# Restart API server
uvicorn src.api:app --reload --port 8001
```

**Problem**: Dashboard loads but forms don't work
**Solution**: 
```bash
# Use dashboard server instead of direct file access
python serve_dashboard.py --port 8080
```

**Problem**: Port conflicts
**Solution**:
```bash
# Use different ports
uvicorn src.api:app --reload --port 8002
python serve_dashboard.py --port 8081
# Then update API_BASE in visual_dashboard.html to http://localhost:8002
```

## 📱 **Dashboard User Experience**

### What You'll See Working:
- ✅ **Live API Status**: Real-time connection indicator
- ✅ **Interactive Forms**: Drop-downs, text inputs, buttons
- ✅ **Color-Coded Results**: Risk levels with appropriate colors
- ✅ **Professional Layout**: Clean, enterprise-ready interface
- ✅ **Real-Time Updates**: Instant results without page refresh

### Sample Assessment Results:
```
System: Credit Risk Assessment Model
Risk Score: 66/100 (High Risk)
CSF Gaps: 5 found

CRITICAL GAPS:
- PR.DS-06: Training data integrity verification not implemented

RECOMMENDATIONS:
- Develop comprehensive supply chain risk management policy
- Implement data integrity verification mechanisms
- Deploy continuous monitoring for ML model performance
```

## 🎯 **Dashboard is Perfect For:**

### Demonstrations
- **Federal Agency Demos**: Professional, government-ready interface
- **Academic Presentations**: Clear visualization of NIST CSF compliance
- **Industry Meetings**: Real-time risk assessment capabilities

### Daily Operations
- **Quick Risk Checks**: Assess new AI systems in minutes
- **Compliance Verification**: Visual CSF gap identification
- **Training**: Educational tool for NIST CSF 2.0 concepts

### Development
- **API Testing**: Interactive endpoint verification
- **Data Validation**: Visual confirmation of risk calculations
- **Integration Testing**: Verify all components working together

## 🚀 **Your Dashboard is Now Ready!**

The visual dashboard provides a **professional, user-friendly interface** for your NIST-AI-SCM Toolkit. It's perfect for:
- Demos to federal agencies
- Training sessions
- Real-world AI system assessments
- Academic research presentations

**Access it at:** http://localhost:8080/visual_dashboard.html