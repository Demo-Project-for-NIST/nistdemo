#!/usr/bin/env python3
"""
NIST-AI-SCM Toolkit System Status Checker

Run this script to verify your system is working correctly.
"""
import requests
import json
import os
import sys
from datetime import datetime

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_status(check_name, status, details=""):
    """Print a status check result."""
    status_icon = "PASS" if status else "FAIL"
    print(f"{status_icon} {check_name}")
    if details:
        print(f"   {details}")

def check_files():
    """Check if required files exist."""
    print_header("FILE SYSTEM CHECKS")
    
    required_files = [
        "src/api.py",
        "src/models.py", 
        "src/database.py",
        "src/csf_mapper.py",
        "src/risk_scorer.py",
        "src/data/csf_categories.json",
        "src/data/ai_risks.json",
        "requirements.txt",
        "README.md"
    ]
    
    all_good = True
    for file_path in required_files:
        exists = os.path.exists(file_path)
        if not exists:
            all_good = False
        print_status(f"File: {file_path}", exists)
    
    # Check database
    db_exists = os.path.exists("nist_ai_scm.db")
    print_status("Database: nist_ai_scm.db", db_exists)
    if db_exists:
        size = os.path.getsize("nist_ai_scm.db")
        print(f"   Database size: {size} bytes")
    
    return all_good and db_exists

def check_api_server():
    """Check if API server is running and responsive."""
    print_header("API SERVER CHECKS")
    
    base_url = "http://localhost:8001"
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        health_ok = response.status_code == 200
        print_status("Health endpoint", health_ok, f"Status: {response.status_code}")
        if health_ok:
            data = response.json()
            print(f"   Service: {data.get('service', 'Unknown')}")
    except requests.RequestException as e:
        print_status("Health endpoint", False, f"Error: {str(e)}")
        print("   FIX Fix: Make sure API server is running with:")
        print("      uvicorn src.api:app --reload --port 8001")
        return False
    
    # Test 2: Root endpoint
    try:
        response = requests.get(base_url, timeout=5)
        root_ok = response.status_code == 200
        print_status("Root endpoint", root_ok, f"Status: {response.status_code}")
        if root_ok:
            data = response.json()
            print(f"   Version: {data.get('version', 'Unknown')}")
    except requests.RequestException as e:
        print_status("Root endpoint", False, f"Error: {str(e)}")
        return False
    
    # Test 3: CSF mapping
    try:
        response = requests.get(f"{base_url}/csf-mapping/training_data_poisoning", timeout=5)
        mapping_ok = response.status_code == 200
        print_status("CSF mapping endpoint", mapping_ok, f"Status: {response.status_code}")
        if mapping_ok:
            data = response.json()
            categories = len(data.get('mapped_categories', {}))
            print(f"   Mapped categories: {categories}")
    except requests.RequestException as e:
        print_status("CSF mapping endpoint", False, f"Error: {str(e)}")
        return False
    
    # Test 4: Risk assessment
    try:
        test_data = {
            "system_name": "System Check Test",
            "model_type": "Random Forest",
            "data_sources": ["test_db"],
            "deployment_env": "test",
            "third_party_libs": ["test_lib"]
        }
        response = requests.post(f"{base_url}/assess", json=test_data, timeout=10)
        assess_ok = response.status_code == 200
        print_status("Risk assessment endpoint", assess_ok, f"Status: {response.status_code}")
        if assess_ok:
            data = response.json()
            risk_score = data.get('overall_risk_score', 'Unknown')
            risk_level = data.get('risk_level', 'Unknown')
            gaps = len(data.get('csf_compliance_gaps', []))
            print(f"   Risk score: {risk_score}/100 ({risk_level})")
            print(f"   CSF gaps found: {gaps}")
    except requests.RequestException as e:
        print_status("Risk assessment endpoint", False, f"Error: {str(e)}")
        return False
    
    return health_ok and root_ok and mapping_ok and assess_ok

def check_data_integrity():
    """Check data file integrity."""
    print_header("DATA INTEGRITY CHECKS")
    
    # Check CSF categories
    try:
        with open("src/data/csf_categories.json", 'r') as f:
            csf_data = json.load(f)
        
        functions = csf_data.get('functions', {})
        function_count = len(functions)
        expected_functions = ['GOVERN', 'IDENTIFY', 'PROTECT', 'DETECT', 'RESPOND', 'RECOVER']
        has_all_functions = all(func in functions for func in expected_functions)
        
        print_status("CSF categories JSON", True, f"Functions: {function_count}")
        print_status("All 6 CSF functions present", has_all_functions)
        
        if has_all_functions:
            total_categories = sum(len(func_data.get('categories', {})) for func_data in functions.values())
            print(f"   Total categories: {total_categories}")
        
    except Exception as e:
        print_status("CSF categories JSON", False, f"Error: {str(e)}")
        return False
    
    # Check AI risks
    try:
        with open("src/data/ai_risks.json", 'r') as f:
            ai_data = json.load(f)
        
        risks = ai_data.get('ai_risk_categories', {})
        risk_count = len(risks)
        
        print_status("AI risks JSON", True, f"Risk categories: {risk_count}")
        
        # Check each risk has required fields
        valid_risks = 0
        for risk_name, risk_data in risks.items():
            required_fields = ['description', 'csf_mappings', 'base_risk_score']
            if all(field in risk_data for field in required_fields):
                valid_risks += 1
        
        print_status("All risks properly formatted", valid_risks == risk_count, 
                    f"{valid_risks}/{risk_count} valid")
        
    except Exception as e:
        print_status("AI risks JSON", False, f"Error: {str(e)}")
        return False
    
    return True

def check_examples():
    """Test example scripts."""
    print_header("EXAMPLE SCRIPTS CHECK")
    
    examples = [
        "examples/basic_assessment.py",
        "examples/supply_chain_scenario.py", 
        "examples/csf_exploration.py"
    ]
    
    all_good = True
    for example in examples:
        exists = os.path.exists(example)
        print_status(f"Example: {os.path.basename(example)}", exists)
        if not exists:
            all_good = False
    
    return all_good

def main():
    """Run complete system verification."""
    print_header("NIST-AI-SCM TOOLKIT SYSTEM VERIFICATION")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    checks = [
        ("File System", check_files),
        ("Data Integrity", check_data_integrity), 
        ("Example Scripts", check_examples),
        ("API Server", check_api_server),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_status(f"{check_name} check failed", False, f"Error: {str(e)}")
            results.append((check_name, False))
    
    # Summary
    print_header("SYSTEM STATUS SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        print_status(check_name, result)
    
    print(f"\nOverall Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("\nSUCCESS SYSTEM IS FULLY OPERATIONAL!")
        print("PASS All components working correctly")
        print("PASS Research prototype ready for evaluation")
        print("PASS Ready for research demonstrations")
        print("\nWEB Access your system:")
        print("   • API Documentation: http://localhost:8001/docs")
        print("   • Alternative Docs: http://localhost:8001/redoc") 
        print("   • Visual Dashboard: examples/visual_dashboard.html")
    else:
        print(f"\nWARNING  SYSTEM NEEDS ATTENTION ({total-passed} issues found)")
        print("📖 See SYSTEM_VERIFICATION_GUIDE.md for troubleshooting")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())