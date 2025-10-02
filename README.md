# NIST AI Risk Management Toolkit

[![Demo](https://img.shields.io/badge/Demo-Live-brightgreen)](https://nistdemo.onrender.com/demo)
[![API Docs](https://img.shields.io/badge/API-Documentation-blue)](https://nistdemo.onrender.com/docs)
[![Status](https://img.shields.io/badge/Status-Production_Ready-green)]()

Open-source AI risk assessment and management toolkit, aligned with NIST Cybersecurity Framework 2.0.

## Live Demo

**Start Here:** [https://nistdemo.onrender.com/demo](https://nistdemo.onrender.com/demo)

### Complete Access Points:
- **Demo Landing Page**: [https://nistdemo.onrender.com/demo](https://nistdemo.onrender.com/demo) - Professional overview with status indicators
- **Interactive Dashboard**: [https://nistdemo.onrender.com/dashboard](https://nistdemo.onrender.com/dashboard) - Visual risk assessment interface
- **API Documentation (Swagger)**: [https://nistdemo.onrender.com/docs](https://nistdemo.onrender.com/docs) - Interactive API testing
- **API Documentation (ReDoc)**: [https://nistdemo.onrender.com/redoc](https://nistdemo.onrender.com/redoc) - Clean documentation format
- **API Overview**: [https://nistdemo.onrender.com/](https://nistdemo.onrender.com/) - JSON endpoint discovery

## Overview

The NIST AI Risk Management Toolkit provides automated risk assessment for AI/ML systems through a mathematically rigorous framework that maps identified risks to NIST Cybersecurity Framework 2.0 categories and generates actionable compliance reports.

### Key Features

- **Six-Factor Risk Scoring**: Mathematical framework with 95-point scale and economic stress multipliers
- **NIST CSF 2.0 Compliance**: Automated mapping to official NIST Cybersecurity Framework categories  
- **Action Plans with References**: Generated remediation plans with direct links to NIST guidelines
- **Real-time API**: FastAPI implementation with automatic OpenAPI documentation
- **Scalable Architecture**: Framework expands without breaking existing assessments
- **Standards Compliance**: Designed for NIST framework requirements
- **Live Demo**: Immediately accessible online demonstration
- **Comprehensive Reporting**: JSON and future PDF compliance reports

### Mathematical Framework

**Risk Calculation:**
```
R = min(100, (Σ wi × fi) × α)
```

Where:
- `R` = Risk score (0-100)
- `wi` = Weight for risk factor i 
- `fi` = Binary indicator for factor presence
- `α` = Economic stress multiplier (VIX + GDP based)

**Current Risk Factors (95 points total):**
- Data lineage documentation (20 points)
- Model explainability (15 points) 
- Drift monitoring (25 points)
- Third-party dependencies (20 points)
- Data encryption (10 points)
- Access controls (5 points)

### Supported AI Risk Categories

- Training data poisoning
- Model drift and performance degradation  
- Adversarial examples and attacks
- Model inversion and data extraction
- Supply chain attacks on ML pipelines
- Data lineage and provenance gaps
- Model backdoors and trojans
- AI system dependency risks

## Quick Start

### Option 1: Try Online Demo (Immediate)
Visit [https://nistdemo.onrender.com/demo](https://nistdemo.onrender.com/demo) - no installation required!

### Option 2: Local Development

**Prerequisites:** Python 3.9+ and pip

```bash
# Clone and setup
git clone <repository-url>
cd nist-ai-scm-toolkit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install and run
pip install -r requirements.txt
uvicorn src.api:app --reload --port 8001

# Access interfaces
# API Documentation: http://localhost:8001/docs
# Dashboard: Open examples/visual_dashboard.html in browser
```

### Option 3: Deploy Your Own (Render)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

See `deploy.md` for detailed deployment instructions.

### Basic Usage Example

```python
import requests

# API endpoint
base_url = "http://localhost:8000"

# AI system configuration
ai_system = {
    "system_name": "Credit Risk Model",
    "model_type": "Random Forest",
    "data_sources": ["internal_db", "credit_bureau"],
    "deployment_env": "aws_sagemaker",
    "third_party_libs": ["scikit-learn", "pandas"]
}

# Perform risk assessment
response = requests.post(f"{base_url}/assess", json=ai_system)
assessment = response.json()

print(f"Risk Score: {assessment['overall_risk_score']}/100")
print(f"Risk Level: {assessment['risk_level']}")
print(f"CSF Gaps: {len(assessment['csf_compliance_gaps'])}")
```

## API Endpoints

### POST /assess
Assess AI system risk and generate NIST CSF compliance gaps.

**Request Body:**
```json
{
  "system_name": "Credit Risk Model v2.1",
  "model_type": "Random Forest",
  "data_sources": ["internal_db", "fred_api"],
  "deployment_env": "aws_sagemaker",
  "third_party_libs": ["scikit-learn", "pandas"]
}
```

**Response:**
```json
{
  "system_name": "Credit Risk Model v2.1",
  "overall_risk_score": 45,
  "risk_level": "Medium",
  "csf_compliance_gaps": [
    {
      "category": "GV.SC-01",
      "description": "Missing supply chain risk management strategy",
      "severity": "High"
    }
  ],
  "recommended_actions": [
    "Develop supply chain risk management policy",
    "Implement model drift monitoring"
  ]
}
```

### GET /csf-mapping/{risk_type}
Get NIST CSF category mappings for specific AI risk types.

Example: `/csf-mapping/training_data_poisoning`

### POST /report
Generate compliance reports in PDF or JSON format.

### GET /health
Health check endpoint for monitoring.

## Examples

The `examples/` directory contains practical usage scenarios:

- `basic_assessment.py` - Simple risk assessment workflow
- `supply_chain_scenario.py` - Multi-system supply chain assessment
- `csf_exploration.py` - Explore NIST CSF mappings and variations

Run examples:
```bash
python examples/basic_assessment.py
python examples/supply_chain_scenario.py
python examples/csf_exploration.py
```

## NIST CSF 2.0 Alignment

The toolkit implements the complete NIST Cybersecurity Framework 2.0 with focus on:

### Core Functions
- **GOVERN**: Cybersecurity governance and risk management
- **IDENTIFY**: Asset and risk understanding  
- **PROTECT**: Safeguards implementation
- **DETECT**: Cybersecurity event detection
- **RESPOND**: Incident response actions
- **RECOVER**: Capability restoration

### Key Categories
- **GV.SC**: Supply Chain Risk Management (10 subcategories)
- **ID.RA**: Risk Assessment
- **PR.DS**: Data Security
- **DE.CM**: Continuous Monitoring
- **RS.AN**: Analysis
- **RC.RP**: Recovery Planning

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Test coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Code Quality

Format code:
```bash
ruff check src/ tests/
```

Type checking:
```bash
mypy src/
```

## Contributing

We welcome contributions from cybersecurity professionals, AI researchers, supply chain analysts, and compliance experts.

### Development Workflow

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes with tests
4. Ensure code quality (`ruff check`, `mypy src/`)
5. Run test suite (`pytest tests/`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open Pull Request

### Contribution Areas

- NIST taxonomy updates and CSF mapping accuracy
- New AI risk patterns and attack vectors
- Integration with GRC platforms and SIEM systems
- Enhanced compliance report formats
- Real-world validation scenarios
- Documentation and tutorials

### Code Standards

- 80%+ test coverage required for all PRs
- Type hints for all Python functions
- Docstrings following Google/NumPy style
- Ruff formatting and MyPy type checking must pass
- 2+ reviewer approval for core changes

## License

MIT License - see LICENSE file for details.

## Support

- GitHub Issues for bug reports and feature requests
- Discussions for questions and community support
- Documentation at `/docs` endpoint when running API server

## Citation

If you use this toolkit in research or compliance work, please cite:

```
NIST AI Risk Management Toolkit
Open-source AI risk assessment aligned with NIST CSF 2.0
GitHub: [repository-url]
```

## Acknowledgments

This project aligns with NIST Cybersecurity Framework 2.0 and AI Risk Management Framework guidelines. We thank the NIST community for their foundational work in cybersecurity standards.