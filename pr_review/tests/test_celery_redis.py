from tasks import analyze_pr_task, celery_app
from celery.result import AsyncResult
from celery_config import redis_client, cleanup_redis
from models import PRRequest
import json
import time

def test_pr_analysis(repo_url: str, pr_number: int, description: str = ""):
    """Test PR analysis with given repo and PR number"""
    print(f"\n=== Testing {description} ===")
    print(f"Repository: {repo_url}")
    print(f"PR Number: {pr_number}")
    
    # Create request dictionary directly
    request_dict = {
        "repo_url": repo_url,
        "pr_number": pr_number
    }
    print("\nRequest Dictionary:", json.dumps(request_dict, indent=2))
    
    print("\n1. Submitting task to Celery...")
    task = analyze_pr_task.delay(request_dict=request_dict)  # Pass as kwarg
    task_id = task.id
    print(f"Task ID: {task_id}")
    
    # Wait for task to complete
    print("\n2. Waiting for task to complete...")
    max_wait = 30  # Maximum wait time in seconds
    start_time = time.time()
    
    while not task.ready() and time.time() - start_time < max_wait:
        print("Task status:", task.status)
        time.sleep(2)
    
    # Get result
    print("\n3. Task Result:")
    print("Final Status:", task.status)
    if task.failed():
        print("Error:", task.result)
    elif task.successful():
        print("Success:", json.dumps(task.result, indent=2))
    else:
        print("Task timed out or is still running")
    
    # Show Redis data
    print("\n4. Redis data for this task:")
    result_key = f"celery-task-meta-{task_id}"
    raw_result = redis_client.get(result_key)
    if raw_result:
        print("Redis key:", result_key)
        print("Raw data:", json.dumps(json.loads(raw_result), indent=2))
    else:
        print("No data found in Redis")

def main():
    # Clean Redis before starting
    print("Cleaning Redis...")
    cleanup_redis()
    
    # Test cases
    test_cases = [
        # Real PR
        {
            "repo_url": "https://github.com/thepersonalaicompany/amurex-backend",
            "pr_number": 31,
            "description": "Real PR"
        }
    ]
    
    # Run tests
    for test_case in test_cases:
        test_pr_analysis(**test_case)
        time.sleep(2)  # Wait between tests
        
    # Show all Redis keys at the end
    print("\n=== Final Redis State ===")
    for key in redis_client.keys("*"):
        print(f"\nKey: {key}")
        value = redis_client.get(key)
        try:
            parsed = json.loads(value)
            print(f"Value: {json.dumps(parsed, indent=2)}")
        except:
            print(f"Value: {value}")

if __name__ == "__main__":
    main()
