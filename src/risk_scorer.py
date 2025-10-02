"""
AI risk scoring engine for AI systems.

Quantifies AI/ML system risks using public data sources and system configuration.
"""
import json
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime


class RiskScorer:
    """Calculates risk scores for AI/ML systems in supply chains."""
    
    def __init__(self):
        """Initialize risk scorer with AI risk data."""
        self.ai_risks = self._load_ai_risks()
        self.economic_stress_cache = {}
    
    def _load_ai_risks(self) -> Dict:
        """Load AI risk categories and scoring data."""
        data_path = os.path.join(os.path.dirname(__file__), "data", "ai_risks.json")
        try:
            with open(data_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"AI risks data file not found at {data_path}")
    
    def assess_system(self, system_config: Dict) -> Dict:
        """
        Assess overall risk score for an AI/ML system.
        
        Args:
            system_config: AI system configuration dictionary
            
        Returns:
            Dictionary with risk assessment results
        """
        risk_score = 0
        risk_factors = []
        
        # Factor 1: Training data provenance (20 points max)
        if not system_config.get("data_lineage_documented", False):
            risk_score += 20
            risk_factors.append("Missing data lineage documentation")
        
        # Factor 2: Model explainability (15 points max)
        model_type = system_config.get("model_type", "").lower()
        if any(term in model_type for term in ["neural", "deep", "black"]):
            risk_score += 15
            risk_factors.append("Black-box model with limited explainability")
        
        # Factor 3: Monitoring and drift detection (25 points max)
        if not system_config.get("drift_monitoring_enabled", False):
            risk_score += 25
            risk_factors.append("No ML model drift monitoring")
        
        # Factor 4: Third-party component risk (20 points max)
        third_party_risk = self._assess_third_party_risk(system_config.get("third_party_libs", []))
        risk_score += third_party_risk
        if third_party_risk > 10:
            risk_factors.append("High-risk third-party dependencies")
        
        # Factor 5: Data security controls (15 points max)
        if not system_config.get("data_encryption", True):
            risk_score += 10
            risk_factors.append("Data encryption not implemented")
        
        if not system_config.get("access_controls", True):
            risk_score += 5
            risk_factors.append("Insufficient access controls")
        
        # Factor 6: Economic stress context (multiplier)
        economic_multiplier = self._get_economic_stress_multiplier()
        risk_score = int(risk_score * economic_multiplier)
        
        if economic_multiplier > 1.2:
            risk_factors.append(f"Elevated economic stress (multiplier: {economic_multiplier})")
        
        # Cap at 100
        risk_score = min(risk_score, 100)
        
        return {
            "overall_risk_score": risk_score,
            "risk_factors": risk_factors,
            "economic_multiplier": economic_multiplier,
            "assessment_timestamp": datetime.utcnow().isoformat()
        }
    
    def _assess_third_party_risk(self, libraries: List[str]) -> int:
        """
        Assess risk from third-party libraries and dependencies.
        
        Args:
            libraries: List of third-party library names
            
        Returns:
            Risk score (0-20)
        """
        if not libraries:
            return 0
        
        # High-risk patterns in library names
        high_risk_patterns = ["pytorch", "tensorflow", "scikit", "pandas", "numpy"]
        medium_risk_patterns = ["requests", "flask", "django"]
        
        risk_score = 0
        
        for lib in libraries:
            lib_lower = lib.lower()
            
            # Check for high-risk ML libraries (more attack surface)
            if any(pattern in lib_lower for pattern in high_risk_patterns):
                risk_score += 3
            elif any(pattern in lib_lower for pattern in medium_risk_patterns):
                risk_score += 1
            else:
                risk_score += 1  # Unknown library
        
        # Additional risk for large number of dependencies
        if len(libraries) > 10:
            risk_score += 5
        elif len(libraries) > 5:
            risk_score += 2
        
        return min(risk_score, 20)
    
    def _get_economic_stress_multiplier(self) -> float:
        """
        Get economic stress multiplier from public economic indicators.
        
        Returns:
            Multiplier value (1.0 = normal, >1.0 = stressed conditions)
        """
        try:
            # Try to get recent economic stress indicator
            # For MVP, use cached value or default
            if "stress_level" in self.economic_stress_cache:
                cached_time = self.economic_stress_cache.get("timestamp", 0)
                current_time = datetime.utcnow().timestamp()
                
                # Use cached value if less than 1 hour old
                if current_time - cached_time < 3600:
                    return self.economic_stress_cache["stress_level"]
            
            # Attempt to fetch real economic data (simplified for MVP)
            stress_level = self._fetch_economic_stress_indicator()
            
            # Cache the result
            self.economic_stress_cache = {
                "stress_level": stress_level,
                "timestamp": datetime.utcnow().timestamp()
            }
            
            return stress_level
            
        except Exception:
            # Default to normal conditions if data unavailable
            return 1.0
    
    def _fetch_economic_stress_indicator(self) -> float:
        """
        Fetch economic stress indicator from public sources.
        
        Returns:
            Stress multiplier based on economic conditions
        """
        try:
            # For MVP, simulate economic stress assessment
            # In production, this would integrate with FRED API or similar
            
            # Placeholder logic based on current date
            # In real implementation, would use actual economic indicators
            current_month = datetime.utcnow().month
            
            # Simulate varying economic conditions
            if current_month in [1, 2, 12]:  # Winter months - higher stress
                return 1.3
            elif current_month in [6, 7, 8]:  # Summer months - lower stress  
                return 1.1
            else:
                return 1.2  # Moderate stress
                
        except Exception:
            return 1.0  # Default to normal conditions
    
    def get_risk_breakdown(self, system_config: Dict) -> Dict:
        """
        Get detailed risk factor breakdown for a system.
        
        Args:
            system_config: AI system configuration
            
        Returns:
            Detailed risk factor analysis
        """
        assessment = self.assess_system(system_config)
        
        return {
            "overall_score": assessment["overall_risk_score"],
            "risk_factors": assessment["risk_factors"],
            "factor_scores": {
                "data_lineage": 20 if not system_config.get("data_lineage_documented") else 0,
                "model_explainability": 15 if self._is_black_box_model(system_config.get("model_type", "")) else 0,
                "drift_monitoring": 25 if not system_config.get("drift_monitoring_enabled") else 0,
                "third_party_risk": self._assess_third_party_risk(system_config.get("third_party_libs", [])),
                "data_security": self._assess_data_security(system_config)
            },
            "economic_context": {
                "multiplier": assessment["economic_multiplier"],
                "description": self._get_economic_description(assessment["economic_multiplier"])
            }
        }
    
    def _is_black_box_model(self, model_type: str) -> bool:
        """Check if model type is considered black-box."""
        black_box_terms = ["neural", "deep", "black", "ensemble"]
        return any(term in model_type.lower() for term in black_box_terms)
    
    def _assess_data_security(self, system_config: Dict) -> int:
        """Assess data security risk factors."""
        risk = 0
        if not system_config.get("data_encryption", True):
            risk += 10
        if not system_config.get("access_controls", True):
            risk += 5
        return risk
    
    def _get_economic_description(self, multiplier: float) -> str:
        """Get description for economic stress level."""
        if multiplier >= 2.0:
            return "Crisis-level economic stress"
        elif multiplier >= 1.5:
            return "High economic stress"
        elif multiplier >= 1.2:
            return "Moderate economic stress"
        else:
            return "Normal economic conditions"