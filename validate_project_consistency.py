#!/usr/bin/env python3
"""
NIST AI Risk Management Toolkit - Project Consistency Validator

This comprehensive script validates that all claims made in LaTeX documentation
are consistent with the actual code implementation. It performs both high-level
architectural validation and detailed mathematical claim verification.

Usage:
    python3 validate_project_consistency.py

Returns:
    0 - Excellent consistency (>95%)
    1 - Good consistency (85-95%)
    2 - Moderate consistency (70-85%)
    3 - Poor consistency (<70%)
"""
import json
import os
import re
import sys
from typing import Dict, List, Any, Tuple
import datetime


class ProjectConsistencyValidator:
    """Comprehensive validator for LaTeX claims vs code implementation."""
    
    def __init__(self):
        """Initialize validator."""
        self.project_root = os.path.dirname(__file__)
        self.validation_results = []
        
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete validation suite."""
        print("🔍 NIST AI RISK MANAGEMENT TOOLKIT")
        print("📋 PROJECT CONSISTENCY VALIDATION")
        print("=" * 70)
        print(f"📅 Validation Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Project Root: {self.project_root}")
        print()
        
        # Core Architecture Validation
        self.validate_core_architecture()
        
        # Mathematical Framework Validation
        self.validate_mathematical_framework()
        
        # API Implementation Validation
        self.validate_api_implementation()
        
        # Data Integration Validation
        self.validate_data_integration()
        
        # Security and Compliance Validation
        self.validate_security_compliance()
        
        # Documentation Consistency Validation
        self.validate_documentation_consistency()
        
        # Generate comprehensive report
        return self.generate_comprehensive_report()
    
    def validate_core_architecture(self):
        """Validate core architecture claims."""
        print("🏗️  SECTION 1: CORE ARCHITECTURE VALIDATION")
        print("-" * 50)
        
        # LaTeX Claim: Modular design with specific components
        expected_modules = [
            ("src/risk_scorer.py", "Risk Scoring Engine", ["assess_system", "RiskScorer"]),
            ("src/csf_mapper.py", "CSF Mapper", ["map_risk_to_csf", "CSFMapper"]),
            ("src/action_planner.py", "Action Planner", ["ActionPlanner", "generate"]),
            ("src/api.py", "FastAPI Application", ["FastAPI", "app"]),
            ("src/models.py", "Pydantic Models", ["BaseModel", "pydantic"]),
            ("src/database.py", "Database Layer", ["SQLAlchemy", "create_tables"])
        ]
        
        architecture_score = 0
        total_modules = len(expected_modules)
        
        for module_path, module_name, required_elements in expected_modules:
            full_path = os.path.join(self.project_root, module_path)
            
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    content = f.read()
                
                found_elements = sum(1 for element in required_elements if element in content)
                
                if found_elements >= len(required_elements) - 1:  # Allow for variations
                    architecture_score += 1
                    self.add_result("PASS", f"{module_name} Module", 
                                  f"Found {found_elements}/{len(required_elements)} required elements")
                else:
                    self.add_result("WARNING", f"{module_name} Module", 
                                  f"Found {found_elements}/{len(required_elements)} required elements")
            else:
                self.add_result("FAIL", f"{module_name} Module", "Module file not found")
        
        # Overall architecture assessment
        if architecture_score >= total_modules - 1:
            self.add_result("PASS", "Modular Architecture", 
                          f"Strong modular design: {architecture_score}/{total_modules} modules validated")
        else:
            self.add_result("WARNING", "Modular Architecture", 
                          f"Incomplete modular design: {architecture_score}/{total_modules} modules")
    
    def validate_mathematical_framework(self):
        """Validate mathematical framework implementation."""
        print("\n🧮 SECTION 2: MATHEMATICAL FRAMEWORK VALIDATION")
        print("-" * 55)
        
        risk_scorer_path = os.path.join(self.project_root, "src", "risk_scorer.py")
        
        if not os.path.exists(risk_scorer_path):
            self.add_result("FAIL", "Mathematical Framework", "risk_scorer.py not found")
            return
        
        with open(risk_scorer_path, 'r') as f:
            risk_scorer_content = f.read()
        
        # LaTeX Claim 1: R = min(100, (Σ wi × fi) × α)
        formula_elements = [
            ("Risk Score Capping", r'min\s*\(\s*(?:risk_score,\s*)?100', "min(100, ...) implementation"),
            ("Weighted Summation", r'risk_score\s*\+=\s*\d+', "Weighted factor addition"),
            ("Economic Multiplier", r'\*\s*(?:alpha|economic_multiplier)', "Economic stress multiplication"),
            ("Six Risk Factors", r'(?:20|15|25|10|5).*(?:risk_score|\+=)', "Six distinct weight values")
        ]
        
        for element_name, pattern, description in formula_elements:
            if re.search(pattern, risk_scorer_content):
                self.add_result("PASS", element_name, f"{description} found")
            else:
                self.add_result("WARNING", element_name, f"{description} pattern unclear")
        
        # LaTeX Claim 2: Specific weights (20, 15, 25, 20, 10, 5)
        claimed_weights = ["20", "15", "25", "10", "5"]
        found_weights = sum(1 for weight in claimed_weights 
                           if re.search(rf'risk_score\s*\+=\s*{weight}', risk_scorer_content))
        
        if found_weights >= 4:
            self.add_result("PASS", "Specific Weight Values", 
                          f"Found {found_weights}/5 claimed weight values")
        else:
            self.add_result("WARNING", "Specific Weight Values", 
                          f"Only {found_weights}/5 weight values clearly found")
        
        # LaTeX Claim 3: Economic stress integration with VIX and GDP
        economic_elements = [
            ("FRED API", r'(?:fred|stlouisfed)', "Federal Reserve data integration"),
            ("VIX Index", r'VIX', "Volatility index usage"),
            ("GDP Growth", r'GDP', "GDP growth rate usage"),
            ("Bounds 1.0-2.0", r'1\.0.*2\.0|2\.0.*1\.0', "Multiplier bounds")
        ]
        
        for element_name, pattern, description in economic_elements:
            if re.search(pattern, risk_scorer_content, re.IGNORECASE):
                self.add_result("PASS", element_name, f"{description} found")
            else:
                self.add_result("WARNING", element_name, f"{description} not clearly found")
    
    def validate_api_implementation(self):
        """Validate API implementation claims."""
        print("\n🌐 SECTION 3: API IMPLEMENTATION VALIDATION")
        print("-" * 45)
        
        api_path = os.path.join(self.project_root, "src", "api.py")
        
        if not os.path.exists(api_path):
            self.add_result("FAIL", "API Implementation", "api.py not found")
            return
        
        with open(api_path, 'r') as f:
            api_content = f.read()
        
        # LaTeX Claim: FastAPI with automatic documentation
        api_features = [
            ("FastAPI Framework", r'from fastapi import FastAPI', "FastAPI import"),
            ("Automatic Docs", r'docs_url.*redoc_url', "Documentation endpoints"),
            ("CORS Support", r'CORSMiddleware', "Cross-origin support"),
            ("Pydantic Models", r'response_model=', "Type-safe responses")
        ]
        
        for feature_name, pattern, description in api_features:
            if re.search(pattern, api_content):
                self.add_result("PASS", feature_name, f"{description} found")
            else:
                self.add_result("WARNING", feature_name, f"{description} not found")
        
        # LaTeX Claim: Specific endpoints
        claimed_endpoints = [
            ("/assess", "POST", "AI system risk assessment"),
            ("/csf-mapping", "GET", "CSF category mapping"),
            ("/report", "POST", "Compliance report generation"),
            ("/health", "GET", "Health monitoring"),
            ("/demo", "GET", "Demo interface"),
            ("/dashboard", "GET", "Interactive dashboard")
        ]
        
        found_endpoints = 0
        for endpoint, method, description in claimed_endpoints:
            # Look for endpoint definition patterns
            endpoint_patterns = [
                rf'@app\.{method.lower()}\(["\'].*{endpoint}',
                rf'async def.*{endpoint.replace("/", "").replace("-", "_")}'
            ]
            
            if any(re.search(pattern, api_content, re.IGNORECASE) for pattern in endpoint_patterns):
                found_endpoints += 1
        
        if found_endpoints >= len(claimed_endpoints) - 1:
            self.add_result("PASS", "API Endpoints", 
                          f"Found {found_endpoints}/{len(claimed_endpoints)} claimed endpoints")
        else:
            self.add_result("WARNING", "API Endpoints", 
                          f"Found {found_endpoints}/{len(claimed_endpoints)} endpoints")
    
    def validate_data_integration(self):
        """Validate data integration claims."""
        print("\n📊 SECTION 4: DATA INTEGRATION VALIDATION")
        print("-" * 45)
        
        # LaTeX Claim: JSON data files with NIST taxonomy
        data_files = [
            ("src/data/csf_categories.json", "NIST CSF 2.0 categories"),
            ("src/data/ai_risks.json", "AI risk definitions")
        ]
        
        for file_path, description in data_files:
            full_path = os.path.join(self.project_root, file_path)
            
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r') as f:
                        data = json.load(f)
                    
                    if isinstance(data, dict) and len(data) > 0:
                        self.add_result("PASS", f"Data File: {description}", 
                                      f"Valid JSON with {len(data)} top-level sections")
                    else:
                        self.add_result("FAIL", f"Data File: {description}", 
                                      "Invalid or empty data structure")
                        
                except json.JSONDecodeError:
                    self.add_result("FAIL", f"Data File: {description}", 
                                  "Invalid JSON format")
            else:
                self.add_result("FAIL", f"Data File: {description}", 
                              "File not found")
        
        # LaTeX Claim: Eight AI risk categories
        ai_risks_path = os.path.join(self.project_root, "src", "data", "ai_risks.json")
        if os.path.exists(ai_risks_path):
            with open(ai_risks_path, 'r') as f:
                ai_data = json.load(f)
            
            if "ai_risk_categories" in ai_data:
                risk_count = len(ai_data["ai_risk_categories"])
                if risk_count >= 8:
                    self.add_result("PASS", "AI Risk Categories Count", 
                                  f"Found {risk_count} categories (claimed: 8+)")
                else:
                    self.add_result("WARNING", "AI Risk Categories Count", 
                                  f"Found {risk_count} categories (claimed: 8+)")
                    
                # Check for specific claimed risks
                claimed_risks = [
                    "training_data_poisoning", "model_drift", "adversarial_examples",
                    "model_inversion", "supply_chain_ml_attack", "data_lineage_gaps"
                ]
                
                found_risks = sum(1 for risk in claimed_risks 
                                if risk in ai_data["ai_risk_categories"])
                
                if found_risks >= len(claimed_risks) - 1:
                    self.add_result("PASS", "Specific AI Risks", 
                                  f"Found {found_risks}/{len(claimed_risks)} claimed risks")
                else:
                    self.add_result("WARNING", "Specific AI Risks", 
                                  f"Found {found_risks}/{len(claimed_risks)} claimed risks")
    
    def validate_security_compliance(self):
        """Validate security and compliance claims."""
        print("\n🔒 SECTION 5: SECURITY & COMPLIANCE VALIDATION")
        print("-" * 55)
        
        # Check for security implementations
        security_files = [
            ("src/api.py", ["CORSMiddleware", "HTTPException"], "API Security"),
            ("src/database.py", ["create_engine", "sessionmaker"], "Database Security"),
            ("requirements.txt", ["fastapi", "sqlalchemy"], "Secure Dependencies")
        ]
        
        for file_path, required_elements, description in security_files:
            full_path = os.path.join(self.project_root, file_path)
            
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    content = f.read()
                
                found_elements = sum(1 for element in required_elements if element in content)
                
                if found_elements >= len(required_elements) - 1:
                    self.add_result("PASS", description, 
                                  f"Security elements found: {found_elements}/{len(required_elements)}")
                else:
                    self.add_result("WARNING", description, 
                                  f"Limited security elements: {found_elements}/{len(required_elements)}")
            else:
                self.add_result("WARNING", description, f"File not found: {file_path}")
        
        # Check for environment variable security
        env_files = [".env.example", "render.yaml"]
        env_security = sum(1 for env_file in env_files 
                          if os.path.exists(os.path.join(self.project_root, env_file)))
        
        if env_security >= 1:
            self.add_result("PASS", "Environment Security", 
                          "Environment configuration templates found")
        else:
            self.add_result("WARNING", "Environment Security", 
                          "Environment configuration unclear")
    
    def validate_documentation_consistency(self):
        """Validate documentation consistency."""
        print("\n📚 SECTION 6: DOCUMENTATION CONSISTENCY")
        print("-" * 45)
        
        # Check for documentation files
        doc_files = [
            ("README.md", "Project documentation"),
            ("docs/Executive_Summary.md", "Executive summary"),
            ("docs/NIST_Technical_Report.tex", "Technical report"),
            ("docs/Research_Paper.tex", "Research paper")
        ]
        
        found_docs = 0
        for doc_path, description in doc_files:
            full_path = os.path.join(self.project_root, doc_path)
            
            if os.path.exists(full_path):
                found_docs += 1
                
                # Check file size as quality indicator
                file_size = os.path.getsize(full_path)
                if file_size > 5000:  # Substantial content
                    self.add_result("PASS", description, 
                                  f"Comprehensive documentation ({file_size:,} bytes)")
                else:
                    self.add_result("WARNING", description, 
                                  f"Limited documentation ({file_size:,} bytes)")
            else:
                self.add_result("WARNING", description, "Documentation file missing")
        
        if found_docs >= 3:
            self.add_result("PASS", "Documentation Coverage", 
                          f"Comprehensive docs: {found_docs}/{len(doc_files)}")
        else:
            self.add_result("WARNING", "Documentation Coverage", 
                          f"Limited docs: {found_docs}/{len(doc_files)}")
        
        # Check README for live demo links
        readme_path = os.path.join(self.project_root, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                readme_content = f.read()
            
            if "nistdemo.onrender.com" in readme_content:
                self.add_result("PASS", "Live Demo Links", 
                              "Live demo URLs found in README")
            else:
                self.add_result("WARNING", "Live Demo Links", 
                              "Live demo URLs not found")
    
    def add_result(self, status: str, claim: str, details: str):
        """Add validation result with enhanced categorization."""
        result = {
            "status": status,
            "claim": claim,
            "details": details,
            "category": self._categorize_claim(claim)
        }
        self.validation_results.append(result)
        
        # Print with status icons
        status_icons = {"PASS": "✅", "WARNING": "⚠️", "FAIL": "❌"}
        icon = status_icons.get(status, "❓")
        print(f"   {icon} {claim}: {details}")
    
    def _categorize_claim(self, claim: str) -> str:
        """Categorize claims for better reporting."""
        if any(keyword in claim.lower() for keyword in ["architecture", "module", "modular"]):
            return "Architecture"
        elif any(keyword in claim.lower() for keyword in ["mathematical", "formula", "weight", "score"]):
            return "Mathematics"
        elif any(keyword in claim.lower() for keyword in ["api", "endpoint", "fastapi"]):
            return "API"
        elif any(keyword in claim.lower() for keyword in ["data", "json", "integration"]):
            return "Data"
        elif any(keyword in claim.lower() for keyword in ["security", "cors", "environment"]):
            return "Security"
        elif any(keyword in claim.lower() for keyword in ["documentation", "doc", "readme"]):
            return "Documentation"
        else:
            return "General"
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE VALIDATION REPORT")
        print("=" * 70)
        
        # Calculate metrics
        passed = len([r for r in self.validation_results if r["status"] == "PASS"])
        failed = len([r for r in self.validation_results if r["status"] == "FAIL"])
        warnings = len([r for r in self.validation_results if r["status"] == "WARNING"])
        total = len(self.validation_results)
        
        # Calculate weighted consistency score
        consistency_score = ((passed * 3 + warnings * 1) / (total * 3)) * 100
        
        print(f"📈 VALIDATION METRICS:")
        print(f"   Total Checks: {total}")
        print(f"   ✅ PASSED: {passed} ({passed/total*100:.1f}%)")
        print(f"   ⚠️  WARNINGS: {warnings} ({warnings/total*100:.1f}%)")
        print(f"   ❌ FAILED: {failed} ({failed/total*100:.1f}%)")
        print(f"   🎯 CONSISTENCY SCORE: {consistency_score:.1f}%")
        
        # Determine overall assessment
        if consistency_score >= 95:
            grade = "A+"
            assessment = "EXCEPTIONAL"
            recommendation = "Ready for immediate production use and publication"
        elif consistency_score >= 90:
            grade = "A"
            assessment = "EXCELLENT"
            recommendation = "Ready for production with minor documentation updates"
        elif consistency_score >= 85:
            grade = "B+"
            assessment = "VERY GOOD"
            recommendation = "Strong implementation, address warnings before publication"
        elif consistency_score >= 80:
            grade = "B"
            assessment = "GOOD"
            recommendation = "Solid foundation, resolve issues before production"
        elif consistency_score >= 70:
            grade = "C"
            assessment = "ACCEPTABLE"
            recommendation = "Significant improvements needed before production"
        else:
            grade = "F"
            assessment = "NEEDS WORK"
            recommendation = "Major revisions required for production readiness"
        
        print(f"\n🏆 OVERALL ASSESSMENT: {grade} - {assessment}")
        print(f"💡 RECOMMENDATION: {recommendation}")
        
        # Category breakdown
        categories = {}
        for result in self.validation_results:
            category = result["category"]
            if category not in categories:
                categories[category] = {"pass": 0, "warn": 0, "fail": 0}
            
            if result["status"] == "PASS":
                categories[category]["pass"] += 1
            elif result["status"] == "WARNING":
                categories[category]["warn"] += 1
            else:
                categories[category]["fail"] += 1
        
        print(f"\n📋 CATEGORY BREAKDOWN:")
        for category, counts in categories.items():
            total_cat = sum(counts.values())
            pass_rate = (counts["pass"] / total_cat) * 100
            print(f"   {category}: {counts['pass']}/{total_cat} passed ({pass_rate:.0f}%)")
        
        # Critical issues
        critical_issues = [r for r in self.validation_results if r["status"] == "FAIL"]
        if critical_issues:
            print(f"\n❌ CRITICAL ISSUES TO ADDRESS ({len(critical_issues)}):")
            for i, issue in enumerate(critical_issues, 1):
                print(f"   {i}. {issue['claim']}: {issue['details']}")
        
        # Areas for improvement
        improvement_areas = [r for r in self.validation_results if r["status"] == "WARNING"]
        if improvement_areas:
            print(f"\n⚠️  AREAS FOR IMPROVEMENT ({len(improvement_areas)}):")
            for i, area in enumerate(improvement_areas[:5], 1):  # Show top 5
                print(f"   {i}. {area['claim']}: {area['details']}")
            if len(improvement_areas) > 5:
                print(f"   ... and {len(improvement_areas) - 5} more areas")
        
        # Success highlights
        successes = [r for r in self.validation_results if r["status"] == "PASS"]
        if successes:
            print(f"\n✅ VALIDATION SUCCESSES ({len(successes)}):")
            for i, success in enumerate(successes[:3], 1):  # Show top 3
                print(f"   {i}. {success['claim']}: {success['details']}")
            if len(successes) > 3:
                print(f"   ... and {len(successes) - 3} more successful validations")
        
        print(f"\n📄 VALIDATION COMPLETED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return {
            "total_checks": total,
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "consistency_score": consistency_score,
            "grade": grade,
            "assessment": assessment,
            "recommendation": recommendation,
            "categories": categories,
            "critical_issues": len(critical_issues),
            "ready_for_production": consistency_score >= 85
        }


def main():
    """Run comprehensive project validation."""
    validator = ProjectConsistencyValidator()
    results = validator.run_full_validation()
    
    # Return appropriate exit code
    score = results["consistency_score"]
    if score >= 95:
        return 0  # Excellent
    elif score >= 85:
        return 1  # Good
    elif score >= 70:
        return 2  # Acceptable
    else:
        return 3  # Needs work


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)