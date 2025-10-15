"""
API Key Manager for Samsung Product Launch Planner
Handles secure loading and management of API keys
"""
import os
from typing import Dict, Optional, Any
import json
from dataclasses import dataclass
from datetime import datetime, timedelta

# Try to load python-dotenv for .env file support
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("💡 Tip: Install python-dotenv to use .env files: pip install python-dotenv")

@dataclass
class APIConfig:
    """Configuration for an API"""
    name: str
    base_url: str
    api_key: Optional[str]
    rate_limit: int  # requests per minute
    timeout: int = 30
    enabled: bool = True

class APIKeyManager:
    """Manages API keys and configurations securely"""
    
    def __init__(self):
        self.apis = {}
        self.load_api_configs()
    
    def load_api_configs(self):
        """Load API configurations from environment variables and config file"""
        
        # Load from config.json first (fallback values)
        self.load_from_config_file()
        
        # Override with environment variables (more secure)
        self.load_from_environment()
    
    def load_from_config_file(self):
        """Load API configs from config.json file"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
                api_keys = config.get('api_keys', {})
                rate_limits = config.get('rate_limits', {})
                
                # Define API configurations
                api_configs = {
                    'alpha_vantage': {
                        'name': 'Alpha Vantage',
                        'base_url': 'https://www.alphavantage.co/query',
                        'key_env': 'ALPHA_VANTAGE_API_KEY',
                        'rate_limit': rate_limits.get('alpha_vantage', 5)
                    },
                    'news_api': {
                        'name': 'News API',
                        'base_url': 'https://newsapi.org/v2',
                        'key_env': 'NEWS_API_KEY',
                        'rate_limit': rate_limits.get('news_api', 16)
                    },
                    'twitter': {
                        'name': 'Twitter API v2',
                        'base_url': 'https://api.twitter.com/2',
                        'key_env': 'TWITTER_BEARER_TOKEN',
                        'rate_limit': rate_limits.get('twitter', 300)
                    },
                    'reddit': {
                        'name': 'Reddit API',
                        'base_url': 'https://www.reddit.com',
                        'key_env': 'REDDIT_CLIENT_ID',
                        'rate_limit': rate_limits.get('reddit', 60)
                    },
                    'fred': {
                        'name': 'FRED Economic Data',
                        'base_url': 'https://api.stlouisfed.org/fred',
                        'key_env': 'FRED_API_KEY',
                        'rate_limit': rate_limits.get('fred', 120)
                    },
                    'rapidapi': {
                        'name': 'RapidAPI',
                        'base_url': 'https://rapidapi.com',
                        'key_env': 'RAPIDAPI_KEY',
                        'rate_limit': rate_limits.get('rapidapi', 100)
                    }
                }
                
                for api_id, config in api_configs.items():
                    api_key = api_keys.get(api_id, '')
                    self.apis[api_id] = APIConfig(
                        name=config['name'],
                        base_url=config['base_url'],
                        api_key=api_key if api_key and api_key != f"YOUR_{config['key_env']}" else None,
                        rate_limit=config['rate_limit'],
                        enabled=bool(api_key and api_key != f"YOUR_{config['key_env']}")
                    )
                    
        except Exception as e:
            print(f"Warning: Could not load config.json: {e}")
    
    def load_from_environment(self):
        """Load API keys from environment variables (overrides config.json)"""
        env_configs = {
            'alpha_vantage': {
                'name': 'Alpha Vantage',
                'base_url': 'https://www.alphavantage.co/query',
                'key_env': 'ALPHA_VANTAGE_API_KEY',
                'rate_limit': int(os.getenv('ALPHA_VANTAGE_RATE_LIMIT', '5'))
            },
            'news_api': {
                'name': 'News API',
                'base_url': 'https://newsapi.org/v2',
                'key_env': 'NEWS_API_KEY',
                'rate_limit': int(os.getenv('NEWS_API_RATE_LIMIT', '16'))
            },
            'twitter': {
                'name': 'Twitter API v2',
                'base_url': 'https://api.twitter.com/2',
                'key_env': 'TWITTER_BEARER_TOKEN',
                'rate_limit': int(os.getenv('TWITTER_RATE_LIMIT', '300'))
            },
            'reddit': {
                'name': 'Reddit API',
                'base_url': 'https://www.reddit.com',
                'key_env': 'REDDIT_CLIENT_ID',
                'rate_limit': int(os.getenv('REDDIT_RATE_LIMIT', '60'))
            },
            'fred': {
                'name': 'FRED Economic Data',
                'base_url': 'https://api.stlouisfed.org/fred',
                'key_env': 'FRED_API_KEY',
                'rate_limit': int(os.getenv('FRED_RATE_LIMIT', '120'))
            },
            'rapidapi': {
                'name': 'RapidAPI',
                'base_url': 'https://rapidapi.com',
                'key_env': 'RAPIDAPI_KEY',
                'rate_limit': int(os.getenv('RAPIDAPI_RATE_LIMIT', '100'))
            },
            'facebook': {
                'name': 'Facebook Graph API',
                'base_url': 'https://graph.facebook.com',
                'key_env': 'FACEBOOK_ACCESS_TOKEN',
                'rate_limit': int(os.getenv('FACEBOOK_RATE_LIMIT', '200'))
            },
            'youtube': {
                'name': 'YouTube Data API',
                'base_url': 'https://www.googleapis.com/youtube/v3',
                'key_env': 'YOUTUBE_API_KEY',
                'rate_limit': int(os.getenv('YOUTUBE_RATE_LIMIT', '100'))
            }
        }
        
        for api_id, config in env_configs.items():
            api_key = os.getenv(config['key_env'])
            
            if api_key:
                # Override or create new API config
                self.apis[api_id] = APIConfig(
                    name=config['name'],
                    base_url=config['base_url'],
                    api_key=api_key,
                    rate_limit=config['rate_limit'],
                    timeout=int(os.getenv('API_TIMEOUT', '30')),
                    enabled=True
                )
    
    def get_api_key(self, api_name: str) -> Optional[str]:
        """Get API key for a specific API"""
        api_config = self.apis.get(api_name)
        if api_config and api_config.enabled:
            return api_config.api_key
        return None
    
    def get_api_config(self, api_name: str) -> Optional[APIConfig]:
        """Get full API configuration"""
        return self.apis.get(api_name)
    
    def is_api_enabled(self, api_name: str) -> bool:
        """Check if an API is enabled and has a valid key"""
        api_config = self.apis.get(api_name)
        return api_config is not None and api_config.enabled and api_config.api_key is not None
    
    def is_any_api_enabled(self) -> bool:
        """Check if any API is enabled"""
        return any(config.enabled and config.api_key for config in self.apis.values())
    
    def get_enabled_apis(self) -> Dict[str, APIConfig]:
        """Get all enabled APIs"""
        return {name: config for name, config in self.apis.items() if config.enabled}
    
    def get_api_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all APIs"""
        status = {}
        for api_id, config in self.apis.items():
            status[api_id] = {
                'name': config.name,
                'enabled': config.enabled,
                'has_key': config.api_key is not None,
                'rate_limit': config.rate_limit,
                'base_url': config.base_url
            }
        return status
    
    def validate_api_key(self, api_name: str) -> bool:
        """Validate an API key by making a test request"""
        import requests
        
        api_config = self.get_api_config(api_name)
        if not api_config or not api_config.api_key:
            return False
        
        try:
            # Define test endpoints for each API
            test_endpoints = {
                'alpha_vantage': f"{api_config.base_url}?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={api_config.api_key}",
                'news_api': f"{api_config.base_url}/everything?q=test&apiKey={api_config.api_key}",
                'fred': f"{api_config.base_url}/series?series_id=GDP&api_key={api_config.api_key}&file_type=json",
            }
            
            test_url = test_endpoints.get(api_name)
            if not test_url:
                return True  # Can't test, assume valid
            
            response = requests.get(test_url, timeout=api_config.timeout)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Warning: Could not validate {api_name} API key: {e}")
            return False
    
    def print_api_status(self):
        """Print status of all APIs"""
        print("\n🔑 API Configuration Status")
        print("=" * 50)
        
        for api_id, config in self.apis.items():
            status_icon = "✅" if config.enabled else "❌"
            key_status = "🔑" if config.api_key else "🚫"
            
            print(f"{status_icon} {config.name}")
            print(f"   {key_status} API Key: {'Configured' if config.api_key else 'Missing'}")
            print(f"   📊 Rate Limit: {config.rate_limit}/min")
            print(f"   🌐 Enabled: {config.enabled}")
            print()

# Global API manager instance
api_manager = APIKeyManager()

# Helper functions for easy access
def get_api_key(api_name: str) -> Optional[str]:
    """Get API key for a specific API"""
    return api_manager.get_api_key(api_name)

def is_api_enabled(api_name: str) -> bool:
    """Check if an API is enabled"""
    return api_manager.is_api_enabled(api_name)

def get_api_config(api_name: str) -> Optional[APIConfig]:
    """Get API configuration"""
    return api_manager.get_api_config(api_name)