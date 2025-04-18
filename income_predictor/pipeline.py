# pipeline.py
import os
import sys
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Add the project root to the path so we can import from config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config.core import get_config
from processing.features import get_feature_pipeline

def create_pipeline():
    """Create the complete modeling pipeline"""
    config = get_config()
    
    # Get feature preprocessing
    preprocessor, _, _ = get_feature_pipeline()
    
    # Create full pipeline with preprocessing and classifier
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=config['model']['n_estimators'],
            random_state=config['model']['random_state']
        ))
    ])
    
    return pipeline