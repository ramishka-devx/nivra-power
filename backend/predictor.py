"""
NILM Model Predictor - Load and use the trained pickle model for predictions
"""

import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List

# Label to device states mapping
LABEL_TO_DEVICE_STATES = {
    0: {"bulb": False, "fan": False, "iron": False},
    1: {"bulb": True, "fan": False, "iron": False},
    2: {"bulb": False, "fan": True, "iron": False},
    3: {"bulb": True, "fan": True, "iron": False},
    4: {"bulb": False, "fan": False, "iron": True},
    5: {"bulb": True, "fan": False, "iron": True},
    6: {"bulb": False, "fan": True, "iron": True},
    7: {"bulb": True, "fan": True, "iron": True},
}


class NILMPredictor:
    """Load trained model and make predictions on new data"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize predictor with trained model
        
        Args:
            model_path: Path to the pickle file (default: backend/artifacts/nilm_rf_model.pkl)
        """
        if model_path is None:
            base_dir = Path(__file__).resolve().parent
            model_path = base_dir / "artifacts" / "nilm_rf_model.pkl"
        
        self.model_path = Path(model_path)
        self.model = None
        self.feature_columns = None
        self.class_labels = None
        
        self.load_model()
    
    def load_model(self):
        """Load the trained model from pickle file"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        with open(self.model_path, 'rb') as f:
            artifact = pickle.load(f)
        
        self.model = artifact['model']
        self.feature_columns = artifact['feature_columns']
        self.class_labels = artifact['class_labels']
        
        print(f"✓ Model loaded from {self.model_path}")
        print(f"  Features: {len(self.feature_columns)}")
        print(f"  Classes: {self.class_labels}")
    
    def predict_single(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict device states from a single data point
        
        Args:
            data: Dictionary with power metrics (voltage, current, active_power, etc.)
            
        Returns:
            Dictionary with prediction results including:
                - label: Predicted class label
                - device_states: Which devices are ON/OFF
                - probabilities: Probability for each class
        """
        # Prepare features in the correct order
        features = []
        for col in self.feature_columns:
            value = data.get(col, 0.0)
            if value is None:
                value = 0.0
            features.append(float(value))
        
        # Make prediction
        X = np.array([features])
        label = int(self.model.predict(X)[0])
        probabilities = self.model.predict_proba(X)[0]
        
        # Get device states for predicted label
        device_states = LABEL_TO_DEVICE_STATES.get(label, {
            "bulb": False,
            "fan": False,
            "iron": False
        })
        
        # Format probability results
        prob_list = []
        for i, prob in enumerate(probabilities):
            class_label = self.class_labels[i]
            prob_list.append({
                "label": int(class_label),
                "probability": float(prob),
                "device_states": LABEL_TO_DEVICE_STATES.get(int(class_label), {
                    "bulb": False,
                    "fan": False,
                    "iron": False
                })
            })
        
        # Sort by probability
        prob_list = sorted(prob_list, key=lambda x: x['probability'], reverse=True)
        
        return {
            "label": label,
            "device_states": device_states,
            "probabilities": prob_list,
            "confidence": float(max(probabilities))
        }
    
    def predict_batch(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Predict device states for multiple data points
        
        Args:
            data_list: List of dictionaries with power metrics
            
        Returns:
            List of prediction results
        """
        return [self.predict_single(data) for data in data_list]
    
    def predict_from_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict device states from a pandas DataFrame
        
        Args:
            df: DataFrame with power metrics
            
        Returns:
            DataFrame with original data plus predictions
        """
        # Prepare features
        X = df[self.feature_columns].fillna(0).values
        
        # Make predictions
        predictions = self.model.predict(X)
        
        # Add predictions to dataframe
        result_df = df.copy()
        result_df['predicted_label'] = predictions
        result_df['bulb'] = result_df['predicted_label'].map(lambda x: LABEL_TO_DEVICE_STATES.get(x, {}).get('bulb', False))
        result_df['fan'] = result_df['predicted_label'].map(lambda x: LABEL_TO_DEVICE_STATES.get(x, {}).get('fan', False))
        result_df['iron'] = result_df['predicted_label'].map(lambda x: LABEL_TO_DEVICE_STATES.get(x, {}).get('iron', False))
        
        return result_df


# Example usage function
def example_prediction():
    """Example of how to use the predictor"""
    
    # Initialize predictor
    predictor = NILMPredictor()
    
    # Example data point (typical power metrics)
    sample_data = {
        'voltage': 230.5,
        'current': 0.5,
        'active_power': 115.2,
        'reactive_power': 10.5,
        'apparent_power': 115.7,
        'power_factor': 0.995
    }
    
    # Make prediction
    result = predictor.predict_single(sample_data)
    
    print("\n=== Prediction Result ===")
    print(f"Predicted Label: {result['label']}")
    print(f"Device States: {result['device_states']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("\nTop 3 Probabilities:")
    for i, prob in enumerate(result['probabilities'][:3], 1):
        print(f"  {i}. Label {prob['label']}: {prob['probability']:.2%} - {prob['device_states']}")
    
    return result


if __name__ == "__main__":
    example_prediction()
