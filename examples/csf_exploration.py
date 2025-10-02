"""
NIST CSF 2.0 exploration example.

This example demonstrates exploring the NIST Cybersecurity Framework
categories and their mappings to AI risks.
"""
import requests
import json


def explore_csf_mappings(base_url: str):
    """Explore all AI risk to CSF mappings."""
    # List of AI risk types from our data
    ai_risk_types = [
        "training_data_poisoning",
        "model_drift", 
        "adversarial_examples",
        "model_inversion",
        "supply_chain_ml_attack",
        "data_lineage_gaps",
        "model_backdoors",
        "ai_system_dependency"
    ]
    
    print("NIST CSF 2.0 AI Risk Mappings")
    print("=" * 50)
    
    csf_category_count = {}
    
    for risk_type in ai_risk_types:
        try:
            response = requests.get(f"{base_url}/csf-mapping/{risk_type}")
            
            if response.status_code == 200:
                mapping = response.json()
                
                print(f"\nRisk: {risk_type.replace('_', ' ').title()}")
                print(f"Description: {mapping['description']}")
                
                if 'supply_chain_impact' in mapping:
                    print(f"Supply Chain Impact: {mapping.get('supply_chain_impact', 'N/A')}")
                
                print("Mapped CSF Categories:")
                for category in mapping['mapped_categories']:
                    print(f"  - {category['code']}: {category['severity']}")
                    print(f"    {category['description']}")
                    
                    # Count category usage
                    function = category['code'].split('.')[0]
                    csf_category_count[function] = csf_category_count.get(function, 0) + 1
                
            else:
                print(f"Error mapping {risk_type}: {response.status_code}")
                
        except Exception as e:
            print(f"Error processing {risk_type}: {str(e)}")
    
    # Summary of CSF function usage
    print("\n" + "=" * 50)
    print("CSF Function Usage Summary")
    print("-" * 30)
    
    function_names = {
        'GV': 'GOVERN - Cybersecurity governance',
        'ID': 'IDENTIFY - Asset and risk understanding',
        'PR': 'PROTECT - Safeguards implementation', 
        'DE': 'DETECT - Cybersecurity event detection',
        'RS': 'RESPOND - Incident response actions',
        'RC': 'RECOVER - Capability restoration'
    }
    
    for function, count in sorted(csf_category_count.items()):
        print(f"{function}: {count} mappings - {function_names.get(function, 'Unknown')}")
    
    # Identify most critical functions for AI systems
    print("\nMost Critical CSF Functions for AI Systems:")
    sorted_functions = sorted(csf_category_count.items(), key=lambda x: x[1], reverse=True)
    
    for i, (function, count) in enumerate(sorted_functions[:3], 1):
        print(f"{i}. {function} ({function_names.get(function, 'Unknown')}): {count} risk mappings")


def demonstrate_assessment_variations(base_url: str):
    """Demonstrate how different configurations affect risk scores."""
    print("\n" + "=" * 50)
    print("Risk Score Variations Demo")
    print("-" * 30)
    
    # Base configuration
    base_config = {
        "system_name": "Demo AI System",
        "model_type": "Random Forest",
        "data_sources": ["internal_db"],
        "deployment_env": "cloud",
        "third_party_libs": ["scikit-learn", "pandas"]
    }
    
    variations = [
        {
            "name": "Well-Secured System",
            "config": {
                **base_config,
                "data_lineage_documented": True,
                "drift_monitoring_enabled": True,
                "data_encryption": True,
                "access_controls": True
            }
        },
        {
            "name": "Basic System (default security)",
            "config": base_config
        },
        {
            "name": "High-Risk System",
            "config": {
                **base_config,
                "model_type": "Deep Neural Network",
                "data_lineage_documented": False,
                "drift_monitoring_enabled": False,
                "data_encryption": False,
                "access_controls": False,
                "third_party_libs": ["tensorflow", "pytorch", "unknown_lib1", "unknown_lib2"]
            }
        }
    ]
    
    for variation in variations:
        try:
            response = requests.post(
                f"{base_url}/assess",
                json=variation["config"],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                assessment = response.json()
                
                print(f"\n{variation['name']}:")
                print(f"  Risk Score: {assessment['overall_risk_score']}/100")
                print(f"  Risk Level: {assessment['risk_level']}")
                print(f"  CSF Gaps: {len(assessment['csf_compliance_gaps'])}")
                
                # Show top 3 recommendations
                if assessment['recommended_actions']:
                    print("  Top Recommendations:")
                    for i, action in enumerate(assessment['recommended_actions'][:3], 1):
                        print(f"    {i}. {action}")
            
        except Exception as e:
            print(f"Error assessing {variation['name']}: {str(e)}")


def main():
    """Run CSF exploration example."""
    base_url = "http://localhost:8001"
    
    try:
        # Check if API is accessible
        response = requests.get(f"{base_url}/health")
        if response.status_code != 200:
            raise Exception("API health check failed")
        
        # Explore CSF mappings
        explore_csf_mappings(base_url)
        
        # Demonstrate assessment variations
        demonstrate_assessment_variations(base_url)
        
        print("\n" + "=" * 50)
        print("CSF exploration completed!")
        print("Visit http://localhost:8000/docs for interactive API documentation")
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server.")
        print("Make sure the server is running with: uvicorn src.api:app --reload")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()