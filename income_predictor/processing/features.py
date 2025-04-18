# processing/features.py
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def get_feature_pipeline():
    """Define preprocessing steps for numeric and categorical features"""
    # Define numeric and categorical features
    numeric_features = ['age', 'hours_per_week', 'capital_gain', 'capital_loss']
    categorical_features = ['education', 'occupation', 'marital_status', 'gender']
    
    # Create preprocessor
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    return preprocessor, numeric_features, categorical_features