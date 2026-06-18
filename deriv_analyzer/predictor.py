import numpy as np
from .digit_analyzer import DigitAnalyzer
from .volatility import VolatilityAnalyzer

class DerivPredictor:
    """Predicts matches/differs and odd/even across volatility levels"""
    
    def __init__(self):
        self.digit_analyzer = DigitAnalyzer()
        self.volatility_analyzer = VolatilityAnalyzer()
    
    def predict(self, digits, volatility_levels=None):
        """Predict outcomes across multiple volatility levels"""
        if volatility_levels is None:
            volatility_levels = [1.0, 2.0, 3.0]
        
        predictions = []
        
        for vol_level in volatility_levels:
            pred = self.predict_for_volatility(digits, vol_level)
            predictions.append(pred)
        
        return {
            'predictions': predictions,
            'summary': self.summarize_predictions(predictions)
        }
    
    def predict_for_volatility(self, digits, volatility_level):
        """Predict for a specific volatility level"""
        digits = np.array(digits)
        
        # Analyze current patterns
        analysis = self.digit_analyzer.analyze(digits)
        
        # Calculate probabilities
        match_prob = self.calculate_match_probability(analysis)
        differ_prob = 1.0 - match_prob
        odd_prob = self.calculate_odd_probability(analysis)
        even_prob = 1.0 - odd_prob
        
        # Apply volatility adjustment
        adjusted_probs = self.adjust_probabilities({
            'match_prob': match_prob,
            'differ_prob': differ_prob,
            'odd_prob': odd_prob,
            'even_prob': even_prob
        }, volatility_level)
        
        return {
            'volatility_level': volatility_level,
            'match_probability': adjusted_probs['match_prob'],
            'differ_probability': adjusted_probs['differ_prob'],
            'odd_probability': adjusted_probs['odd_prob'],
            'even_probability': adjusted_probs['even_prob'],
            'predicted_outcome': self.determine_outcome(adjusted_probs),
            'confidence': self.calculate_confidence(adjusted_probs)
        }
    
    def calculate_match_probability(self, analysis):
        """Calculate probability of matches"""
        total_pairs = len(analysis['matches']) + len(analysis['differs'])
        if total_pairs == 0:
            return 0.5
        return len(analysis['matches']) / total_pairs
    
    def calculate_odd_probability(self, analysis):
        """Calculate probability of odd digits"""
        total = len(analysis['odd_even']['odd']) + len(analysis['odd_even']['even'])
        if total == 0:
            return 0.5
        return len(analysis['odd_even']['odd']) / total
    
    def adjust_probabilities(self, probs, volatility_level):
        """Adjust probabilities based on volatility"""
        # Higher volatility increases uncertainty (moves toward 0.5)
        adjustment = min(volatility_level / 10.0, 0.3)
        
        adjusted = {}
        for key, prob in probs.items():
            adjusted[key] = prob * (1 - adjustment) + 0.5 * adjustment
        
        return adjusted
    
    def determine_outcome(self, probs):
        """Determine most likely outcome"""
        return {
            'match_vs_differ': 'match' if probs['match_prob'] > 0.5 else 'differ',
            'odd_vs_even': 'odd' if probs['odd_prob'] > 0.5 else 'even'
        }
    
    def calculate_confidence(self, probs):
        """Calculate confidence in predictions"""
        match_diff_confidence = abs(probs['match_prob'] - 0.5) * 2
        odd_even_confidence = abs(probs['odd_prob'] - 0.5) * 2
        return {
            'match_differ': float(match_diff_confidence),
            'odd_even': float(odd_even_confidence),
            'average': float((match_diff_confidence + odd_even_confidence) / 2)
        }
    
    def summarize_predictions(self, predictions):
        """Summarize predictions across all volatility levels"""
        match_votes = sum(1 for p in predictions if p['predicted_outcome']['match_vs_differ'] == 'match')
        odd_votes = sum(1 for p in predictions if p['predicted_outcome']['odd_vs_even'] == 'odd')
        
        return {
            'consensus_match_vs_differ': 'match' if match_votes > len(predictions) / 2 else 'differ',
            'consensus_odd_vs_even': 'odd' if odd_votes > len(predictions) / 2 else 'even',
            'match_consensus_strength': match_votes / len(predictions),
            'odd_consensus_strength': odd_votes / len(predictions)
        }
