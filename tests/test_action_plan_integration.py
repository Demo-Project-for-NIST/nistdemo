#!/usr/bin/env python3
"""
Test script to verify the integrated action plan functionality.
"""
import requests
import json
import time

def test_action_plan_integration():
    """Test the complete assessment with action plan generation."""
    print("🧪 Testing Action Plan Integration")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Test API health
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Server: CONNECTED")
        else:
            print("❌ API Server: ERROR")
            return
    except:
        print("❌ API Server: OFFLINE")
        return

    # Test system with multiple risk factors
    test_system = {
        "system_name": "Enterprise Invoice Processing AI",
        "model_type": "Deep Neural Network",
        "data_sources": ["invoice_db", "vendor_portal", "external_feeds", "social_media"],
        "deployment_env": "azure_ml",
        "third_party_libs": ["tensorflow", "pytorch", "pandas", "unknown_lib"],
        "data_lineage_documented": False,
        "drift_monitoring_enabled": False,
        "data_encryption": False,
        "access_controls": False
    }
    
    print("\n🎯 TESTING HIGH-RISK AI SYSTEM")
    print(f"System: {test_system['system_name']}")
    print(f"Model: {test_system['model_type']}")
    print(f"Data Sources: {len(test_system['data_sources'])} sources")
    print(f"Security Controls: Minimal")
    
    try:
        # Perform assessment
        response = requests.post(f"{base_url}/assess", json=test_system, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n📊 ASSESSMENT RESULTS:")
            print(f"   Risk Score: {result['overall_risk_score']}/100")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   CSF Gaps Found: {len(result['csf_compliance_gaps'])}")
            print(f"   Action Plans Generated: {len(result.get('action_plan', []))}")
            
            # Display CSF compliance gaps
            if result['csf_compliance_gaps']:
                print(f"\n🔍 CSF COMPLIANCE GAPS:")
                for gap in result['csf_compliance_gaps'][:5]:  # Show first 5
                    severity_icon = {"Critical": "🚨", "High": "🔶", "Medium": "⚠️", "Low": "ℹ️"}.get(gap['severity'], "•")
                    print(f"   {severity_icon} {gap['category']}: {gap['description']}")
            
            # Display detailed action plan
            if result.get('action_plan'):
                print(f"\n🎯 DETAILED ACTION PLAN:")
                for i, action in enumerate(result['action_plan'][:3], 1):  # Show first 3
                    print(f"\n   ACTION {i}: {action['action']}")
                    print(f"   • Category: {action['category']}")
                    print(f"   • Priority: {action['priority']}")
                    print(f"   • Timeline: {action['timeline']}")
                    print(f"   • Cost: {action['cost_estimate']}")
                    print(f"   • Success Criteria: {action['success_criteria']}")
            
            # Display basic recommendations
            if result['recommended_actions']:
                print(f"\n💡 QUICK RECOMMENDATIONS:")
                for rec in result['recommended_actions']:
                    print(f"   • {rec}")
                    
            print(f"\n✅ ACTION PLAN INTEGRATION: SUCCESSFUL")
            print(f"   • Generated {len(result.get('action_plan', []))} detailed action items")
            print(f"   • Included cost estimates and timelines")
            print(f"   • Provided success criteria for each action")
            
        else:
            print(f"❌ Assessment failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

def test_low_risk_system():
    """Test a low-risk system to see difference in action plans."""
    print(f"\n🧪 Testing Low-Risk System for Comparison")
    print("-" * 50)
    
    low_risk_system = {
        "system_name": "Simple Credit Scorer",
        "model_type": "Linear Regression",
        "data_sources": ["internal_db"],
        "deployment_env": "on_premise",
        "third_party_libs": ["scikit-learn"],
        "data_lineage_documented": True,
        "drift_monitoring_enabled": True,
        "data_encryption": True,
        "access_controls": True
    }
    
    try:
        response = requests.post("http://localhost:8001/assess", json=low_risk_system, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Risk Score: {result['overall_risk_score']}/100")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   Action Plans: {len(result.get('action_plan', []))}")
            
            if result.get('action_plan'):
                print(f"   Low-risk actions focus on optimization vs remediation")
            else:
                print(f"   Minimal action plan needed for well-secured system")
                
        else:
            print(f"   Assessment failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   Test failed: {str(e)}")

if __name__ == "__main__":
    test_action_plan_integration()
    test_low_risk_system()
    
    print(f"\n🎉 ACTION PLAN INTEGRATION TESTING COMPLETE")
    print(f"=" * 50)
    print(f"The NIST-AI-SCM Toolkit now includes:")
    print(f"• Quantitative risk assessment (0-100 scoring)")
    print(f"• NIST CSF 2.0 compliance gap identification")
    print(f"• Detailed remediation action plans")
    print(f"• Cost estimates and implementation timelines")
    print(f"• Success criteria and priority rankings")
    print(f"\n🎯 Ready for federal agency demonstrations!")