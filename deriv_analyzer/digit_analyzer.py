import numpy as np
from collections import Counter

class DigitAnalyzer:
    """Analyzes digit patterns, matches, differs, and parity"""
    
    def __init__(self):
        pass
    
    def analyze(self, digits):
        """Comprehensive digit analysis"""
        return {
            'matches': self.find_matches(digits),
            'differs': self.find_differs(digits),
            'odd_even': self.classify_odd_even(digits),
            'statistics': self.get_statistics(digits)
        }
    
    def find_matches(self, digits):
        """Find matching consecutive digits"""
        matches = []
        for i in range(len(digits) - 1):
            if digits[i] == digits[i + 1]:
                matches.append({
                    'index': i,
                    'value': digits[i],
                    'positions': [i, i + 1]
                })
        return matches
    
    def find_differs(self, digits):
        """Find differing consecutive digits"""
        differs = []
        for i in range(len(digits) - 1):
            if digits[i] != digits[i + 1]:
                differs.append({
                    'index': i,
                    'value1': digits[i],
                    'value2': digits[i + 1],
                    'positions': [i, i + 1],
                    'difference': abs(digits[i] - digits[i + 1])
                })
        return differs
    
    def classify_odd_even(self, digits):
        """Classify digits as odd or even"""
        odd = []
        even = []
        for i, digit in enumerate(digits):
            if digit % 2 == 0:
                even.append({'index': i, 'value': digit})
            else:
                odd.append({'index': i, 'value': digit})
        return {'odd': odd, 'even': even}
    
    def get_statistics(self, digits):
        """Get statistical information about digits"""
        return {
            'count': len(digits),
            'mean': float(np.mean(digits)),
            'std': float(np.std(digits)),
            'min': float(np.min(digits)),
            'max': float(np.max(digits)),
            'frequency': dict(Counter(digits))
        }
