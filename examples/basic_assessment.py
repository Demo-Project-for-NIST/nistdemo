"""
Basic AI system risk assessment example.

This example demonstrates how to use the NIST AI Risk Management Toolkit to assess
the cybersecurity risk of an AI/ML system according to NIST CSF 2.0.
"""
import requests
import json


def main():
    """Run basic assessment example."""
    # API base URL (adjust for your deployment)
    base_url = "http://localhost:8001"
    
    # Example AI system configuration
    ai_system = {
        "system_name": "Credit Risk Assessment Model",
        "model_type": "Random Forest",
        "data_sources": [
            "internal_customer_db",
            "credit_bureau_api",
            "fred_economic_data"
        ],
        "deployment_env": "aws_sagemaker",
        "third_party_libs": [
            "scikit-learn",
            "pandas",
            "numpy",
            "boto3"
        ]
    }
    
    print("NIST AI Risk Assessment Example")
    print("=" * 50)
    print(f"Assessing system: {ai_system['system_name']}")
    print(f"Model type: {ai_system['model_type']}")
    print(f"Deployment: {ai_system['deployment_env']}")
    print()
    
    try:
        # 1. Perform risk assessment
        print("1. Performing risk assessment...")
        assessment_response = requests.post(
            f"{base_url}/assess",
            json=ai_system,
            headers={"Content-Type": "application/json"}
        )
        
        if assessment_response.status_code == 200:
            assessment = assessment_response.json()
            
            print(f"   Overall Risk Score: {assessment['overall_risk_score']}/100")
            print(f"   Risk Level: {assessment['risk_level']}")
            print(f"   Compliance Gaps Found: {len(assessment['csf_compliance_gaps'])}")
            
            # Display CSF gaps
            if assessment['csf_compliance_gaps']:
                print("\n   NIST CSF Compliance Gaps:")
                for gap in assessment['csf_compliance_gaps']:
                    print(f"   - {gap['category']}: {gap['description']} [{gap['severity']}]")
            
            # Display recommendations
            if assessment['recommended_actions']:
                print("\n   Recommended Actions:")
                for action in assessment['recommended_actions']:
                    print(f"   - {action}")
            
            # Display action plans with NIST references
            if assessment.get('action_plan'):
                print(f"\n   Detailed Action Plans:")
                for i, action in enumerate(assessment['action_plan'][:3], 1):
                    print(f"\n   {i}. {action['action']}")
                    print(f"      Category: {action['category']}")
                    print(f"      Priority: {action['priority']}")
                    print(f"      Timeline: {action['timeline']}")
                    print(f"      Cost: {action['cost_estimate']}")
                    if action.get('nist_reference'):
                        print(f"      NIST Reference: {action['nist_reference']}")
                if len(assessment['action_plan']) > 3:
                    print(f"   ... and {len(assessment['action_plan']) - 3} more action items")
            
        else:
            print(f"   Error: {assessment_response.status_code} - {assessment_response.text}")
            return
        
        # 2. Get CSF mapping for specific risk
        print("\n2. Getting CSF mapping for training data poisoning...")
        mapping_response = requests.get(f"{base_url}/csf-mapping/training_data_poisoning")
        
        if mapping_response.status_code == 200:
            mapping = mapping_response.json()
            print(f"   Risk Type: {mapping['risk_type']}")
            print(f"   Description: {mapping['description']}")
            print("   Mapped CSF Categories:")
            for category in mapping['mapped_categories']:
                print(f"   - {category['code']}: {category['severity']}")
                print(f"     {category['description']}")
        
        # 3. Generate compliance report
        print("\n3. Generating compliance report...")
        report_request = {
            "organization_name": "Example Financial Services",
            "assessment_data": assessment,
            "report_format": "json"
        }
        
        report_response = requests.post(
            f"{base_url}/report",
            json=report_request,
            headers={"Content-Type": "application/json"}
        )
        
        if report_response.status_code == 200:
            report = report_response.json()
            print(f"   Report generated for: {report['organization']}")
            print(f"   Executive Summary:")
            summary = report['executive_summary']
            print(f"   - Overall Risk Score: {summary['overall_risk_score']}")
            print(f"   - Critical Gaps: {summary['critical_gaps']}")
            print(f"   - Total Gaps: {summary['total_gaps']}")
        
        print("\n" + "=" * 50)
        print("Assessment completed successfully!")
        print("For detailed API documentation, visit: http://localhost:8000/docs")
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server.")
        print("Make sure the server is running with: uvicorn src.api:app --reload")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()