"""
Data Loading Module
Handles loading raw data from various sources
"""

import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Class to handle data loading operations"""
    
    def __init__(self, data_path: str = "data/raw"):
        """
        Initialize DataLoader
        
        Args:
            data_path: Path to raw data directory
        """
        self.data_path = Path(data_path)
        
    def load_csv(self, filename: str, **kwargs) -> pd.DataFrame:
        """
        Load CSV file into pandas DataFrame
        
        Args:
            filename: Name of the CSV file
            **kwargs: Additional arguments for pd.read_csv
            
        Returns:
            DataFrame containing the data
        """
        try:
            file_path = self.data_path / filename
            logger.info(f"Loading data from {file_path}")
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def load_psl_dataset(self) -> pd.DataFrame:
        """
        Load PSL dataset specifically
        
        Returns:
            DataFrame containing PSL data
        """
        return self.load_csv("Psl_Complete_Dataset(2016-2024).csv")
    
    def get_data_info(self, df: pd.DataFrame) -> dict:
        """
        Get basic information about the dataset
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with dataset information
        """
        info = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum()
        }
        return info


if __name__ == "__main__":
    # Example usage
    loader = DataLoader()
    df = loader.load_psl_dataset()
    info = loader.get_data_info(df)
    print(f"Dataset shape: {info['shape']}")
    print(f"Columns: {info['columns']}")
