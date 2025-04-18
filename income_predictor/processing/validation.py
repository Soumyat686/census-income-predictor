# processing/validation.py
import pandas as pd
import numpy as np

def validate_input_data(data):
    """
    Validate that input data meets the requirements for prediction
    
    Args:
        data: DataFrame or dict containing input data
        
    Returns:
        is_valid: Boolean indicating if data is valid
        error_messages: List of error messages if any
    """
    # Convert dict to DataFrame if needed
    if isinstance(data, dict):
        data = pd.DataFrame([data])
    
    error_messages = []
    
    # Check required columns
    required_columns = [
        'age', 'education', 'occupation', 'hours_per_week', 
        'marital_status', 'gender', 'capital_gain', 'capital_loss'
    ]
    
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        error_messages.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Validate data types and ranges
    if 'age' in data.columns:
        if not pd.api.types.is_numeric_dtype(data['age']):
            error_messages.append("Age must be numeric")
        elif (data['age'] < 18).any() or (data['age'] > 90).any():
            error_messages.append("Age must be between 18 and 90")
    
    if 'hours_per_week' in data.columns:
        if not pd.api.types.is_numeric_dtype(data['hours_per_week']):
            error_messages.append("Hours per week must be numeric")
        elif (data['hours_per_week'] < 1).any() or (data['hours_per_week'] > 168).any():
            error_messages.append("Hours per week must be between 1 and 168")
    
    if 'capital_gain' in data.columns and not pd.api.types.is_numeric_dtype(data['capital_gain']):
        error_messages.append("Capital gain must be numeric")
        
    if 'capital_loss' in data.columns and not pd.api.types.is_numeric_dtype(data['capital_loss']):
        error_messages.append("Capital loss must be numeric")
    
    # Check categorical variables
    if 'education' in data.columns:
        valid_education = ['Bachelors', 'HS-grad', 'Masters', 'Doctorate', 'Some-college', 'Assoc', 'Elementary']
        invalid_education = data['education'][~data['education'].isin(valid_education)].unique()
        if len(invalid_education) > 0:
            error_messages.append(f"Invalid education values: {', '.join(invalid_education)}")
    
    # Return validation result
    is_valid = len(error_messages) == 0
    return is_valid, error_messages