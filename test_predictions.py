"""
Test script to demonstrate pickle model usage for predictions
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.predictor import NILMPredictor

def test_single_prediction():
    """Test single data point prediction"""
    print("=" * 60)
    print("TEST 1: Single Data Point Prediction")
    print("=" * 60)
    
    # Initialize predictor
    predictor = NILMPredictor()
    
    # Test data - typical household power consumption
    test_cases = [
        {
            "name": "Only Bulb ON",
            "data": {"voltage": 230, "current": 0.26, "active_power": 60, "reactive_power": 0, "apparent_power": 60, "power_factor": 1.0}
        },
        {
            "name": "Only Fan ON",
            "data": {"voltage": 230, "current": 0.35, "active_power": 80, "reactive_power": 14, "apparent_power": 81, "power_factor": 0.98}
        },
        {
            "name": "Only Iron ON",
            "data": {"voltage": 230, "current": 4.78, "active_power": 1100, "reactive_power": 0, "apparent_power": 1100, "power_factor": 1.0}
        },
        {
            "name": "Bulb + Fan ON",
            "data": {"voltage": 230, "current": 0.61, "active_power": 140, "reactive_power": 14, "apparent_power": 141, "power_factor": 0.99}
        },
        {
            "name": "All Devices ON",
            "data": {"voltage": 230, "current": 5.22, "active_power": 1240, "reactive_power": 124, "apparent_power": 1246, "power_factor": 0.99}
        },
    ]
    
    for test_case in test_cases:
        print(f"\n📊 {test_case['name']}")
        print(f"   Input: {test_case['data']}")
        
        result = predictor.predict_single(test_case['data'])
        
        print(f"   Predicted Label: {result['label']}")
        print(f"   Device States: {result['device_states']}")
        print(f"   Confidence: {result['confidence']:.2%}")

def test_batch_prediction():
    """Test batch prediction"""
    print("\n" + "=" * 60)
    print("TEST 2: Batch Prediction")
    print("=" * 60)
    
    predictor = NILMPredictor()
    
    # Multiple data points
    batch_data = [
        {"voltage": 230, "current": 0.26, "active_power": 60, "reactive_power": 0, "apparent_power": 60, "power_factor": 1.0},
        {"voltage": 230, "current": 0.35, "active_power": 80, "reactive_power": 14, "apparent_power": 81, "power_factor": 0.98},
        {"voltage": 230, "current": 4.78, "active_power": 1100, "reactive_power": 0, "apparent_power": 1100, "power_factor": 1.0},
    ]
    
    results = predictor.predict_batch(batch_data)
    
    print(f"\n✓ Processed {len(results)} predictions")
    for i, (data, result) in enumerate(zip(batch_data, results), 1):
        print(f"\n   {i}. Power: {data['active_power']}W → {result['device_states']}")

def test_dataframe_prediction():
    """Test DataFrame prediction"""
    print("\n" + "=" * 60)
    print("TEST 3: DataFrame Prediction")
    print("=" * 60)
    
    import pandas as pd
    
    predictor = NILMPredictor()
    
    # Create sample DataFrame
    data = {
        'voltage': [230, 230, 230, 230],
        'current': [0.26, 0.35, 4.78, 5.22],
        'active_power': [60, 80, 1100, 1240],
        'reactive_power': [0, 14, 0, 124],
        'apparent_power': [60, 81, 1100, 1246],
        'power_factor': [1.0, 0.98, 1.0, 0.99]
    }
    df = pd.DataFrame(data)
    
    print("\n📊 Input DataFrame:")
    print(df)
    
    result_df = predictor.predict_from_dataframe(df)
    
    print("\n📊 Predictions:")
    print(result_df[['active_power', 'predicted_label', 'bulb', 'fan', 'iron']])

def test_api_format():
    """Test prediction in API format (JSON-like)"""
    print("\n" + "=" * 60)
    print("TEST 4: API Format (JSON)")
    print("=" * 60)
    
    import json
    
    predictor = NILMPredictor()
    
    # Simulated API request
    api_request = {
        "voltage": 230.5,
        "current": 4.78,
        "active_power": 1100,
        "reactive_power": 0,
        "apparent_power": 1100,
        "power_factor": 1.0
    }
    
    print("\n📥 API Request (JSON):")
    print(json.dumps(api_request, indent=2))
    
    result = predictor.predict_single(api_request)
    
    print("\n📤 API Response (JSON):")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    print("\n" + "🔬 NILM Model Prediction Tests ".center(60, "="))
    print()
    
    try:
        test_single_prediction()
        test_batch_prediction()
        test_dataframe_prediction()
        test_api_format()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Please run the notebook cell to save the model first:")
        print("   1. Open NILM_RF.ipynb")
        print("   2. Run all cells including the 'Save Model as Pickle File' cell")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
