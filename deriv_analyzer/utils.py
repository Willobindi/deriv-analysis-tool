import json
import numpy as np

def serialize_results(results):
    """Convert numpy types to JSON-serializable types"""
    def convert(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(item) for item in obj]
        return obj
    
    return convert(results)

def format_results_for_display(results):
    """Format results nicely for display"""
    return json.dumps(results, indent=2)
