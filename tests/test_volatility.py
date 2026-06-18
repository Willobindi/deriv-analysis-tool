import pytest
from deriv_analyzer.volatility import VolatilityAnalyzer

class TestVolatilityAnalyzer:
    
    @pytest.fixture
    def analyzer(self):
        return VolatilityAnalyzer()
    
    def test_calculate_volatility(self, analyzer):
        window = [1, 2, 3, 4, 5]
        vol = analyzer.calculate_volatility(window)
        assert vol > 0
    
    def test_calculate_with_rolling_window(self, analyzer):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = analyzer.calculate(data, window_size=3)
        assert 'volatilities' in result
        assert len(result['volatilities']) == 8
    
    def test_classify_volatility_level(self, analyzer):
        level_low = analyzer.classify_volatility_level(0.5)
        level_high = analyzer.classify_volatility_level(5.0)
        assert level_low == 'low'
        assert level_high == 'extreme'
