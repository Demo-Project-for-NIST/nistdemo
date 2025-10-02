"""
FastAPI application for NIST AI Risk Management Toolkit.

Provides REST API endpoints for AI risk assessment and NIST CSF compliance reporting.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
import os
from typing import Dict

from .models import (
    AISystemRequest, 
    RiskAssessmentResponse, 
    CSFMappingResponse, 
    CSFCategory,
    ReportRequest,
    RiskLevel
)
from .database import get_db, create_tables
from .csf_mapper import CSFMapper
from .risk_scorer import RiskScorer
from .action_planner import ActionPlanner

# Initialize FastAPI app
app = FastAPI(
    title="NIST AI Risk Management Toolkit",
    description="Open-source AI risk assessment and management, aligned with NIST CSF 2.0",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow web browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
csf_mapper = CSFMapper()
risk_scorer = RiskScorer()
action_planner = ActionPlanner()

# Create database tables on startup
create_tables()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "NIST AI Risk Management Toolkit",
        "version": "0.1.0",
        "documentation": "/docs",
        "endpoints": {
            "assess": "POST /assess - AI system risk assessment",
            "csf-mapping": "GET /csf-mapping/{risk_type} - CSF category mapping",
            "report": "POST /report - Generate compliance report"
        }
    }


@app.post("/assess", response_model=RiskAssessmentResponse)
async def assess_ai_system(
    request: AISystemRequest, 
    db: Session = Depends(get_db)
):
    """
    Assess AI system risk and generate NIST CSF compliance gaps.
    
    This endpoint analyzes an AI/ML system configuration and returns:
    - Overall risk score (0-100)
    - Risk level classification
    - NIST CSF compliance gaps
    - Recommended remediation actions
    """
    try:
        # Calculate risk score
        risk_assessment = risk_scorer.assess_system(request.dict())
        
        # Map risks to CSF categories
        csf_gaps = csf_mapper.identify_gaps(request.dict(), risk_assessment)
        
        # Generate recommendations
        recommendations = _generate_recommendations(csf_gaps)
        
        # Generate detailed action plan
        action_plan = action_planner.generate_action_plan_simple(csf_gaps, request.dict(), risk_assessment["overall_risk_score"])
        
        # Determine risk level
        risk_level = _classify_risk_level(risk_assessment["overall_risk_score"])
        
        response = RiskAssessmentResponse(
            system_name=request.system_name,
            overall_risk_score=risk_assessment["overall_risk_score"],
            risk_level=risk_level,
            csf_compliance_gaps=csf_gaps,
            recommended_actions=recommendations,
            action_plan=action_plan
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")


@app.get("/csf-mapping/{risk_type}", response_model=CSFMappingResponse)
async def get_csf_mapping(risk_type: str):
    """
    Get NIST CSF category mappings for a specific AI risk type.
    
    Example risk types:
    - training_data_poisoning
    - model_drift
    - adversarial_examples
    - model_inversion
    """
    try:
        mapping = csf_mapper.map_risk_to_csf(risk_type)
        
        if not mapping:
            raise HTTPException(
                status_code=404, 
                detail=f"Risk type '{risk_type}' not found"
            )
        
        return CSFMappingResponse(
            risk_type=risk_type,
            mapped_categories=mapping["categories"],
            description=mapping["description"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mapping failed: {str(e)}")


@app.post("/report")
async def generate_report(request: ReportRequest):
    """
    Generate NIST CSF compliance report in PDF or JSON format.
    
    Returns downloadable compliance report with:
    - Executive summary
    - Risk assessment details
    - CSF compliance status
    - Remediation roadmap
    """
    try:
        if request.report_format not in ["pdf", "json"]:
            raise HTTPException(
                status_code=400, 
                detail="Report format must be 'pdf' or 'json'"
            )
        
        # For MVP, return JSON response
        # TODO: Implement PDF generation with ReportLab
        report_data = {
            "organization": request.organization_name,
            "assessment_date": "2024-01-01",  # TODO: Use actual date
            "executive_summary": {
                "overall_risk_score": request.assessment_data.overall_risk_score,
                "risk_level": request.assessment_data.risk_level,
                "critical_gaps": len([
                    gap for gap in request.assessment_data.csf_compliance_gaps 
                    if gap.severity == RiskLevel.CRITICAL
                ]),
                "total_gaps": len(request.assessment_data.csf_compliance_gaps)
            },
            "detailed_findings": request.assessment_data.dict(),
            "report_format": request.report_format
        }
        
        return JSONResponse(content=report_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "nist-ai-risk-management-toolkit"}


def _classify_risk_level(risk_score: int) -> RiskLevel:
    """Classify risk score into risk level."""
    if risk_score >= 80:
        return RiskLevel.CRITICAL
    elif risk_score >= 60:
        return RiskLevel.HIGH
    elif risk_score >= 40:
        return RiskLevel.MEDIUM
    else:
        return RiskLevel.LOW


def _generate_recommendations(csf_gaps) -> list:
    """Generate remediation recommendations based on CSF gaps."""
    recommendations = []
    
    gap_categories = [gap.category for gap in csf_gaps]
    
    if any("GV.SC" in cat for cat in gap_categories):
        recommendations.append("Develop comprehensive risk management policy")
    
    if any("PR.DS" in cat for cat in gap_categories):
        recommendations.append("Implement data integrity verification mechanisms")
    
    if any("DE.CM" in cat for cat in gap_categories):
        recommendations.append("Deploy continuous monitoring for ML model performance")
    
    if any("ID.RA" in cat for cat in gap_categories):
        recommendations.append("Conduct thorough risk assessment of AI system components")
    
    return recommendations or ["Continue following current security practices"]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)