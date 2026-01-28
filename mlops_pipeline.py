"""
MLOps Pipeline for Continuous Integration and Deployment
Handles automated training, testing, and deployment workflows
"""

import os
import sys
import logging
import joblib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.data.load_data import DataLoader
from src.data.preprocess import DataPreprocessor
from src.features.build_features import FeatureEngineer
from src.models.train_model import ModelTrainer
from src.utils.logger import setup_logger
from src.utils.config import ConfigManager
from src.utils.helpers import save_json, ensure_dir

# Setup logging
logger = setup_logger('mlops_pipeline', log_dir='logs')


class MLOpsPipeline:
    """MLOps Pipeline for automated model training and deployment"""
    
    def __init__(self, config_file: str = 'config/pipeline_config.json'):
        """
        Initialize MLOps Pipeline
        
        Args:
            config_file: Path to configuration file
        """
        self.config_manager = ConfigManager()
        self.config_file = config_file
        self.run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.results = {}
        
        # Load configuration if exists
        if Path(config_file).exists():
            self.config = self.config_manager.load_json(Path(config_file).name)
        else:
            self.config = self._get_default_config()
            logger.info("Using default configuration")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default pipeline configuration"""
        return {
            'data': {
                'raw_path': 'data/raw',
                'processed_path': 'data/processed',
                'test_size': 0.2,
                'random_state': 42
            },
            'preprocessing': {
                'missing_value_strategy': 'drop',
                'remove_duplicates': True,
                'scale_features': False
            },
            'model': {
                'type': 'random_forest',
                'hyperparameter_tuning': False,
                'cv_folds': 5
            },
            'output': {
                'model_path': 'models',
                'model_name': 'psl_model.pkl',
                'reports_path': 'reports',
                'metrics_file': 'metrics.json'
            },
            'thresholds': {
                'min_accuracy': 0.7,
                'min_f1_score': 0.6
            }
        }
    
    def load_data(self) -> pd.DataFrame:
        """
        Load raw data
        
        Returns:
            Loaded DataFrame
        """
        logger.info("=" * 80)
        logger.info("STEP 1: Loading Data")
        logger.info("=" * 80)
        
        data_path = self.config['data']['raw_path']
        loader = DataLoader(data_path=data_path)
        
        try:
            df = loader.load_psl_dataset()
            logger.info(f"Data loaded successfully: {df.shape}")
            self.results['data_shape'] = df.shape
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data
        
        Args:
            df: Input DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        logger.info("=" * 80)
        logger.info("STEP 2: Preprocessing Data")
        logger.info("=" * 80)
        
        preprocessor = DataPreprocessor()
        
        # Handle missing values
        strategy = self.config['preprocessing']['missing_value_strategy']
        df = preprocessor.handle_missing_values(df, strategy=strategy)
        logger.info(f"Missing values handled using '{strategy}' strategy")
        
        # Remove duplicates
        if self.config['preprocessing']['remove_duplicates']:
            df = preprocessor.remove_duplicates(df)
            logger.info("Duplicates removed")
        
        # Save processed data
        processed_path = self.config['data']['processed_path']
        preprocessor.save_processed_data(df, f'processed_data_{self.run_id}.csv', 
                                        output_path=processed_path)
        
        self.results['processed_shape'] = df.shape
        return df
    
    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform feature engineering
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("=" * 80)
        logger.info("STEP 3: Feature Engineering")
        logger.info("=" * 80)
        
        engineer = FeatureEngineer()
        
        # Add custom feature engineering here
        # For now, just return the dataframe
        logger.info("Feature engineering completed")
        
        self.results['feature_count'] = len(df.columns)
        return df
    
    def prepare_train_test_split(self, df: pd.DataFrame, 
                                  target_column: str) -> tuple:
        """
        Prepare training and testing datasets
        
        Args:
            df: Input DataFrame
            target_column: Name of target column
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        logger.info("=" * 80)
        logger.info("STEP 4: Preparing Train/Test Split")
        logger.info("=" * 80)
        
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame")
        
        # Separate features and target
        X = df.drop(target_column, axis=1)
        y = df[target_column]
        
        # Select only numerical features
        X = X.select_dtypes(include=[np.number])
        
        # Split data
        test_size = self.config['data']['test_size']
        random_state = self.config['data']['random_state']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        logger.info(f"Train set size: {X_train.shape}")
        logger.info(f"Test set size: {X_test.shape}")
        
        self.results['train_size'] = len(X_train)
        self.results['test_size'] = len(X_test)
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series,
                   X_test: pd.DataFrame, y_test: pd.Series) -> ModelTrainer:
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            
        Returns:
            Trained ModelTrainer instance
        """
        logger.info("=" * 80)
        logger.info("STEP 5: Model Training")
        logger.info("=" * 80)
        
        model_type = self.config['model']['type']
        random_state = self.config['data']['random_state']
        
        trainer = ModelTrainer(model_type=model_type, random_state=random_state)
        
        # Train model
        trainer.train(X_train, y_train)
        logger.info(f"Model training completed: {model_type}")
        
        # Hyperparameter tuning (if enabled)
        if self.config['model']['hyperparameter_tuning']:
            logger.info("Starting hyperparameter tuning...")
            param_grid = self._get_param_grid(model_type)
            cv_folds = self.config['model']['cv_folds']
            trainer.hyperparameter_tuning(X_train, y_train, param_grid, cv=cv_folds)
            self.results['best_params'] = trainer.best_params
        
        # Evaluate model
        metrics = trainer.evaluate(X_test, y_test)
        logger.info("Model Evaluation Metrics:")
        for metric, value in metrics.items():
            logger.info(f"  {metric}: {value:.4f}")
        
        self.results['metrics'] = metrics
        self.results['model_type'] = model_type
        
        return trainer
    
    def _get_param_grid(self, model_type: str) -> Dict[str, list]:
        """Get hyperparameter grid for model type"""
        param_grids = {
            'random_forest': {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5]
            },
            'logistic_regression': {
                'C': [0.1, 1, 10],
                'penalty': ['l2']
            }
        }
        return param_grids.get(model_type, {})
    
    def validate_model(self) -> bool:
        """
        Validate model against thresholds
        
        Returns:
            True if model meets thresholds, False otherwise
        """
        logger.info("=" * 80)
        logger.info("STEP 6: Model Validation")
        logger.info("=" * 80)
        
        metrics = self.results['metrics']
        thresholds = self.config['thresholds']
        
        passed = True
        
        # Check accuracy threshold
        if metrics['accuracy'] < thresholds['min_accuracy']:
            logger.warning(f"Accuracy {metrics['accuracy']:.4f} below threshold {thresholds['min_accuracy']}")
            passed = False
        
        # Check F1 score threshold
        if metrics['f1_score'] < thresholds['min_f1_score']:
            logger.warning(f"F1 Score {metrics['f1_score']:.4f} below threshold {thresholds['min_f1_score']}")
            passed = False
        
        if passed:
            logger.info("✓ Model passed all validation thresholds")
        else:
            logger.warning("✗ Model did not meet validation thresholds")
        
        self.results['validation_passed'] = passed
        return passed
    
    def save_model(self, trainer: ModelTrainer) -> None:
        """
        Save the trained model
        
        Args:
            trainer: Trained ModelTrainer instance
        """
        logger.info("=" * 80)
        logger.info("STEP 7: Saving Model")
        logger.info("=" * 80)
        
        model_path = self.config['output']['model_path']
        model_name = self.config['output']['model_name']
        
        trainer.save_model(model_name, model_path=model_path)
        logger.info(f"Model saved: {model_path}/{model_name}")
        
        self.results['model_saved'] = True
        self.results['model_path'] = f"{model_path}/{model_name}"
    
    def save_results(self) -> None:
        """Save pipeline results and metrics"""
        logger.info("=" * 80)
        logger.info("STEP 8: Saving Results")
        logger.info("=" * 80)
        
        reports_path = self.config['output']['reports_path']
        ensure_dir(reports_path)
        
        # Add metadata
        self.results['run_id'] = self.run_id
        self.results['timestamp'] = datetime.now().isoformat()
        
        # Save metrics
        metrics_file = Path(reports_path) / f"metrics_{self.run_id}.json"
        save_json(self.results, str(metrics_file))
        logger.info(f"Results saved: {metrics_file}")
    
    def run_pipeline(self, target_column: str = 'target') -> Dict[str, Any]:
        """
        Run the complete MLOps pipeline
        
        Args:
            target_column: Name of the target column
            
        Returns:
            Dictionary with pipeline results
        """
        logger.info("\n" + "=" * 80)
        logger.info("MLOPS PIPELINE STARTED")
        logger.info(f"Run ID: {self.run_id}")
        logger.info("=" * 80 + "\n")
        
        try:
            # Step 1: Load data
            df = self.load_data()
            
            # Step 2: Preprocess data
            df = self.preprocess_data(df)
            
            # Step 3: Feature engineering
            df = self.feature_engineering(df)
            
            # Step 4: Prepare train/test split
            X_train, X_test, y_train, y_test = self.prepare_train_test_split(df, target_column)
            
            # Step 5: Train model
            trainer = self.train_model(X_train, y_train, X_test, y_test)
            
            # Step 6: Validate model
            validation_passed = self.validate_model()
            
            # Step 7: Save model (only if validation passed)
            if validation_passed:
                self.save_model(trainer)
            else:
                logger.warning("Model not saved due to validation failure")
                self.results['model_saved'] = False
            
            # Step 8: Save results
            self.save_results()
            
            logger.info("\n" + "=" * 80)
            logger.info("MLOPS PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 80 + "\n")
            
            return self.results
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            self.results['error'] = str(e)
            self.results['status'] = 'failed'
            raise


if __name__ == "__main__":
    # Example usage
    pipeline = MLOpsPipeline()
    
    # Note: Update 'target' with your actual target column name
    try:
        results = pipeline.run_pipeline(target_column='target')
        print("\nPipeline Results:")
        print(f"Accuracy: {results['metrics']['accuracy']:.4f}")
        print(f"F1 Score: {results['metrics']['f1_score']:.4f}")
    except Exception as e:
        print(f"Pipeline execution failed: {str(e)}")
        print("Please ensure you have a valid dataset with a target column.")
