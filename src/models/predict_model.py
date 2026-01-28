"""
Model Prediction Module
Handles making predictions with trained models
"""

import pandas as pd
import numpy as np
import logging
import joblib
from pathlib import Path
from typing import Union, List, Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelPredictor:
    """Class to handle model predictions"""
    
    def __init__(self, model_path: str = "models"):
        """
        Initialize ModelPredictor
        
        Args:
            model_path: Directory containing saved models
        """
        self.model_path = Path(model_path)
        self.model = None
        self.model_name = None
        
    def load_model(self, model_filename: str) -> None:
        """
        Load a trained model
        
        Args:
            model_filename: Name of the model file
        """
        model_file = self.model_path / model_filename
        
        if not model_file.exists():
            raise FileNotFoundError(f"Model file not found: {model_file}")
        
        logger.info(f"Loading model from {model_file}")
        self.model = joblib.load(model_file)
        self.model_name = model_filename
        logger.info("Model loaded successfully")
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray, Dict[str, Any]]) -> np.ndarray:
        """
        Make predictions using the loaded model
        
        Args:
            X: Input features (DataFrame, array, or dictionary)
            
        Returns:
            Array of predictions
        """
        if self.model is None:
            raise ValueError("No model loaded. Call load_model() first.")
        
        # Convert dictionary to DataFrame if needed
        if isinstance(X, dict):
            X = pd.DataFrame([X])
        
        logger.info(f"Making predictions with {self.model_name}")
        predictions = self.model.predict(X)
        
        return predictions
    
    def predict_proba(self, X: Union[pd.DataFrame, np.ndarray, Dict[str, Any]]) -> np.ndarray:
        """
        Predict probabilities using the loaded model
        
        Args:
            X: Input features (DataFrame, array, or dictionary)
            
        Returns:
            Array of prediction probabilities
        """
        if self.model is None:
            raise ValueError("No model loaded. Call load_model() first.")
        
        if not hasattr(self.model, 'predict_proba'):
            raise ValueError("Loaded model does not support probability predictions")
        
        # Convert dictionary to DataFrame if needed
        if isinstance(X, dict):
            X = pd.DataFrame([X])
        
        logger.info(f"Predicting probabilities with {self.model_name}")
        probabilities = self.model.predict_proba(X)
        
        return probabilities
    
    def predict_single(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a single prediction with detailed output
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Dictionary containing prediction and probabilities (if available)
        """
        prediction = self.predict(features)[0]
        
        result = {
            'prediction': int(prediction) if isinstance(prediction, (np.integer, np.floating)) else prediction,
            'model': self.model_name
        }
        
        # Add probabilities if available
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.predict_proba(features)[0]
            result['probabilities'] = probabilities.tolist()
            result['confidence'] = float(max(probabilities))
        
        return result
    
    def batch_predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions on a batch of data
        
        Args:
            X: DataFrame of features
            
        Returns:
            DataFrame with predictions
        """
        predictions = self.predict(X)
        
        result_df = X.copy()
        result_df['prediction'] = predictions
        
        # Add probabilities if available
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.predict_proba(X)
            for i in range(probabilities.shape[1]):
                result_df[f'probability_class_{i}'] = probabilities[:, i]
            result_df['confidence'] = probabilities.max(axis=1)
        
        return result_df


if __name__ == "__main__":
    # Example usage
    predictor = ModelPredictor()
    # predictor.load_model('model.pkl')
    # prediction = predictor.predict_single({'feature1': 1.0, 'feature2': 2.0})
    # print(prediction)
