from celery_config import redis_client
import json

def clean_redis():
    """Clean all Celery-related keys from Redis"""
    # List all keys before cleaning
    print("\nCurrent keys in Redis:")
    for key in redis_client.keys("celery*"):
        value = redis_client.get(key)
        print(f"\nKey: {key}")
        try:
            parsed = json.loads(value)
            print(f"Value: {json.dumps(parsed, indent=2)}")
        except:
            print(f"Value: {value}")
    
    # Delete all Celery-related keys
    count = redis_client.delete(*redis_client.keys("celery*"))
    print(f"\nDeleted {count} keys from Redis")

if __name__ == "__main__":
    clean_redis()
