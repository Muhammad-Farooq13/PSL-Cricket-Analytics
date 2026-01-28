"""
Helper Utilities Module
General utility functions for the project
"""

import os
import json
import pickle
from pathlib import Path
from typing import Any, Dict, List
import numpy as np


def save_pickle(obj: Any, filepath: str) -> None:
    """
    Save object to pickle file
    
    Args:
        obj: Object to save
        filepath: Output file path
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def load_pickle(filepath: str) -> Any:
    """
    Load object from pickle file
    
    Args:
        filepath: Input file path
        
    Returns:
        Loaded object
    """
    with open(filepath, 'rb') as f:
        return pickle.load(f)


def save_json(data: Dict, filepath: str, indent: int = 4) -> None:
    """
    Save dictionary to JSON file
    
    Args:
        data: Dictionary to save
        filepath: Output file path
        indent: JSON indentation
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def load_json(filepath: str) -> Dict:
    """
    Load dictionary from JSON file
    
    Args:
        filepath: Input file path
        
    Returns:
        Loaded dictionary
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def ensure_dir(directory: str) -> Path:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Directory path
        
    Returns:
        Path object
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_project_root() -> Path:
    """
    Get the project root directory
    
    Returns:
        Path to project root
    """
    return Path(__file__).parent.parent.parent


def list_files(directory: str, extension: str = None) -> List[Path]:
    """
    List all files in a directory
    
    Args:
        directory: Directory path
        extension: File extension filter (e.g., '.csv')
        
    Returns:
        List of file paths
    """
    dir_path = Path(directory)
    
    if extension:
        return list(dir_path.glob(f'*{extension}'))
    else:
        return [f for f in dir_path.iterdir() if f.is_file()]


def memory_usage_mb(obj: Any) -> float:
    """
    Calculate memory usage of an object in MB
    
    Args:
        obj: Object to measure
        
    Returns:
        Memory usage in MB
    """
    import sys
    return sys.getsizeof(obj) / (1024 * 1024)


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder for numpy types"""
    
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)
