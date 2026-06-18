#!/usr/bin/env python3
"""
Real-time analysis with Alpaca market data
"""

import asyncio
from deriv_analyzer import RealtimeDerivAnalyzer
from deriv_analyzer.visualization import AnalysisReporter


async def prediction_callback(symbol: str, prediction: dict):
    """Callback when new prediction is available"""
    print(f"\n{'='*60}")
    print(f"New prediction for {symbol}")
    print(f"{'='*60}")
    
    # Print prediction summary
    predictions = prediction.get('predictions', {})
    if predictions and predictions.get('predictions'):
        summary = predictions.get('summary', {})
        print(f"Current Price: {prediction.get('price', 'N/A')}")
        print(f"Match vs Differ Consensus: {summary.get('consensus_match_vs_differ', 'N/A').upper()}")
        print(f"Odd vs Even Consensus: {summary.get('consensus_odd_vs_even', 'N/A').upper()}")
        print(f"Match Confidence: {summary.get('match_consensus_strength', 0)*100:.1f}%")
        print(f"Odd Confidence: {summary.get('odd_consensus_strength', 0)*100:.1f}%")


async def main():
    # Initialize analyzer
    analyzer = RealtimeDerivAnalyzer()
    
    # Register callback
    analyzer.register_callback(prediction_callback)
    
    # Initialize Alpaca provider
    try:
        # Replace with your actual Alpaca API credentials
        ALPACA_API_KEY = "your_api_key"
        ALPACA_SECRET_KEY = "your_secret_key"
        
        await analyzer.initialize_alpaca(ALPACA_API_KEY, ALPACA_SECRET_KEY)
        
        # Subscribe to symbols
        symbols = ['BTC/USD', 'ETH/USD', 'AAPL']  # Example symbols
        print(f"Starting real-time analysis for: {symbols}")
        print("Press Ctrl+C to stop\n")
        
        # Start subscription
        await analyzer.subscribe_to_symbols('alpaca', symbols)
    
    except KeyboardInterrupt:
        print("\nStopping analyzer...")
        await analyzer.disconnect_all()
    except Exception as e:
        print(f"Error: {e}")
        await analyzer.disconnect_all()


if __name__ == "__main__":
    asyncio.run(main())
