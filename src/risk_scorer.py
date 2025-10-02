"""
AI risk scoring engine for AI systems.

Quantifies AI/ML system risks using public data sources and system configuration.
"""
import json
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


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
        Assess overall risk score for an AI/ML system using six weighted factors.
        
        Implements the mathematical formula: R = min(100, (Σ wi × fi) × α)
        Where wi are weights [20, 15, 25, 20, 10, 5] and fi are binary indicators.
        
        The six risk factors are:
        1. Data lineage documentation (weight: 20) - Training data provenance
        2. Model explainability (weight: 15) - Black-box vs interpretable models  
        3. Drift monitoring (weight: 25) - Performance degradation detection
        4. Third-party components (weight: 20) - Dependency vulnerability assessment
        5. Data encryption (weight: 10) - Data security controls
        6. Access controls (weight: 5) - Authentication and authorization
        
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
        base_score = risk_score
        risk_score = int(risk_score * economic_multiplier)
        
        if economic_multiplier > 1.2:
            risk_factors.append(f"Elevated economic stress (multiplier: {economic_multiplier:.1f})")
        
        # Cap at 100 and ensure consistent scoring
        risk_score = min(risk_score, 100)
        
        # Add validation note for base score calculation
        if base_score > 95:
            risk_factors.append("Note: Base risk factors exceed design parameters")
        
        return {
            "overall_risk_score": risk_score,
            "risk_factors": risk_factors,
            "economic_multiplier": economic_multiplier,
            "assessment_timestamp": datetime.utcnow().isoformat()
        }
    
    def _assess_third_party_risk(self, libraries: List[str]) -> int:
        """
        Assess risk from third-party libraries using real vulnerability data.
        
        Args:
            libraries: List of third-party library names
            
        Returns:
            Risk score (0-20)
        """
        if not libraries:
            return 0
        
        risk_score = 0
        high_risk_libs = 0
        
        for lib in libraries:
            # Look up real vulnerabilities for this library
            vuln_score = self._get_library_vulnerability_score(lib)
            risk_score += vuln_score
            
            if vuln_score >= 5:  # High-risk library
                high_risk_libs += 1
        
        # Additional risk for large number of dependencies
        if len(libraries) > 15:
            risk_score += 5
        elif len(libraries) > 10:
            risk_score += 3
        elif len(libraries) > 5:
            risk_score += 1
            
        # Bonus penalty for multiple high-risk libraries
        if high_risk_libs > 3:
            risk_score += 3
        elif high_risk_libs > 1:
            risk_score += 1
        
        return min(risk_score, 20)
    
    def _get_library_vulnerability_score(self, library_name: str) -> int:
        """
        Get vulnerability score for a library using NVD API.
        
        Args:
            library_name: Name of the library to check
            
        Returns:
            Vulnerability score (0-8)
        """
        try:
            # Use NIST NVD API 2.0 to search for vulnerabilities
            url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
            params = {
                'keywordSearch': library_name,
                'resultsPerPage': 10,
                'startIndex': 0
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code != 200:
                return self._fallback_library_risk(library_name)
                
            data = response.json()
            vulnerabilities = data.get('vulnerabilities', [])
            
            if not vulnerabilities:
                return self._fallback_library_risk(library_name)
            
            # Calculate score based on vulnerability severity
            critical_count = 0
            high_count = 0
            medium_count = 0
            
            for vuln in vulnerabilities[:10]:  # Check first 10 CVEs
                metrics = vuln.get('cve', {}).get('metrics', {})
                
                # Try CVSS v3.1 first, then v3.0, then v2.0
                cvss_score = None
                for version in ['cvssMetricV31', 'cvssMetricV30', 'cvssMetricV2']:
                    if version in metrics and metrics[version]:
                        cvss_data = metrics[version][0]
                        if version.startswith('cvssMetricV3'):
                            cvss_score = cvss_data.get('cvssData', {}).get('baseScore')
                        else:  # v2
                            cvss_score = cvss_data.get('cvssData', {}).get('baseScore')
                        break
                
                if cvss_score:
                    if cvss_score >= 9.0:
                        critical_count += 1
                    elif cvss_score >= 7.0:
                        high_count += 1
                    elif cvss_score >= 4.0:
                        medium_count += 1
            
            # Calculate risk score based on severity distribution
            # More conservative scoring - not all vulnerabilities are equal
            if critical_count >= 3:
                score = 8  # Maximum risk
            elif critical_count >= 2:
                score = 7
            elif critical_count >= 1:
                score = 6
            elif high_count >= 3:
                score = 5
            elif high_count >= 2:
                score = 4
            elif high_count >= 1 or medium_count >= 3:
                score = 3
            elif medium_count >= 2:
                score = 2
            elif medium_count >= 1:
                score = 1
            else:
                score = 0  # No significant vulnerabilities found
                
            return score
            
        except Exception:
            # Fall back to pattern-based assessment
            return self._fallback_library_risk(library_name)
    
    def _fallback_library_risk(self, library_name: str) -> int:
        """
        Fallback risk assessment when CVE lookup fails.
        
        Args:
            library_name: Library name
            
        Returns:
            Risk score based on known patterns (0-4)
        """
        lib_lower = library_name.lower()
        
        # Known high-risk ML/data libraries (larger attack surface)
        high_risk_patterns = ["tensorflow", "pytorch", "scikit-learn", "numpy", "pandas"]
        medium_risk_patterns = ["requests", "flask", "django", "pillow", "opencv"]
        
        if any(pattern in lib_lower for pattern in high_risk_patterns):
            return 3  # Higher risk due to complexity and widespread use
        elif any(pattern in lib_lower for pattern in medium_risk_patterns):
            return 2  # Medium risk
        else:
            return 1  # Unknown library - minimal risk
    
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
        Fetch economic stress indicator from FRED API.
        
        Returns:
            Stress multiplier based on real economic conditions
        """
        try:
            fred_api_key = os.getenv('FRED_API_KEY')
            if not fred_api_key:
                return self._fallback_economic_stress()
            
            # Fetch VIX (volatility index) as primary stress indicator
            vix_data = self._fetch_fred_series('VIXCLS', fred_api_key)
            
            # Fetch GDP growth rate as economic health indicator
            gdp_data = self._fetch_fred_series('A191RL1Q225SBEA', fred_api_key)  # Real GDP % change
            
            # Calculate stress multiplier based on real data
            stress_multiplier = self._calculate_stress_multiplier(vix_data, gdp_data)
            
            # Enforce bounds: 1.0 <= alpha <= 2.0 as per mathematical framework
            return max(1.0, min(stress_multiplier, 2.0))
            
        except Exception as e:
            # Fall back to safe default if API fails
            return self._fallback_economic_stress()
    
    def _fetch_fred_series(self, series_id: str, api_key: str, days_back: int = 30) -> Optional[float]:
        """
        Fetch the most recent value from a FRED economic series.
        
        Args:
            series_id: FRED series identifier (e.g., 'VIXCLS', 'A191RL1Q225SBEA')
            api_key: FRED API key
            days_back: How many days back to look for data
            
        Returns:
            Most recent value or None if unavailable
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # FRED API endpoint
            url = f"https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': series_id,
                'api_key': api_key,
                'file_type': 'json',
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'sort_order': 'desc',
                'limit': 1
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            observations = data.get('observations', [])
            
            if observations and observations[0]['value'] != '.':
                return float(observations[0]['value'])
                
            return None
            
        except Exception:
            return None
    
    def _calculate_stress_multiplier(self, vix: Optional[float], gdp_growth: Optional[float]) -> float:
        """
        Calculate economic stress multiplier from real indicators.
        
        Args:
            vix: VIX volatility index value
            gdp_growth: Real GDP growth rate (annualized %)
            
        Returns:
            Stress multiplier (1.0 = normal, higher = more stress)
        """
        multiplier = 1.0
        
        # VIX-based stress (normal VIX ~15-20, crisis >30)
        if vix is not None:
            if vix > 40:  # Extreme volatility - financial crisis
                multiplier += 0.8
            elif vix > 30:  # High volatility - market stress
                multiplier += 0.5
            elif vix > 25:  # Elevated volatility - uncertainty
                multiplier += 0.3
            elif vix > 20:  # Moderate volatility - some concern
                multiplier += 0.1
                
        # GDP-based stress (normal growth ~2-3%, recession <0%)
        # GDP impacts supply chain stability, vendor reliability, and economic capacity
        if gdp_growth is not None:
            if gdp_growth < -2:  # Severe recession - supply chain disruption
                multiplier += 0.7
            elif gdp_growth < 0:  # Recession - economic contraction
                multiplier += 0.5
            elif gdp_growth < 1:  # Slow growth - economic weakness
                multiplier += 0.3
            elif gdp_growth < 2:  # Below trend growth - mild concern
                multiplier += 0.1
            # No penalty for strong growth (>2%) - stable supply chains
                
        return multiplier
    
    def _fallback_economic_stress(self) -> float:
        """
        Fallback economic stress calculation when API unavailable.
        Uses conservative baseline rather than seasonal simulation.
        
        Returns:
            Economic stress multiplier within bounds [1.0, 2.0]
        """
        # Conservative baseline - moderate stress assumption
        # Ensures multiplier stays within mathematical framework bounds
        fallback_multiplier = 1.2
        return max(1.0, min(fallback_multiplier, 2.0))
    
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