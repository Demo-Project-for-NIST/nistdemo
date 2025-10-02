"""
Tests for FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "NIST AI Risk Management Toolkit" in data["message"]
    assert "endpoints" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "nist-ai-risk-management-toolkit"


def test_assess_endpoint():
    """Test AI system assessment endpoint."""
    test_request = {
        "system_name": "Test Credit Risk Model",
        "model_type": "Random Forest",
        "data_sources": ["internal_db", "external_api"],
        "deployment_env": "aws",
        "third_party_libs": ["scikit-learn", "pandas"]
    }
    
    response = client.post("/assess", json=test_request)
    assert response.status_code == 200
    
    data = response.json()
    assert data["system_name"] == "Test Credit Risk Model"
    assert "overall_risk_score" in data
    assert 0 <= data["overall_risk_score"] <= 100
    assert "risk_level" in data
    assert "csf_compliance_gaps" in data
    assert "recommended_actions" in data


def test_csf_mapping_endpoint():
    """Test CSF mapping endpoint with valid risk type."""
    response = client.get("/csf-mapping/training_data_poisoning")
    assert response.status_code == 200
    
    data = response.json()
    assert data["risk_type"] == "training_data_poisoning"
    assert "mapped_categories" in data
    assert "description" in data


def test_csf_mapping_invalid_risk():
    """Test CSF mapping endpoint with invalid risk type."""
    response = client.get("/csf-mapping/invalid_risk_type")
    assert response.status_code == 404


def test_report_endpoint():
    """Test report generation endpoint."""
    test_assessment = {
        "system_name": "Test System",
        "overall_risk_score": 65,
        "risk_level": "Medium",
        "csf_compliance_gaps": [
            {
                "category": "GV.SC-01",
                "description": "Missing supply chain policy",
                "severity": "High"
            }
        ],
        "recommended_actions": ["Develop policy"]
    }
    
    test_request = {
        "organization_name": "Test Organization",
        "assessment_data": test_assessment,
        "report_format": "json"
    }
    
    response = client.post("/report", json=test_request)
    assert response.status_code == 200
    
    data = response.json()
    assert data["organization"] == "Test Organization"
    assert "executive_summary" in data
    assert "detailed_findings" in data


def test_report_invalid_format():
    """Test report endpoint with invalid format."""
    test_assessment = {
        "system_name": "Test System",
        "overall_risk_score": 65,
        "risk_level": "Medium",
        "csf_compliance_gaps": [],
        "recommended_actions": []
    }
    
    test_request = {
        "organization_name": "Test Organization",
        "assessment_data": test_assessment,
        "report_format": "invalid"
    }
    
    response = client.post("/report", json=test_request)
    assert response.status_code == 400