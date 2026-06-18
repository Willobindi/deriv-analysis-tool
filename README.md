# Derivative Analysis Tool

A comprehensive tool for analyzing digit patterns, volatilities, and predicting matches/differs with odd/even classification.

## Features

- **Digit Pattern Analysis**: Analyze matches and differences in digit sequences
- **Odd/Even Classification**: Classify digits by parity
- **Volatility Analysis**: Predict across multiple volatility levels
- **Statistical Prediction**: Machine learning-based predictions

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from deriv_analyzer import DerivAnalyzer

analyzer = DerivAnalyzer()
results = analyzer.analyze_digits([1, 2, 3, 4, 5])
print(results)
```

## Project Structure

```
.
├── deriv_analyzer/
│   ├── __init__.py
│   ├── digit_analyzer.py
│   ├── volatility.py
│   ├── predictor.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_digit_analyzer.py
│   ├── test_volatility.py
│   └── test_predictor.py
├── examples/
│   └── basic_usage.py
├── requirements.txt
├── setup.py
└── README.md
```

## License

MIT
