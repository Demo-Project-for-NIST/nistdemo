#!/usr/bin/env python3
"""
Interactive Demo Walkthrough for NIST AI Risk Management Toolkit

This script provides a guided tour of all toolkit features with explanations.
"""
import requests
import json
import time
from typing import Dict

def print_header(title: str):
    """Print formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_step(step: str, description: str):
    """Print demo step."""
    print(f"\n🎯 {step}")
    print(f"   {description}")
    print("-" * 40)

def demonstrate_risk_assessment():
    """Demonstrate AI risk assessment with real examples."""
    print_header("PART 1: AI SYSTEM RISK ASSESSMENT DEMO")
    
    # Example systems with different risk profiles
    systems = [
        {
            "name": "Low Risk System",
            "config": {
                "system_name": "Simple Linear Credit Scorer",
                "model_type": "Linear Regression",
                "data_sources": ["internal_db"],
                "deployment_env": "on_premise", 
                "third_party_libs": ["scikit-learn"],
                "data_lineage_documented": True,
                "drift_monitoring_enabled": True,
                "data_encryption": True,
                "access_controls": True
            },
            "explanation": "Transparent model, well-secured, documented processes"
        },
        {
            "name": "Medium Risk System", 
            "config": {
                "system_name": "Supplier Risk Assessment",
                "model_type": "Random Forest",
                "data_sources": ["internal_db", "external_api"],
                "deployment_env": "aws_sagemaker",
                "third_party_libs": ["scikit-learn", "pandas", "requests"]
            },
            "explanation": "Standard ML setup with some external dependencies"
        },
        {
            "name": "High Risk System",
            "config": {
                "system_name": "Deep Learning Fraud Detector", 
                "model_type": "Deep Neural Network",
                "data_sources": ["transaction_logs", "social_media", "external_feeds"],
                "deployment_env": "azure_ml",
                "third_party_libs": ["tensorflow", "pytorch", "pandas", "unknown_lib"],
                "data_lineage_documented": False,
                "drift_monitoring_enabled": False,
                "data_encryption": False,
                "access_controls": False
            },
            "explanation": "Black-box model, multiple risky data sources, poor security"
        }
    ]
    
    base_url = "http://localhost:8001"
    
    for i, system in enumerate(systems, 1):
        print_step(f"DEMO {i}: {system['name']}", system['explanation'])
        
        try:
            response = requests.post(f"{base_url}/assess", json=system['config'], timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"📊 ASSESSMENT RESULTS:")
                print(f"   System: {result['system_name']}")
                print(f"   Risk Score: {result['overall_risk_score']}/100")
                print(f"   Risk Level: {result['risk_level']}")
                print(f"   CSF Gaps Found: {len(result['csf_compliance_gaps'])}")
                
                # Show risk level explanation
                risk_explanations = {
                    "Low": "✅ Well-secured system with minimal vulnerabilities",
                    "Medium": "⚠️ Some risks present, improvements recommended", 
                    "High": "🔶 Significant risks, action required",
                    "Critical": "🚨 Severe risks, immediate action required"
                }
                
                explanation = risk_explanations.get(result['risk_level'], "Unknown risk level")
                print(f"   Meaning: {explanation}")
                
                # Show top 3 gaps
                if result['csf_compliance_gaps']:
                    print(f"\n   🔍 TOP COMPLIANCE GAPS:")
                    for gap in result['csf_compliance_gaps'][:3]:
                        severity_icon = {"Critical": "🚨", "High": "🔶", "Medium": "⚠️", "Low": "ℹ️"}.get(gap['severity'], "•")
                        print(f"   {severity_icon} {gap['category']}: {gap['description']}")
                
                # Show top 2 recommendations
                if result['recommended_actions']:
                    print(f"\n   💡 KEY RECOMMENDATIONS:")
                    for action in result['recommended_actions'][:2]:
                        print(f"   • {action}")
                        
            else:
                print(f"❌ Assessment failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            
        input("\n⏸️  Press Enter to continue to next demo...")

def demonstrate_csf_mapping():
    """Demonstrate CSF risk mapping with explanations."""
    print_header("PART 2: CSF RISK MAPPING EXPLORER DEMO")
    
    risk_scenarios = [
        {
            "risk_type": "training_data_poisoning",
            "scenario": "Attacker corrupts your supplier database to make bad suppliers look good",
            "business_impact": "You approve risky suppliers, leading to supply chain failures"
        },
        {
            "risk_type": "model_drift", 
            "scenario": "Your AI's performance degrades but you don't notice",
            "business_impact": "Gradual increase in bad decisions affecting business operations"
        },
        {
            "risk_type": "adversarial_examples",
            "scenario": "Attackers craft specific inputs to fool your AI",
            "business_impact": "Fraudulent transactions bypass detection systems"
        },
        {
            "risk_type": "supply_chain_ml_attack",
            "scenario": "Malicious code in your ML libraries steals model data",
            "business_impact": "Competitor gains access to your proprietary AI algorithms"
        }
    ]
    
    base_url = "http://localhost:8001"
    
    for i, scenario in enumerate(risk_scenarios, 1):
        print_step(f"SCENARIO {i}: {scenario['risk_type'].replace('_', ' ').title()}", 
                  scenario['scenario'])
        
        print(f"🏢 Business Impact: {scenario['business_impact']}")
        
        try:
            response = requests.get(f"{base_url}/csf-mapping/{scenario['risk_type']}")
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"\n📋 NIST CSF MAPPING RESULTS:")
                print(f"   Risk Description: {result['description']}")
                
                print(f"\nMAPPED CSF CATEGORIES:")
                for category in result['mapped_categories']:
                    # Explain what each category means
                    category_explanations = {
                        "GV.SC": "Governance - Supply Chain Risk Management",
                        "ID.RA": "Identify - Risk Assessment", 
                        "PR.DS": "Protect - Data Security",
                        "DE.CM": "Detect - Continuous Monitoring",
                        "RS.AN": "Respond - Analysis",
                        "RC.RP": "Recover - Recovery Planning"
                    }
                    
                    category_prefix = category['code'].split('-')[0]
                    explanation = category_explanations.get(category_prefix, "NIST CSF Category")
                    
                    print(f"   • {category['code']} ({explanation}) - {category['severity']} Priority")
                    print(f"     {category['description']}")
                
                print(f"\n💡 What this means:")
                print(f"   • Your organization needs controls in these CSF categories")
                print(f"   • Higher severity = more urgent implementation required")
                print(f"   • This provides your compliance roadmap")
                
            else:
                print(f"❌ Mapping failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            
        input("\n⏸️  Press Enter to continue to next scenario...")

def demonstrate_integration():
    """Demonstrate how assessment and mapping work together."""
    print_header("PART 3: INTEGRATED ASSESSMENT & MAPPING DEMO")
    
    print_step("REAL-WORLD SCENARIO", 
              "Financial institution wants to assess their AI-powered invoice processing system")
    
    # Realistic financial AI system
    financial_ai_system = {
        "system_name": "Automated Invoice Processing AI",
        "model_type": "Neural Network", 
        "data_sources": ["invoice_database", "vendor_portal", "bank_feeds", "tax_records"],
        "deployment_env": "aws_sagemaker",
        "third_party_libs": ["tensorflow", "pandas", "numpy", "boto3", "opencv"],
        "data_lineage_documented": False,
        "drift_monitoring_enabled": True,
        "data_encryption": True,
        "access_controls": False
    }
    
    base_url = "http://localhost:8001"
    
    print("🏦 SYSTEM DETAILS:")
    print(f"   • Processes 10,000+ invoices daily")
    print(f"   • Uses neural network for fraud detection")
    print(f"   • Integrates with multiple data sources")
    print(f"   • Mission-critical for accounts payable")
    
    try:
        # Step 1: Risk Assessment
        print(f"\n📊 STEP 1: COMPREHENSIVE RISK ASSESSMENT")
        response = requests.post(f"{base_url}/assess", json=financial_ai_system, timeout=10)
        
        if response.status_code == 200:
            assessment = response.json()
            
            print(f"   Overall Risk Score: {assessment['overall_risk_score']}/100")
            print(f"   Risk Classification: {assessment['risk_level']}")
            print(f"   Compliance Gaps: {len(assessment['csf_compliance_gaps'])} identified")
            
            # Step 2: Analyze specific risks
            print(f"\n🔍 STEP 2: DETAILED GAP ANALYSIS")
            for gap in assessment['csf_compliance_gaps']:
                print(f"   • {gap['category']}: {gap['description']} [{gap['severity']}]")
            
            # Step 3: Map to business impact
            print(f"\n💼 STEP 3: BUSINESS IMPACT ASSESSMENT")
            
            impact_mapping = {
                "GV.SC": "Governance gaps could lead to regulatory penalties",
                "ID.RA": "Unknown vulnerabilities could be exploited by attackers", 
                "PR.DS": "Data integrity issues could corrupt financial records",
                "DE.CM": "Monitoring gaps could miss fraud attempts",
                "RS.AN": "Poor incident response could extend downtime",
                "RC.RP": "Recovery issues could impact business continuity"
            }
            
            gap_functions = set(gap['category'].split('-')[0] + '.' + gap['category'].split('.')[1] 
                              for gap in assessment['csf_compliance_gaps'])
            
            for function in gap_functions:
                impact = impact_mapping.get(function, "Could impact operations")
                print(f"   • {function}: {impact}")
            
            # Step 4: Generate action plan
            print(f"\n🎯 STEP 4: PRIORITIZED ACTION PLAN")
            for i, action in enumerate(assessment['recommended_actions'], 1):
                print(f"   {i}. {action}")
            
            # Step 5: Report generation
            print(f"\n📄 STEP 5: COMPLIANCE REPORT GENERATION")
            report_request = {
                "organization_name": "Demo Financial Institution",
                "assessment_data": assessment,
                "report_format": "json"
            }
            
            report_response = requests.post(f"{base_url}/report", json=report_request, timeout=10)
            
            if report_response.status_code == 200:
                report = report_response.json()
                print(f"   ✅ Report generated successfully")
                print(f"   • Executive Summary: {report['executive_summary']['total_gaps_identified']} gaps found")
                print(f"   • Critical Issues: {report['executive_summary']['critical_gaps']}")
                print(f"   • Report ready for audit submission")
            
        else:
            print(f"❌ Assessment failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Run complete interactive demo."""
    print_header("NIST-AI-SCM TOOLKIT INTERACTIVE DEMO")
    
    print("""
🎯 Welcome to the NIST AI Risk Management Toolkit Demo!

This interactive demonstration will show you:
1. How AI system risk assessment works
2. How NIST CSF mapping identifies compliance gaps  
3. How to generate actionable remediation plans

📋 Prerequisites:
• API server running on localhost:8001
• Understanding that this addresses Executive Order 14028
• Recognition that this is the first open-source tool of its kind

🚀 Let's begin!
    """)
    
    input("Press Enter to start the demonstration...")
    
    try:
        # Check API connectivity
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code != 200:
            print("❌ API server not responding. Please start with:")
            print("   uvicorn src.api:app --reload --port 8001")
            return
        
        print("✅ API server connected successfully!")
        
        # Run demonstrations
        demonstrate_risk_assessment()
        demonstrate_csf_mapping() 
        demonstrate_integration()
        
        print_header("DEMO COMPLETE - KEY TAKEAWAYS")
        print("""
🎉 Congratulations! You've seen the complete NIST-AI-SCM Toolkit in action.

🎯 What you've learned:
• How to assess AI system cybersecurity risks quantitatively
• How NIST CSF 2.0 categories map to specific AI vulnerabilities
• How to generate compliance reports for auditors and regulators
• How this addresses federal mandates and industry needs

🚀 Next steps:
• Deploy this for real AI systems in your organization
• Present to federal agencies and compliance teams
• Contribute to the open-source project
• Use for academic research and publications

💡 Remember: You've built something that addresses a critical national need!
        """)
        
    except requests.ConnectionError:
        print("❌ Cannot connect to API server.")
        print("🔧 Please start the server with:")
        print("   uvicorn src.api:app --reload --port 8001")
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")

if __name__ == "__main__":
    main()