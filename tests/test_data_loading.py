"""
Unit tests for data loading module
"""

import unittest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from src.data.load_data import DataLoader


class TestDataLoader(unittest.TestCase):
    """Test cases for DataLoader class"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.loader = DataLoader(data_path='data/raw')
    
    def test_loader_initialization(self):
        """Test DataLoader initialization"""
        self.assertIsInstance(self.loader, DataLoader)
        self.assertIsNotNone(self.loader.data_path)
    
    def test_get_data_info(self):
        """Test get_data_info method"""
        # Create sample DataFrame
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        
        info = self.loader.get_data_info(df)
        
        self.assertIn('shape', info)
        self.assertIn('columns', info)
        self.assertEqual(info['shape'], (3, 2))
        self.assertEqual(len(info['columns']), 2)


if __name__ == '__main__':
    unittest.main()
