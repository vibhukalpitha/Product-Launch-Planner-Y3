"""
API Key Rotation Manager
Automatically rotates between multiple API keys when rate limits are hit
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json

@dataclass
class APIKeyStatus:
    """Track status of an individual API key"""
    key: str
    is_active: bool = True
    rate_limited_until: Optional[datetime] = None
    error_count: int = 0
    last_used: Optional[datetime] = None
    total_requests: int = 0
    
    def is_available(self) -> bool:
        """Check if key is available for use"""
        if not self.is_active:
            return False
        if self.rate_limited_until and datetime.now() < self.rate_limited_until:
            return False
        return True
    
    def mark_rate_limited(self, duration_hours: int = 24):
        """Mark key as rate limited"""
        self.rate_limited_until = datetime.now() + timedelta(hours=duration_hours)
        self.error_count += 1
        print(f"[RATE LIMIT] Key ending in ...{self.key[-4:]} rate limited until {self.rate_limited_until}")
    
    def mark_success(self):
        """Mark successful request"""
        self.last_used = datetime.now()
        self.total_requests += 1
        self.error_count = max(0, self.error_count - 1)  # Reduce error count on success


class APIKeyRotator:
    """Manages rotation of multiple API keys"""
    
    def __init__(self):
        self.api_keys: Dict[str, List[APIKeyStatus]] = {}
        self.current_index: Dict[str, int] = {}
        self.load_api_keys()
    
    def load_api_keys(self):
        """Load multiple API keys from environment variables"""
        
        # Define which APIs support multiple keys
        api_key_patterns = {
            'news_api': 'NEWS_API_KEY',
            'youtube': 'YOUTUBE_API_KEY',
            'serpapi': 'SERPAPI_KEY',
            'google_analytics': 'GOOGLE_ANALYTICS_API_KEY',
        }
        
        for api_name, key_prefix in api_key_patterns.items():
            keys = []
            
            # Load primary key
            primary_key = os.getenv(key_prefix)
            if primary_key:
                keys.append(APIKeyStatus(key=primary_key))
            
            # Load additional keys (KEY_1, KEY_2, etc.)
            i = 1
            while True:
                additional_key = os.getenv(f"{key_prefix}_{i}")
                if not additional_key:
                    break
                keys.append(APIKeyStatus(key=additional_key))
                i += 1
            
            if keys:
                self.api_keys[api_name] = keys
                self.current_index[api_name] = 0
                print(f"[API KEYS] Loaded {len(keys)} key(s) for {api_name}")
    
    def get_api_key(self, api_name: str) -> Optional[str]:
        """Get next available API key for the specified API"""
        
        if api_name not in self.api_keys:
            return None
        
        keys = self.api_keys[api_name]
        if not keys:
            return None
        
        # Try to find an available key
        for _ in range(len(keys)):
            current_idx = self.current_index[api_name]
            key_status = keys[current_idx]
            
            if key_status.is_available():
                # Found available key
                key_status.mark_success()
                return key_status.key
            
            # Move to next key
            self.current_index[api_name] = (current_idx + 1) % len(keys)
        
        # All keys are rate limited
        print(f"[WARNING] All keys for {api_name} are rate limited!")
        return None
    
    def mark_rate_limited(self, api_name: str, api_key: str, duration_hours: int = 24):
        """Mark a specific key as rate limited"""
        
        if api_name not in self.api_keys:
            return
        
        for key_status in self.api_keys[api_name]:
            if key_status.key == api_key:
                key_status.mark_rate_limited(duration_hours)
                
                # Automatically rotate to next key
                self.rotate_to_next(api_name)
                break
    
    def rotate_to_next(self, api_name: str):
        """Rotate to the next available key"""
        
        if api_name not in self.api_keys:
            return
        
        keys = self.api_keys[api_name]
        current_idx = self.current_index[api_name]
        
        # Find next available key
        for i in range(len(keys)):
            next_idx = (current_idx + i + 1) % len(keys)
            if keys[next_idx].is_available():
                self.current_index[api_name] = next_idx
                print(f"[ROTATION] Switched to key #{next_idx + 1} for {api_name}")
                return
        
        print(f"[WARNING] No available keys for {api_name}")
    
    def get_key_count(self, api_name: str) -> int:
        """Get total number of keys for an API"""
        return len(self.api_keys.get(api_name, []))
    
    def get_available_key_count(self, api_name: str) -> int:
        """Get number of available keys for an API"""
        if api_name not in self.api_keys:
            return 0
        return sum(1 for key in self.api_keys[api_name] if key.is_available())
    
    def get_status(self, api_name: str) -> Dict:
        """Get status of all keys for an API"""
        
        if api_name not in self.api_keys:
            return {"error": "API not found"}
        
        keys = self.api_keys[api_name]
        current_idx = self.current_index[api_name]
        
        status = {
            "total_keys": len(keys),
            "available_keys": self.get_available_key_count(api_name),
            "current_key_index": current_idx + 1,
            "keys": []
        }
        
        for i, key_status in enumerate(keys):
            key_info = {
                "index": i + 1,
                "key_preview": f"...{key_status.key[-4:]}",
                "is_active": key_status.is_active,
                "is_available": key_status.is_available(),
                "error_count": key_status.error_count,
                "total_requests": key_status.total_requests,
                "is_current": i == current_idx
            }
            
            if key_status.rate_limited_until:
                time_remaining = key_status.rate_limited_until - datetime.now()
                key_info["rate_limited_for"] = str(time_remaining).split('.')[0]
            
            status["keys"].append(key_info)
        
        return status
    
    def print_status(self):
        """Print status of all API keys"""
        
        print("\n[ROTATION] API Key Rotation Status")
        print("=" * 60)
        
        for api_name in self.api_keys.keys():
            status = self.get_status(api_name)
            
            print(f"\n[API] {api_name.upper()}")
            print(f"   Total Keys: {status['total_keys']}")
            print(f"   Available: {status['available_keys']}/{status['total_keys']}")
            print(f"   Current: Key #{status['current_key_index']}")
            
            for key_info in status['keys']:
                icon = "[OK]" if key_info['is_available'] else "[||]"
                current = "<- CURRENT" if key_info['is_current'] else ""
                
                print(f"   {icon} Key #{key_info['index']} ({key_info['key_preview']}) {current}")
                print(f"      Requests: {key_info['total_requests']} | Errors: {key_info['error_count']}")
                
                if 'rate_limited_for' in key_info:
                    print(f"      [TIME] Rate limited for: {key_info['rate_limited_for']}")
        
        print("=" * 60)


# Global rotator instance
api_key_rotator = APIKeyRotator()


# Helper functions
def get_rotated_api_key(api_name: str) -> Optional[str]:
    """Get next available API key with automatic rotation"""
    return api_key_rotator.get_api_key(api_name)


def handle_rate_limit(api_name: str, api_key: str, duration_hours: int = 24):
    """Handle rate limit error by marking key and rotating"""
    api_key_rotator.mark_rate_limited(api_name, api_key, duration_hours)


def get_api_key_status(api_name: str) -> Dict:
    """Get status of API keys"""
    return api_key_rotator.get_status(api_name)

