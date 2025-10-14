"""
Utility functions for the Product Launch Planner system
Common helper functions used across all agents
"""
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from functools import wraps
import time

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry functions on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator

def validate_product_info(product_info: Dict[str, Any]) -> bool:
    """Validate product information structure"""
    required_fields = ['name', 'category', 'price', 'description']
    
    for field in required_fields:
        if field not in product_info or not product_info[field]:
            return False
    
    if not isinstance(product_info['price'], (int, float)) or product_info['price'] <= 0:
        return False
    
    return True

def format_currency(amount: float, currency: str = 'USD') -> str:
    """Format currency with proper symbols"""
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'KRW': '₩',
        'JPY': '¥'
    }
    
    symbol = symbols.get(currency, '$')
    
    if amount >= 1000000:
        return f"{symbol}{amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"{symbol}{amount/1000:.1f}K"
    else:
        return f"{symbol}{amount:.2f}"

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100

def normalize_scores(scores: List[float], min_val: float = 0.0, max_val: float = 1.0) -> List[float]:
    """Normalize scores to a specific range"""
    if not scores:
        return []
    
    min_score = min(scores)
    max_score = max(scores)
    
    if max_score == min_score:
        return [0.5] * len(scores)  # Return middle value if all scores are same
    
    normalized = []
    for score in scores:
        norm_score = (score - min_score) / (max_score - min_score)
        norm_score = norm_score * (max_val - min_val) + min_val
        normalized.append(norm_score)
    
    return normalized

