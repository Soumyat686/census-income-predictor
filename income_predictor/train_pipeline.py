# train_pipeline.py
import os
import sys
import pickle
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split


# Add the project root to the path so we can import from config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config.core import get_config, get_models_path
from processing.data_manager import load_dataset
from pipeline import create_pipeline

def train_model():
    """Train the model and save it"""
    # Load config
    config = get_config()
    
    # Load or generate data
    data = load_dataset()
    
    # Split data
    X = data.drop('high_income', axis=1)
    y = data['high_income']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=config['model']['test_size'], 
        random_state=config['model']['random_state']
    )
    
    # Create and train pipeline
    pipeline = create_pipeline()
    pipeline.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save model
    models_path = get_models_path()
    os.makedirs(models_path, exist_ok=True)
    model_path = os.path.join(models_path, config['paths']['model_filename'])
    
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
    
    print(f"Model saved to {model_path}")
    
    return pipeline

if __name__ == "__main__":
    train_model()