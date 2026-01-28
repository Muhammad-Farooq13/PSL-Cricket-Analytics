"""
Model Training Module
Handles model training, hyperparameter tuning, and evaluation
"""

import pandas as pd
import numpy as np
import logging
import joblib
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, confusion_matrix, classification_report)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Class to handle model training and evaluation"""
    
    def __init__(self, model_type: str = 'random_forest', random_state: int = 42):
        """
        Initialize ModelTrainer
        
        Args:
            model_type: Type of model to train ('random_forest', 'gradient_boosting', 'logistic_regression')
            random_state: Random state for reproducibility
        """
        self.model_type = model_type
        self.random_state = random_state
        self.model = None
        self.best_params = None
        self.feature_importance = None
        
        # Initialize model based on type
        self.models = {
            'random_forest': RandomForestClassifier(random_state=random_state),
            'gradient_boosting': GradientBoostingClassifier(random_state=random_state),
            'logistic_regression': LogisticRegression(random_state=random_state, max_iter=1000)
        }
        
        if model_type in self.models:
            self.model = self.models[model_type]
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def split_data(self, 
                   X: pd.DataFrame, 
                   y: pd.Series, 
                   test_size: float = 0.2,
                   stratify: bool = True) -> Tuple:
        """
        Split data into training and testing sets
        
        Args:
            X: Features DataFrame
            y: Target Series
            test_size: Proportion of test set
            stratify: Whether to stratify split
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        logger.info(f"Splitting data with test_size={test_size}")
        stratify_param = y if stratify else None
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=stratify_param
        )
        
        logger.info(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training target
        """
        logger.info(f"Training {self.model_type} model")
        self.model.fit(X_train, y_train)
        
        # Store feature importance if available
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
        logger.info("Model training completed")
    
    def hyperparameter_tuning(self, 
                             X_train: pd.DataFrame, 
                             y_train: pd.Series,
                             param_grid: Dict[str, Any],
                             cv: int = 5,
                             scoring: str = 'accuracy') -> None:
        """
        Perform hyperparameter tuning using GridSearchCV
        
        Args:
            X_train: Training features
            y_train: Training target
            param_grid: Dictionary of parameters to search
            cv: Number of cross-validation folds
            scoring: Scoring metric
        """
        logger.info(f"Starting hyperparameter tuning with {cv}-fold cross-validation")
        
        grid_search = GridSearchCV(
            self.model, 
            param_grid, 
            cv=cv, 
            scoring=scoring, 
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        self.best_params = grid_search.best_params_
        self.model = grid_search.best_estimator_
        
        logger.info(f"Best parameters: {self.best_params}")
        logger.info(f"Best cross-validation score: {grid_search.best_score_:.4f}")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions
        
        Args:
            X: Features to predict on
            
        Returns:
            Array of predictions
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict probabilities
        
        Args:
            X: Features to predict on
            
        Returns:
            Array of prediction probabilities
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        else:
            raise ValueError("Model does not support probability predictions")
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """
        Evaluate model performance
        
        Args:
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary of evaluation metrics
        """
        logger.info("Evaluating model performance")
        
        y_pred = self.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1_score': f1_score(y_test, y_pred, average='weighted')
        }
        
        # Add ROC AUC for binary classification
        if len(np.unique(y_test)) == 2 and hasattr(self.model, 'predict_proba'):
            y_pred_proba = self.predict_proba(X_test)[:, 1]
            metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba)
        
        logger.info(f"Evaluation metrics: {metrics}")
        return metrics
    
    def get_classification_report(self, X_test: pd.DataFrame, y_test: pd.Series) -> str:
        """
        Get detailed classification report
        
        Args:
            X_test: Test features
            y_test: Test target
            
        Returns:
            Classification report string
        """
        y_pred = self.predict(X_test)
        return classification_report(y_test, y_pred)
    
    def save_model(self, filename: str, model_path: str = "models") -> None:
        """
        Save trained model to file
        
        Args:
            filename: Model filename
            model_path: Directory to save model
        """
        model_dir = Path(model_path)
        model_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = model_dir / filename
        logger.info(f"Saving model to {file_path}")
        
        joblib.dump(self.model, file_path)
        logger.info("Model saved successfully")
    
    def load_model(self, filename: str, model_path: str = "models") -> None:
        """
        Load trained model from file
        
        Args:
            filename: Model filename
            model_path: Directory containing model
        """
        file_path = Path(model_path) / filename
        logger.info(f"Loading model from {file_path}")
        
        self.model = joblib.load(file_path)
        logger.info("Model loaded successfully")
    
    def get_feature_importance(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get feature importance scores
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            DataFrame with feature importance
        """
        if self.feature_importance is None:
            raise ValueError("Feature importance not available for this model")
        
        return self.feature_importance.head(top_n)


if __name__ == "__main__":
    # Example usage
    logger.info("Model training module loaded")
