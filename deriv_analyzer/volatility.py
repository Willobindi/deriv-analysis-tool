import numpy as np
from scipy import stats

class VolatilityAnalyzer:
    """Analyzes volatility across data"""
    
    def __init__(self):
        pass
    
    def calculate(self, data, window_size=10):
        """Calculate volatility using rolling window"""
        data = np.array(data)
        volatilities = []
        
        for i in range(len(data) - window_size + 1):
            window = data[i:i + window_size]
            vol = self.calculate_volatility(window)
            volatilities.append({
                'window_start': i,
                'window_end': i + window_size - 1,
                'volatility': vol,
                'values': window.tolist()
            })
        
        return {
            'volatilities': volatilities,
            'mean_volatility': float(np.mean([v['volatility'] for v in volatilities])),
            'max_volatility': float(np.max([v['volatility'] for v in volatilities])),
            'min_volatility': float(np.min([v['volatility'] for v in volatilities]))
        }
    
    def calculate_volatility(self, window):
        """Calculate volatility for a window (standard deviation)"""
        return float(np.std(window))
    
    def classify_volatility_level(self, volatility, thresholds=None):
        """Classify volatility into levels"""
        if thresholds is None:
            thresholds = {'low': 1.0, 'medium': 2.0, 'high': 3.0}
        
        if volatility <= thresholds['low']:
            return 'low'
        elif volatility <= thresholds['medium']:
            return 'medium'
        elif volatility <= thresholds['high']:
            return 'high'
        else:
            return 'extreme'
