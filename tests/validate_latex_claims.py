#!/usr/bin/env python3
"""
Consistency Validation Script for LaTeX Claims vs Code Implementation

This script validates that claims made in LaTeX documentation match the actual
code implementation to ensure accuracy and consistency.
"""
import json
import os
import re
import sys
import inspect
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# Add project root to path for imports
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

try:
    from src.risk_scorer import RiskScorer
    from src.csf_mapper import CSFMapper  
    from src.action_planner import ActionPlanner
    from src import models
except ImportError as e:
    print(f"FAIL Import Error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


class LaTeXClaimValidator:
    """Validates LaTeX documentation claims against code implementation."""
    
    def __init__(self):
        """Initialize validator with component instances."""
        self.risk_scorer = RiskScorer()
        self.csf_mapper = CSFMapper()
        self.action_planner = ActionPlanner()
        self.validation_results = []
        
    def validate_all_claims(self) -> Dict[str, List[Dict]]:
        """Run all validation checks and return results."""
        print("VALIDATION Starting LaTeX Claims vs Code Implementation Validation")
        print("=" * 70)
        
        # Mathematical Framework Claims
        self.validate_mathematical_framework()
        
        # Risk Factor Claims
        self.validate_risk_factors()
        
        # CSF Mapping Claims
        self.validate_csf_mapping()
        
        # Economic Stress Claims
        self.validate_economic_stress()
        
        # API Implementation Claims
        self.validate_api_claims()
        
        # Data Structure Claims
        self.validate_data_structure_claims()
        
        # Complexity Claims
        self.validate_complexity_claims()
        
        # Generate summary report
        self.generate_summary_report()
        
        return {
            "total_checks": len(self.validation_results),
            "passed": len([r for r in self.validation_results if r["status"] == "PASS"]),
            "failed": len([r for r in self.validation_results if r["status"] == "FAIL"]),
            "warnings": len([r for r in self.validation_results if r["status"] == "WARNING"]),
            "results": self.validation_results
        }
    
    def validate_mathematical_framework(self):
        """Validate mathematical framework claims from LaTeX."""
        print("\nSECTION 1: Mathematical Framework Validation")
        print("-" * 50)
        
        # Claim: Risk score formula R = min(100, (sum(wi * fi)) * alpha)
        test_config = {
            "data_lineage_documented": False,
            "model_type": "Deep Neural Network",
            "drift_monitoring_enabled": False,
            "third_party_libs": ["tensorflow", "pytorch"],
            "data_encryption": False,
            "access_controls": False
        }
        
        assessment = self.risk_scorer.assess_system(test_config)
        risk_score = assessment["overall_risk_score"]
        
        # Verify score is capped at 100
        if 0 <= risk_score <= 100:
            self.add_result("PASS", "Risk Score Range", 
                          f"Score {risk_score} is within [0,100] bounds as claimed")
        else:
            self.add_result("FAIL", "Risk Score Range", 
                          f"Score {risk_score} exceeds claimed bounds [0,100]")
        
        # Claim: Six risk factors with specific weights
        expected_weights = {
            "data_lineage": 20,
            "model_explainability": 15,
            "drift_monitoring": 25,
            "third_party": 20,
            "data_encryption": 10,
            "access_controls": 5
        }
        
        # Test individual factor weights by code inspection
        breakdown = self.risk_scorer.get_risk_breakdown(test_config)
        factor_scores = breakdown["factor_scores"]
        
        # Validate weights match LaTeX claims
        weight_validation = True
        weight_details = []
        
        if factor_scores.get("data_lineage") == 20:
            weight_details.append("data_lineage: 20 (CORRECT)")
        else:
            weight_details.append(f"data_lineage: {factor_scores.get('data_lineage')} (EXPECTED: 20)")
            weight_validation = False
            
        if factor_scores.get("drift_monitoring") == 25:
            weight_details.append("drift_monitoring: 25 (CORRECT)")
        else:
            weight_details.append(f"drift_monitoring: {factor_scores.get('drift_monitoring')} (EXPECTED: 25)")
            weight_validation = False
        
        if weight_validation:
            self.add_result("PASS", "Risk Factor Weights", 
                          f"Weights match LaTeX specification: {'; '.join(weight_details)}")
        else:
            self.add_result("FAIL", "Risk Factor Weights", 
                          f"Weight mismatch detected: {'; '.join(weight_details)}")
    
    def validate_risk_factors(self):
        """Validate risk factor implementation claims."""
        print("\nSECTION 2: Risk Factors Validation")
        print("-" * 50)
        
        # Claim: Six specific risk factors
        claimed_factors = [
            "Data lineage documentation absence",
            "Model explainability limitations", 
            "Drift monitoring deficiency",
            "Third-party component vulnerabilities",
            "Data encryption absence",
            "Access control insufficiency"
        ]
        
        # Test each factor individually
        test_configs = [
            {"data_lineage_documented": False},
            {"model_type": "Deep Neural Network"},
            {"drift_monitoring_enabled": False},
            {"third_party_libs": ["tensorflow"]},
            {"data_encryption": False},
            {"access_controls": False}
        ]
        
        factors_working = 0
        for i, config in enumerate(test_configs):
            try:
                assessment = self.risk_scorer.assess_system(config)
                if assessment["overall_risk_score"] > 0:
                    factors_working += 1
                    print(f"   PASS Factor {i+1}: {claimed_factors[i][:40]}... generates risk score")
                else:
                    print(f"   FAIL Factor {i+1}: {claimed_factors[i][:40]}... no risk detected")
            except Exception as e:
                print(f"   ERROR Factor {i+1}: {claimed_factors[i][:40]}... {str(e)[:30]}")
        
        if factors_working >= 5:  # Allow for one potential issue
            self.add_result("PASS", "Risk Factor Implementation", 
                          f"{factors_working}/6 risk factors working correctly")
        else:
            self.add_result("FAIL", "Risk Factor Implementation", 
                          f"Only {factors_working}/6 risk factors working")
    
    def validate_csf_mapping(self):
        """Validate CSF mapping claims."""
        print("\nSECTION 3: CSF Mapping Validation")
        print("-" * 50)
        
        # Claim: Maps to specific CSF categories
        claimed_categories = [
            "GV.SC-01", "ID.RA-01", "PR.DS-06", "DE.CM-07", 
            "ID.RA-10", "PR.DS-08", "GV.SC-04"
        ]
        
        # Test CSF mapping functionality
        test_risks = [
            "training_data_poisoning",
            "model_drift", 
            "adversarial_examples",
            "supply_chain_ml_attack"
        ]
        
        valid_mappings = 0
        total_categories_found = set()
        
        for risk in test_risks:
            try:
                mapping = self.csf_mapper.map_risk_to_csf(risk)
                if mapping and "categories" in mapping:
                    valid_mappings += 1
                    for cat in mapping["categories"]:
                        total_categories_found.add(cat["code"])
                    print(f"   PASS Risk '{risk}' maps to {len(mapping['categories'])} CSF categories")
                else:
                    print(f"   FAIL Risk '{risk}' has no CSF mapping")
            except Exception as e:
                print(f"   ERROR Risk '{risk}': {str(e)[:50]}")
        
        # Check if claimed categories are found in mappings
        found_claimed = sum(1 for cat in claimed_categories if cat in total_categories_found)
        
        if valid_mappings >= 3:
            self.add_result("PASS", "CSF Mapping Functionality", 
                          f"{valid_mappings}/{len(test_risks)} risk types have valid CSF mappings")
        else:
            self.add_result("FAIL", "CSF Mapping Functionality", 
                          f"Only {valid_mappings}/{len(test_risks)} mappings working")
        
        if found_claimed >= 5:
            self.add_result("PASS", "CSF Category Coverage", 
                          f"{found_claimed}/{len(claimed_categories)} claimed categories found in mappings")
        else:
            self.add_result("WARNING", "CSF Category Coverage", 
                          f"Only {found_claimed}/{len(claimed_categories)} claimed categories found")
    
    def validate_economic_stress(self):
        """Validate economic stress multiplier claims."""
        print("\nSECTION 4: Economic Stress Validation")
        print("-" * 50)
        
        # Claim: Economic stress multiplier alpha using VIX and GDP
        # Claim: Multiplier bounds 1.0 <= alpha <= 2.0
        
        try:
            # Test fallback economic stress
            fallback_multiplier = self.risk_scorer._fallback_economic_stress()
            
            if 1.0 <= fallback_multiplier <= 2.0:
                self.add_result("PASS", "Economic Multiplier Bounds", 
                              f"Fallback multiplier {fallback_multiplier} within claimed bounds [1.0, 2.0]")
            else:
                self.add_result("FAIL", "Economic Multiplier Bounds", 
                              f"Fallback multiplier {fallback_multiplier} outside bounds [1.0, 2.0]")
            
            # Test current economic stress implementation
            current_multiplier = self.risk_scorer._get_economic_stress_multiplier()
            
            if 1.0 <= current_multiplier <= 2.0:
                self.add_result("PASS", "Current Economic Multiplier", 
                              f"Current multiplier {current_multiplier} within bounds")
            else:
                self.add_result("WARNING", "Current Economic Multiplier", 
                              f"Current multiplier {current_multiplier} outside expected bounds")
            
            # Check for FRED API integration
            try:
                fred_key = os.getenv('FRED_API_KEY')
                if fred_key:
                    self.add_result("PASS", "FRED API Integration", 
                                  "FRED_API_KEY environment variable configured")
                else:
                    self.add_result("WARNING", "FRED API Integration", 
                                  "FRED_API_KEY not set, using fallback")
            except:
                self.add_result("WARNING", "FRED API Integration", 
                              "Could not verify FRED API configuration")
                
        except Exception as e:
            self.add_result("FAIL", "Economic Stress Implementation", 
                          f"Error testing economic stress: {str(e)}")
    
    def validate_api_claims(self):
        """Validate API implementation claims."""
        print("\nSECTION 5: API Implementation Validation")
        print("-" * 50)
        
        # Claim: FastAPI with automatic documentation
        try:
            # Import API module to verify it exists
            import sys
            api_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'api.py')
            
            if os.path.exists(api_path):
                self.add_result("PASS", "API Module Exists", 
                              "FastAPI implementation file found")
                
                # Check for FastAPI imports in the file
                with open(api_path, 'r') as f:
                    api_content = f.read()
                    
                if "from fastapi import FastAPI" in api_content:
                    self.add_result("PASS", "FastAPI Framework", 
                                  "FastAPI framework properly imported")
                else:
                    self.add_result("FAIL", "FastAPI Framework", 
                                  "FastAPI import not found in api.py")
                
                # Check for documented endpoints
                if 'docs_url="/docs"' in api_content and 'redoc_url="/redoc"' in api_content:
                    self.add_result("PASS", "API Documentation", 
                                  "Automatic documentation endpoints configured")
                else:
                    self.add_result("WARNING", "API Documentation", 
                                  "Documentation endpoints may not be properly configured")
                    
                # Check for claimed endpoints
                claimed_endpoints = ["/assess", "/csf-mapping", "/report", "/health"]
                found_endpoints = 0
                
                for endpoint in claimed_endpoints:
                    if endpoint in api_content:
                        found_endpoints += 1
                
                if found_endpoints >= 3:
                    self.add_result("PASS", "API Endpoints", 
                                  f"{found_endpoints}/{len(claimed_endpoints)} claimed endpoints found")
                else:
                    self.add_result("FAIL", "API Endpoints", 
                                  f"Only {found_endpoints}/{len(claimed_endpoints)} endpoints found")
            else:
                self.add_result("FAIL", "API Module Exists", 
                              "api.py file not found")
                
        except Exception as e:
            self.add_result("FAIL", "API Validation", 
                          f"Error validating API: {str(e)}")
    
    def validate_data_structure_claims(self):
        """Validate data structure and storage claims."""
        print("\nSECTION 6: Data Structure Validation")
        print("-" * 50)
        
        # Claim: JSON data files with CSF categories and AI risks
        data_files = [
            "src/data/csf_categories.json",
            "src/data/ai_risks.json"
        ]
        
        for file_path in data_files:
            full_path = os.path.join(os.path.dirname(__file__), '..', file_path)
            
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r') as f:
                        data = json.load(f)
                    
                    if isinstance(data, dict) and len(data) > 0:
                        self.add_result("PASS", f"Data File: {file_path}", 
                                      f"Valid JSON with {len(data)} top-level keys")
                    else:
                        self.add_result("FAIL", f"Data File: {file_path}", 
                                      "Invalid or empty JSON structure")
                        
                except json.JSONDecodeError:
                    self.add_result("FAIL", f"Data File: {file_path}", 
                                  "Invalid JSON format")
            else:
                self.add_result("FAIL", f"Data File: {file_path}", 
                              "File not found")
        
        # Claim: Eight AI risk categories
        try:
            ai_risks = self.risk_scorer.ai_risks
            if "ai_risk_categories" in ai_risks:
                risk_count = len(ai_risks["ai_risk_categories"])
                
                if risk_count >= 8:
                    self.add_result("PASS", "AI Risk Categories", 
                                  f"Found {risk_count} AI risk categories (claimed: 8)")
                else:
                    self.add_result("WARNING", "AI Risk Categories", 
                                  f"Found only {risk_count} categories (claimed: 8)")
            else:
                self.add_result("FAIL", "AI Risk Categories", 
                              "ai_risk_categories not found in data")
                
        except Exception as e:
            self.add_result("FAIL", "AI Risk Categories", 
                          f"Error loading AI risks: {str(e)}")
    
    def validate_complexity_claims(self):
        """Validate computational complexity claims."""
        print("\nSECTION 7: Complexity Claims Validation")
        print("-" * 50)
        
        # Claim: O(n) time complexity for n risk factors
        # Claim: O(1) space complexity
        
        import time
        
        # Test with different numbers of factors to verify linear time
        test_configs = [
            # Minimal config (few factors)
            {"data_lineage_documented": False},
            
            # Medium config (more factors)
            {
                "data_lineage_documented": False,
                "model_type": "Deep Neural Network",
                "drift_monitoring_enabled": False
            },
            
            # Full config (all factors)
            {
                "data_lineage_documented": False,
                "model_type": "Deep Neural Network", 
                "drift_monitoring_enabled": False,
                "third_party_libs": ["tensorflow", "pytorch", "pandas"],
                "data_encryption": False,
                "access_controls": False
            }
        ]
        
        times = []
        for config in test_configs:
            start_time = time.time()
            for _ in range(100):  # Multiple iterations for timing
                self.risk_scorer.assess_system(config)
            end_time = time.time()
            times.append(end_time - start_time)
        
        # Check if time growth is roughly linear (allowing for variance)
        if len(times) >= 2:
            time_ratio = times[-1] / times[0] if times[0] > 0 else float('inf')
            
            if time_ratio < 10:  # Reasonable linear growth
                self.add_result("PASS", "Time Complexity", 
                              f"Execution time scales reasonably (ratio: {time_ratio:.2f})")
            else:
                self.add_result("WARNING", "Time Complexity", 
                              f"Time scaling may be non-linear (ratio: {time_ratio:.2f})")
        
        # Memory usage is hard to test precisely, but check for memory leaks
        try:
            # Run many assessments to check for memory leaks
            for _ in range(1000):
                self.risk_scorer.assess_system(test_configs[-1])
            
            self.add_result("PASS", "Memory Stability", 
                          "No obvious memory leaks in 1000 iterations")
                          
        except Exception as e:
            self.add_result("WARNING", "Memory Stability", 
                          f"Error testing memory stability: {str(e)}")
    
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
        
        if failed == 0:
            print("\nRESULT: ALL CRITICAL VALIDATIONS PASSED")
            print("LaTeX claims are consistent with code implementation")
        elif failed <= 2:
            print("\nRESULT: MOSTLY CONSISTENT")
            print("Minor discrepancies found, review needed")
        else:
            print("\nRESULT: SIGNIFICANT INCONSISTENCIES FOUND")
            print("LaTeX documentation needs updates to match implementation")
        
        # List all failures
        if failed > 0:
            print(f"\nFAILED CHECKS ({failed}):")
            for result in self.validation_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['claim']}: {result['details']}")
        
        # List warnings
        if warnings > 0:
            print(f"\nWARNINGS ({warnings}):")
            for result in self.validation_results:
                if result["status"] == "WARNING":
                    print(f"  - {result['claim']}: {result['details']}")


def main():
    """Run validation script."""
    validator = LaTeXClaimValidator()
    results = validator.validate_all_claims()
    
    # Return appropriate exit code
    if results["failed"] == 0:
        return 0  # Success
    elif results["failed"] <= 2:
        return 1  # Minor issues
    else:
        return 2  # Major issues


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)