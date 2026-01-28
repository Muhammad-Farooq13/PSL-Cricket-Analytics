"""
Unit tests for preprocessing module
"""

import unittest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from src.data.preprocess import DataPreprocessor


class TestDataPreprocessor(unittest.TestCase):
    """Test cases for DataPreprocessor class"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.preprocessor = DataPreprocessor()
        
        # Create sample DataFrame with missing values and duplicates
        self.df = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 4],
            'B': [5, np.nan, 7, 8, 8],
            'C': ['x', 'y', 'z', 'w', 'w']
        })
    
    def test_preprocessor_initialization(self):
        """Test DataPreprocessor initialization"""
        self.assertIsInstance(self.preprocessor, DataPreprocessor)
        self.assertIsInstance(self.preprocessor.scalers, dict)
        self.assertIsInstance(self.preprocessor.encoders, dict)
    
    def test_handle_missing_values_drop(self):
        """Test handling missing values with drop strategy"""
        result = self.preprocessor.handle_missing_values(self.df, strategy='drop')
        self.assertEqual(len(result), 2)  # Should drop 2 rows with NaN
    
    def test_handle_missing_values_mean(self):
        """Test handling missing values with mean strategy"""
        result = self.preprocessor.handle_missing_values(self.df, strategy='mean')
        self.assertFalse(result[['A', 'B']].isnull().any().any())
    
    def test_remove_duplicates(self):
        """Test duplicate removal"""
        result = self.preprocessor.remove_duplicates(self.df)
        self.assertEqual(len(result), 4)  # Should remove 1 duplicate row
    
    def test_encode_categorical_label(self):
        """Test label encoding"""
        result = self.preprocessor.encode_categorical(self.df, ['C'], method='label')
        self.assertTrue(pd.api.types.is_numeric_dtype(result['C']))


class TestDataPreprocessorEdgeCases(unittest.TestCase):
    """Test edge cases for DataPreprocessor"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.preprocessor = DataPreprocessor()
    
    def test_empty_dataframe(self):
        """Test preprocessing empty DataFrame"""
        df = pd.DataFrame()
        result = self.preprocessor.handle_missing_values(df)
        self.assertTrue(result.empty)
    
    def test_no_missing_values(self):
        """Test DataFrame with no missing values"""
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result = self.preprocessor.handle_missing_values(df, strategy='drop')
        self.assertEqual(len(result), 3)


if __name__ == '__main__':
    unittest.main()
