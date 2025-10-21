#!/usr/bin/env python3
"""
Multi-Key API Manager for Group Project
=======================================
Automatically rotates between multiple API keys to maximize usage limits.
"""

import os
import random
import time
from typing import List, Optional, Dict
from dotenv import load_dotenv

class MultiKeyManager:
    """Manages multiple API keys for the same service with automatic rotation"""
    
    def __init__(self):
        load_dotenv()
        self.key_usage = {}  # Track usage per key
        self.key_errors = {}  # Track errors per key
        self.last_key_used = {}  # Track last used key per service
        
    def get_keys_for_service(self, service_name: str) -> List[str]:
        """Get all available keys for a service"""
        keys = []
        
        # Handle special naming patterns
        if service_name == 'NEWS_API':
            key_pattern = 'NEWS_API_KEY'
        elif service_name == 'YOUTUBE':
            key_pattern = 'YOUTUBE_API_KEY'
        elif service_name == 'ALPHA_VANTAGE':
            key_pattern = 'ALPHA_VANTAGE_API_KEY'
        elif service_name == 'FRED':
            key_pattern = 'FRED_API_KEY'
        elif service_name == 'SERP_API':
            key_pattern = 'SERP_API_KEY'
        else:
            key_pattern = f"{service_name}_API_KEY"
        
        # Look for numbered keys (multi-key setup)
        for i in range(1, 5):  # Support up to 4 keys per service
            key = os.getenv(f"{key_pattern}_{i}")
            if key and key != f"your_group_member_{i}_{service_name.lower()}_key_here":
                keys.append(key)
        
        # Fallback to single key format if multi-key not found
        if not keys:
            single_key = os.getenv(key_pattern)
            if single_key and not single_key.startswith('your_'):
                keys.append(single_key)
                
        return keys
    
    def get_best_key(self, service_name: str, strategy: str = "round_robin") -> Optional[str]:
        """
        Get the best available key for a service
        
        Strategies:
        - round_robin: Rotate through keys sequentially
        - random: Pick a random key
        - least_used: Use the key with least usage
        - avoid_errors: Avoid keys that recently had errors
        """
        keys = self.get_keys_for_service(service_name)
        if not keys:
            return None
            
        if len(keys) == 1:
            return keys[0]
            
        if strategy == "round_robin":
            last_index = self.last_key_used.get(service_name, -1)
            next_index = (last_index + 1) % len(keys)
            self.last_key_used[service_name] = next_index
            return keys[next_index]
            
        elif strategy == "random":
            return random.choice(keys)
            
        elif strategy == "least_used":
            # Find key with minimum usage
            min_usage = float('inf')
            best_key = keys[0]
            for key in keys:
                usage = self.key_usage.get(key, 0)
                if usage < min_usage:
                    min_usage = usage
                    best_key = key
            return best_key
            
        elif strategy == "avoid_errors":
            # Prefer keys without recent errors
            good_keys = [k for k in keys if self.key_errors.get(k, 0) == 0]
            if good_keys:
                return random.choice(good_keys)
            else:
                return random.choice(keys)  # All keys have errors, pick any
                
        return keys[0]  # Default fallback
    
    def record_usage(self, key: str, success: bool = True):
        """Record usage and success/failure for a key"""
        if key not in self.key_usage:
            self.key_usage[key] = 0
        if key not in self.key_errors:
            self.key_errors[key] = 0
            
        self.key_usage[key] += 1
        if not success:
            self.key_errors[key] += 1
    
    def get_usage_stats(self) -> Dict[str, Dict]:
        """Get usage statistics for all keys"""
        stats = {}
        for key in list(self.key_usage.keys()) + list(self.key_errors.keys()):
            stats[key[:20] + "..."] = {
                'usage': self.key_usage.get(key, 0),
                'errors': self.key_errors.get(key, 0),
                'success_rate': self._calculate_success_rate(key)
            }
        return stats
    
    def _calculate_success_rate(self, key: str) -> float:
        """Calculate success rate for a key"""
        usage = self.key_usage.get(key, 0)
        errors = self.key_errors.get(key, 0)
        if usage == 0:
            return 100.0
        return ((usage - errors) / usage) * 100
    
    def get_service_summary(self) -> Dict[str, Dict]:
        """Get summary of available keys per service"""
        services = ['ALPHA_VANTAGE', 'FRED', 'NEWS_API', 'YOUTUBE', 'SERP_API']
        summary = {}
        
        for service in services:
            keys = self.get_keys_for_service(service)
            summary[service] = {
                'total_keys': len(keys),
                'available_keys': [k[:20] + "..." for k in keys],
                'estimated_daily_limit': self._get_estimated_limit(service, len(keys))
            }
            
        return summary
    
    def _get_estimated_limit(self, service: str, key_count: int) -> str:
        """Estimate total daily limits based on service and key count"""
        limits = {
            'ALPHA_VANTAGE': 25,     # requests per day
            'FRED': 120,             # requests per minute (practically unlimited daily)
            'NEWS_API': 100,         # requests per day  
            'YOUTUBE': 10000,        # requests per day
            'SERP_API': 3.3          # ~100 per month = 3.3 per day
        }
        
        base_limit = limits.get(service, 100)
        total_limit = base_limit * key_count
        
        if service == 'FRED':
            return f"{total_limit * 60 * 24:,} requests/day (practically unlimited)"
        elif service == 'SERP_API':
            return f"{total_limit:.0f} searches/day ({total_limit * 30:.0f}/month)"
        else:
            return f"{total_limit:,} requests/day"


# Global instance for easy use
multi_key_manager = MultiKeyManager()


def get_api_key(service_name: str, strategy: str = "round_robin") -> Optional[str]:
    """
    Convenience function to get the best API key for a service
    
    Usage:
        youtube_key = get_api_key('YOUTUBE')
        news_key = get_api_key('NEWS_API', strategy='least_used')
    """
    return multi_key_manager.get_best_key(service_name, strategy)


def record_api_usage(key: str, success: bool = True):
    """
    Convenience function to record API usage
    
    Usage:
        record_api_usage(youtube_key, success=True)
        record_api_usage(news_key, success=False)  # If API call failed
    """
    multi_key_manager.record_usage(key, success)


if __name__ == "__main__":
    # Test the multi-key manager
    print("🔄 MULTI-KEY API MANAGER TEST")
    print("=" * 50)
    
    manager = MultiKeyManager()
    
    # Show service summary
    print("\n📊 SERVICE SUMMARY:")
    summary = manager.get_service_summary()
    for service, info in summary.items():
        print(f"\n{service}:")
        print(f"  Keys available: {info['total_keys']}")
        print(f"  Estimated limit: {info['estimated_daily_limit']}")
        if info['available_keys']:
            print(f"  Keys: {', '.join(info['available_keys'])}")
    
    # Test key rotation
    print(f"\n🔄 KEY ROTATION TEST:")
    print("Testing YouTube API key rotation:")
    for i in range(3):
        key = get_api_key('YOUTUBE')
        if key:
            print(f"  Request {i+1}: {key[:20]}...")
            record_api_usage(key, success=True)
        else:
            print(f"  Request {i+1}: No key available")
    
    # Show usage stats
    print(f"\n📈 USAGE STATISTICS:")
    stats = manager.get_usage_stats()
    for key_preview, stat in stats.items():
        print(f"  {key_preview}: {stat['usage']} uses, {stat['success_rate']:.1f}% success")
    
    print("\n✅ Multi-key manager ready for group project!")