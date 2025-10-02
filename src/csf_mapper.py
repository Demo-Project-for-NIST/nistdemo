"""
NIST CSF 2.0 mapping engine for AI/ML risks.

Maps AI system risks to appropriate NIST Cybersecurity Framework categories.
"""
import json
import os
from typing import Dict, List, Optional
from .models import CSFGap, RiskLevel


class CSFMapper:
    """Maps AI/ML risks to NIST CSF 2.0 categories."""
    
    def __init__(self):
        """Initialize with CSF and AI risk data."""
        self.csf_data = self._load_csf_data()
        self.ai_risks = self._load_ai_risks()
    
    def _load_csf_data(self) -> Dict:
        """Load NIST CSF 2.0 category data."""
        data_path = os.path.join(os.path.dirname(__file__), "data", "csf_categories.json")
        try:
            with open(data_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSF data file not found at {data_path}")
    
    def _load_ai_risks(self) -> Dict:
        """Load AI risk category data."""
        data_path = os.path.join(os.path.dirname(__file__), "data", "ai_risks.json")
        try:
            with open(data_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"AI risks data file not found at {data_path}")
    
    def map_risk_to_csf(self, risk_type: str) -> Optional[Dict]:
        """
        Map a specific AI risk type to NIST CSF categories.
        
        Args:
            risk_type: AI risk category (e.g., 'training_data_poisoning')
            
        Returns:
            Dictionary with mapped CSF categories and description
        """
        if risk_type not in self.ai_risks["ai_risk_categories"]:
            return None
        
        risk_data = self.ai_risks["ai_risk_categories"][risk_type]
        
        # Map to CSF categories with severity assessment and descriptions
        mapped_categories = []
        for csf_category in risk_data["csf_mappings"]:
            severity = self._assess_category_severity(risk_type, csf_category)
            description = self.get_csf_category_description(csf_category)
            
            mapped_categories.append({
                "code": csf_category,
                "severity": severity,
                "description": description or f"NIST CSF category {csf_category}"
            })
        
        return {
            "categories": mapped_categories,
            "description": risk_data["description"],
            "supply_chain_impact": risk_data["supply_chain_impact"]
        }
    
    def identify_gaps(self, system_config: Dict, risk_assessment: Dict) -> List[CSFGap]:
        """
        Identify NIST CSF compliance gaps for an AI system.
        
        Args:
            system_config: AI system configuration
            risk_assessment: Risk assessment results
            
        Returns:
            List of CSF compliance gaps
        """
        gaps = []
        
        # Check for supply chain risk management gaps
        if not system_config.get("supply_chain_policy", False):
            gaps.append(CSFGap(
                category="GV.SC-01",
                description="Missing cybersecurity supply chain risk management strategy",
                severity=RiskLevel.HIGH
            ))
        
        # Check for data lineage gaps
        if not system_config.get("data_lineage_documented", False):
            gaps.append(CSFGap(
                category="ID.AM-03",
                description="Data flow and lineage not documented",
                severity=RiskLevel.MEDIUM
            ))
        
        # Check for model monitoring gaps
        if not system_config.get("drift_monitoring_enabled", False):
            gaps.append(CSFGap(
                category="DE.CM-07",
                description="ML model drift monitoring not implemented",
                severity=RiskLevel.HIGH
            ))
        
        # Check for third-party component assessment
        if system_config.get("third_party_libs") and not system_config.get("vendor_assessment", False):
            gaps.append(CSFGap(
                category="ID.SC-04",
                description="Third-party ML libraries not assessed for security",
                severity=RiskLevel.MEDIUM
            ))
        
        # Check for data integrity verification
        if not system_config.get("data_integrity_checks", False):
            gaps.append(CSFGap(
                category="PR.DS-06",
                description="Training data integrity verification not implemented",
                severity=RiskLevel.CRITICAL if risk_assessment.get("overall_risk_score", 0) > 70 else RiskLevel.HIGH
            ))
        
        return gaps
    
    def _assess_category_severity(self, risk_type: str, csf_category: str) -> RiskLevel:
        """
        Assess the severity level for a risk-CSF category mapping.
        
        Args:
            risk_type: AI risk type
            csf_category: NIST CSF category code
            
        Returns:
            Risk severity level
        """
        risk_data = self.ai_risks["ai_risk_categories"][risk_type]
        base_score = risk_data["base_risk_score"]
        
        # High-impact CSF categories
        critical_categories = ["GV.SC-01", "PR.DS-06", "ID.RA-01"]
        high_categories = ["DE.CM-07", "GV.SC-04", "PR.DS-08"]
        
        if csf_category in critical_categories and base_score > 30:
            return RiskLevel.CRITICAL
        elif csf_category in high_categories or base_score > 25:
            return RiskLevel.HIGH
        elif base_score > 15:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def get_csf_category_description(self, category_code: str) -> Optional[str]:
        """Get description for a CSF category code."""
        for function_name, function_data in self.csf_data["functions"].items():
            for cat_code, cat_data in function_data["categories"].items():
                if cat_code == category_code:
                    return cat_data["name"]
                if "subcategories" in cat_data:
                    for subcat_code, subcat_desc in cat_data["subcategories"].items():
                        if subcat_code == category_code:
                            return subcat_desc
        return None