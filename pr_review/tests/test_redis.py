import redis
import json
from dotenv import load_dotenv
import os
from aiagent import process_and_analyze

# Load environment variables
load_dotenv()

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_USERNAME = os.getenv('REDIS_USERNAME', '')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_DB = int(os.getenv('REDIS_DB', '0'))

# Initialize Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    decode_responses=True
)

def test_redis_storage():
    # Test data
    repo_url = "https://github.com/fossasia/eventyay-video"
    pr_number = 304
    
    print(f"\nAnalyzing PR #{pr_number} from {repo_url}")
    
    # Get the analysis result
    result = process_and_analyze({"repo_url": repo_url, "pr_number": pr_number})
    
    # Store in Redis
    key = f"pr:{repo_url}:{pr_number}"
    redis_client.set(key, result if isinstance(result, str) else json.dumps(result))
    print("\nStored in Redis with key:", key)
    
    # Retrieve from Redis
    print("\nRetrieving from Redis:")
    retrieved = redis_client.get(key)
    print(retrieved)
    
    # Verify it's valid JSON
    print("\nParsed JSON:")
    parsed = json.loads(retrieved)
    print(json.dumps(parsed, indent=2))

if __name__ == "__main__":
    test_redis_storage()
