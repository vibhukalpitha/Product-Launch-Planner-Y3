"""
Google Trends Cache Manager
Caches Google Trends API responses for 24 hours to avoid rate limiting
"""

import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Any, Optional

class GoogleTrendsCache:
    """Simple file-based cache for Google Trends data"""
    
    def __init__(self, cache_dir: str = "cache", expiry_hours: int = 24):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
            expiry_hours: Cache expiry time in hours (default: 24)
        """
        self.cache_dir = cache_dir
        self.expiry_hours = expiry_hours
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            print(f"[CACHE] Created cache directory: {cache_dir}")
    
    def _get_cache_key(self, query_params: dict) -> str:
        """Generate unique cache key from query parameters"""
        # Sort dict for consistent hashing
        sorted_params = json.dumps(query_params, sort_keys=True)
        return hashlib.md5(sorted_params.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get file path for cache key"""
        return os.path.join(self.cache_dir, f"trends_{cache_key}.json")
    
    def get(self, query_params: dict) -> Optional[Any]:
        """
        Retrieve cached data if available and not expired
        
        Args:
            query_params: Dictionary of query parameters (e.g., product_name, country_code)
        
        Returns:
            Cached data if available and fresh, None otherwise
        """
        cache_key = self._get_cache_key(query_params)
        cache_path = self._get_cache_path(cache_key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check expiry
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            expiry_time = cached_time + timedelta(hours=self.expiry_hours)
            
            if datetime.now() < expiry_time:
                # Cache is still fresh
                time_left = expiry_time - datetime.now()
                hours_left = time_left.total_seconds() / 3600
                print(f"[CACHE] ✓ Using cached data (expires in {hours_left:.1f}h)")
                return cache_data['data']
            else:
                # Cache expired
                print(f"[CACHE] ✗ Cache expired, will fetch fresh data")
                # Delete expired cache file
                os.remove(cache_path)
                return None
                
        except Exception as e:
            print(f"[CACHE] Error reading cache: {e}")
            return None
    
    def set(self, query_params: dict, data: Any) -> None:
        """
        Store data in cache
        
        Args:
            query_params: Dictionary of query parameters
            data: Data to cache
        """
        cache_key = self._get_cache_key(query_params)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'query_params': query_params,
                'data': data
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            print(f"[CACHE] ✓ Cached data for {self.expiry_hours} hours")
            
        except Exception as e:
            print(f"[CACHE] Error writing cache: {e}")
    
    def clear_expired(self) -> int:
        """
        Clear all expired cache entries
        
        Returns:
            Number of cache entries cleared
        """
        cleared = 0
        
        try:
            for filename in os.listdir(self.cache_dir):
                if not filename.startswith('trends_') or not filename.endswith('.json'):
                    continue
                
                cache_path = os.path.join(self.cache_dir, filename)
                
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    cached_time = datetime.fromisoformat(cache_data['timestamp'])
                    expiry_time = cached_time + timedelta(hours=self.expiry_hours)
                    
                    if datetime.now() >= expiry_time:
                        os.remove(cache_path)
                        cleared += 1
                        
                except Exception as e:
                    print(f"[CACHE] Error processing {filename}: {e}")
                    
        except Exception as e:
            print(f"[CACHE] Error clearing cache: {e}")
        
        if cleared > 0:
            print(f"[CACHE] Cleared {cleared} expired cache entries")
        
        return cleared
    
    def clear_all(self) -> int:
        """
        Clear all cache entries
        
        Returns:
            Number of cache entries cleared
        """
        cleared = 0
        
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.startswith('trends_') and filename.endswith('.json'):
                    cache_path = os.path.join(self.cache_dir, filename)
                    os.remove(cache_path)
                    cleared += 1
        except Exception as e:
            print(f"[CACHE] Error clearing all cache: {e}")
        
        if cleared > 0:
            print(f"[CACHE] Cleared {cleared} cache entries")
        
        return cleared
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        total = 0
        fresh = 0
        expired = 0
        
        try:
            for filename in os.listdir(self.cache_dir):
                if not filename.startswith('trends_') or not filename.endswith('.json'):
                    continue
                
                total += 1
                cache_path = os.path.join(self.cache_dir, filename)
                
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    cached_time = datetime.fromisoformat(cache_data['timestamp'])
                    expiry_time = cached_time + timedelta(hours=self.expiry_hours)
                    
                    if datetime.now() < expiry_time:
                        fresh += 1
                    else:
                        expired += 1
                        
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"[CACHE] Error getting stats: {e}")
        
        return {
            'total_entries': total,
            'fresh_entries': fresh,
            'expired_entries': expired,
            'cache_dir': self.cache_dir,
            'expiry_hours': self.expiry_hours
        }


# Global cache instance
trends_cache = GoogleTrendsCache(cache_dir="cache/google_trends", expiry_hours=24)

