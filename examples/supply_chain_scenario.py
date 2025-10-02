"""
Supply chain AI risk assessment scenario.

This example demonstrates assessing multiple AI systems in a supply chain
environment with different risk profiles.
"""
import requests
import json
from typing import List, Dict


def assess_system(base_url: str, system_config: Dict) -> Dict:
    """Assess a single AI system."""
    response = requests.post(
        f"{base_url}/assess",
        json=system_config,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Assessment failed: {response.status_code} - {response.text}")


def main():
    """Run supply chain assessment scenario."""
    base_url = "http://localhost:8001"
    
    # Define multiple AI systems in supply chain
    supply_chain_systems = [
        {
            "system_name": "Demand Forecasting Model",
            "model_type": "LSTM Neural Network",
            "data_sources": ["sales_history", "market_trends", "weather_data"],
            "deployment_env": "azure_ml",
            "third_party_libs": ["tensorflow", "pandas", "numpy", "scipy"],
            "data_lineage_documented": False,
            "drift_monitoring_enabled": True
        },
        {
            "system_name": "Supplier Risk Scoring",
            "model_type": "Gradient Boosting",
            "data_sources": ["financial_data", "compliance_records", "news_sentiment"],
            "deployment_env": "on_premise",
            "third_party_libs": ["xgboost", "scikit-learn", "pandas"],
            "data_lineage_documented": True,
            "drift_monitoring_enabled": False
        },
        {
            "system_name": "Fraud Detection System",
            "model_type": "Random Forest",
            "data_sources": ["transaction_logs", "user_behavior", "external_fraud_db"],
            "deployment_env": "aws_sagemaker",
            "third_party_libs": ["scikit-learn", "pandas", "numpy"],
            "data_lineage_documented": True,
            "drift_monitoring_enabled": True,
            "data_encryption": True,
            "access_controls": True
        },
        {
            "system_name": "Inventory Optimization",
            "model_type": "Linear Programming",
            "data_sources": ["inventory_levels", "demand_forecast", "supplier_lead_times"],
            "deployment_env": "google_cloud",
            "third_party_libs": ["scipy", "pandas", "numpy"],
            "data_lineage_documented": True,
            "drift_monitoring_enabled": False
        }
    ]
    
    print("Supply Chain AI Risk Assessment Scenario")
    print("=" * 60)
    print(f"Assessing {len(supply_chain_systems)} AI systems in supply chain")
    print()
    
    try:
        assessments = []
        total_risk_score = 0
        
        for i, system in enumerate(supply_chain_systems, 1):
            print(f"{i}. Assessing: {system['system_name']}")
            print(f"   Model Type: {system['model_type']}")
            print(f"   Environment: {system['deployment_env']}")
            
            assessment = assess_system(base_url, system)
            assessments.append(assessment)
            
            risk_score = assessment['overall_risk_score']
            risk_level = assessment['risk_level']
            total_risk_score += risk_score
            
            print(f"   Risk Score: {risk_score}/100 ({risk_level})")
            print(f"   CSF Gaps: {len(assessment['csf_compliance_gaps'])}")
            
            # Show critical gaps
            critical_gaps = [
                gap for gap in assessment['csf_compliance_gaps'] 
                if gap['severity'] == 'Critical'
            ]
            if critical_gaps:
                print(f"   Critical Issues:")
                for gap in critical_gaps:
                    print(f"   - {gap['category']}: {gap['description']}")
            
            print()
        
        # Supply chain summary
        avg_risk_score = total_risk_score / len(supply_chain_systems)
        
        print("Supply Chain Risk Summary")
        print("-" * 30)
        print(f"Average Risk Score: {avg_risk_score:.1f}/100")
        
        if avg_risk_score >= 70:
            print("Overall Risk Level: HIGH - Immediate action required")
        elif avg_risk_score >= 50:
            print("Overall Risk Level: MEDIUM - Review and improve")
        else:
            print("Overall Risk Level: LOW - Monitor and maintain")
        
        # Identify highest risk system
        highest_risk = max(assessments, key=lambda x: x['overall_risk_score'])
        print(f"Highest Risk System: {highest_risk['system_name']} ({highest_risk['overall_risk_score']}/100)")
        
        # Count gaps by CSF function
        all_gaps = []
        for assessment in assessments:
            all_gaps.extend(assessment['csf_compliance_gaps'])
        
        function_gaps = {}
        for gap in all_gaps:
            function = gap['category'].split('.')[0]  # Extract function (e.g., 'GV' from 'GV.SC-01')
            function_gaps[function] = function_gaps.get(function, 0) + 1
        
        if function_gaps:
            print("\nGaps by NIST CSF Function:")
            for function, count in sorted(function_gaps.items()):
                function_names = {
                    'GV': 'GOVERN',
                    'ID': 'IDENTIFY', 
                    'PR': 'PROTECT',
                    'DE': 'DETECT',
                    'RS': 'RESPOND',
                    'RC': 'RECOVER'
                }
                print(f"   {function_names.get(function, function)}: {count} gaps")
        
        # Recommendations for supply chain
        print("\nSupply Chain Recommendations:")
        print("1. Prioritize fixing critical gaps in highest risk systems")
        print("2. Implement standardized monitoring across all AI systems")
        print("3. Establish supply chain risk management policy (GV.SC-01)")
        print("4. Create incident response plan for AI system failures")
        print("5. Regular assessment schedule (quarterly recommended)")
        
        print("\n" + "=" * 60)
        print("Supply chain assessment completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server.")
        print("Make sure the server is running with: uvicorn src.api:app --reload")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()