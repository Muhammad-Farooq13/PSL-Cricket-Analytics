"""
Unit tests for model training module
"""

import unittest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from src.models.train_model import ModelTrainer


class TestModelTrainer(unittest.TestCase):
    """Test cases for ModelTrainer class"""
    
    def setUp(self):
        """Setup test fixtures"""
        # Create sample data
        np.random.seed(42)
        self.X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100),
            'feature3': np.random.randn(100)
        })
        self.y = pd.Series(np.random.choice([0, 1], size=100))
        
        self.trainer = ModelTrainer(model_type='random_forest', random_state=42)
    
    def test_trainer_initialization(self):
        """Test ModelTrainer initialization"""
        self.assertIsInstance(self.trainer, ModelTrainer)
        self.assertEqual(self.trainer.model_type, 'random_forest')
        self.assertIsNotNone(self.trainer.model)
    
    def test_split_data(self):
        """Test data splitting"""
        X_train, X_test, y_train, y_test = self.trainer.split_data(
            self.X, self.y, test_size=0.2
        )
        
        self.assertEqual(len(X_train), 80)
        self.assertEqual(len(X_test), 20)
        self.assertEqual(len(y_train), 80)
        self.assertEqual(len(y_test), 20)
    
    def test_train_model(self):
        """Test model training"""
        X_train, X_test, y_train, y_test = self.trainer.split_data(
            self.X, self.y, test_size=0.2
        )
        
        self.trainer.train(X_train, y_train)
        
        # Check if model is trained
        self.assertIsNotNone(self.trainer.model)
        
        # Check if predictions can be made
        predictions = self.trainer.predict(X_test)
        self.assertEqual(len(predictions), len(X_test))
    
    def test_evaluate_model(self):
        """Test model evaluation"""
        X_train, X_test, y_train, y_test = self.trainer.split_data(
            self.X, self.y, test_size=0.2
        )
        
        self.trainer.train(X_train, y_train)
        metrics = self.trainer.evaluate(X_test, y_test)
        
        # Check if all metrics are present
        self.assertIn('accuracy', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        self.assertIn('f1_score', metrics)
        
        # Check if metrics are valid (between 0 and 1)
        for metric, value in metrics.items():
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1)
    
    def test_invalid_model_type(self):
        """Test initialization with invalid model type"""
        with self.assertRaises(ValueError):
            ModelTrainer(model_type='invalid_model')


if __name__ == '__main__':
    unittest.main()
