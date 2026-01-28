"""
Data Preprocessing Module
Handles data cleaning, transformation, and preprocessing
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Optional, Union
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Class to handle data preprocessing operations"""
    
    def __init__(self):
        """Initialize DataPreprocessor"""
        self.scalers = {}
        self.encoders = {}
        
    def handle_missing_values(self, 
                             df: pd.DataFrame, 
                             strategy: str = 'drop',
                             fill_value: Optional[Union[int, float, str]] = None) -> pd.DataFrame:
        """
        Handle missing values in the dataset
        
        Args:
            df: Input DataFrame
            strategy: Strategy to handle missing values ('drop', 'mean', 'median', 'mode', 'fill')
            fill_value: Value to fill if strategy is 'fill'
            
        Returns:
            DataFrame with missing values handled
        """
        df_copy = df.copy()
        
        if strategy == 'drop':
            logger.info("Dropping rows with missing values")
            df_copy = df_copy.dropna()
        elif strategy == 'mean':
            logger.info("Filling missing values with mean")
            numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
            df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].mean())
        elif strategy == 'median':
            logger.info("Filling missing values with median")
            numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
            df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].median())
        elif strategy == 'mode':
            logger.info("Filling missing values with mode")
            df_copy = df_copy.fillna(df_copy.mode().iloc[0])
        elif strategy == 'fill' and fill_value is not None:
            logger.info(f"Filling missing values with {fill_value}")
            df_copy = df_copy.fillna(fill_value)
        
        return df_copy
    
    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows from the dataset
        
        Args:
            df: Input DataFrame
            subset: Columns to consider for identifying duplicates
            
        Returns:
            DataFrame with duplicates removed
        """
        logger.info("Removing duplicate rows")
        df_copy = df.copy()
        before_count = len(df_copy)
        df_copy = df_copy.drop_duplicates(subset=subset, keep='first')
        after_count = len(df_copy)
        logger.info(f"Removed {before_count - after_count} duplicate rows")
        return df_copy
    
    def encode_categorical(self, 
                          df: pd.DataFrame, 
                          columns: List[str],
                          method: str = 'label') -> pd.DataFrame:
        """
        Encode categorical variables
        
        Args:
            df: Input DataFrame
            columns: List of categorical columns to encode
            method: Encoding method ('label' or 'onehot')
            
        Returns:
            DataFrame with encoded categorical variables
        """
        df_copy = df.copy()
        
        for col in columns:
            if col not in df_copy.columns:
                logger.warning(f"Column {col} not found in DataFrame")
                continue
                
            if method == 'label':
                logger.info(f"Label encoding column: {col}")
                if col not in self.encoders:
                    self.encoders[col] = LabelEncoder()
                    df_copy[col] = self.encoders[col].fit_transform(df_copy[col].astype(str))
                else:
                    df_copy[col] = self.encoders[col].transform(df_copy[col].astype(str))
            elif method == 'onehot':
                logger.info(f"One-hot encoding column: {col}")
                dummies = pd.get_dummies(df_copy[col], prefix=col, drop_first=True)
                df_copy = pd.concat([df_copy.drop(col, axis=1), dummies], axis=1)
        
        return df_copy
    
    def scale_features(self, 
                      df: pd.DataFrame, 
                      columns: List[str],
                      method: str = 'standard') -> pd.DataFrame:
        """
        Scale numerical features
        
        Args:
            df: Input DataFrame
            columns: List of columns to scale
            method: Scaling method ('standard' or 'minmax')
            
        Returns:
            DataFrame with scaled features
        """
        df_copy = df.copy()
        
        if method == 'standard':
            logger.info(f"Standardizing columns: {columns}")
            for col in columns:
                if col not in df_copy.columns:
                    logger.warning(f"Column {col} not found in DataFrame")
                    continue
                    
                if col not in self.scalers:
                    self.scalers[col] = StandardScaler()
                    df_copy[col] = self.scalers[col].fit_transform(df_copy[[col]])
                else:
                    df_copy[col] = self.scalers[col].transform(df_copy[[col]])
        
        return df_copy
    
    def save_processed_data(self, df: pd.DataFrame, filename: str, output_path: str = "data/processed"):
        """
        Save processed data to file
        
        Args:
            df: DataFrame to save
            filename: Output filename
            output_path: Output directory path
        """
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / filename
        
        logger.info(f"Saving processed data to {file_path}")
        df.to_csv(file_path, index=False)
        logger.info(f"Successfully saved {len(df)} rows")


if __name__ == "__main__":
    # Example usage
    from load_data import DataLoader
    
    loader = DataLoader()
    preprocessor = DataPreprocessor()
    
    # Load data
    df = loader.load_psl_dataset()
    
    # Preprocess
    df = preprocessor.handle_missing_values(df, strategy='drop')
    df = preprocessor.remove_duplicates(df)
    
    # Save processed data
    preprocessor.save_processed_data(df, "processed_data.csv")
