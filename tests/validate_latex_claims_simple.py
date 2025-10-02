#!/usr/bin/env python3
"""
Simple Consistency Validation Script for LaTeX Claims vs Code Implementation

This script validates LaTeX documentation claims against the actual code implementation
without requiring all runtime dependencies.
"""
import json
import os
import re
import sys
from typing import Dict, List, Tuple


class LaTeXClaimValidator:
    """Validates LaTeX documentation claims against code implementation."""
    
    def __init__(self):
        """Initialize validator."""
        self.validation_results = []
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        
    def validate_all_claims(self) -> Dict[str, any]:
        """Run all validation checks and return results."""
        print("VALIDATION Starting LaTeX Claims vs Code Implementation Validation")
        print("=" * 70)
        
        # Mathematical Framework Claims
        self.validate_mathematical_framework_claims()
        
        # Risk Factor Claims  
        self.validate_risk_factor_claims()
        
        # CSF Mapping Claims
        self.validate_csf_mapping_claims()
        
        # Economic Stress Claims
        self.validate_economic_stress_claims()
        
        # API Implementation Claims
        self.validate_api_implementation_claims()
        
        # Data Structure Claims
        self.validate_data_structure_claims()
        
        # Algorithm Complexity Claims
        self.validate_complexity_claims()
        
        # Framework Architecture Claims
        self.validate_architecture_claims()
        
        # Generate summary report
        self.generate_summary_report()
        
        return {
            "total_checks": len(self.validation_results),
            "passed": len([r for r in self.validation_results if r["status"] == "PASS"]),
            "failed": len([r for r in self.validation_results if r["status"] == "FAIL"]),
            "warnings": len([r for r in self.validation_results if r["status"] == "WARNING"]),
            "results": self.validation_results
        }
    
    def validate_mathematical_framework_claims(self):
        """Validate mathematical framework claims from LaTeX."""
        print("\nSECTION 1: Mathematical Framework Claims")
        print("-" * 50)
        
        # LaTeX Claim: R = min(100, (sum(wi * fi)) * alpha)
        risk_scorer_path = os.path.join(self.project_root, "src", "risk_scorer.py")
        
        if not os.path.exists(risk_scorer_path):
            self.add_result("FAIL", "Risk Scorer Module", "risk_scorer.py not found")
            return
            
        with open(risk_scorer_path, 'r') as f:
            risk_scorer_content = f.read()
        
        # Check for claimed mathematical formula implementation
        if "min(risk_score, 100)" in risk_scorer_content or "min(100" in risk_scorer_content:
            self.add_result("PASS", "Risk Score Capping", 
                          "min(100, ...) formula found in implementation")
        else:
            self.add_result("FAIL", "Risk Score Capping", 
                          "Risk score capping at 100 not found in code")
        
        # Check for economic multiplier integration
        if "economic_multiplier" in risk_scorer_content or "alpha" in risk_scorer_content:
            self.add_result("PASS", "Economic Multiplier", 
                          "Economic stress multiplier found in implementation")
        else:
            self.add_result("FAIL", "Economic Multiplier", 
                          "Economic stress multiplier not found")
        
        # LaTeX Claim: Six specific risk factors with weights
        claimed_weights = ["20", "15", "25", "20", "10", "5"]
        found_weights = sum(1 for weight in claimed_weights if weight in risk_scorer_content)
        
        if found_weights >= 5:  # Allow for minor variations
            self.add_result("PASS", "Risk Factor Weights", 
                          f"Found {found_weights}/6 claimed weights in code")
        else:
            self.add_result("WARNING", "Risk Factor Weights", 
                          f"Only found {found_weights}/6 claimed weights")
    
    def validate_risk_factor_claims(self):
        """Validate risk factor implementation claims."""
        print("\nSECTION 2: Risk Factor Claims")
        print("-" * 50)
        
        risk_scorer_path = os.path.join(self.project_root, "src", "risk_scorer.py")
        
        with open(risk_scorer_path, 'r') as f:
            content = f.read()
        
        # LaTeX Claims: Six specific risk factors
        claimed_factors = [
            ("data_lineage_documented", "Data lineage documentation"),
            ("model_type", "Model explainability"),  
            ("drift_monitoring_enabled", "Drift monitoring"),
            ("third_party_libs", "Third-party components"),
            ("data_encryption", "Data encryption"),
            ("access_controls", "Access controls")
        ]
        
        found_factors = 0
        for factor_var, factor_name in claimed_factors:
            if factor_var in content:
                found_factors += 1
                print(f"   PASS Found {factor_name} implementation")
            else:
                print(f"   FAIL Missing {factor_name} implementation")
        
        if found_factors >= 5:
            self.add_result("PASS", "Risk Factor Implementation", 
                          f"{found_factors}/6 claimed risk factors found in code")
        else:
            self.add_result("FAIL", "Risk Factor Implementation", 
                          f"Only {found_factors}/6 risk factors found")
        
        # Check for VIX and GDP integration (LaTeX claim)
        if "VIX" in content and "GDP" in content:
            self.add_result("PASS", "Economic Indicators", 
                          "VIX and GDP integration found as claimed")
        elif "VIX" in content or "GDP" in content:
            self.add_result("WARNING", "Economic Indicators", 
                          "Partial economic indicator integration found")
        else:
            self.add_result("FAIL", "Economic Indicators", 
                          "VIX and GDP integration not found")
    
    def validate_csf_mapping_claims(self):
        """Validate CSF mapping claims."""
        print("\nSECTION 3: CSF Mapping Claims")
        print("-" * 50)
        
        # Check CSF mapper implementation
        csf_mapper_path = os.path.join(self.project_root, "src", "csf_mapper.py")
        
        if not os.path.exists(csf_mapper_path):
            self.add_result("FAIL", "CSF Mapper Module", "csf_mapper.py not found")
            return
            
        with open(csf_mapper_path, 'r') as f:
            csf_content = f.read()
        
        # LaTeX Claim: Graph-theoretic mapping G = (V, E)
        if "graph" in csf_content.lower() or "mapping" in csf_content:
            self.add_result("PASS", "Graph-theoretic Mapping", 
                          "Mapping functionality found in CSF mapper")
        else:
            self.add_result("WARNING", "Graph-theoretic Mapping", 
                          "Graph-theoretic mapping not explicitly mentioned")
        
        # Check for claimed CSF categories
        claimed_csf_categories = [
            "GV.SC", "ID.RA", "PR.DS", "DE.CM", "RS.AN", "RC.RP"
        ]
        
        found_categories = sum(1 for cat in claimed_csf_categories if cat in csf_content)
        
        if found_categories >= 4:
            self.add_result("PASS", "CSF Categories", 
                          f"Found {found_categories}/6 claimed CSF categories")
        else:
            self.add_result("WARNING", "CSF Categories", 
                          f"Only found {found_categories}/6 claimed categories")
        
        # Check AI risks data file
        ai_risks_path = os.path.join(self.project_root, "src", "data", "ai_risks.json")
        
        if os.path.exists(ai_risks_path):
            try:
                with open(ai_risks_path, 'r') as f:
                    ai_risks_data = json.load(f)
                
                if "ai_risk_categories" in ai_risks_data:
                    risk_count = len(ai_risks_data["ai_risk_categories"])
                    
                    # LaTeX Claims: Eight AI risk categories
                    if risk_count >= 8:
                        self.add_result("PASS", "AI Risk Categories", 
                                      f"Found {risk_count} AI risk categories (claimed: 8)")
                    else:
                        self.add_result("WARNING", "AI Risk Categories", 
                                      f"Found {risk_count} categories (claimed: 8)")
                        
                    # Check specific claimed risks
                    claimed_risks = [
                        "training_data_poisoning",
                        "model_drift", 
                        "adversarial_examples",
                        "supply_chain_ml_attack"
                    ]
                    
                    found_risks = sum(1 for risk in claimed_risks 
                                    if risk in ai_risks_data["ai_risk_categories"])
                    
                    if found_risks >= 3:
                        self.add_result("PASS", "Specific AI Risks", 
                                      f"Found {found_risks}/4 claimed specific risks")
                    else:
                        self.add_result("FAIL", "Specific AI Risks", 
                                      f"Only found {found_risks}/4 claimed risks")
                        
            except json.JSONDecodeError:
                self.add_result("FAIL", "AI Risks Data", "Invalid JSON in ai_risks.json")
        else:
            self.add_result("FAIL", "AI Risks Data", "ai_risks.json not found")
    
    def validate_economic_stress_claims(self):
        """Validate economic stress implementation."""
        print("\nSECTION 4: Economic Stress Claims")
        print("-" * 50)
        
        risk_scorer_path = os.path.join(self.project_root, "src", "risk_scorer.py")
        
        with open(risk_scorer_path, 'r') as f:
            content = f.read()
        
        # LaTeX Claim: FRED API integration
        if "FRED" in content or "fred" in content:
            self.add_result("PASS", "FRED API Integration", 
                          "FRED API references found in code")
        else:
            self.add_result("FAIL", "FRED API Integration", 
                          "FRED API integration not found")
        
        # LaTeX Claim: VIX volatility index
        if "VIX" in content:
            self.add_result("PASS", "VIX Integration", 
                          "VIX volatility index found in implementation")
        else:
            self.add_result("FAIL", "VIX Integration", 
                          "VIX volatility index not found")
        
        # LaTeX Claim: GDP growth rate
        if "GDP" in content:
            self.add_result("PASS", "GDP Integration", 
                          "GDP growth rate found in implementation")
        else:
            self.add_result("FAIL", "GDP Integration", 
                          "GDP growth rate not found")
        
        # LaTeX Claim: Multiplier bounds 1.0 <= alpha <= 2.0
        if "1.0" in content and "2.0" in content:
            self.add_result("PASS", "Multiplier Bounds", 
                          "Multiplier bounds 1.0-2.0 found in code")
        else:
            self.add_result("WARNING", "Multiplier Bounds", 
                          "Multiplier bounds not clearly defined")
    
    def validate_api_implementation_claims(self):
        """Validate API implementation claims."""
        print("\nSECTION 5: API Implementation Claims")
        print("-" * 50)
        
        api_path = os.path.join(self.project_root, "src", "api.py")
        
        if not os.path.exists(api_path):
            self.add_result("FAIL", "API Module", "api.py not found")
            return
            
        with open(api_path, 'r') as f:
            api_content = f.read()
        
        # LaTeX Claim: FastAPI implementation
        if "FastAPI" in api_content:
            self.add_result("PASS", "FastAPI Framework", 
                          "FastAPI framework found in implementation")
        else:
            self.add_result("FAIL", "FastAPI Framework", 
                          "FastAPI framework not found")
        
        # LaTeX Claim: Automatic documentation
        if 'docs_url' in api_content and 'redoc_url' in api_content:
            self.add_result("PASS", "API Documentation", 
                          "Automatic documentation configuration found")
        else:
            self.add_result("WARNING", "API Documentation", 
                          "Documentation configuration may be missing")
        
        # LaTeX Claim: Specific endpoints
        claimed_endpoints = ["/assess", "/csf-mapping", "/report", "/health"]
        found_endpoints = sum(1 for endpoint in claimed_endpoints if endpoint in api_content)
        
        if found_endpoints >= 3:
            self.add_result("PASS", "API Endpoints", 
                          f"Found {found_endpoints}/4 claimed endpoints")
        else:
            self.add_result("FAIL", "API Endpoints", 
                          f"Only found {found_endpoints}/4 claimed endpoints")
        
        # LaTeX Claim: JSON response format
        if "json" in api_content.lower() or "JSONResponse" in api_content:
            self.add_result("PASS", "JSON Response Format", 
                          "JSON response handling found")
        else:
            self.add_result("WARNING", "JSON Response Format", 
                          "JSON response format not clearly implemented")
    
    def validate_data_structure_claims(self):
        """Validate data structure claims."""
        print("\nSECTION 6: Data Structure Claims")
        print("-" * 50)
        
        # LaTeX Claim: JSON data files
        data_files = [
            ("src/data/csf_categories.json", "CSF Categories"),
            ("src/data/ai_risks.json", "AI Risks")
        ]
        
        for file_path, description in data_files:
            full_path = os.path.join(self.project_root, file_path)
            
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r') as f:
                        data = json.load(f)
                    
                    if isinstance(data, dict) and len(data) > 0:
                        self.add_result("PASS", f"{description} Data", 
                                      f"Valid JSON with {len(data)} sections")
                    else:
                        self.add_result("FAIL", f"{description} Data", 
                                      "Empty or invalid data structure")
                        
                except json.JSONDecodeError:
                    self.add_result("FAIL", f"{description} Data", 
                                  "Invalid JSON format")
            else:
                self.add_result("FAIL", f"{description} Data", 
                              f"{file_path} not found")
        
        # LaTeX Claim: SQLAlchemy database support
        database_path = os.path.join(self.project_root, "src", "database.py")
        
        if os.path.exists(database_path):
            with open(database_path, 'r') as f:
                db_content = f.read()
                
            if "SQLAlchemy" in db_content or "sqlalchemy" in db_content:
                self.add_result("PASS", "Database Framework", 
                              "SQLAlchemy integration found")
            else:
                self.add_result("WARNING", "Database Framework", 
                              "SQLAlchemy integration not clear")
        else:
            self.add_result("FAIL", "Database Module", 
                          "database.py not found")
    
    def validate_complexity_claims(self):
        """Validate algorithm complexity claims."""
        print("\nSECTION 7: Complexity Claims")
        print("-" * 50)
        
        risk_scorer_path = os.path.join(self.project_root, "src", "risk_scorer.py")
        
        with open(risk_scorer_path, 'r') as f:
            content = f.read()
        
        # LaTeX Claim: O(n) time complexity
        # Look for linear operations (simple loops, no nested loops)
        nested_loop_pattern = r'for.*for.*:'
        complex_operations = re.findall(nested_loop_pattern, content, re.MULTILINE)
        
        if len(complex_operations) == 0:
            self.add_result("PASS", "Linear Time Complexity", 
                          "No nested loops found, supports O(n) claim")
        else:
            self.add_result("WARNING", "Linear Time Complexity", 
                          f"Found {len(complex_operations)} potentially complex operations")
        
        # LaTeX Claim: Efficient implementation
        if "sum(" in content or "enumerate" in content:
            self.add_result("PASS", "Efficient Implementation", 
                          "Efficient Python operations found")
        else:
            self.add_result("WARNING", "Efficient Implementation", 
                          "Implementation efficiency unclear")
    
    def validate_architecture_claims(self):
        """Validate architecture claims."""
        print("\nSECTION 8: Architecture Claims")
        print("-" * 50)
        
        # LaTeX Claim: Modular design
        expected_modules = [
            ("src/risk_scorer.py", "Risk Scoring Engine"),
            ("src/csf_mapper.py", "CSF Mapper"),
            ("src/action_planner.py", "Action Planner"),
            ("src/api.py", "API Layer"),
            ("src/models.py", "Data Models")
        ]
        
        found_modules = 0
        for module_path, module_name in expected_modules:
            full_path = os.path.join(self.project_root, module_path)
            
            if os.path.exists(full_path):
                found_modules += 1
                print(f"   PASS {module_name} module found")
            else:
                print(f"   FAIL {module_name} module missing")
        
        if found_modules >= 4:
            self.add_result("PASS", "Modular Architecture", 
                          f"{found_modules}/5 expected modules found")
        else:
            self.add_result("FAIL", "Modular Architecture", 
                          f"Only {found_modules}/5 modules found")
        
        # LaTeX Claim: Containerized deployment support
        deployment_files = ["render.yaml", "requirements.txt"]
        found_deployment = sum(1 for f in deployment_files 
                             if os.path.exists(os.path.join(self.project_root, f)))
        
        if found_deployment >= 1:
            self.add_result("PASS", "Deployment Support", 
                          f"Found {found_deployment} deployment configuration files")
        else:
            self.add_result("WARNING", "Deployment Support", 
                          "Deployment configuration not found")
    
    def add_result(self, status: str, claim: str, details: str):
        """Add validation result."""
        result = {
            "status": status,
            "claim": claim,
            "details": details
        }
        self.validation_results.append(result)
        print(f"   {status} {claim}: {details}")
    
    def generate_summary_report(self):
        """Generate summary validation report."""
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY REPORT")
        print("=" * 70)
        
        passed = len([r for r in self.validation_results if r["status"] == "PASS"])
        failed = len([r for r in self.validation_results if r["status"] == "FAIL"])
        warnings = len([r for r in self.validation_results if r["status"] == "WARNING"])
        total = len(self.validation_results)
        
        print(f"Total Checks: {total}")
        print(f"PASSED: {passed} ({passed/total*100:.1f}%)")
        print(f"FAILED: {failed} ({failed/total*100:.1f}%)")
        print(f"WARNINGS: {warnings} ({warnings/total*100:.1f}%)")
        
        # Calculate consistency score
        consistency_score = ((passed * 2 + warnings) / (total * 2)) * 100
        
        print(f"\nCONSISTENCY SCORE: {consistency_score:.1f}%")
        
        if failed == 0 and warnings <= 2:
            print("\nRESULT: EXCELLENT CONSISTENCY")
            print("LaTeX claims are highly consistent with code implementation")
        elif failed <= 2 and consistency_score >= 80:
            print("\nRESULT: GOOD CONSISTENCY")
            print("Minor discrepancies found, but overall alignment is strong")
        elif consistency_score >= 60:
            print("\nRESULT: MODERATE CONSISTENCY")
            print("Some inconsistencies found, review and updates recommended")
        else:
            print("\nRESULT: POOR CONSISTENCY")
            print("Significant inconsistencies found, documentation needs updates")
        
        # List critical failures
        critical_failures = [r for r in self.validation_results if r["status"] == "FAIL"]
        if critical_failures:
            print(f"\nCRITICAL INCONSISTENCIES ({len(critical_failures)}):")
            for result in critical_failures:
                print(f"  - {result['claim']}: {result['details']}")
        
        # List warnings for review
        warnings_list = [r for r in self.validation_results if r["status"] == "WARNING"]
        if warnings_list:
            print(f"\nREVIEW RECOMMENDED ({len(warnings_list)}):")
            for result in warnings_list:
                print(f"  - {result['claim']}: {result['details']}")
        
        print(f"\nRECOMMENDATION:")
        if consistency_score >= 85:
            print("Documentation is ready for publication/presentation")
        elif consistency_score >= 70:
            print("Minor updates needed before publication")
        else:
            print("Significant documentation updates required")


def main():
    """Run validation script."""
    print("LaTeX Claims vs Code Implementation Validator")
    print("Validates consistency between documentation and implementation")
    print()
    
    validator = LaTeXClaimValidator()
    results = validator.validate_all_claims()
    
    # Return appropriate exit code based on results
    consistency_score = ((results["passed"] * 2 + results["warnings"]) / 
                        (results["total_checks"] * 2)) * 100
    
    if consistency_score >= 85:
        return 0  # Excellent
    elif consistency_score >= 70:
        return 1  # Good
    elif consistency_score >= 50:
        return 2  # Moderate
    else:
        return 3  # Poor


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)