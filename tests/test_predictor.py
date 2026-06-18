import pytest
from deriv_analyzer.predictor import DerivPredictor

class TestDerivPredictor:
    
    @pytest.fixture
    def predictor(self):
        return DerivPredictor()
    
    def test_predict(self, predictor):
        digits = [1, 1, 2, 3, 3, 4, 5, 5]
        result = predictor.predict(digits, volatility_levels=[1.0, 2.0, 3.0])
        assert 'predictions' in result
        assert 'summary' in result
        assert len(result['predictions']) == 3
    
    def test_predict_for_volatility(self, predictor):
        digits = [1, 2, 3, 4, 5]
        result = predictor.predict_for_volatility(digits, 2.0)
        assert 'match_probability' in result
        assert 'differ_probability' in result
        assert 'odd_probability' in result
        assert 'even_probability' in result
    
    def test_probabilities_sum_to_one(self, predictor):
        digits = [1, 2, 3, 4, 5]
        result = predictor.predict_for_volatility(digits, 1.0)
        match_sum = result['match_probability'] + result['differ_probability']
        odd_sum = result['odd_probability'] + result['even_probability']
        assert abs(match_sum - 1.0) < 0.01
        assert abs(odd_sum - 1.0) < 0.01
