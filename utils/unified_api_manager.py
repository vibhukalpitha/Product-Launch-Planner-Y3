"""
Unified API Key Manager - Fixes the Multi-Location Key Problem
============================================================
This fixes the chaos of having API keys in multiple places:
- config.json
- .env files  
- environment variables
- multi-key configurations

Creates ONE source of truth with proper priority order.
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

# Try to load python-dotenv
try:
    from dotenv import load_dotenv
    # Load ALL .env files
    load_dotenv('.env')
    load_dotenv('.env.example')  # Fallback
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

@dataclass
class APIKey:
    """Represents a single API key with metadata"""
    key: str
    source: str
    service: str
    key_index: int = 0
    usage_count: int = 0
    error_count: int = 0
    is_active: bool = True

class UnifiedAPIManager:
    """Unified API key manager with clear priority order"""
    
    def __init__(self):
        self.api_keys: Dict[str, List[APIKey]] = {}
        self.load_order = [
            "environment_variables",  # Highest priority
            "dotenv_file",           # Second priority  
            "config_json"            # Lowest priority
        ]
        self.load_all_keys()
    
    def load_all_keys(self):
        """Load keys from all sources in priority order"""
        print("🔧 UNIFIED API KEY MANAGER - Loading keys...")
        
        # Initialize key storage
        self.api_keys = {}
        
        # Load from each source in priority order
        for source in self.load_order:
            if source == "environment_variables":
                self._load_from_environment()
            elif source == "dotenv_file":
                self._load_from_dotenv()
            elif source == "config_json":
                self._load_from_config()
    
    def _load_from_environment(self):
        """Load keys from environment variables (highest priority)"""
        print("📊 Loading from environment variables...")
        
        # Define services we're looking for
        services = [
            'NEWS_API', 'YOUTUBE', 'FRED', 'ALPHA_VANTAGE', 'SERP_API', 'CENSUS', 'TWITTER',
            'REDDIT', 'FACEBOOK', 'FACEBOOK_MARKETING', 'INSTAGRAM', 'BING_SEARCH', 'RAPIDAPI', 'SCRAPERAPI',
            'OPENWEATHER', 'EXCHANGE_RATES', 'AMAZON', 'EBAY', 'GOOGLE_ANALYTICS'
        ]
        
        for service in services:
            service_keys = []
            
            # Look for multi-key format: SERVICE_API_KEY_1, SERVICE_API_KEY_2, etc.
            for i in range(1, 10):  # Support up to 9 keys
                key_name = f"{service}_API_KEY_{i}"
                key_value = os.getenv(key_name)
                
                if key_value and not key_value.startswith('your_'):
                    service_keys.append(APIKey(
                        key=key_value,
                        source="environment",
                        service=service,
                        key_index=i
                    ))
                    print(f"  ✅ Found {key_name}: {key_value[:20]}...")
            
            # Look for single key format: SERVICE_API_KEY
            single_key_name = f"{service}_API_KEY"
            single_key_value = os.getenv(single_key_name)
            
            if single_key_value and not single_key_value.startswith('your_'):
                service_keys.append(APIKey(
                    key=single_key_value,
                    source="environment",
                    service=service,
                    key_index=0
                ))
                print(f"  ✅ Found {single_key_name}: {single_key_value[:20]}...")
            
            # Look for alternative patterns: SERVICE_KEY, SERVICE_TOKEN, etc.
            alternative_patterns = [f"{service}_KEY", f"{service}_TOKEN", f"{service}_BEARER_TOKEN"]
            for pattern in alternative_patterns:
                alt_key = os.getenv(pattern)
                if alt_key and not alt_key.startswith('your_'):
                    service_keys.append(APIKey(
                        key=alt_key,
                        source="environment",
                        service=service,
                        key_index=0
                    ))
                    print(f"  ✅ Found {pattern}: {alt_key[:20]}...")
            
            if service_keys:
                self.api_keys[service] = service_keys
    
    def _load_from_dotenv(self):
        """Load keys from .env file (medium priority)"""
        if not DOTENV_AVAILABLE:
            return
            
        print("📄 Loading from .env file...")
        # Environment variables are already loaded by load_dotenv()
        # This is handled by _load_from_environment()
    
    def _load_from_config(self):
        """Load keys from config.json (lowest priority)"""
        try:
            print("📋 Loading from config.json...")
            
            # Get the correct path to config.json relative to this file
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            api_keys = config.get('api_keys', {})
            
            # Map config keys to service names
            key_mapping = {
                'news_api': 'NEWS_API',
                'youtube_api': 'YOUTUBE', 
                'fred': 'FRED',
                'alpha_vantage': 'ALPHA_VANTAGE',
                'serp_api': 'SERP_API',
                'census_api': 'CENSUS',
                'twitter_bearer': 'TWITTER',
                'reddit_client_id': 'REDDIT',
                'reddit_client_secret': 'REDDIT_SECRET',  
                'world_bank': 'WORLD_BANK',
                'facebook_marketing': 'FACEBOOK_MARKETING',
                'facebook_access_token': 'FACEBOOK_MARKETING',
                'google_analytics': 'GOOGLE_ANALYTICS',
                'statista_api': 'STATISTA_API',
                'bing_search': 'BING_SEARCH',
                'amazon_api': 'AMAZON',
                'ebay_api': 'EBAY',
                'rapidapi': 'RAPIDAPI',
                'scraperapi': 'SCRAPERAPI'
            }
            
            for config_key, service in key_mapping.items():
                key_value = api_keys.get(config_key)
                
                if key_value and not key_value.startswith('YOUR_'):
                    # Only add if not already found from higher priority sources
                    if service not in self.api_keys:
                        self.api_keys[service] = []
                    
                    # Check if we already have this key from a higher priority source
                    existing_keys = [k.key for k in self.api_keys[service]]
                    if key_value not in existing_keys:
                        self.api_keys[service].append(APIKey(
                            key=key_value,
                            source="config.json",
                            service=service,
                            key_index=0
                        ))
                        print(f"  ✅ Found {config_key}: {key_value[:20]}...")
                        
        except Exception as e:
            print(f"⚠️ Error loading config.json: {e}")
    
    def get_working_key(self, service: str) -> Optional[APIKey]:
        """Get the next working key for a service (with rotation)"""
        service = service.upper()
        
        if service not in self.api_keys:
            print(f"❌ No keys found for service: {service}")
            return None
        
        keys = self.api_keys[service]
        active_keys = [k for k in keys if k.is_active]
        
        if not active_keys:
            print(f"❌ No active keys for service: {service}")
            return None
        
        # Simple round-robin rotation based on usage count
        best_key = min(active_keys, key=lambda k: k.usage_count)
        best_key.usage_count += 1
        
        print(f"🔑 Using {service} key #{best_key.key_index} from {best_key.source}")
        return best_key
    
    def mark_key_error(self, service: str, key: str):
        """Mark a key as having an error"""
        service = service.upper()
        
        if service in self.api_keys:
            for api_key in self.api_keys[service]:
                if api_key.key == key:
                    api_key.error_count += 1
                    if api_key.error_count >= 3:  # Disable after 3 errors
                        api_key.is_active = False
                        print(f"🚫 Disabled {service} key after 3 errors")
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get a comprehensive status report"""
        report = {}
        
        for service, keys in self.api_keys.items():
            active_keys = [k for k in keys if k.is_active]
            report[service] = {
                'total_keys': len(keys),
                'active_keys': len(active_keys),
                'keys_by_source': {}
            }
            
            # Group by source
            for key in keys:
                source = key.source
                if source not in report[service]['keys_by_source']:
                    report[service]['keys_by_source'][source] = 0
                report[service]['keys_by_source'][source] += 1
        
        return report
    
    def print_status(self):
        """Print a nice status report"""
        print("🎯 UNIFIED API KEY STATUS")
        print("=" * 40)
        
        for service, keys in self.api_keys.items():
            active_keys = [k for k in keys if k.is_active]
            print(f"\n📊 {service}:")
            print(f"  Total keys: {len(keys)}")
            print(f"  Active keys: {len(active_keys)}")
            
            for key in keys:
                status = "✅ Active" if key.is_active else "🚫 Disabled"
                print(f"    Key #{key.key_index} ({key.source}): {status}")

