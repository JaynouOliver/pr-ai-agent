import os
from dotenv import load_dotenv
import redis

load_dotenv()

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_USERNAME = os.getenv('REDIS_USERNAME', '')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Construct Redis URL
if REDIS_USERNAME and REDIS_PASSWORD:
    REDIS_URL = f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Celery Configuration
broker_url = REDIS_URL
result_backend = REDIS_URL

# Task settings
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True

# Retry settings
broker_connection_retry_on_startup = True  # New setting for Celery 6.0
broker_connection_max_retries = 0  # Unlimited retries

# Result settings
result_expires = 3600  # Results expire in 1 hour

# Create Redis client for direct operations
redis_client = redis.from_url(REDIS_URL)

def cleanup_redis():
    """Clean up Redis keys related to our tasks"""
    pattern = "pr_review_*"
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)
    return len(keys)