def generate_color_palette(n_colors: int) -> List[str]:
    """Generate a color palette for visualizations"""
    # Samsung brand colors and complementary colors
    base_colors = [
        '#1f4e79',  # Samsung Blue
        '#2e86ab',  # Light Blue
        '#a23b72',  # Magenta
        '#f18f01',  # Orange
        '#c73e1d',  # Red
        '#4a90e2',  # Sky Blue
        '#7ed321',  # Green
        '#f5a623',  # Yellow
        '#9013fe',  # Purple
        '#50e3c2'   # Teal
    ]
    
    if n_colors <= len(base_colors):
        return base_colors[:n_colors]
    
    # Generate additional colors if needed
    additional_colors = []
    for i in range(n_colors - len(base_colors)):
        hue = (i * 137.5) % 360  # Golden angle for good distribution
        additional_colors.append(f'hsl({hue}, 70%, 50%)')
    
    return base_colors + additional_colors

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero"""
    if denominator == 0:
        return default
    return numerator / denominator

def clean_text(text: str) -> str:
    """Clean and normalize text for analysis"""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    import re
    text = re.sub(r'[^\w\s\-\.\,\!\?]', '', text)
    
    return text.strip()

def calculate_compound_growth_rate(initial_value: float, final_value: float, periods: int) -> float:
    """Calculate compound annual growth rate"""
    if initial_value <= 0 or final_value <= 0 or periods <= 0:
        return 0.0
    
    return (pow(final_value / initial_value, 1 / periods) - 1) * 100

def create_date_range(start_date: str, end_date: str, freq: str = 'D') -> List[str]:
    """Create a range of dates between start and end"""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    date_range = pd.date_range(start=start, end=end, freq=freq)
    return [date.strftime('%Y-%m-%d') for date in date_range]

def aggregate_metrics(data: List[Dict[str, Any]], metric_key: str, aggregation: str = 'mean') -> float:
    """Aggregate metrics from a list of dictionaries"""
    values = [item.get(metric_key, 0) for item in data if metric_key in item]
    
    if not values:
        return 0.0
    
    if aggregation == 'mean':
        return np.mean(values)
    elif aggregation == 'sum':
        return np.sum(values)
    elif aggregation == 'max':
        return np.max(values)
    elif aggregation == 'min':
        return np.min(values)
    elif aggregation == 'median':
        return np.median(values)
    else:
        return np.mean(values)

def create_confidence_interval(values: List[float], confidence: float = 0.95) -> Dict[str, float]:
    """Create confidence interval for a list of values"""
    if not values:
        return {'lower': 0, 'upper': 0, 'mean': 0}
    
    mean_val = np.mean(values)
    std_val = np.std(values)
    n = len(values)
    
    # Calculate margin of error (simplified)
    margin = 1.96 * (std_val / np.sqrt(n))  # 95% confidence interval
    
    return {
        'lower': mean_val - margin,
        'upper': mean_val + margin,
        'mean': mean_val
    }

def rank_items(items: Dict[str, float], ascending: bool = False) -> List[tuple]:
    """Rank items by their values"""
    return sorted(items.items(), key=lambda x: x[1], reverse=not ascending)

def calculate_market_share(company_value: float, total_market: float) -> float:
    """Calculate market share percentage"""
    if total_market <= 0:
        return 0.0
    return (company_value / total_market) * 100

def estimate_seasonality_factor(month: int, category: str) -> float:
    """Estimate seasonality factor based on month and product category"""
    # Seasonal patterns for different product categories
    seasonal_patterns = {
        'smartphones': {
            1: 0.9, 2: 0.8, 3: 1.1, 4: 1.0, 5: 1.0, 6: 1.1,
            7: 1.0, 8: 0.9, 9: 1.2, 10: 1.1, 11: 1.3, 12: 1.4
        },
        'tablets': {
            1: 0.9, 2: 0.8, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.1,
            7: 1.1, 8: 1.2, 9: 1.0, 10: 0.9, 11: 1.2, 12: 1.3
        },
        'laptops': {
            1: 0.9, 2: 0.9, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.1,
            7: 1.2, 8: 1.3, 9: 1.1, 10: 1.0, 11: 1.2, 12: 1.1
        },
        'wearables': {
            1: 1.1, 2: 0.9, 3: 1.0, 4: 1.1, 5: 1.2, 6: 1.0,
            7: 0.9, 8: 0.9, 9: 1.0, 10: 1.1, 11: 1.3, 12: 1.4
        },
        'tv': {
            1: 0.8, 2: 0.9, 3: 1.0, 4: 1.0, 5: 1.1, 6: 1.2,
            7: 1.1, 8: 1.0, 9: 1.0, 10: 1.1, 11: 1.4, 12: 1.3
        }
    }
    
    pattern = seasonal_patterns.get(category.lower(), seasonal_patterns['smartphones'])
    return pattern.get(month, 1.0)

def calculate_price_elasticity(price_change_percent: float, demand_change_percent: float) -> float:
    """Calculate price elasticity of demand"""
    if price_change_percent == 0:
        return 0.0
    return demand_change_percent / price_change_percent

class DataValidator:
    """Class for validating different types of data"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        import re
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        # Check if it has 10-15 digits
        return 10 <= len(digits) <= 15
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        import re
        pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> bool:
        """Validate that end date is after start date"""
        try:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            return end > start
        except:
            return False

class APIRateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def can_make_call(self) -> bool:
        """Check if we can make another API call"""
        now = datetime.now()
        # Remove calls older than 1 minute
        self.calls = [call_time for call_time in self.calls 
                     if (now - call_time).seconds < 60]
        
        return len(self.calls) < self.calls_per_minute
    
    def record_call(self):
        """Record that an API call was made"""
        self.calls.append(datetime.now())
    
    def wait_time(self) -> float:
        """Get seconds to wait before next call"""
        if self.can_make_call():
            return 0.0
        
        oldest_call = min(self.calls)
        wait_until = oldest_call + timedelta(minutes=1)
        return (wait_until - datetime.now()).total_seconds()

def export_results_to_json(results: Dict[str, Any], filename: str):
    """Export analysis results to JSON file"""
    try:
        # Convert numpy types to native Python types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_numpy(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            else:
                return obj
        
        converted_results = convert_numpy(results)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(converted_results, f, indent=2, ensure_ascii=False, default=str)
        
        return True
    except Exception as e:
        print(f"Error exporting results: {e}")
        return False

def load_config(config_file: str = 'config.json') -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default configuration
        return {
            'api_keys': {},
            'rate_limits': {
                'default': 60
            },
            'cache_duration': 3600,
            'timeout': 30
        }