"""
Pydantic models for NIST-AI-SCM Toolkit API requests and responses.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum


class RiskLevel(str, Enum):
    """Risk severity levels."""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class AISystemRequest(BaseModel):
    """Request model for AI system risk assessment."""
    system_name: str = Field(..., description="Name of the AI/ML system")
    model_type: str = Field(..., description="Type of ML model (e.g., Random Forest, Neural Network)")
    data_sources: List[str] = Field(..., description="List of data sources used")
    deployment_env: str = Field(..., description="Deployment environment")
    third_party_libs: List[str] = Field(default=[], description="Third-party libraries used")
    
    class Config:
        schema_extra = {
            "example": {
                "system_name": "Credit Risk Model v2.1",
                "model_type": "Random Forest",
                "data_sources": ["internal_db", "fred_api"],
                "deployment_env": "aws_sagemaker",
                "third_party_libs": ["scikit-learn", "pandas"]
            }
        }


class CSFGap(BaseModel):
    """NIST CSF compliance gap."""
    category: str = Field(..., description="NIST CSF category code")
    description: str = Field(..., description="Gap description")
    severity: RiskLevel = Field(..., description="Gap severity level")


class ActionPlan(BaseModel):
    """Remediation action plan."""
    action: str = Field(..., description="Remediation action description")
    category: str = Field(..., description="CSF category this addresses")
    priority: str = Field(..., description="Implementation priority")
    timeline: str = Field(..., description="Estimated timeline")
    cost_estimate: str = Field(..., description="Cost estimate range")
    success_criteria: str = Field(..., description="Success measurement criteria")
    nist_reference: str = Field(default="", description="Official NIST guideline reference link")


class RiskAssessmentResponse(BaseModel):
    """Response model for risk assessment."""
    system_name: str
    overall_risk_score: int = Field(..., ge=0, le=100, description="Risk score 0-100")
    risk_level: RiskLevel
    csf_compliance_gaps: List[CSFGap]
    recommended_actions: List[str]
    action_plan: List[ActionPlan] = Field(default=[], description="Detailed remediation action plan")
    
    class Config:
        schema_extra = {
            "example": {
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
        }


class CSFCategory(BaseModel):
    """CSF category with description."""
    code: str = Field(..., description="CSF category code")
    severity: RiskLevel = Field(..., description="Risk severity level")
    description: str = Field(..., description="Category description")


class CSFMappingResponse(BaseModel):
    """Response model for CSF risk mapping."""
    risk_type: str
    mapped_categories: List[CSFCategory]
    description: str


class ReportRequest(BaseModel):
    """Request model for compliance report generation."""
    organization_name: str = Field(..., description="Organization name")
    assessment_data: RiskAssessmentResponse
    report_format: str = Field(default="pdf", description="Report format (pdf or json)")