# Create global instance
unified_api_manager = UnifiedAPIManager()

# Convenience functions for backward compatibility
def get_api_key(service: str) -> Optional[str]:
    """Get an API key for a service with smart name mapping"""
    # Normalize service names to handle different naming patterns
    service_mappings = {
        'census': 'CENSUS',
        'census_api': 'CENSUS',
        'fred': 'FRED',
        'fred_api': 'FRED', 
        'facebook_marketing': 'FACEBOOK_MARKETING',
        'facebook': 'FACEBOOK_MARKETING',
        'statista_api': 'STATISTA_API',
        'statista': 'STATISTA_API',
        'world_bank': 'WORLD_BANK',
        'worldbank': 'WORLD_BANK',
        'google_analytics': 'GOOGLE_ANALYTICS',
        'google_analytics_key': 'GOOGLE_ANALYTICS',
        'youtube': 'YOUTUBE',
        'youtube_api': 'YOUTUBE',
        'news_api': 'NEWS_API',
        'news': 'NEWS_API',
        'serp_api': 'SERP_API',
        'serp': 'SERP_API',
        'twitter': 'TWITTER',
        'reddit': 'REDDIT',
        'alpha_vantage': 'ALPHA_VANTAGE',
        'bing_search': 'BING_SEARCH',
        'bing': 'BING_SEARCH'
    }
    
    # Try direct mapping first, then normalized mapping
    normalized_service = service_mappings.get(service.lower(), service.upper())
    key_obj = unified_api_manager.get_working_key(normalized_service)
    return key_obj.key if key_obj else None

def mark_key_failed(service: str, key: str):
    """Mark a key as failed"""
    unified_api_manager.mark_key_error(service, key)

if __name__ == "__main__":
    # Test the system
    unified_api_manager.print_status()