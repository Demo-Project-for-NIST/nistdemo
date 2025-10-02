#!/usr/bin/env python3
"""
Detailed Claims Validation Script

This script performs deep validation of specific mathematical and implementation
claims made in the LaTeX documentation against the actual code.
"""
import json
import os
import re
import sys
from typing import Dict, List, Any


class DetailedClaimsValidator:
    """Validates specific detailed claims from LaTeX documentation."""
    
    def __init__(self):
        """Initialize validator."""
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.validation_results = []
        
    def validate_specific_claims(self):
        """Validate specific mathematical and implementation claims."""
        print("DETAILED CLAIMS VALIDATION")
        print("=" * 60)
        
        # Mathematical Formula Claims
        self.validate_risk_formula_implementation()
        
        # Specific Weight Claims  
        self.validate_exact_weight_values()
        
        # Economic Formula Claims
        self.validate_economic_formula()
        
        # CSF Category Claims
        self.validate_specific_csf_categories()
        
        # API Endpoint Claims
        self.validate_exact_api_claims()
        
        # File Structure Claims
        self.validate_file_structure_claims()
        
        # Mathematical Bounds Claims
        self.validate_mathematical_bounds()
        
        # Integration Claims
        self.validate_integration_claims()
        
        self.generate_detailed_report()
    
    def validate_risk_formula_implementation(self):
        """Validate the exact risk formula implementation."""
        print("\n1. RISK FORMULA VALIDATION")
        print("-" * 30)
        
        risk_scorer_path = os.path.join(self.project_root, "src", "risk_scorer.py")
        
        with open(risk_scorer_path, 'r') as f:
            content = f.read()
        
        # LaTeX Claim: R = min(100, (sum(wi * fi)) * alpha)
        
        # Check for min(100, ...) pattern
        min_pattern = r'min\s*\(\s*(?:risk_score,\s*)?100|min\s*\(\s*100'
        if re.search(min_pattern, content):
            self.add_result("PASS", "Min Function Implementation", 
                          "min(100, ...) pattern found in code")
        else:
            self.add_result("FAIL", "Min Function Implementation", 
                          "min(100, ...) pattern not found")
        
        # Check for summation of weighted factors
        summation_patterns = [
            r'risk_score\s*\+=\s*\d+',  # risk_score += weight
            r'sum\s*\(',                # sum() function
            r'\+\s*\d+\s*\*'           # + weight * factor
        ]
        
        found_summation = any(re.search(pattern, content) for pattern in summation_patterns)
        
        if found_summation:
            self.add_result("PASS", "Weighted Summation", 
                          "Weighted factor summation found")
        else:
            self.add_result("FAIL", "Weighted Summation", 
                          "Weighted factor summation not found")
        
        # Check for multiplier application
        multiplier_patterns = [
            r'\*\s*(?:alpha|economic_multiplier|multiplier)',
            r'risk_score\s*\*\s*'
        ]
        
        found_multiplier = any(re.search(pattern, content) for pattern in multiplier_patterns)
        
        if found_multiplier:
            self.add_result("PASS", "Economic Multiplier Application", 
                          "Economic multiplier application found")
        else:
            self.add_result("WARNING", "Economic Multiplier Application", 
                          "Economic multiplier application unclear")
    
    def validate_exact_weight_values(self):
        """Validate the exact weight values claimed in LaTeX."""
        print("\n2. EXACT WEIGHT VALUES VALIDATION")
        print("-" * 35)
        
        risk_scorer_path = os.path.join(self.project_root, "src", "risk_scorer.py")
        
        with open(risk_scorer_path, 'r') as f:
            content = f.read()
        
        # LaTeX Claims: Specific weights
        claimed_weights = {
            "data_lineage": 20,
            "model_explainability": 15,
            "drift_monitoring": 25,
            "third_party": 20,
            "data_encryption": 10,
            "access_controls": 5
        }
        
        # Look for specific weight patterns
        weight_checks = [
            ("Data Lineage (20)", r'(?:risk_score\s*\+=\s*20|20.*data_lineage)'),
            ("Model Explainability (15)", r'(?:risk_score\s*\+=\s*15|15.*(?:neural|deep|black))'),
            ("Drift Monitoring (25)", r'(?:risk_score\s*\+=\s*25|25.*drift)'),
            ("Third Party (20)", r'(?:20.*third|third.*20)'),
            ("Data Encryption (10)", r'(?:risk_score\s*\+=\s*10|10.*encryption)'),
            ("Access Controls (5)", r'(?:risk_score\s*\+=\s*5|5.*access)')
        ]
        
        found_weights = 0
        for weight_name, pattern in weight_checks:
            if re.search(pattern, content, re.IGNORECASE):
                found_weights += 1
                print(f"   PASS {weight_name} weight found")
            else:
                print(f"   WARNING {weight_name} weight pattern not clearly found")
        
        if found_weights >= 4:
            self.add_result("PASS", "Exact Weight Values", 
                          f"{found_weights}/6 exact weights verified")
        else:
            self.add_result("WARNING", "Exact Weight Values", 
                          f"Only {found_weights}/6 weights clearly verified")
    
    def validate_economic_formula(self):
        """Validate economic stress formula claims."""
        print("\n3. ECONOMIC FORMULA VALIDATION")
        print("-" * 30)
        
        risk_scorer_path = os.path.join(self.project_root, "src", "risk_scorer.py")
        
        with open(risk_scorer_path, 'r') as f:
            content = f.read()
        
        # LaTeX Claim: alpha = 1.0 + VIX_stress + GDP_stress
        
        # Check for FRED API implementation
        fred_patterns = [
            r'fred.*api',
            r'stlouisfed\.org',
            r'FRED_API_KEY'
        ]
        
        found_fred = any(re.search(pattern, content, re.IGNORECASE) for pattern in fred_patterns)
        
        if found_fred:
            self.add_result("PASS", "FRED API Implementation", 
                          "FRED API implementation found")
        else:
            self.add_result("FAIL", "FRED API Implementation", 
                          "FRED API implementation not found")
        
        # Check for VIX series
        if "VIXCLS" in content or "VIX" in content:
            self.add_result("PASS", "VIX Series Integration", 
                          "VIX volatility index integration found")
        else:
            self.add_result("FAIL", "VIX Series Integration", 
                          "VIX integration not found")
        
        # Check for GDP series
        gdp_patterns = [
            r'A191RL1Q225SBEA',  # Specific GDP series ID
            r'GDP.*growth',
            r'real.*gdp'
        ]
        
        found_gdp = any(re.search(pattern, content, re.IGNORECASE) for pattern in gdp_patterns)
        
        if found_gdp:
            self.add_result("PASS", "GDP Series Integration", 
                          "GDP growth rate integration found")
        else:
            self.add_result("FAIL", "GDP Series Integration", 
                          "GDP integration not found")
        
        # Check for multiplier bounds
        if "1.0" in content and "2.0" in content:
            self.add_result("PASS", "Multiplier Bounds", 
                          "1.0-2.0 bounds found in implementation")
        else:
            self.add_result("WARNING", "Multiplier Bounds", 
                          "Multiplier bounds not clearly specified")
    
    def validate_specific_csf_categories(self):
        """Validate specific CSF category claims."""
        print("\n4. SPECIFIC CSF CATEGORIES VALIDATION")
        print("-" * 40)
        
        # Check AI risks data for specific CSF mappings
        ai_risks_path = os.path.join(self.project_root, "src", "data", "ai_risks.json")
        
        if not os.path.exists(ai_risks_path):
            self.add_result("FAIL", "AI Risks Data File", "ai_risks.json not found")
            return
        
        with open(ai_risks_path, 'r') as f:
            ai_risks_data = json.load(f)
        
        # LaTeX Claims: Specific CSF categories
        claimed_categories = [
            "GV.SC-01", "GV.SC-03", "GV.SC-04", "GV.SC-07",
            "ID.RA-01", "ID.RA-05", "ID.RA-09", "ID.RA-10",
            "PR.DS-01", "PR.DS-06", "PR.DS-08", "PR.DS-09",
            "DE.CM-04", "DE.CM-07", "DE.AE-02",
            "RS.AN-01", "RS.AN-02",
            "RC.RP-04", "PR.AC-01", "PR.AC-07"
        ]
        
        found_categories = set()
        
        if "ai_risk_categories" in ai_risks_data:
            for risk_name, risk_data in ai_risks_data["ai_risk_categories"].items():
                if "csf_mappings" in risk_data:
                    for category in risk_data["csf_mappings"]:
                        found_categories.add(category)
        
        # Check how many claimed categories are found
        claimed_found = sum(1 for cat in claimed_categories if cat in found_categories)
        
        if claimed_found >= 15:
            self.add_result("PASS", "Specific CSF Categories", 
                          f"{claimed_found}/{len(claimed_categories)} claimed categories found")
        elif claimed_found >= 10:
            self.add_result("WARNING", "Specific CSF Categories", 
                          f"{claimed_found}/{len(claimed_categories)} claimed categories found")
        else:
            self.add_result("FAIL", "Specific CSF Categories", 
                          f"Only {claimed_found}/{len(claimed_categories)} categories found")
        
        # Check for claimed risk types
        claimed_risks = [
            "training_data_poisoning",
            "model_drift", 
            "adversarial_examples",
            "model_inversion",
            "supply_chain_ml_attack",
            "data_lineage_gaps",
            "model_backdoors",
            "ai_system_dependency"
        ]
        
        found_risks = sum(1 for risk in claimed_risks 
                         if risk in ai_risks_data.get("ai_risk_categories", {}))
        
        if found_risks >= 7:
            self.add_result("PASS", "Claimed AI Risk Types", 
                          f"{found_risks}/8 claimed risk types found")
        else:
            self.add_result("WARNING", "Claimed AI Risk Types", 
                          f"Only {found_risks}/8 claimed risk types found")
    
    def validate_exact_api_claims(self):
        """Validate exact API endpoint claims."""
        print("\n5. EXACT API ENDPOINT VALIDATION")
        print("-" * 35)
        
        api_path = os.path.join(self.project_root, "src", "api.py")
        
        with open(api_path, 'r') as f:
            api_content = f.read()
        
        # LaTeX Claims: Specific endpoints
        endpoint_claims = [
            ("/assess", "POST", "AI system risk assessment"),
            ("/csf-mapping/{risk_type}", "GET", "CSF category mapping"),
            ("/report", "POST", "Generate compliance report"),
            ("/health", "GET", "Health check endpoint")
        ]
        
        found_endpoints = 0
        for endpoint, method, description in endpoint_claims:
            # Look for endpoint definition
            endpoint_base = endpoint.split("{")[0]  # Remove path parameters
            
            if endpoint_base in api_content:
                found_endpoints += 1
                print(f"   PASS {method} {endpoint}: Found")
            else:
                print(f"   FAIL {method} {endpoint}: Not found")
        
        if found_endpoints >= 3:
            self.add_result("PASS", "API Endpoints Implementation", 
                          f"{found_endpoints}/4 claimed endpoints found")
        else:
            self.add_result("FAIL", "API Endpoints Implementation", 
                          f"Only {found_endpoints}/4 endpoints found")
        
        # Check for response models
        response_models = ["RiskAssessmentResponse", "CSFMappingResponse"]
        found_models = sum(1 for model in response_models if model in api_content)
        
        if found_models >= 1:
            self.add_result("PASS", "Response Models", 
                          f"{found_models}/2 response models found")
        else:
            self.add_result("WARNING", "Response Models", 
                          "Response models not clearly defined")
    
    def validate_file_structure_claims(self):
        """Validate file structure claims."""
        print("\n6. FILE STRUCTURE VALIDATION")
        print("-" * 30)
        
        # LaTeX Claims: Specific file structure
        claimed_structure = {
            "src/api.py": "FastAPI REST endpoints",
            "src/models.py": "Pydantic data models", 
            "src/database.py": "SQLAlchemy database setup",
            "src/csf_mapper.py": "CSF 2.0 risk mapping engine",
            "src/risk_scorer.py": "AI risk quantification",
            "src/report_generator.py": "PDF/JSON report creation",
            "src/data/csf_categories.json": "NIST CSF 2.0 taxonomy",
            "src/data/ai_risks.json": "AI risk categories",
            "requirements.txt": "Dependencies",
            "render.yaml": "Deployment config"
        }
        
        found_files = 0
        for file_path, description in claimed_structure.items():
            full_path = os.path.join(self.project_root, file_path)
            
            if os.path.exists(full_path):
                found_files += 1
                print(f"   PASS {file_path}: Found")
            else:
                print(f"   FAIL {file_path}: Missing")
        
        if found_files >= 8:
            self.add_result("PASS", "File Structure", 
                          f"{found_files}/{len(claimed_structure)} claimed files found")
        else:
            self.add_result("WARNING", "File Structure", 
                          f"Only {found_files}/{len(claimed_structure)} files found")
    
    def validate_mathematical_bounds(self):
        """Validate mathematical bounds claims."""
        print("\n7. MATHEMATICAL BOUNDS VALIDATION")
        print("-" * 35)
        
        risk_scorer_path = os.path.join(self.project_root, "src", "risk_scorer.py")
        
        with open(risk_scorer_path, 'r') as f:
            content = f.read()
        
        # LaTeX Claim: Risk score R ∈ [0, 100]
        bounds_patterns = [
            r'min\s*\(\s*(?:risk_score,\s*)?100',
            r'max.*100',
            r'100.*min'
        ]
        
        found_upper_bound = any(re.search(pattern, content) for pattern in bounds_patterns)
        
        if found_upper_bound:
            self.add_result("PASS", "Upper Bound (100)", 
                          "Upper bound enforcement found")
        else:
            self.add_result("FAIL", "Upper Bound (100)", 
                          "Upper bound enforcement not found")
        
        # LaTeX Claim: Economic multiplier α ∈ [1.0, 2.0]
        if "1.0" in content and "2.0" in content:
            self.add_result("PASS", "Economic Multiplier Bounds", 
                          "Economic multiplier bounds 1.0-2.0 found")
        else:
            self.add_result("WARNING", "Economic Multiplier Bounds", 
                          "Economic multiplier bounds not explicit")
        
        # Check for non-negative constraints
        if ">= 0" in content or "max(0" in content:
            self.add_result("PASS", "Non-negative Constraints", 
                          "Non-negative value constraints found")
        else:
            self.add_result("WARNING", "Non-negative Constraints", 
                          "Non-negative constraints not explicit")
    
    def validate_integration_claims(self):
        """Validate integration claims."""
        print("\n8. INTEGRATION CLAIMS VALIDATION")
        print("-" * 35)
        
        # Check for claimed integrations
        integrations = {
            "CORS": ("api.py", ["CORSMiddleware", "cors"]),
            "Environment Variables": ("risk_scorer.py", ["dotenv", "getenv"]),
            "JSON Processing": ("csf_mapper.py", ["json.load", "json"]),
            "HTTP Requests": ("risk_scorer.py", ["requests.get", "requests"]),
            "Database ORM": ("database.py", ["SQLAlchemy", "sqlalchemy"])
        }
        
        found_integrations = 0
        for integration_name, (file_name, patterns) in integrations.items():
            file_path = os.path.join(self.project_root, "src", file_name)
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    file_content = f.read()
                
                if any(pattern in file_content for pattern in patterns):
                    found_integrations += 1
                    print(f"   PASS {integration_name}: Found in {file_name}")
                else:
                    print(f"   FAIL {integration_name}: Not found in {file_name}")
            else:
                print(f"   FAIL {integration_name}: {file_name} not found")
        
        if found_integrations >= 4:
            self.add_result("PASS", "Third-party Integrations", 
                          f"{found_integrations}/5 claimed integrations found")
        else:
            self.add_result("WARNING", "Third-party Integrations", 
                          f"Only {found_integrations}/5 integrations found")
    
    def add_result(self, status: str, claim: str, details: str):
        """Add validation result."""
        result = {
            "status": status,
            "claim": claim,
            "details": details
        }
        self.validation_results.append(result)
    
    def generate_detailed_report(self):
        """Generate detailed validation report."""
        print("\n" + "=" * 60)
        print("DETAILED VALIDATION REPORT")
        print("=" * 60)
        
        passed = len([r for r in self.validation_results if r["status"] == "PASS"])
        failed = len([r for r in self.validation_results if r["status"] == "FAIL"])
        warnings = len([r for r in self.validation_results if r["status"] == "WARNING"])
        total = len(self.validation_results)
        
        print(f"Detailed Checks: {total}")
        print(f"PASSED: {passed} ({passed/total*100:.1f}%)")
        print(f"FAILED: {failed} ({failed/total*100:.1f}%)")
        print(f"WARNINGS: {warnings} ({warnings/total*100:.1f}%)")
        
        # Calculate detailed accuracy score
        accuracy_score = ((passed * 3 + warnings) / (total * 3)) * 100
        
        print(f"\nDETAILED ACCURACY SCORE: {accuracy_score:.1f}%")
        
        if accuracy_score >= 90:
            print("EXCELLENT: Implementation matches documentation claims precisely")
        elif accuracy_score >= 80:
            print("VERY GOOD: Strong alignment with minor discrepancies")
        elif accuracy_score >= 70:
            print("GOOD: Generally aligned with some issues to address")
        else:
            print("NEEDS IMPROVEMENT: Significant alignment issues found")
        
        # Detailed breakdown
        if failed > 0:
            print(f"\nCRITICAL ISSUES ({failed}):")
            for result in self.validation_results:
                if result["status"] == "FAIL":
                    print(f"  ❌ {result['claim']}: {result['details']}")
        
        if warnings > 0:
            print(f"\nREVIEW NEEDED ({warnings}):")
            for result in self.validation_results:
                if result["status"] == "WARNING":
                    print(f"  ⚠️  {result['claim']}: {result['details']}")
        
        top_successes = [r for r in self.validation_results if r["status"] == "PASS"][:5]
        if top_successes:
            print(f"\nTOP VALIDATIONS ({len(top_successes)}):")
            for result in top_successes:
                print(f"  ✅ {result['claim']}: {result['details']}")


def main():
    """Run detailed validation."""
    validator = DetailedClaimsValidator()
    validator.validate_specific_claims()


if __name__ == "__main__":
    main()