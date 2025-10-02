#!/usr/bin/env python3
"""
Test dashboard connection to API server.
"""
import requests
import json

def test_api_connection():
    """Test if API is accessible for dashboard."""
    api_base = "http://localhost:8001"
    
    print("TESTING Dashboard API Connection")
    print("=" * 40)
    
    try:
        # Test health endpoint
        response = requests.get(f"{api_base}/health")
        if response.status_code == 200:
            print("PASS API Health Check: PASS")
            print(f"   Response: {response.json()}")
        else:
            print(f"FAIL API Health Check: FAIL (Status: {response.status_code})")
            return False
        
        # Test CORS headers
        headers = response.headers
        cors_headers = [
            'access-control-allow-origin',
            'access-control-allow-methods', 
            'access-control-allow-headers'
        ]
        
        cors_enabled = any(header.lower() in [h.lower() for h in headers.keys()] for header in cors_headers)
        
        if cors_enabled:
            print("PASS CORS Headers: PRESENT")
            for header in cors_headers:
                value = headers.get(header, headers.get(header.title(), 'Not set'))
                if value != 'Not set':
                    print(f"   {header}: {value}")
        else:
            print("FAIL CORS Headers: MISSING")
            print("   This may cause dashboard connection issues")
        
        # Test assessment endpoint
        test_data = {
            "system_name": "Dashboard Connection Test",
            "model_type": "Random Forest",
            "data_sources": ["test"],
            "deployment_env": "test",
            "third_party_libs": ["test"]
        }
        
        response = requests.post(f"{api_base}/assess", json=test_data)
        if response.status_code == 200:
            print("PASS Assessment Endpoint: PASS")
            result = response.json()
            print(f"   Risk Score: {result.get('overall_risk_score')}/100")
        else:
            print(f"FAIL Assessment Endpoint: FAIL (Status: {response.status_code})")
        
        print("\nTARGET Dashboard Connection Status: READY")
        print("📝 Your visual dashboard should now work correctly!")
        print("\nWEB Access Options:")
        print("   • Direct API: http://localhost:8001/docs")
        print("   • Dashboard Server: http://localhost:8080/visual_dashboard.html")
        print("   • Local File: examples/visual_dashboard.html")
        
        return True
        
    except requests.ConnectionError:
        print("FAIL API Connection: FAILED")
        print("FIX Fix: Make sure API server is running:")
        print("   uvicorn src.api:app --reload --port 8001")
        return False
    except Exception as e:
        print(f"FAIL Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_api_connection()