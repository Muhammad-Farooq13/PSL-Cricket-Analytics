"""
Data Visualization Module
Create visualizations for data analysis and model results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
from typing import List, Optional, Tuple

# Setup logging and style
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


class DataVisualizer:
    """Class to handle data visualization operations"""
    
    def __init__(self, output_dir: str = "reports/figures"):
        """
        Initialize DataVisualizer
        
        Args:
            output_dir: Directory to save visualization outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def plot_distribution(self, 
                         df: pd.DataFrame, 
                         columns: List[str],
                         save_name: Optional[str] = None) -> None:
        """
        Plot distributions of numerical columns
        
        Args:
            df: Input DataFrame
            columns: List of columns to plot
            save_name: Optional filename to save plot
        """
        logger.info(f"Plotting distributions for {len(columns)} columns")
        
        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 4*n_rows))
        axes = axes.flatten() if len(columns) > 1 else [axes]
        
        for idx, col in enumerate(columns):
            if col in df.columns:
                df[col].hist(bins=30, ax=axes[idx], edgecolor='black')
                axes[idx].set_title(f'Distribution of {col}')
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Frequency')
        
        # Hide unused subplots
        for idx in range(len(columns), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_name:
            save_path = self.output_dir / save_name
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_correlation_matrix(self, 
                               df: pd.DataFrame,
                               save_name: Optional[str] = None) -> None:
        """
        Plot correlation matrix heatmap
        
        Args:
            df: Input DataFrame
            save_name: Optional filename to save plot
        """
        logger.info("Creating correlation matrix")
        
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            logger.warning("No numeric columns found for correlation matrix")
            return
        
        plt.figure(figsize=(12, 10))
        correlation = numeric_df.corr()
        
        sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=1)
        plt.title('Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_name:
            save_path = self.output_dir / save_name
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_categorical_counts(self,
                               df: pd.DataFrame,
                               columns: List[str],
                               save_name: Optional[str] = None) -> None:
        """
        Plot count plots for categorical columns
        
        Args:
            df: Input DataFrame
            columns: List of categorical columns to plot
            save_name: Optional filename to save plot
        """
        logger.info(f"Plotting categorical counts for {len(columns)} columns")
        
        n_cols = min(2, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(7*n_cols, 5*n_rows))
        axes = axes.flatten() if len(columns) > 1 else [axes]
        
        for idx, col in enumerate(columns):
            if col in df.columns:
                value_counts = df[col].value_counts()
                axes[idx].bar(range(len(value_counts)), value_counts.values)
                axes[idx].set_title(f'Count Plot of {col}')
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Count')
                axes[idx].set_xticks(range(len(value_counts)))
                axes[idx].set_xticklabels(value_counts.index, rotation=45, ha='right')
        
        # Hide unused subplots
        for idx in range(len(columns), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_name:
            save_path = self.output_dir / save_name
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_feature_importance(self,
                               importance_df: pd.DataFrame,
                               top_n: int = 20,
                               save_name: Optional[str] = None) -> None:
        """
        Plot feature importance
        
        Args:
            importance_df: DataFrame with 'feature' and 'importance' columns
            top_n: Number of top features to display
            save_name: Optional filename to save plot
        """
        logger.info(f"Plotting top {top_n} feature importances")
        
        top_features = importance_df.head(top_n)
        
        plt.figure(figsize=(10, max(6, top_n * 0.3)))
        plt.barh(range(len(top_features)), top_features['importance'].values)
        plt.yticks(range(len(top_features)), top_features['feature'].values)
        plt.xlabel('Importance')
        plt.title(f'Top {top_n} Feature Importances', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        if save_name:
            save_path = self.output_dir / save_name
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_confusion_matrix(self,
                             y_true: np.ndarray,
                             y_pred: np.ndarray,
                             labels: Optional[List] = None,
                             save_name: Optional[str] = None) -> None:
        """
        Plot confusion matrix
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            labels: Class labels
            save_name: Optional filename to save plot
        """
        from sklearn.metrics import confusion_matrix
        
        logger.info("Creating confusion matrix plot")
        
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=labels, yticklabels=labels)
        plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        if save_name:
            save_path = self.output_dir / save_name
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_roc_curve(self,
                      y_true: np.ndarray,
                      y_pred_proba: np.ndarray,
                      save_name: Optional[str] = None) -> None:
        """
        Plot ROC curve
        
        Args:
            y_true: True labels
            y_pred_proba: Predicted probabilities
            save_name: Optional filename to save plot
        """
        from sklearn.metrics import roc_curve, auc
        
        logger.info("Creating ROC curve")
        
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        if save_name:
            save_path = self.output_dir / save_name
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        plt.show()


if __name__ == "__main__":
    # Example usage
    visualizer = DataVisualizer()
    logger.info("Visualization module loaded")
