# processing/data_manager.py
import pandas as pd
import numpy as np
import os
import sys

# Add the project root to the path so we can import from config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.core import get_config, get_data_path

def generate_census_data(n_samples=5000):
    """Generate synthetic census data for income prediction"""
    np.random.seed(42)
    
    # Generate features based on typical census data
    age = np.random.randint(18, 90, n_samples)
    
    # Education levels
    education_levels = ['Bachelors', 'HS-grad', 'Masters', 'Doctorate', 'Some-college', 'Assoc', 'Elementary']
    education_weights = [0.25, 0.3, 0.15, 0.05, 0.15, 0.07, 0.03]
    education = np.random.choice(education_levels, n_samples, p=education_weights)
    
    # Occupations
    occupations = ['Professional', 'White-collar', 'Sales', 'Blue-collar', 'Service', 'Other']
    occupation_weights = [0.25, 0.30, 0.15, 0.2, 0.07, 0.03]
    occupation = np.random.choice(occupations, n_samples, p=occupation_weights)
    
    # Work hours
    hours_per_week = np.random.normal(loc=40, scale=10, size=n_samples).clip(min=10, max=80).astype(int)
    
    # Marital status
    marital_status = np.random.choice(['Married', 'Never-married', 'Divorced', 'Separated', 'Widowed'], n_samples)
    
    # Gender
    gender = np.random.choice(['Male', 'Female'], n_samples)
    
    # Capital gain and loss
    capital_gain = np.zeros(n_samples)
    capital_gain_mask = np.random.random(n_samples) < 0.2  # 20% have capital gain
    capital_gain[capital_gain_mask] = np.random.exponential(scale=5000, size=capital_gain_mask.sum())
    
    capital_loss = np.zeros(n_samples)
    capital_loss_mask = np.random.random(n_samples) < 0.1  # 10% have capital loss
    capital_loss[capital_loss_mask] = np.random.exponential(scale=2000, size=capital_loss_mask.sum())
    
    # Create synthetic relationship for income prediction
    education_score = pd.Series(education).map({
        'Doctorate': 5, 'Masters': 4, 'Bachelors': 3, 'Assoc': 2, 
        'Some-college': 1.5, 'HS-grad': 1, 'Elementary': 0.5
    }).values
    
    occupation_score = pd.Series(occupation).map({
        'Professional': 5, 'White-collar': 4, 'Sales': 3, 
        'Blue-collar': 2, 'Service': 1.5, 'Other': 1
    }).values
    
    marital_score = pd.Series(marital_status).map({
        'Married': 1.2, 'Never-married': 0.8, 'Divorced': 0.9, 'Separated': 0.9, 'Widowed': 0.9
    }).values
    
    gender_score = pd.Series(gender).map({'Male': 1.1, 'Female': 0.9}).values  # Historical bias in data
    
    # Calculate income score
    income_score = (
        0.3 * age / 50 + 
        0.8 * education_score + 
        0.7 * occupation_score +
        0.4 * hours_per_week / 40 +
        0.2 * marital_score +
        0.2 * gender_score +
        0.0002 * capital_gain -
        0.0001 * capital_loss +
        np.random.normal(0, 0.3, n_samples)
    )
    
    # Convert to binary outcome (1 = income > $50K, 0 = income <= $50K)
    high_income = (income_score > 2.2).astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'age': age,
        'education': education,
        'occupation': occupation,
        'hours_per_week': hours_per_week,
        'marital_status': marital_status,
        'gender': gender,
        'capital_gain': capital_gain,
        'capital_loss': capital_loss,
        'high_income': high_income
    })
    
    return data

def save_dataset(data):
    """Save the dataset to the specified path"""
    config = get_config()
    data_path = get_data_path()
    
    # Ensure directory exists
    os.makedirs(data_path, exist_ok=True)
    
    # Save file
    output_path = os.path.join(data_path, config['data']['output_file'])
    data.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    
    return output_path

def load_dataset():
    """Load the dataset from the specified path"""
    config = get_config()
    data_path = get_data_path()
    file_path = os.path.join(data_path, config['data']['output_file'])
    
    if not os.path.exists(file_path):
        print(f"Dataset not found at {file_path}. Generating new dataset.")
        data = generate_census_data()
        save_dataset(data)
    else:
        data = pd.read_csv(file_path)
        print(f"Dataset loaded from {file_path}")
    
    return data