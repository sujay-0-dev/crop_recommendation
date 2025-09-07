"""
Model training and evaluation utilities
"""
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import logging
from pathlib import Path
from typing import Dict, Any, Tuple

from data_processing import DataProcessor
from config import MODELS_DIR, MODEL_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Handle model training and evaluation"""
    
    def __init__(self):
        self.model = None
        self.data_processor = DataProcessor()
        self.model_metrics = {}
        
    def train_model(self, data_path: str) -> Dict[str, Any]:
        """
        Train the XGBoost model
        
        Args:
            data_path: Path to the training CSV file
            
        Returns:
            Dictionary with training metrics
        """
        logger.info("Starting model training")
        
        # Load data
        data = pd.read_csv(data_path)
        logger.info(f"Loaded {len(data)} samples from {data_path}")
        
        # Prepare data
        X_train, X_test, y_train, y_test = self.data_processor.prepare_training_data(
            data, 
            test_size=MODEL_CONFIG['test_size'],
            random_state=MODEL_CONFIG['random_state']
        )
        
        # Initialize XGBoost model
        self.model = XGBClassifier(**MODEL_CONFIG['xgboost_params'])
        
        # Train model
        logger.info("Training XGBoost model")
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_predictions = self.model.predict(X_train)
        test_predictions = self.model.predict(X_test)
        
        train_accuracy = accuracy_score(y_train, train_predictions)
        test_accuracy = accuracy_score(y_test, test_predictions)
        
        # Store metrics
        self.model_metrics = {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'features': len(X_train[0]),
            'classes': len(np.unique(y_train))
        }
        
        # Detailed classification report
        report = classification_report(
            y_test, 
            test_predictions, 
            target_names=self.data_processor.get_all_crops(),
            output_dict=True
        )
        
        logger.info(f"Training completed - Test Accuracy: {test_accuracy:.4f}")
        logger.info(f"Training Accuracy: {train_accuracy:.4f}")
        
        return {
            'metrics': self.model_metrics,
            'classification_report': report
        }
    
    def predict(self, input_data: Dict[str, Any]) -> Tuple[str, float, Dict[str, float]]:
        """
        Make prediction for single input
        
        Args:
            input_data: Dictionary with input features
            
        Returns:
            Tuple of (predicted_crop, confidence, all_probabilities)
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        # Prepare input data
        X = self.data_processor.prepare_prediction_data(input_data)
        
        # Get prediction and probabilities
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        # Convert to crop names and probabilities
        predicted_crop = self.data_processor.decode_prediction(prediction)
        confidence = float(probabilities.max())
        
        all_probabilities = {
            self.data_processor.decode_prediction(idx): float(prob)
            for idx, prob in enumerate(probabilities)
        }
        
        return predicted_crop, confidence, all_probabilities
    
    def batch_predict(self, input_batch: list) -> list:
        """
        Make predictions for batch of inputs
        
        Args:
            input_batch: List of input dictionaries
            
        Returns:
            List of prediction results
        """
        results = []
        for input_data in input_batch:
            crop, confidence, probs = self.predict(input_data)
            results.append({
                'predicted_crop': crop,
                'confidence': confidence,
                'all_probabilities': probs
            })
        return results
    
    def save_model(self, model_path: str = None):
        """Save trained model and processors"""
        if model_path is None:
            model_path = MODELS_DIR / "crop_recommendation_model.joblib"
        
        if self.model is None:
            raise ValueError("No model to save")
        
        # Save model
        joblib.dump(self.model, model_path)
        
        # Save data processors
        processors_path = MODELS_DIR / "data_processors.joblib"
        self.data_processor.save_processors(processors_path)
        
        # Save metrics
        metrics_path = MODELS_DIR / "model_metrics.joblib"
        joblib.dump(self.model_metrics, metrics_path)
        
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Processors saved to {processors_path}")
        
    def load_model(self, model_path: str = None):
        """Load trained model and processors"""
        if model_path is None:
            model_path = MODELS_DIR / "crop_recommendation_model.joblib"
        
        # Load model
        self.model = joblib.load(model_path)
        
        # Load data processors
        processors_path = MODELS_DIR / "data_processors.joblib"
        self.data_processor.load_processors(processors_path)
        
        # Load metrics if available
        metrics_path = MODELS_DIR / "model_metrics.joblib"
        try:
            self.model_metrics = joblib.load(metrics_path)
        except FileNotFoundError:
            logger.warning("Model metrics not found")
            
        logger.info(f"Model loaded from {model_path}")
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from trained model"""
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        feature_names = self.data_processor.feature_columns + [
            'NPK', 'THI', 'rainfall_level', 'ph_category',
            'temp_rain_interaction', 'ph_rain_interaction'
        ]
        
        importance_scores = self.model.feature_importances_
        
        return dict(zip(feature_names, importance_scores.tolist()))


def train_and_save_model(data_path: str):
    """Utility function to train and save model"""
    trainer = ModelTrainer()
    results = trainer.train_model(data_path)
    trainer.save_model()
    
    logger.info("Model training completed and saved")
    return results


if __name__ == "__main__":
    # Example usage
    data_path = "data/Crop_recommendation.csv"  # Update path as needed
    results = train_and_save_model(data_path)
    print("Training Results:", results['metrics'])