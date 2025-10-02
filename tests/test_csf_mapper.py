"""
Tests for CSF mapping functionality.
"""
import pytest
from src.csf_mapper import CSFMapper
from src.models import RiskLevel


def test_csf_mapper_initialization():
    """Test CSFMapper initializes correctly."""
    mapper = CSFMapper()
    assert mapper.csf_data is not None
    assert mapper.ai_risks is not None
    assert "functions" in mapper.csf_data
    assert "ai_risk_categories" in mapper.ai_risks


def test_map_valid_risk_type():
    """Test mapping valid AI risk type to CSF categories."""
    mapper = CSFMapper()
    result = mapper.map_risk_to_csf("training_data_poisoning")
    
    assert result is not None
    assert "categories" in result
    assert "description" in result
    assert "supply_chain_impact" in result
    assert len(result["categories"]) > 0


def test_map_invalid_risk_type():
    """Test mapping invalid risk type returns None."""
    mapper = CSFMapper()
    result = mapper.map_risk_to_csf("invalid_risk_type")
    assert result is None


def test_identify_gaps_basic():
    """Test basic gap identification."""
    mapper = CSFMapper()
    
    system_config = {
        "system_name": "Test System",
        "data_lineage_documented": False,
        "drift_monitoring_enabled": False,
        "third_party_libs": ["scikit-learn"]
    }
    
    risk_assessment = {"overall_risk_score": 60}
    
    gaps = mapper.identify_gaps(system_config, risk_assessment)
    
    assert len(gaps) > 0
    gap_categories = [gap.category for gap in gaps]
    assert "ID.AM-03" in gap_categories  # Data lineage gap
    assert "DE.CM-07" in gap_categories  # Monitoring gap


def test_identify_gaps_high_risk_system():
    """Test gap identification for high-risk system."""
    mapper = CSFMapper()
    
    system_config = {
        "system_name": "High Risk System",
        "data_lineage_documented": False,
        "drift_monitoring_enabled": False,
        "data_integrity_checks": False
    }
    
    risk_assessment = {"overall_risk_score": 85}
    
    gaps = mapper.identify_gaps(system_config, risk_assessment)
    
    # Should have critical gaps for high-risk system
    critical_gaps = [gap for gap in gaps if gap.severity == RiskLevel.CRITICAL]
    assert len(critical_gaps) > 0


def test_assess_category_severity():
    """Test CSF category severity assessment."""
    mapper = CSFMapper()
    
    # Test critical category with high base score
    severity = mapper._assess_category_severity("model_backdoors", "GV.SC-01")
    assert severity in [RiskLevel.CRITICAL, RiskLevel.HIGH]
    
    # Test low-risk scenario
    severity = mapper._assess_category_severity("data_lineage_gaps", "PR.DS-11")
    assert severity in [RiskLevel.LOW, RiskLevel.MEDIUM]


def test_get_csf_category_description():
    """Test getting CSF category descriptions."""
    mapper = CSFMapper()
    
    # Test function category
    description = mapper.get_csf_category_description("GV.SC")
    assert description is not None
    assert "Supply Chain" in description
    
    # Test subcategory
    description = mapper.get_csf_category_description("GV.SC-01")
    assert description is not None
    assert len(description) > 10
    
    # Test invalid category
    description = mapper.get_csf_category_description("INVALID.XX-99")
    assert description is None


def test_all_ai_risks_have_csf_mappings():
    """Test that all AI risk categories have valid CSF mappings."""
    mapper = CSFMapper()
    
    for risk_type in mapper.ai_risks["ai_risk_categories"]:
        risk_data = mapper.ai_risks["ai_risk_categories"][risk_type]
        
        # Check required fields exist
        assert "csf_mappings" in risk_data
        assert "description" in risk_data
        assert "base_risk_score" in risk_data
        
        # Check CSF mappings are valid
        assert len(risk_data["csf_mappings"]) > 0
        for csf_category in risk_data["csf_mappings"]:
            assert isinstance(csf_category, str)
            assert "." in csf_category  # Should be format like "GV.SC-01"


def test_csf_data_structure():
    """Test CSF data has correct structure."""
    mapper = CSFMapper()
    
    assert "functions" in mapper.csf_data
    functions = mapper.csf_data["functions"]
    
    # Check required functions exist
    required_functions = ["GOVERN", "IDENTIFY", "PROTECT", "DETECT", "RESPOND", "RECOVER"]
    for function in required_functions:
        assert function in functions
        
        # Check function structure
        function_data = functions[function]
        assert "description" in function_data
        assert "categories" in function_data
        
        # Check at least one category exists
        assert len(function_data["categories"]) > 0