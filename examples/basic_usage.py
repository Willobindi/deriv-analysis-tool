#!/usr/bin/env python3
"""
Basic usage example for Derivative Analysis Tool
"""

from deriv_analyzer import DerivAnalyzer
import json

def main():
    # Initialize the analyzer
    analyzer = DerivAnalyzer()
    
    # Sample digit data
    digits = [1, 1, 2, 3, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 9]
    
    print("=" * 50)
    print("Derivative Analysis Tool - Basic Usage")
    print("=" * 50)
    
    # 1. Analyze digits
    print("\n1. DIGIT ANALYSIS")
    print("-" * 50)
    digit_analysis = analyzer.analyze_digits(digits)
    print(f"Matches found: {len(digit_analysis['matches'])}")
    print(f"Differs found: {len(digit_analysis['differs'])}")
    print(f"Odd digits: {len(digit_analysis['odd_even']['odd'])}")
    print(f"Even digits: {len(digit_analysis['odd_even']['even'])}")
    print(f"Statistics: {digit_analysis['statistics']}")
    
    # 2. Volatility Analysis
    print("\n2. VOLATILITY ANALYSIS")
    print("-" * 50)
    volatility_data = analyzer.analyze_volatility(digits, window_size=5)
    print(f"Mean volatility: {volatility_data['mean_volatility']:.4f}")
    print(f"Max volatility: {volatility_data['max_volatility']:.4f}")
    print(f"Min volatility: {volatility_data['min_volatility']:.4f}")
    
    # 3. Predictions across volatility levels
    print("\n3. PREDICTIONS FOR ALL VOLATILITIES")
    print("-" * 50)
    predictions = analyzer.predict(digits, volatility_levels=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    
    for pred in predictions['predictions']:
        print(f"\nVolatility Level: {pred['volatility_level']}")
        print(f"  Match Probability: {pred['match_probability']:.4f}")
        print(f"  Differ Probability: {pred['differ_probability']:.4f}")
        print(f"  Odd Probability: {pred['odd_probability']:.4f}")
        print(f"  Even Probability: {pred['even_probability']:.4f}")
        print(f"  Predicted: {pred['predicted_outcome']}")
        print(f"  Confidence: {pred['confidence']['average']:.4f}")
    
    print("\n4. SUMMARY")
    print("-" * 50)
    summary = predictions['summary']
    print(f"Consensus (Match vs Differ): {summary['consensus_match_vs_differ']}")
    print(f"Consensus (Odd vs Even): {summary['consensus_odd_vs_even']}")
    print(f"Match consensus strength: {summary['match_consensus_strength']:.2%}")
    print(f"Odd consensus strength: {summary['odd_consensus_strength']:.2%}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
