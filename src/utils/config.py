"""
Configuration Helper Module
Load and manage configuration settings
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Class to manage configuration files"""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize ConfigManager
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config = {}
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file
        
        Args:
            filename: JSON config file name
            
        Returns:
            Dictionary with configuration
        """
        config_path = self.config_dir / filename
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        return self.config
    
    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file
        
        Args:
            filename: YAML config file name
            
        Returns:
            Dictionary with configuration
        """
        config_path = self.config_dir / filename
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        return self.config
    
    def save_json(self, config: Dict[str, Any], filename: str) -> None:
        """
        Save configuration to JSON file
        
        Args:
            config: Configuration dictionary
            filename: Output filename
        """
        config_path = self.config_dir / filename
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
    
    def save_yaml(self, config: Dict[str, Any], filename: str) -> None:
        """
        Save configuration to YAML file
        
        Args:
            config: Configuration dictionary
            filename: Output filename
        """
        config_path = self.config_dir / filename
        
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
