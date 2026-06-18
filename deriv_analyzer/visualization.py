import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealtimeVisualizer:
    """Real-time visualization of predictions and market data"""
    
    def __init__(self, max_points: int = 100):
        self.max_points = max_points
        self.data = {}
        self.fig = None
        self.axes = None
    
    def setup_figure(self, num_symbols: int = 1):
        """Setup matplotlib figure with subplots"""
        self.fig, self.axes = plt.subplots(
            num_symbols, 3,
            figsize=(15, 5 * num_symbols)
        )
        
        if num_symbols == 1:
            self.axes = [self.axes]
        
        plt.tight_layout()
    
    def update_price_chart(self, ax, symbol: str, prices: List[float]):
        """Update price chart"""
        ax.clear()
        ax.plot(prices, label='Price', color='blue', linewidth=2)
        ax.set_title(f'{symbol} - Price History')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def update_prediction_chart(self, ax, predictions: Dict):
        """Update prediction probabilities chart"""
        ax.clear()
        
        volatility_levels = []
        match_probs = []
        odd_probs = []
        
        for pred in predictions['predictions']:
            volatility_levels.append(pred['volatility_level'])
            match_probs.append(pred['match_probability'])
            odd_probs.append(pred['odd_probability'])
        
        ax.plot(volatility_levels, match_probs, 'o-', label='Match', linewidth=2)
        ax.plot(volatility_levels, odd_probs, 's-', label='Odd', linewidth=2)
        ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='50/50')
        ax.set_title('Predictions Across Volatility Levels')
        ax.set_xlabel('Volatility Level')
        ax.set_ylabel('Probability')
        ax.set_ylim([0, 1])
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def update_confidence_chart(self, ax, predictions: Dict):
        """Update confidence scores chart"""
        ax.clear()
        
        volatility_levels = []
        confidences = []
        
        for pred in predictions['predictions']:
            volatility_levels.append(pred['volatility_level'])
            confidences.append(pred['confidence']['average'])
        
        colors = ['green' if c > 0.7 else 'orange' if c > 0.5 else 'red' for c in confidences]
        ax.bar(range(len(volatility_levels)), confidences, color=colors)
        ax.set_title('Prediction Confidence')
        ax.set_xlabel('Volatility Level')
        ax.set_ylabel('Confidence')
        ax.set_xticklabels([f"{v:.1f}" for v in volatility_levels])
        ax.set_ylim([0, 1])
        ax.grid(True, alpha=0.3, axis='y')
    
    def create_symbol_dashboard(self, symbol: str, prediction: Dict):
        """Create a dashboard for a single symbol"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'{symbol} - Real-Time Analysis Dashboard', fontsize=16)
        
        # Price history
        prices = [p['price'] for p in prediction.get('price_history', [])]
        if prices:
            axes[0, 0].plot(prices, color='blue', linewidth=2)
            axes[0, 0].set_title('Price History')
            axes[0, 0].set_ylabel('Price')
            axes[0, 0].grid(True, alpha=0.3)
        
        # Digit analysis
        digits = prediction.get('digits', [])
        if digits:
            axes[0, 1].bar(range(len(digits)), digits, color='skyblue')
            axes[0, 1].set_title('Digit Sequence')
            axes[0, 1].set_ylabel('Digit Value')
            axes[0, 1].set_ylim([0, 10])
            axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Predictions
        predictions = prediction.get('predictions', {})
        if predictions.get('predictions'):
            volatility_levels = []
            match_probs = []
            odd_probs = []
            
            for pred in predictions['predictions']:
                volatility_levels.append(pred['volatility_level'])
                match_probs.append(pred['match_probability'])
                odd_probs.append(pred['odd_probability'])
            
            axes[1, 0].plot(volatility_levels, match_probs, 'o-', label='Match', linewidth=2)
            axes[1, 0].plot(volatility_levels, odd_probs, 's-', label='Odd', linewidth=2)
            axes[1, 0].axhline(y=0.5, color='r', linestyle='--', alpha=0.5)
            axes[1, 0].set_title('Match vs Odd Predictions')
            axes[1, 0].set_xlabel('Volatility')
            axes[1, 0].set_ylabel('Probability')
            axes[1, 0].set_ylim([0, 1])
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Confidence
        if predictions.get('predictions'):
            confidences = [p['confidence']['average'] for p in predictions['predictions']]
            colors = ['green' if c > 0.7 else 'orange' if c > 0.5 else 'red' for c in confidences]
            axes[1, 1].bar(range(len(confidences)), confidences, color=colors)
            axes[1, 1].set_title('Prediction Confidence')
            axes[1, 1].set_ylabel('Confidence')
            axes[1, 1].set_ylim([0, 1])
            axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def save_dashboard(self, symbol: str, prediction: Dict, filepath: str):
        """Save dashboard to file"""
        fig = self.create_symbol_dashboard(symbol, prediction)
        fig.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close(fig)
        logger.info(f"Dashboard saved to {filepath}")
    
    def show_dashboard(self, symbol: str, prediction: Dict):
        """Display dashboard"""
        fig = self.create_symbol_dashboard(symbol, prediction)
        plt.show()


class AnalysisReporter:
    """Generate detailed analysis reports"""
    
    @staticmethod
    def generate_text_report(symbol: str, prediction: Dict) -> str:
        """Generate a text report of predictions"""
        report = f"""
{'='*60}
REAL-TIME DERIVATIVE ANALYSIS REPORT
{'='*60}

