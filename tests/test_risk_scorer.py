"""
Tests for AI risk scoring functionality.
"""
import pytest
from src.risk_scorer import RiskScorer


def test_risk_scorer_initialization():
    """Test RiskScorer initializes correctly."""
    scorer = RiskScorer()
    assert scorer.ai_risks is not None
    assert "ai_risk_categories" in scorer.ai_risks


def test_assess_system_basic():
    """Test basic system risk assessment."""
    scorer = RiskScorer()
    
    system_config = {
        "system_name": "Test System",
        "model_type": "Random Forest",
        "data_lineage_documented": True,
        "drift_monitoring_enabled": True,
        "third_party_libs": ["scikit-learn"]
    }
    
    result = scorer.assess_system(system_config)
    
    assert "overall_risk_score" in result
    assert 0 <= result["overall_risk_score"] <= 100
    assert "risk_factors" in result
    assert "economic_multiplier" in result
    assert "assessment_timestamp" in result


def test_assess_high_risk_system():
    """Test assessment of high-risk system."""
    scorer = RiskScorer()
    
    high_risk_config = {
        "system_name": "High Risk System",
        "model_type": "Deep Neural Network",
        "data_lineage_documented": False,
        "drift_monitoring_enabled": False,
        "data_encryption": False,
        "access_controls": False,
        "third_party_libs": ["tensorflow", "pytorch", "unknown_lib1", "unknown_lib2"]
    }
    
    result = scorer.assess_system(high_risk_config)
    
    # High-risk system should have elevated score
    assert result["overall_risk_score"] > 50
    assert len(result["risk_factors"]) > 3


def test_assess_low_risk_system():
    """Test assessment of well-secured system."""
    scorer = RiskScorer()
    
    low_risk_config = {
        "system_name": "Secure System",
        "model_type": "Linear Regression",
        "data_lineage_documented": True,
        "drift_monitoring_enabled": True,
        "data_encryption": True,
        "access_controls": True,
        "third_party_libs": []
    }
    
    result = scorer.assess_system(low_risk_config)
    
    # Well-secured system should have lower score
    assert result["overall_risk_score"] < 40


def test_assess_third_party_risk():
    """Test third-party library risk assessment."""
    scorer = RiskScorer()
    
    # No libraries
    risk = scorer._assess_third_party_risk([])
    assert risk == 0
    
    # Few safe libraries
    risk = scorer._assess_third_party_risk(["requests", "json"])
    assert 0 < risk < 10
    
    # Many ML libraries
    risk = scorer._assess_third_party_risk([
        "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
        "keras", "xgboost", "lightgbm", "unknown1", "unknown2", "unknown3"
    ])
    assert risk > 10


def test_economic_stress_multiplier():
    """Test economic stress multiplier calculation."""
    scorer = RiskScorer()
    
    multiplier = scorer._get_economic_stress_multiplier()
    
    # Should be reasonable multiplier
    assert 1.0 <= multiplier <= 3.0
    
    # Should be cached on second call
    multiplier2 = scorer._get_economic_stress_multiplier()
    assert multiplier == multiplier2


def test_get_risk_breakdown():
    """Test detailed risk breakdown analysis."""
    scorer = RiskScorer()
    
    system_config = {
        "system_name": "Test System",
        "model_type": "Neural Network",
        "data_lineage_documented": False,
        "drift_monitoring_enabled": True,
        "third_party_libs": ["tensorflow", "pandas"]
    }
    
    breakdown = scorer.get_risk_breakdown(system_config)
    
    assert "overall_score" in breakdown
    assert "risk_factors" in breakdown
    assert "factor_scores" in breakdown
    assert "economic_context" in breakdown
    
    # Check factor scores structure
    factor_scores = breakdown["factor_scores"]
    expected_factors = [
        "data_lineage", "model_explainability", "drift_monitoring",
        "third_party_risk", "data_security"
    ]
    for factor in expected_factors:
        assert factor in factor_scores
        assert isinstance(factor_scores[factor], int)


def test_is_black_box_model():
    """Test black-box model detection."""
    scorer = RiskScorer()
    
    # Black-box models
    assert scorer._is_black_box_model("Deep Neural Network")
    assert scorer._is_black_box_model("neural network")
    assert scorer._is_black_box_model("Random Forest Ensemble")
    
    # Transparent models
    assert not scorer._is_black_box_model("Linear Regression")
    assert not scorer._is_black_box_model("Decision Tree")
    assert not scorer._is_black_box_model("Logistic Regression")


def test_assess_data_security():
    """Test data security risk assessment."""
    scorer = RiskScorer()
    
    # Secure configuration
    secure_config = {
        "data_encryption": True,
        "access_controls": True
    }
    risk = scorer._assess_data_security(secure_config)
    assert risk == 0
    
    # Insecure configuration
    insecure_config = {
        "data_encryption": False,
        "access_controls": False
    }
    risk = scorer._assess_data_security(insecure_config)
    assert risk == 15
    
    # Partially secure
    partial_config = {
        "data_encryption": True,
        "access_controls": False
    }
    risk = scorer._assess_data_security(partial_config)
    assert risk == 5


def test_economic_description():
    """Test economic stress level descriptions."""
    scorer = RiskScorer()
    
    descriptions = [
        scorer._get_economic_description(1.0),
        scorer._get_economic_description(1.3),
        scorer._get_economic_description(1.7),
        scorer._get_economic_description(2.5)
    ]
    
    # All descriptions should be non-empty strings
    for desc in descriptions:
        assert isinstance(desc, str)
        assert len(desc) > 0
    
    # Should have different descriptions for different levels
    assert len(set(descriptions)) > 2