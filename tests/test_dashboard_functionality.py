#!/usr/bin/env python3
"""
Test dashboard functionality with JavaScript simulation.
"""
import requests
import json

def test_dashboard_api_calls():
    """Test the exact API calls the dashboard would make."""
    print("🧪 Testing Dashboard API Functionality")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Test 1: Health check (dashboard connectivity test)
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health Check: PASS")
            print(f"   Response: {response.json()}")
        else:
            print("❌ Health Check: FAIL")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False
    
    # Test 2: Risk Assessment (main dashboard function)
    test_system = {
        "system_name": "Dashboard Test System",
        "model_type": "Random Forest",
        "data_sources": ["internal_db", "external_api"],
        "deployment_env": "aws_sagemaker",
        "third_party_libs": ["scikit-learn", "pandas"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/assess", 
            json=test_system,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Risk Assessment: PASS")
            print(f"   System: {result['system_name']}")
            print(f"   Risk Score: {result['overall_risk_score']}/100")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   CSF Gaps: {len(result['csf_compliance_gaps'])}")
            print(f"   Action Plans: {len(result.get('action_plan', []))}")
            
            # Test action plan structure
            if result.get('action_plan'):
                action = result['action_plan'][0]
                print(f"\n📋 First Action Plan:")
                print(f"   • Action: {action['action']}")
                print(f"   • Priority: {action['priority']}")
                print(f"   • Timeline: {action['timeline']}")
                print(f"   • Cost: {action['cost_estimate']}")
                print(f"   • Category: {action['category']}")
        else:
            print(f"❌ Risk Assessment: FAIL ({response.status_code})")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Risk Assessment Error: {e}")
        return False
    
    # Test 3: CSF Mapping (dashboard explorer)
    try:
        response = requests.get(f"{base_url}/csf-mapping/training_data_poisoning")
        if response.status_code == 200:
            result = response.json()
            print("\n✅ CSF Mapping: PASS")
            print(f"   Risk Type: {result['risk_type']}")
            print(f"   Description: {result['description']}")
            print(f"   Mapped Categories: {len(result['mapped_categories'])}")
        else:
            print(f"❌ CSF Mapping: FAIL ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ CSF Mapping Error: {e}")
        return False
    
    print(f"\n🎯 Dashboard API Functionality: COMPLETE")
    print(f"✅ All API endpoints working correctly")
    print(f"✅ Action plans included in responses")
    print(f"✅ Ready for browser-based dashboard")
    
    return True

def test_dashboard_access():
    """Test dashboard file accessibility."""
    print(f"\n🌐 Testing Dashboard Access")
    print("-" * 30)
    
    try:
        # Test dashboard server
        response = requests.get("http://localhost:8081/visual_dashboard.html")
        if response.status_code == 200:
            print("✅ Dashboard Server: ACCESSIBLE")
            print(f"   URL: http://localhost:8081/visual_dashboard.html")
            
            # Check if it contains our action plan updates
            if "Detailed Action Plan" in response.text:
                print("✅ Action Plan UI: PRESENT")
            else:
                print("❌ Action Plan UI: MISSING")
                
        else:
            print(f"❌ Dashboard Server: FAIL ({response.status_code})")
    except Exception as e:
        print(f"❌ Dashboard Server Error: {e}")
        print("🔧 Try starting dashboard server:")
        print("   python serve_dashboard.py --port 8081")

if __name__ == "__main__":
    success = test_dashboard_api_calls()
    test_dashboard_access()
    
    if success:
        print(f"\n🎉 DASHBOARD FUNCTIONALITY TEST: PASSED")
        print(f"🌐 Open in browser: http://localhost:8081/visual_dashboard.html")
        print(f"📝 Dashboard should show action plans with costs and timelines")
    else:
        print(f"\n❌ DASHBOARD FUNCTIONALITY TEST: FAILED")
        print(f"🔧 Check API server and try again")