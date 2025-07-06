import json
from typing import Dict, Any, Optional
from pathlib import Path
from .exceptions import ConfigError

class ConfigManager:
    DEFAULT_CONFIG = {
        "max_retries": 5,
        "video_url": "",
        "wait_times": {
            "element_timeout": 10,
            "retry_delay": 15,
            "error_delay": 300
        },
        "ad_settings": {
            "max_attempts": 3,
            "check_timeout": 5
        },
        "browser_settings": {
            "headless": False,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    }

    @classmethod
    def load_config(cls, config_path: str = "config.json") -> Dict[str, Any]:
        try:
            config_file = Path(config_path)

            if not config_file.exists():
                cls.create_default_config(config_path)
                return cls.DEFAULT_CONFIG

            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)

            config = cls._deep_merge(cls.DEFAULT_CONFIG, user_config)
            cls._validate_config(config)

            return config

        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON format in config file: {str(e)}")
        except Exception as e:
            raise ConfigError(f"Failed to load config: {str(e)}")

    @classmethod
    def create_default_config(cls, config_path: str = "config.json"):
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(cls.DEFAULT_CONFIG, f, indent=4)
        except Exception as e:
            raise ConfigError(f"Failed to create default config: {str(e)}")

    @classmethod
    def get_setting(cls, config: Dict[str, Any], key_path: str, default: Optional[Any] = None) -> Any:
        try:
            keys = key_path.split('.')
            value = config
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            if default is not None:
                return default
            raise ConfigError(f"Config key not found: {key_path}")

    @staticmethod
    def _deep_merge(default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigManager._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    @staticmethod
    def _validate_config(config: Dict[str, Any]):
        if not isinstance(config.get("video_url"), str):
            raise ConfigError("video_url must be a string")

        if not isinstance(config.get("max_retries"), int) or config["max_retries"] < 0:
            raise ConfigError("max_retries must be a positive integer")

    @classmethod
    def update_config(cls, config_path: str = "config.json", **kwargs):
        try:
            current_config = cls.load_config(config_path)
            updated_config = {**current_config, **kwargs}

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(updated_config, f, indent=4)

            return updated_config
        except Exception as e:
            raise ConfigError(f"Failed to update config: {str(e)}")
