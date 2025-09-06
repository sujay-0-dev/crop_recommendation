"""
Data Preprocessing and Feature Engineering Libraries
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import logging

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Handle Data processing and feature engineering"""
    
    def  __init__(self):
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.feature_columns = [
            'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'
        ]
        self.crop_labels = {}
        
    def feature_engineer(self, data: pd.DataFrame) -> pd.DataFrame:
        """ 
        Apply feature engineering to the dataset
        
        Args:
            data: Input DataFrame with raw features
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Applying feature engineering")
        data = data.copy()
        
        # create composite features 
        data['NPK'] = (data['N'] + data['P'] + data['K']) / 3
        data['THI'] = data['temperature'] * data['humidity'] / 100
        
        # Rainfall level categorization
        data['rainfall_level'] = pd.cut(
            data['rainfall'],
            bins=[0, 50, 100, 200, 400],
            labels=[0, 1, 2, 3]  # Low, Medium, High, Very High
        ).astype(float)
        
        # pH category
        def ph_category(p):
            if p < 5.5:
                return 0  # Acidic
            elif p <= 7.5:
                return 1  # Neutral
            else:
                return 2  # Alkaline
        
        data['ph_category'] = data['ph'].apply(ph_category)
        
        # Interaction features 
        data['temp_rain_interaction'] = data['temperature'] * data['rainfall']
        data['ph_rain_interaction'] = data['ph'] * data['rainfall']
        
        return data
    
    def prepare_training_data(
        self, 
        data: pd.DataFrame, 
        test_size: float = 0.2, 
        random_state: int = 42
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepare training and testing datasets
        
        Args:
            data: Input DataFrame
            test_size: Proportion of test data
            random_state: Random seed
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        logger.info("Preparing training data")
        
        # Apply feature engineering
        data_fe = self.feature_engineer(data)
        
        # Encode target labels
        y_encoded = self.label_encoder.fit_transform(data_fe['label'])
        
        # Store crop labels mapping
        self.crop_labels = {
            idx: label for idx, label in enumerate(self.label_encoder.classes_)
        }
        
        # Prepare features
        feature_cols = self.feature_columns + [
            'NPK', 'THI', 'rainfall_level', 'ph_category',
            'temp_rain_interaction', 'ph_rain_interaction'
        ]
        
        X = data_fe[feature_cols].fillna(0)  # Handle any NaN values
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=random_state
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    
    def prepare_prediction_data(self, input_data: Dict[str, Any]) -> np.ndarray:
        """
        Prepare single prediction input
        
        Args:
            input_data: Dictionary with input features
            
        Returns:
            Scaled feature array ready for prediction
        """
        # Create DataFrame from input
        df = pd.DataFrame([input_data])
        
        # Apply feature engineering
        df_fe = self.feature_engineer(df)
        
        # Select features in correct order
        feature_cols = self.feature_columns + [
            'NPK', 'THI', 'rainfall_level', 'ph_category',
            'temp_rain_interaction', 'ph_rain_interaction'
        ]
        
        X = df_fe[feature_cols].fillna(0)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def decode_prediction(self, prediction: int) -> str:
        """
        Convert encoded prediction back to crop name
        
        Args:
            prediction: Encoded crop label
            
        Returns:
            Crop name string
        """
        return self.crop_labels.get(prediction, "unknown")
    
    def get_all_crops(self) -> list:
        """Get list of all supported crops"""
        return list(self.crop_labels.values()) if self.crop_labels else []
    
    def save_processors(self, filepath: str):
        """Save label encoder and scaler"""
        processors = {
            'label_encoder': self.label_encoder,
            'scaler': self.scaler,
            'crop_labels': self.crop_labels,
            'feature_columns': self.feature_columns
        }
        joblib.dump(processors, filepath)
        logger.info(f"Processors saved to {filepath}")
    
    def load_processors(self, filepath: str):
        """Load label encoder and scaler"""
        processors = joblib.load(filepath)
        self.label_encoder = processors['label_encoder']
        self.scaler = processors['scaler']
        self.crop_labels = processors['crop_labels']
        self.feature_columns = processors['feature_columns']
        logger.info(f"Processors loaded from {filepath}")