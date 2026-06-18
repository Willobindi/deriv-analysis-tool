import pytest
from deriv_analyzer.digit_analyzer import DigitAnalyzer

class TestDigitAnalyzer:
    
    @pytest.fixture
    def analyzer(self):
        return DigitAnalyzer()
    
    def test_find_matches(self, analyzer):
        digits = [1, 1, 2, 3, 3, 3]
        matches = analyzer.find_matches(digits)
        assert len(matches) == 3  # (1,1), (3,3), (3,3)
    
    def test_find_differs(self, analyzer):
        digits = [1, 2, 3, 4, 5]
        differs = analyzer.find_differs(digits)
        assert len(differs) == 4  # All consecutive pairs
    
    def test_classify_odd_even(self, analyzer):
        digits = [1, 2, 3, 4, 5, 6]
        result = analyzer.classify_odd_even(digits)
        assert len(result['odd']) == 3
        assert len(result['even']) == 3
    
    def test_analyze(self, analyzer):
        digits = [1, 1, 2, 3, 3]
        result = analyzer.analyze(digits)
        assert 'matches' in result
        assert 'differs' in result
        assert 'odd_even' in result
        assert 'statistics' in result
