"""
Action Plan Generator for NIST-AI-SCM Toolkit.

Generates detailed, prioritized remediation action plans based on risk assessments and CSF gaps.
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .models import CSFGap, RiskLevel, ActionPlan


class ActionPlanner:
    """Generates prioritized action plans for AI system risk remediation."""
    
    def __init__(self):
        """Initialize action planner with remediation knowledge base."""
        self.remediation_templates = self._load_remediation_templates()
        self.timeline_matrix = self._build_timeline_matrix()
        self.cost_estimates = self._build_cost_estimates()
        self.nist_references = self._load_nist_references()
    
    def _load_remediation_templates(self) -> Dict:
        """Load remediation action templates."""
        return {
            # Governance Actions (GV)
            "GV.SC-01": {
                "title": "Establish Supply Chain Risk Management Strategy",
                "description": "Develop comprehensive cybersecurity supply chain risk management program",
                "actions": [
                    "Draft supply chain cybersecurity policy document",
                    "Define roles and responsibilities for supply chain security",
                    "Establish supplier security assessment criteria",
                    "Create incident response procedures for supply chain events",
                    "Implement regular supplier security reviews"
                ],
                "effort": "High",
                "timeline": "60-90 days",
                "priority": "Critical"
            },
            "GV.OC-02": {
                "title": "Implement AI Governance and Transparency",
                "description": "Establish oversight and transparency for AI decision-making processes",
                "actions": [
                    "Create AI governance committee with cross-functional representation",
                    "Develop AI ethics and responsible use guidelines",
                    "Implement AI decision audit trails and logging",
                    "Establish human oversight requirements for critical AI decisions",
                    "Create AI risk tolerance and acceptance criteria"
                ],
                "effort": "Medium",
                "timeline": "30-60 days",
                "priority": "High"
            },
            
            # Identify Actions (ID)
            "ID.RA-01": {
                "title": "Comprehensive AI Asset Vulnerability Assessment", 
                "description": "Identify and document vulnerabilities in AI/ML system components",
                "actions": [
                    "Conduct thorough inventory of all AI system components",
                    "Perform vulnerability scanning on AI infrastructure",
                    "Assess model architecture for inherent vulnerabilities",
                    "Evaluate training data sources for integrity risks",
                    "Document all identified vulnerabilities with severity ratings"
                ],
                "effort": "Medium",
                "timeline": "14-30 days",
                "priority": "High"
            },
            "ID.AM-03": {
                "title": "Implement Data Lineage Documentation",
                "description": "Establish comprehensive data flow and lineage tracking",
                "actions": [
                    "Map all data sources feeding into AI systems",
                    "Document data transformation and processing steps",
                    "Implement automated data lineage tracking tools",
                    "Create data quality monitoring and validation processes",
                    "Establish data provenance verification procedures"
                ],
                "effort": "Medium",
                "timeline": "30-45 days", 
                "priority": "Medium"
            },
            "ID.SC-04": {
                "title": "Third-Party Component Security Assessment",
                "description": "Assess and prioritize security of third-party ML libraries and dependencies",
                "actions": [
                    "Inventory all third-party ML libraries and dependencies",
                    "Assess security posture of critical ML library vendors",
                    "Implement dependency vulnerability scanning",
                    "Establish approved library whitelist and approval process",
                    "Create vendor security questionnaire and assessment program"
                ],
                "effort": "Medium",
                "timeline": "21-45 days",
                "priority": "Medium"
            },
            
            # Protect Actions (PR)
            "PR.DS-06": {
                "title": "Implement Training Data Integrity Verification",
                "description": "Establish cryptographic and procedural controls for training data integrity",
                "actions": [
                    "Implement cryptographic hashing for training datasets",
                    "Establish data integrity verification procedures",
                    "Deploy automated data validation and anomaly detection",
                    "Create secure data storage and access controls",
                    "Implement training data version control and audit trails"
                ],
                "effort": "High",
                "timeline": "45-90 days",
                "priority": "Critical"
            },
            "PR.AC-07": {
                "title": "Implement Access Controls for AI Systems",
                "description": "Establish robust access controls and authentication for AI system components",
                "actions": [
                    "Implement multi-factor authentication for AI system access",
                    "Establish role-based access controls (RBAC) for AI operations",
                    "Deploy privileged access management (PAM) for AI infrastructure",
                    "Create API security and rate limiting controls",
                    "Implement session management and timeout controls"
                ],
                "effort": "Medium",
                "timeline": "30-60 days",
                "priority": "High"
            },
            
            # Detect Actions (DE)
            "DE.CM-07": {
                "title": "Deploy Continuous ML Model Monitoring",
                "description": "Implement comprehensive monitoring for ML model performance and drift",
                "actions": [
                    "Deploy automated model drift detection systems",
                    "Implement performance degradation alerting",
                    "Create model behavior anomaly detection",
                    "Establish baseline performance metrics and thresholds",
                    "Implement real-time model prediction monitoring"
                ],
                "effort": "High",
                "timeline": "30-60 days",
                "priority": "Critical"
            },
            "DE.AE-02": {
                "title": "Implement Adversarial Attack Detection",
                "description": "Deploy systems to detect adversarial examples and input manipulation",
                "actions": [
                    "Implement input validation and sanitization",
                    "Deploy adversarial example detection algorithms",
                    "Create statistical input distribution monitoring",
                    "Establish input anomaly detection and alerting",
                    "Implement ensemble model consensus checking"
                ],
                "effort": "High",
                "timeline": "60-90 days",
                "priority": "High"
            },
            
            # Respond Actions (RS)
            "RS.AN-01": {
                "title": "Establish AI Incident Analysis Procedures",
                "description": "Create procedures for investigating and analyzing AI-related security incidents",
                "actions": [
                    "Develop AI-specific incident response playbooks",
                    "Train incident response team on AI system forensics",
                    "Establish model rollback and recovery procedures",
                    "Create AI incident classification and severity matrix",
                    "Implement automated incident data collection for AI systems"
                ],
                "effort": "Medium",
                "timeline": "21-45 days",
                "priority": "Medium"
            },
            
            # Recover Actions (RC)
            "RC.RP-04": {
                "title": "Develop AI System Recovery Planning",
                "description": "Establish recovery procedures for AI system failures and incidents",
                "actions": [
                    "Create AI system backup and recovery procedures",
                    "Develop model retraining and redeployment protocols",
                    "Establish fallback procedures for AI system failures",
                    "Create business continuity plans for AI-dependent operations",
                    "Implement automated recovery testing and validation"
                ],
                "effort": "Medium", 
                "timeline": "30-60 days",
                "priority": "Medium"
            }
        }
    
    def _build_timeline_matrix(self) -> Dict:
        """Build timeline matrix for different effort levels."""
        return {
            "Critical": {
                "Low": "7-14 days",
                "Medium": "14-30 days", 
                "High": "30-45 days"
            },
            "High": {
                "Low": "14-21 days",
                "Medium": "21-45 days",
                "High": "45-60 days"
            },
            "Medium": {
                "Low": "21-30 days",
                "Medium": "30-60 days",
                "High": "60-90 days"
            },
            "Low": {
                "Low": "30-60 days",
                "Medium": "60-90 days",
                "High": "90-120 days"
            }
        }
    
    def _build_cost_estimates(self) -> Dict:
        """Build cost estimation matrix."""
        return {
            "Low": {"min": 5000, "max": 15000, "description": "Primarily process and policy changes"},
            "Medium": {"min": 15000, "max": 50000, "description": "Some tooling and system modifications"},
            "High": {"min": 50000, "max": 150000, "description": "Significant system changes and new tools"}
        }
    
    def _load_nist_references(self) -> Dict:
        """Load official NIST guideline reference links."""
        return {
            # NIST CSF 2.0 Core References
            "GV.SC-01": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=25",
            "GV.SC-02": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=25", 
            "GV.SC-03": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=25",
            "GV.SC-04": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=25",
            "GV.OC-02": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=23",
            
            # AI Risk Management Framework
            "ID.RA-01": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf#page=45",
            "ID.AM-03": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=30",
            "ID.SC-04": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=32",
            
            # Data Security and Protection
            "PR.DS-06": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf#page=195",
            "PR.DS-08": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf#page=195",
            
            # Detection and Monitoring
            "DE.CM-07": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=40",
            "DE.AE-02": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=39",
            
            # Response and Analysis
            "RS.AN-01": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=43",
            "RS.AN-02": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=43",
            
            # Recovery Planning
            "RC.RP-04": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=46",
            
            # Default CSF 2.0 Reference
            "default": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf"
        }
    
    def generate_action_plan_simple(
        self, 
        csf_gaps: List[CSFGap], 
        system_config: Dict,
        overall_risk_score: int
    ) -> List[ActionPlan]:
        """
        Generate simplified action plan as list of ActionPlan objects for API response.
        
        Args:
            csf_gaps: List of identified CSF compliance gaps
            system_config: AI system configuration
            overall_risk_score: Overall risk score (0-100)
            
        Returns:
            List of ActionPlan objects for API response
        """
        action_plans = []
        
        # Process each CSF gap
        for gap in csf_gaps:
            category = gap.category
            
            if category in self.remediation_templates:
                template = self.remediation_templates[category]
                
                # Determine urgency and priority
                urgency = self._calculate_urgency(gap.severity, overall_risk_score)
                priority = "High" if gap.severity in [RiskLevel.CRITICAL, RiskLevel.HIGH] else "Medium"
                
                # Format cost estimate as string
                cost_data = self._estimate_cost(template["effort"])
                cost_str = f"${cost_data['min']:,} - ${cost_data['max']:,}"
                
                # Format success criteria as string
                criteria_list = self._generate_success_criteria(category)
                criteria_str = "; ".join(criteria_list) if isinstance(criteria_list, list) else str(criteria_list)
                
                # Get NIST reference link
                nist_ref = self.nist_references.get(category, self.nist_references["default"])
                
                action_plan = ActionPlan(
                    action=template["title"],
                    category=category,
                    priority=priority,
                    timeline=template["timeline"],
                    cost_estimate=cost_str,
                    success_criteria=criteria_str,
                    nist_reference=nist_ref
                )
                
                action_plans.append(action_plan)
        
        # Sort by priority and severity
        action_plans.sort(key=lambda x: (
            0 if x.priority == "High" else 1,
            x.category
        ))
        
        return action_plans[:10]  # Return top 10 actions

    def generate_action_plan(
        self, 
        csf_gaps: List[CSFGap], 
        system_config: Dict,
        overall_risk_score: int
    ) -> Dict:
        """
        Generate comprehensive action plan based on CSF gaps and system configuration.
        
        Args:
            csf_gaps: List of identified CSF compliance gaps
            system_config: AI system configuration
            overall_risk_score: Overall risk score (0-100)
            
        Returns:
            Comprehensive action plan with priorities, timelines, and costs
        """
        
        # Phase 1: Immediate Actions (0-30 days)
        phase_1_actions = []
        # Phase 2: Short-term Actions (30-90 days)  
        phase_2_actions = []
        # Phase 3: Long-term Actions (90+ days)
        phase_3_actions = []
        
        total_estimated_cost = 0
        
        # Process each CSF gap
        for gap in csf_gaps:
            category = gap.category
            
            if category in self.remediation_templates:
                template = self.remediation_templates[category]
                
                # Determine urgency based on severity and overall risk
                urgency = self._calculate_urgency(gap.severity, overall_risk_score)
                
                action_item = {
                    "csf_category": category,
                    "title": template["title"],
                    "description": template["description"],
                    "severity": gap.severity,
                    "urgency": urgency,
                    "effort_level": template["effort"],
                    "estimated_timeline": template["timeline"],
                    "detailed_actions": template["actions"],
                    "estimated_cost": self._estimate_cost(template["effort"]),
                    "success_criteria": self._generate_success_criteria(category),
                    "responsible_team": self._assign_responsible_team(category),
                    "dependencies": self._identify_dependencies(category, csf_gaps)
                }
                
                # Assign to appropriate phase based on urgency and effort
                if urgency == "Immediate" or gap.severity == RiskLevel.CRITICAL:
                    phase_1_actions.append(action_item)
                elif urgency == "High" or gap.severity == RiskLevel.HIGH:
                    phase_2_actions.append(action_item)
                else:
                    phase_3_actions.append(action_item)
                
                total_estimated_cost += action_item["estimated_cost"]["max"]
        
        # Add system-specific recommendations
        system_actions = self._generate_system_specific_actions(system_config, overall_risk_score)
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(
            len(csf_gaps), overall_risk_score, total_estimated_cost
        )
        
        # Build comprehensive action plan
        action_plan = {
            "generated_date": datetime.utcnow().isoformat(),
            "system_name": system_config.get("system_name", "Unknown System"),
            "overall_risk_score": overall_risk_score,
            "total_gaps": len(csf_gaps),
            "estimated_total_cost": {
                "min": total_estimated_cost * 0.6,  # 40% contingency reduction
                "max": total_estimated_cost * 1.2,  # 20% contingency increase
                "currency": "USD"
            },
            "estimated_completion_time": "3-6 months",
            "executive_summary": executive_summary,
            "implementation_phases": {
                "phase_1_immediate": {
                    "timeline": "0-30 days",
                    "description": "Critical security gaps requiring immediate attention", 
                    "actions": sorted(phase_1_actions, key=lambda x: self._severity_sort_key(x["severity"])),
                    "total_actions": len(phase_1_actions)
                },
                "phase_2_short_term": {
                    "timeline": "30-90 days",
                    "description": "High-priority improvements and system enhancements",
                    "actions": sorted(phase_2_actions, key=lambda x: self._severity_sort_key(x["severity"])),
                    "total_actions": len(phase_2_actions)
                },
                "phase_3_long_term": {
                    "timeline": "90+ days", 
                    "description": "Strategic improvements and advanced security measures",
                    "actions": sorted(phase_3_actions, key=lambda x: self._severity_sort_key(x["severity"])),
                    "total_actions": len(phase_3_actions)
                }
            },
            "system_specific_recommendations": system_actions,
            "success_metrics": self._generate_success_metrics(),
            "risk_reduction_projection": self._calculate_risk_reduction(csf_gaps, overall_risk_score)
        }
        
        return action_plan
    
    def _calculate_urgency(self, severity: RiskLevel, overall_risk_score: int) -> str:
        """Calculate action urgency based on severity and overall risk."""
        if severity == RiskLevel.CRITICAL or overall_risk_score >= 80:
            return "Immediate"
        elif severity == RiskLevel.HIGH or overall_risk_score >= 60:
            return "High"
        elif severity == RiskLevel.MEDIUM or overall_risk_score >= 40:
            return "Medium"
        else:
            return "Low"
    
    def _estimate_cost(self, effort_level: str) -> Dict:
        """Estimate cost based on effort level."""
        return self.cost_estimates.get(effort_level, self.cost_estimates["Medium"])
    
    def _generate_success_criteria(self, category: str) -> List[str]:
        """Generate success criteria for CSF category."""
        criteria_map = {
            "GV.SC-01": [
                "Supply chain risk management policy approved and published",
                "Supplier security assessment program operational", 
                "100% of critical suppliers assessed within 90 days"
            ],
            "PR.DS-06": [
                "Cryptographic integrity verification implemented for all training data",
                "Automated data validation processes operational",
                "Zero data integrity incidents in 30-day period"
            ],
            "DE.CM-07": [
                "Model drift detection system deployed and operational",
                "Performance monitoring dashboards accessible to operations team",
                "Automated alerting functional with <5 minute response time"
            ]
        }
        
        return criteria_map.get(category, [
            "Implementation completed and tested",
            "Documentation updated and approved", 
            "Team trained on new procedures"
        ])
    
    def _assign_responsible_team(self, category: str) -> str:
        """Assign responsible team based on CSF category."""
        team_map = {
            "GV": "Governance, Risk & Compliance (GRC)",
            "ID": "Security Operations Center (SOC)",
            "PR": "Information Security Team",
            "DE": "Security Operations Center (SOC)", 
            "RS": "Incident Response Team",
            "RC": "Business Continuity Team"
        }
        
        function = category.split('.')[0]
        return team_map.get(function, "Information Security Team")
    
    def _identify_dependencies(self, category: str, all_gaps: List[CSFGap]) -> List[str]:
        """Identify dependencies between remediation actions."""
        dependencies = []
        
        # Common dependency patterns
        if category == "DE.CM-07":  # Monitoring depends on data lineage
            if any(gap.category == "ID.AM-03" for gap in all_gaps):
                dependencies.append("ID.AM-03: Data lineage documentation must be completed first")
        
        if category.startswith("PR."):  # Protection often depends on identification
            id_gaps = [gap.category for gap in all_gaps if gap.category.startswith("ID.")]
            if id_gaps:
                dependencies.append(f"Complete identification phase first: {', '.join(id_gaps[:2])}")
        
        return dependencies
    
    def _generate_system_specific_actions(self, system_config: Dict, risk_score: int) -> List[Dict]:
        """Generate actions specific to the system configuration."""
        actions = []
        
        # Model-specific recommendations
        model_type = system_config.get("model_type", "").lower()
        if "neural" in model_type or "deep" in model_type:
            actions.append({
                "category": "Model Explainability",
                "recommendation": "Implement explainable AI techniques (SHAP, LIME) for black-box model transparency",
                "timeline": "45-60 days",
                "effort": "Medium"
            })
        
        # Deployment-specific recommendations
        deployment = system_config.get("deployment_env", "").lower()
        if "cloud" in deployment:
            actions.append({
                "category": "Cloud Security",
                "recommendation": "Implement cloud-specific security controls and shared responsibility model documentation",
                "timeline": "30-45 days", 
                "effort": "Medium"
            })
        
        # Data source-specific recommendations
        data_sources = system_config.get("data_sources", [])
        external_sources = [src for src in data_sources if any(term in src.lower() for term in ["api", "external", "social", "web"])]
        if external_sources:
            actions.append({
                "category": "External Data Security",
                "recommendation": f"Implement enhanced validation and monitoring for external data sources: {', '.join(external_sources[:3])}",
                "timeline": "21-30 days",
                "effort": "Medium"
            })
        
        return actions
    
    def _generate_success_metrics(self) -> Dict:
        """Generate success metrics for the action plan."""
        return {
            "risk_score_target": "Reduce overall risk score to <40 (Medium risk)",
            "compliance_target": "Achieve 95% CSF compliance within 6 months",
            "operational_metrics": [
                "Zero critical security incidents related to AI systems",
                "100% of remediation actions completed within timeline", 
                "All team members trained on new security procedures"
            ],
            "business_metrics": [
                "Maintain AI system availability >99.5%",
                "Zero regulatory compliance violations",
                "Audit readiness achieved within 90 days"
            ]
        }
    
    def _calculate_risk_reduction(self, csf_gaps: List[CSFGap], current_score: int) -> Dict:
        """Calculate projected risk reduction from implementing action plan."""
        # Estimate risk reduction based on gap severity
        total_reduction = 0
        
        for gap in csf_gaps:
            if gap.severity == RiskLevel.CRITICAL:
                total_reduction += 20
            elif gap.severity == RiskLevel.HIGH:
                total_reduction += 15
            elif gap.severity == RiskLevel.MEDIUM:
                total_reduction += 10
            else:
                total_reduction += 5
        
        # Cap reduction to reasonable levels
        max_reduction = min(total_reduction, current_score * 0.6)  # Max 60% reduction
        projected_score = max(current_score - max_reduction, 15)  # Minimum score of 15
        
        return {
            "current_risk_score": current_score,
            "projected_risk_score": int(projected_score),
            "estimated_reduction": int(max_reduction),
            "reduction_percentage": f"{int((max_reduction / current_score) * 100)}%",
            "target_risk_level": "Low" if projected_score < 40 else "Medium" if projected_score < 60 else "High"
        }
    
    def _generate_executive_summary(self, total_gaps: int, risk_score: int, total_cost: int) -> str:
        """Generate executive summary for the action plan."""
        risk_level = "Critical" if risk_score >= 80 else "High" if risk_score >= 60 else "Medium"
        
        return f"""
This AI system presents {risk_level.lower()} cybersecurity risk with {total_gaps} NIST CSF compliance gaps identified. 
The remediation plan addresses all critical vulnerabilities through a phased approach over 3-6 months.

Key highlights:
• {total_gaps} compliance gaps across multiple NIST CSF functions
• Estimated investment: ${total_cost:,.0f} - ${total_cost*1.2:,.0f}
• Projected risk reduction: {risk_score} → {max(risk_score-30, 15)} points
• Timeline: 3-6 months for complete implementation
• ROI: Prevention of potential multi-million dollar AI-related incidents

Immediate action required for {len([g for g in [] if getattr(g, 'severity', None) == RiskLevel.CRITICAL])} critical security gaps.
        """.strip()
    
    def _severity_sort_key(self, severity) -> int:
        """Sort key for severity levels."""
        severity_order = {
            RiskLevel.CRITICAL: 0,
            "Critical": 0,
            RiskLevel.HIGH: 1, 
            "High": 1,
            RiskLevel.MEDIUM: 2,
            "Medium": 2,
            RiskLevel.LOW: 3,
            "Low": 3
        }
        return severity_order.get(severity, 4)