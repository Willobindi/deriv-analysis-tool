from .digit_analyzer import DigitAnalyzer
from .volatility import VolatilityAnalyzer
from .predictor import DerivPredictor

class DerivAnalyzer:
    """Main interface for derivative analysis"""
    
    def __init__(self):
        self.digit_analyzer = DigitAnalyzer()
        self.volatility_analyzer = VolatilityAnalyzer()
        self.predictor = DerivPredictor()
    
    def analyze_digits(self, digits):
        """Analyze digit patterns"""
        return self.digit_analyzer.analyze(digits)
    
    def analyze_volatility(self, data, window_size=10):
        """Analyze volatility across data"""
        return self.volatility_analyzer.calculate(data, window_size)
    
    def predict(self, digits, volatility_levels):
        """Predict matches/differs and odd/even for all volatilities"""
        return self.predictor.predict(digits, volatility_levels)

__all__ = ['DerivAnalyzer', 'DigitAnalyzer', 'VolatilityAnalyzer', 'DerivPredictor']
