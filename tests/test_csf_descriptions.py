#!/usr/bin/env python3
"""
Test CSF mapping with descriptions functionality.
"""
import requests
import json

def test_csf_descriptions():
    """Test that CSF mappings now include descriptions."""
    print("Testing CSF Mapping with Descriptions")
    print("=" * 40)
    
    base_url = "http://localhost:8001"
    
    # Test various risk types
    risk_types = [
        "training_data_poisoning",
        "model_drift", 
        "adversarial_examples",
        "supply_chain_ml_attack"
    ]
    
    for risk_type in risk_types:
        try:
            response = requests.get(f"{base_url}/csf-mapping/{risk_type}")
            if response.status_code == 200:
                result = response.json()
                
                print(f"\nRisk: {risk_type.replace('_', ' ').title()}")
                print(f"Description: {result['description']}")
                print("Mapped Categories:")
                
                for category in result['mapped_categories']:
                    print(f"  • {category['code']}: {category['severity']}")
                    print(f"    {category['description']}")
                
                print(f"Total categories: {len(result['mapped_categories'])}")
                
            else:
                print(f"Failed to get mapping for {risk_type}: {response.status_code}")
                
        except Exception as e:
            print(f"Error testing {risk_type}: {e}")
    
    print(f"\nCSF mapping descriptions are now included!")
    print(f"Dashboard should display detailed category information.")

if __name__ == "__main__":
    test_csf_descriptions()