#!/usr/bin/env python3
"""
Real-time analysis using all providers simultaneously
"""

import asyncio
from deriv_analyzer import RealtimeDerivAnalyzer
from deriv_analyzer.visualization import AnalysisReporter
import json


async def prediction_callback(symbol: str, prediction: dict):
    """Callback for predictions"""
    print(f"\n{'='*70}")
    print(f"PREDICTION UPDATE: {symbol}")
    print(f"{'='*70}")
    
    predictions = prediction.get('predictions', {})
    if predictions and predictions.get('predictions'):
        summary = predictions.get('summary', {})
        price = prediction.get('price', 'N/A')
        
        print(f"Current Price: {price}")
        print(f"\nConsensus:")
        print(f"  Match vs Differ: {summary.get('consensus_match_vs_differ', 'N/A').upper()}")
        print(f"  Odd vs Even: {summary.get('consensus_odd_vs_even', 'N/A').upper()}")
        print(f"\nConfidence:")
        print(f"  Match Consensus: {summary.get('match_consensus_strength', 0)*100:.1f}%")
        print(f"  Odd Consensus: {summary.get('odd_consensus_strength', 0)*100:.1f}%")
        
        # Print detailed predictions
        print(f"\nDetailed Predictions:")
        print(f"{'Vol Level':<12}{'Match %':<12}{'Odd %':<12}{'Confidence':<12}")
        print(f"{'-'*48}")
        
        for pred in predictions['predictions']:
            vol = pred.get('volatility_level', 0)
            match = pred.get('match_probability', 0) * 100
            odd = pred.get('odd_probability', 0) * 100
            conf = pred.get('confidence', {}).get('average', 0) * 100
            print(f"{vol:<12.1f}{match:<12.1f}{odd:<12.1f}{conf:<12.1f}")


async def main():
    analyzer = RealtimeDerivAnalyzer()
    analyzer.register_callback(prediction_callback)
    
    print("\n" + "="*70)
    print("DERIVATIVE ANALYSIS TOOL - MULTI-PROVIDER DEMO")
    print("="*70)
    print("\nSupported Providers:")
    print("  1. Alpaca (stocks, options, crypto)")
    print("  2. dxFeed (derivatives, low-latency)")
    print("  3. Alpha Vantage (global data)")
    print("  4. CME Group (futures)")
    print("\nTo use any provider, add your API credentials and uncomment below.\n")
    
    try:
        # Example: Initialize Alpaca (uncomment and add credentials)
        # ALPACA_API_KEY = "your_key"
        # ALPACA_SECRET_KEY = "your_secret"
        # await analyzer.initialize_alpaca(ALPACA_API_KEY, ALPACA_SECRET_KEY)
        # await analyzer.subscribe_to_symbols('alpaca', ['BTC/USD', 'ETH/USD'])
        
        # Example: Initialize Alpha Vantage (uncomment and add credentials)
        # ALPHAVANTAGE_API_KEY = "your_key"
        # await analyzer.initialize_alphavantage(ALPHAVANTAGE_API_KEY)
        # await analyzer.subscribe_to_symbols('alphavantage', ['AAPL', 'GOOGL'])
        
        # Example: Initialize dxFeed (uncomment and add credentials)
        # DXFEED_API_KEY = "your_key"
        # await analyzer.initialize_dxfeed(DXFEED_API_KEY)
        # await analyzer.subscribe_to_symbols('dxfeed', ['ES', 'NQ', 'ZB'])
        
        # Example: Initialize CME Group (uncomment and add credentials)
        # CME_API_KEY = "your_key"
        # await analyzer.initialize_cme(CME_API_KEY)
        # await analyzer.subscribe_to_symbols('cme', ['ES', 'NQ', 'YM'])
        
        print("Running demo with sample data...\n")
        print("To enable real data, add your API credentials and uncomment providers.")
        print("\nExample: predictions/reports saved to:")
        print("  - predictions.json")
        print("  - report.txt")
        print("  - report.html")
        print("  - dashboard.png")
        
        # Keep running
        await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nStopping analyzer...")
        await analyzer.disconnect_all()
    except Exception as e:
        print(f"Error: {e}")
        await analyzer.disconnect_all()


if __name__ == "__main__":
    asyncio.run(main())
