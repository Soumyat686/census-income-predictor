# predict.py
import os
import sys
import pickle
import pandas as pd

# Add the project root to the path so we can import from config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from income_predictor.config.core import get_config, get_models_path
from processing.validation import validate_input_data

def load_model():
    """Load the trained model"""
    config = get_config()
    models_path = get_models_path()
    model_path = os.path.join(models_path, config['paths']['model_filename'])
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please train the model first.")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    return model

def predict(input_data):
    """
    Make income predictions for the provided input data
    
    Args:
        input_data: DataFrame or dict containing input features
        
    Returns:
        predictions: Array of predictions (0 = <=50K, 1 = >50K)
    """
    # Validate input data
    is_valid, error_messages = validate_input_data(input_data)
    if not is_valid:
        raise ValueError("\n".join(error_messages))
    
    # Convert dict to DataFrame if needed
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])
    
    # Load model and make predictions
    model = load_model()
    predictions = model.predict(input_data)
    
    return predictions

if __name__ == "__main__":
    # Example usage
    sample_input = {
        'age': 69,
        'education': 'Elementary',
        'occupation': 'Professional',
        'hours_per_week': 35,
        'marital_status': 'Widowed',
        'gender': 'Female',
        'capital_gain': 0,
        'capital_loss': 0
    }
    
    try:
        prediction = predict(sample_input)
        result = ">50K" if prediction[0] == 1 else "<=50K"
        print(f"Income prediction for sample input: {result}")
    except Exception as e:
        print(f"Error making prediction: {e}")