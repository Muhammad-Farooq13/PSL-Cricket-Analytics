"""
Logging Utility Module
Setup and configure logging for the project
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str, 
                log_file: str = None, 
                level=logging.INFO,
                log_dir: str = "logs") -> logging.Logger:
    """
    Setup a logger with console and file handlers
    
    Args:
        name: Logger name
        log_file: Log file name (if None, uses timestamp)
        level: Logging level
        log_dir: Directory to save log files
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        log_file = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_path / log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a basic one
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
