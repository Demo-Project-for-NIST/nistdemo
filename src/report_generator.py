"""
NIST CSF compliance report generator.

Generates professional PDF and JSON reports for NIST CSF 2.0 compliance assessments.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from io import BytesIO

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, black, red, orange, green
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.platypus.tableofcontents import TableOfContents
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from .models import RiskAssessmentResponse, RiskLevel


class ReportGenerator:
    """Generates NIST CSF compliance reports in various formats."""
    
    def __init__(self):
        """Initialize report generator."""
        self.styles = self._setup_styles() if REPORTLAB_AVAILABLE else None
    
    def _setup_styles(self) -> Dict:
        """Setup ReportLab styles for PDF generation."""
        if not REPORTLAB_AVAILABLE:
            return {}
        
        styles = getSampleStyleSheet()
        
        custom_styles = {
            'Title': ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                spaceAfter=30,
                textColor=HexColor('#1f4788')
            ),
            'Heading2': ParagraphStyle(
                'CustomHeading2',
                parent=styles['Heading2'],
                fontSize=14,
                spaceBefore=20,
                spaceAfter=10,
                textColor=HexColor('#2c5aa0')
            ),
            'RiskCritical': ParagraphStyle(
                'RiskCritical',
                parent=styles['Normal'],
                textColor=red,
                fontName='Helvetica-Bold'
            ),
            'RiskHigh': ParagraphStyle(
                'RiskHigh',
                parent=styles['Normal'],
                textColor=orange,
                fontName='Helvetica-Bold'
            ),
            'RiskMedium': ParagraphStyle(
                'RiskMedium',
                parent=styles['Normal'],
                textColor=HexColor('#ff8c00'),
                fontName='Helvetica'
            ),
            'RiskLow': ParagraphStyle(
                'RiskLow',
                parent=styles['Normal'],
                textColor=green,
                fontName='Helvetica'
            )
        }
        
        return {**styles, **custom_styles}
    
    def generate_json_report(
        self, 
        organization_name: str,
        assessment_data: RiskAssessmentResponse,
        additional_context: Optional[Dict] = None
    ) -> Dict:
        """
        Generate JSON format compliance report.
        
        Args:
            organization_name: Name of the organization
            assessment_data: Risk assessment results
            additional_context: Additional context data
            
        Returns:
            Dictionary containing complete report data
        """
        report_data = {
            "report_metadata": {
                "organization": organization_name,
                "report_type": "NIST CSF 2.0 AI Risk Assessment",
                "generated_date": datetime.utcnow().isoformat(),
                "toolkit_version": "0.1.0",
                "standard_version": "NIST CSF 2.0"
            },
            "executive_summary": {
                "system_name": assessment_data.system_name,
                "overall_risk_score": assessment_data.overall_risk_score,
                "risk_level": assessment_data.risk_level,
                "total_gaps_identified": len(assessment_data.csf_compliance_gaps),
                "critical_gaps": len([
                    gap for gap in assessment_data.csf_compliance_gaps 
                    if gap.severity == RiskLevel.CRITICAL
                ]),
                "high_priority_gaps": len([
                    gap for gap in assessment_data.csf_compliance_gaps 
                    if gap.severity == RiskLevel.HIGH
                ]),
                "medium_priority_gaps": len([
                    gap for gap in assessment_data.csf_compliance_gaps 
                    if gap.severity == RiskLevel.MEDIUM
                ]),
                "low_priority_gaps": len([
                    gap for gap in assessment_data.csf_compliance_gaps 
                    if gap.severity == RiskLevel.LOW
                ])
            },
            "compliance_by_function": self._analyze_compliance_by_function(assessment_data.csf_compliance_gaps),
            "detailed_findings": {
                "csf_compliance_gaps": [gap.dict() for gap in assessment_data.csf_compliance_gaps],
                "recommended_actions": assessment_data.recommended_actions
            },
            "remediation_roadmap": self._generate_remediation_roadmap(assessment_data.csf_compliance_gaps),
            "additional_context": additional_context or {}
        }
        
        return report_data
    
    def generate_pdf_report(
        self,
        organization_name: str,
        assessment_data: RiskAssessmentResponse,
        output_path: Optional[str] = None
    ) -> bytes:
        """
        Generate PDF format compliance report.
        
        Args:
            organization_name: Name of the organization
            assessment_data: Risk assessment results
            output_path: Optional file path to save PDF
            
        Returns:
            PDF content as bytes
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab is required for PDF generation. Install with: pip install reportlab")
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        
        # Build document content
        story = []
        
        # Title page
        story.extend(self._build_title_page(organization_name, assessment_data))
        
        # Executive summary
        story.extend(self._build_executive_summary(assessment_data))
        
        # Compliance analysis
        story.extend(self._build_compliance_analysis(assessment_data))
        
        # Detailed findings
        story.extend(self._build_detailed_findings(assessment_data))
        
        # Remediation roadmap
        story.extend(self._build_remediation_roadmap(assessment_data))
        
        # Build PDF
        doc.build(story)
        
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # Save to file if path provided
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(pdf_content)
        
        return pdf_content
    
    def _analyze_compliance_by_function(self, gaps: List) -> Dict:
        """Analyze compliance gaps by NIST CSF function."""
        function_analysis = {
            'GOVERN': {'gaps': 0, 'categories': set()},
            'IDENTIFY': {'gaps': 0, 'categories': set()},
            'PROTECT': {'gaps': 0, 'categories': set()},
            'DETECT': {'gaps': 0, 'categories': set()},
            'RESPOND': {'gaps': 0, 'categories': set()},
            'RECOVER': {'gaps': 0, 'categories': set()}
        }
        
        function_mapping = {
            'GV': 'GOVERN',
            'ID': 'IDENTIFY',
            'PR': 'PROTECT',
            'DE': 'DETECT',
            'RS': 'RESPOND',
            'RC': 'RECOVER'
        }
        
        for gap in gaps:
            function_code = gap.category.split('.')[0]
            function_name = function_mapping.get(function_code, 'UNKNOWN')
            
            if function_name in function_analysis:
                function_analysis[function_name]['gaps'] += 1
                function_analysis[function_name]['categories'].add(gap.category)
        
        # Convert sets to lists for JSON serialization
        for function in function_analysis:
            function_analysis[function]['categories'] = list(function_analysis[function]['categories'])
        
        return function_analysis
    
    def _generate_remediation_roadmap(self, gaps: List) -> Dict:
        """Generate prioritized remediation roadmap."""
        roadmap = {
            "phase_1_critical": {
                "timeline": "0-30 days",
                "priority": "Critical",
                "actions": []
            },
            "phase_2_high": {
                "timeline": "30-90 days", 
                "priority": "High",
                "actions": []
            },
            "phase_3_medium": {
                "timeline": "90-180 days",
                "priority": "Medium",
                "actions": []
            },
            "phase_4_low": {
                "timeline": "180+ days",
                "priority": "Low", 
                "actions": []
            }
        }
        
        for gap in gaps:
            action = f"{gap.category}: {gap.description}"
            
            if gap.severity == RiskLevel.CRITICAL:
                roadmap["phase_1_critical"]["actions"].append(action)
            elif gap.severity == RiskLevel.HIGH:
                roadmap["phase_2_high"]["actions"].append(action)
            elif gap.severity == RiskLevel.MEDIUM:
                roadmap["phase_3_medium"]["actions"].append(action)
            else:
                roadmap["phase_4_low"]["actions"].append(action)
        
        return roadmap
    
    def _build_title_page(self, organization_name: str, assessment_data: RiskAssessmentResponse) -> List:
        """Build PDF title page."""
        story = []
        
        title = Paragraph(
            "NIST CSF 2.0 AI Supply Chain Risk Assessment Report",
            self.styles['Title']
        )
        story.append(title)
        story.append(Spacer(1, 0.5*inch))
        
        org_info = Paragraph(
            f"<b>Organization:</b> {organization_name}<br/>"
            f"<b>System Assessed:</b> {assessment_data.system_name}<br/>"
            f"<b>Assessment Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>"
            f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        )
        story.append(org_info)
        story.append(Spacer(1, 1*inch))
        
        return story
    
    def _build_executive_summary(self, assessment_data: RiskAssessmentResponse) -> List:
        """Build executive summary section."""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['Heading2']))
        
        risk_color_style = {
            RiskLevel.CRITICAL: 'RiskCritical',
            RiskLevel.HIGH: 'RiskHigh', 
            RiskLevel.MEDIUM: 'RiskMedium',
            RiskLevel.LOW: 'RiskLow'
        }.get(assessment_data.risk_level, 'Normal')
        
        summary_text = f"""
        This assessment evaluated the cybersecurity risk posture of {assessment_data.system_name} 
        against NIST Cybersecurity Framework 2.0 requirements for AI systems in supply chains.
        <br/><br/>
        <b>Overall Risk Score:</b> {assessment_data.overall_risk_score}/100<br/>
        <b>Risk Level:</b> <font color="{self.styles[risk_color_style].textColor}">{assessment_data.risk_level}</font><br/>
        <b>Total Compliance Gaps:</b> {len(assessment_data.csf_compliance_gaps)}<br/>
        """
        
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        return story
    
    def _build_compliance_analysis(self, assessment_data: RiskAssessmentResponse) -> List:
        """Build compliance analysis section."""
        story = []
        
        story.append(Paragraph("Compliance Analysis by CSF Function", self.styles['Heading2']))
        
        function_analysis = self._analyze_compliance_by_function(assessment_data.csf_compliance_gaps)
        
        # Create table data
        table_data = [['CSF Function', 'Gaps Found', 'Status']]
        
        for function, data in function_analysis.items():
            gap_count = data['gaps']
            if gap_count == 0:
                status = "Compliant"
                status_color = green
            elif gap_count <= 2:
                status = "Minor Issues"
                status_color = orange
            else:
                status = "Needs Attention"
                status_color = red
            
            table_data.append([function, str(gap_count), status])
        
        table = Table(table_data, colWidths=[2*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        return story
    
    def _build_detailed_findings(self, assessment_data: RiskAssessmentResponse) -> List:
        """Build detailed findings section."""
        story = []
        
        story.append(Paragraph("Detailed Compliance Gaps", self.styles['Heading2']))
        
        if not assessment_data.csf_compliance_gaps:
            story.append(Paragraph("No compliance gaps identified.", self.styles['Normal']))
        else:
            for i, gap in enumerate(assessment_data.csf_compliance_gaps, 1):
                gap_text = f"""
                <b>{i}. {gap.category}</b> - {gap.severity}<br/>
                {gap.description}
                """
                
                style_name = {
                    RiskLevel.CRITICAL: 'RiskCritical',
                    RiskLevel.HIGH: 'RiskHigh',
                    RiskLevel.MEDIUM: 'RiskMedium', 
                    RiskLevel.LOW: 'RiskLow'
                }.get(gap.severity, 'Normal')
                
                story.append(Paragraph(gap_text, self.styles[style_name]))
                story.append(Spacer(1, 0.1*inch))
        
        return story
    
    def _build_remediation_roadmap(self, assessment_data: RiskAssessmentResponse) -> List:
        """Build remediation roadmap section."""
        story = []
        
        story.append(Paragraph("Recommended Actions", self.styles['Heading2']))
        
        if assessment_data.recommended_actions:
            for i, action in enumerate(assessment_data.recommended_actions, 1):
                story.append(Paragraph(f"{i}. {action}", self.styles['Normal']))
        else:
            story.append(Paragraph("No specific actions recommended at this time.", self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        return story