Symbol: {symbol}
Timestamp: {prediction.get('timestamp', 'N/A')}
Current Price: {prediction.get('price', 'N/A')}

{'-'*60}
DIGIT ANALYSIS
{'-'*60}
"""
        
        analysis = prediction.get('analysis', {})
        if analysis:
            report += f"Matches Found: {len(analysis.get('matches', []))}"
            report += f"\nDiffers Found: {len(analysis.get('differs', []))}"
            
            odd_even = analysis.get('odd_even', {})
            report += f"\nOdd Digits: {len(odd_even.get('odd', []))}"
            report += f"\nEven Digits: {len(odd_even.get('even', []))}"
            
            stats = analysis.get('statistics', {})
            report += f"\n\nStatistics:"
            report += f"\n  Mean: {stats.get('mean', 'N/A'):.4f}"
            report += f"\n  Std Dev: {stats.get('std', 'N/A'):.4f}"
            report += f"\n  Min: {stats.get('min', 'N/A')}"
            report += f"\n  Max: {stats.get('max', 'N/A')}"
        
        report += f"\n\n{'-'*60}\nVOLATILITY ANALYSIS\n{'-'*60}\n"
        
        volatility = prediction.get('volatility', {})
        if volatility:
            report += f"Mean Volatility: {volatility.get('mean_volatility', 'N/A'):.4f}"
            report += f"\nMax Volatility: {volatility.get('max_volatility', 'N/A'):.4f}"
            report += f"\nMin Volatility: {volatility.get('min_volatility', 'N/A'):.4f}"
        
        report += f"\n\n{'-'*60}\nPREDICTIONS\n{'-'*60}\n"
        
        predictions = prediction.get('predictions', {})
        if predictions and predictions.get('predictions'):
            report += f"\n{'Vol Level':<12}{'Match %':<12}{'Odd %':<12}{'Confidence':<12}\n"
            report += f"{'-'*48}\n"
            
            for pred in predictions['predictions']:
                vol = pred.get('volatility_level', 0)
                match = pred.get('match_probability', 0) * 100
                odd = pred.get('odd_probability', 0) * 100
                conf = pred.get('confidence', {}).get('average', 0)
                report += f"{vol:<12.1f}{match:<12.1f}{odd:<12.1f}{conf:<12.3f}\n"
            
            report += f"\n{'-'*48}\nCONSENSUS\n{'-'*48}\n"
            summary = predictions.get('summary', {})
            report += f"Match vs Differ: {summary.get('consensus_match_vs_differ', 'N/A').upper()}"
            report += f"\nOdd vs Even: {summary.get('consensus_odd_vs_even', 'N/A').upper()}"
            report += f"\nMatch Consensus Strength: {summary.get('match_consensus_strength', 0)*100:.1f}%"
            report += f"\nOdd Consensus Strength: {summary.get('odd_consensus_strength', 0)*100:.1f}%"
        
        report += f"\n\n{'='*60}\n"
        return report
    
    @staticmethod
    def save_report(symbol: str, prediction: Dict, filepath: str):
        """Save report to file"""
        report = AnalysisReporter.generate_text_report(symbol, prediction)
        with open(filepath, 'w') as f:
            f.write(report)
        logger.info(f"Report saved to {filepath}")
    
    @staticmethod
    def generate_html_report(symbol: str, prediction: Dict) -> str:
        """Generate an HTML report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{symbol} Analysis Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .metric {{
            display: inline-block;
            background-color: #e7f3ff;
            padding: 10px 15px;
            margin: 5px;
            border-radius: 4px;
            border-left: 4px solid #007bff;
        }}
        .metric-label {{
            font-weight: bold;
            color: #333;
        }}
        .metric-value {{
            color: #007bff;
            font-size: 1.2em;
        }}
        .consensus {{
            background-color: #d4edda;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #28a745;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Real-Time Derivative Analysis Report</h1>
        <h2>Market Information</h2>
        <div class="metric">
            <span class="metric-label">Symbol:</span>
            <span class="metric-value">{symbol}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Timestamp:</span>
            <span class="metric-value">{prediction.get('timestamp', 'N/A')}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Price:</span>
            <span class="metric-value">${prediction.get('price', 'N/A'):.4f}</span>
        </div>
        
        <h2>Digit Analysis</h2>
"""
        
        analysis = prediction.get('analysis', {})
        if analysis:
            html += f"""
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Matches</td>
                <td>{len(analysis.get('matches', []))}</td>
            </tr>
            <tr>
                <td>Differs</td>
                <td>{len(analysis.get('differs', []))}</td>
            </tr>
            <tr>
                <td>Odd Digits</td>
                <td>{len(analysis.get('odd_even', {}).get('odd', []))}</td>
            </tr>
            <tr>
                <td>Even Digits</td>
                <td>{len(analysis.get('odd_even', {}).get('even', []))}</td>
            </tr>
        </table>
"""
        
        predictions = prediction.get('predictions', {})
        if predictions and predictions.get('predictions'):
            html += "<h2>Predictions</h2>"
            html += "<table><tr><th>Vol Level</th><th>Match %</th><th>Odd %</th><th>Confidence</th></tr>"
            
            for pred in predictions['predictions']:
                vol = pred.get('volatility_level', 0)
                match = pred.get('match_probability', 0) * 100
                odd = pred.get('odd_probability', 0) * 100
                conf = pred.get('confidence', {}).get('average', 0) * 100
                html += f"<tr><td>{vol:.1f}</td><td>{match:.1f}%</td><td>{odd:.1f}%</td><td>{conf:.1f}%</td></tr>"
            
            html += "</table>"
            
            summary = predictions.get('summary', {})
            html += f"""
        <h2>Consensus</h2>
        <div class="consensus">
            <p><strong>Match vs Differ:</strong> {summary.get('consensus_match_vs_differ', 'N/A').upper()}</p>
            <p><strong>Odd vs Even:</strong> {summary.get('consensus_odd_vs_even', 'N/A').upper()}</p>
            <p><strong>Match Consensus Strength:</strong> {summary.get('match_consensus_strength', 0)*100:.1f}%</p>
            <p><strong>Odd Consensus Strength:</strong> {summary.get('odd_consensus_strength', 0)*100:.1f}%</p>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    @staticmethod
    def save_html_report(symbol: str, prediction: Dict, filepath: str):
        """Save HTML report to file"""
        html = AnalysisReporter.generate_html_report(symbol, prediction)
        with open(filepath, 'w') as f:
            f.write(html)
        logger.info(f"HTML report saved to {filepath}")
