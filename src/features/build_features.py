"""
Feature Engineering Module
Create and transform features for machine learning models
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Optional
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Class to handle feature engineering operations"""
    
    def __init__(self):
        """Initialize FeatureEngineer"""
        self.created_features = []
        
    def create_datetime_features(self, 
                                 df: pd.DataFrame, 
                                 date_column: str) -> pd.DataFrame:
        """
        Create datetime-based features from a date column
        
        Args:
            df: Input DataFrame
            date_column: Name of the date column
            
        Returns:
            DataFrame with new datetime features
        """
        df_copy = df.copy()
        
        try:
            logger.info(f"Creating datetime features from {date_column}")
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            
            df_copy[f'{date_column}_year'] = df_copy[date_column].dt.year
            df_copy[f'{date_column}_month'] = df_copy[date_column].dt.month
            df_copy[f'{date_column}_day'] = df_copy[date_column].dt.day
            df_copy[f'{date_column}_dayofweek'] = df_copy[date_column].dt.dayofweek
            df_copy[f'{date_column}_quarter'] = df_copy[date_column].dt.quarter
            df_copy[f'{date_column}_is_weekend'] = df_copy[date_column].dt.dayofweek.isin([5, 6]).astype(int)
            
            self.created_features.extend([
                f'{date_column}_year', f'{date_column}_month', f'{date_column}_day',
                f'{date_column}_dayofweek', f'{date_column}_quarter', f'{date_column}_is_weekend'
            ])
            
            logger.info(f"Created {len(self.created_features)} datetime features")
        except Exception as e:
            logger.error(f"Error creating datetime features: {str(e)}")
            raise
            
        return df_copy
    
    def create_aggregation_features(self, 
                                   df: pd.DataFrame,
                                   group_columns: List[str],
                                   agg_column: str,
                                   agg_functions: List[str] = ['mean', 'sum', 'std']) -> pd.DataFrame:
        """
        Create aggregation-based features
        
        Args:
            df: Input DataFrame
            group_columns: Columns to group by
            agg_column: Column to aggregate
            agg_functions: List of aggregation functions
            
        Returns:
            DataFrame with aggregation features
        """
        df_copy = df.copy()
        
        try:
            logger.info(f"Creating aggregation features for {agg_column} grouped by {group_columns}")
            
            for func in agg_functions:
                feature_name = f"{agg_column}_{'_'.join(group_columns)}_{func}"
                grouped = df_copy.groupby(group_columns)[agg_column].transform(func)
                df_copy[feature_name] = grouped
                self.created_features.append(feature_name)
                
            logger.info(f"Created {len(agg_functions)} aggregation features")
        except Exception as e:
            logger.error(f"Error creating aggregation features: {str(e)}")
            raise
            
        return df_copy
    
    def create_interaction_features(self,
                                   df: pd.DataFrame,
                                   feature_pairs: List[tuple]) -> pd.DataFrame:
        """
        Create interaction features between feature pairs
        
        Args:
            df: Input DataFrame
            feature_pairs: List of tuples containing feature pairs
            
        Returns:
            DataFrame with interaction features
        """
        df_copy = df.copy()
        
        try:
            logger.info(f"Creating interaction features for {len(feature_pairs)} pairs")
            
            for feat1, feat2 in feature_pairs:
                if feat1 in df_copy.columns and feat2 in df_copy.columns:
                    # Multiplication interaction
                    feature_name = f"{feat1}_x_{feat2}"
                    df_copy[feature_name] = df_copy[feat1] * df_copy[feat2]
                    self.created_features.append(feature_name)
                    
                    # Division interaction (if no zeros)
                    if (df_copy[feat2] != 0).all():
                        feature_name_div = f"{feat1}_div_{feat2}"
                        df_copy[feature_name_div] = df_copy[feat1] / df_copy[feat2]
                        self.created_features.append(feature_name_div)
                        
            logger.info(f"Created interaction features")
        except Exception as e:
            logger.error(f"Error creating interaction features: {str(e)}")
            raise
            
        return df_copy
    
    def create_binning_features(self,
                               df: pd.DataFrame,
                               column: str,
                               bins: int = 5,
                               labels: Optional[List] = None) -> pd.DataFrame:
        """
        Create binned versions of continuous features
        
        Args:
            df: Input DataFrame
            column: Column to bin
            bins: Number of bins or list of bin edges
            labels: Labels for bins
            
        Returns:
            DataFrame with binned feature
        """
        df_copy = df.copy()
        
        try:
            logger.info(f"Creating binned feature for {column}")
            feature_name = f"{column}_binned"
            df_copy[feature_name] = pd.cut(df_copy[column], bins=bins, labels=labels)
            self.created_features.append(feature_name)
            logger.info(f"Created binned feature: {feature_name}")
        except Exception as e:
            logger.error(f"Error creating binned feature: {str(e)}")
            raise
            
        return df_copy
    
    def create_polynomial_features(self,
                                  df: pd.DataFrame,
                                  columns: List[str],
                                  degree: int = 2) -> pd.DataFrame:
        """
        Create polynomial features
        
        Args:
            df: Input DataFrame
            columns: Columns to create polynomial features from
            degree: Degree of polynomial
            
        Returns:
            DataFrame with polynomial features
        """
        df_copy = df.copy()
        
        try:
            logger.info(f"Creating polynomial features of degree {degree}")
            
            for col in columns:
                if col in df_copy.columns:
                    for d in range(2, degree + 1):
                        feature_name = f"{col}_pow_{d}"
                        df_copy[feature_name] = df_copy[col] ** d
                        self.created_features.append(feature_name)
                        
            logger.info(f"Created polynomial features")
        except Exception as e:
            logger.error(f"Error creating polynomial features: {str(e)}")
            raise
            
        return df_copy
    
    def get_created_features(self) -> List[str]:
        """
        Get list of all created features
        
        Returns:
            List of feature names
        """
        return self.created_features


if __name__ == "__main__":
    # Example usage
    from src.data.load_data import DataLoader
    
    loader = DataLoader()
    engineer = FeatureEngineer()
    
    # Load data
    df = loader.load_psl_dataset()
    
    # Create features (example)
    # df = engineer.create_datetime_features(df, 'date_column')
    
    print(f"Created features: {engineer.get_created_features()}")
