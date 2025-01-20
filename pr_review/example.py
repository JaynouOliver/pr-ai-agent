import os
import uvicorn
from fastapi import FastAPI
from pyngrok import ngrok, conf
import asyncio
import json

# Get the auth token from environment variable
ngrok_token = os.getenv("NGROK_AUTHTOKEN")
if not ngrok_token:
    raise ValueError("NGROK_AUTHTOKEN environment variable is not set")

# Configure ngrok
conf.get_default().auth_token = ngrok_token

# Get the FastAPI app from main.py
from main import app

# Example request data
example_request = {
    "repo_url": "https://github.com/NixOS/nixpkgs",
    "pr_number": 350177
}

# Create ngrok tunnel
try:
    # Kill any existing ngrok processes
    ngrok.kill()
    
    # Create new tunnel
    public_url = ngrok.connect(8000).public_url
    print(f"\n🚀 Ngrok tunnel created! Your API is now available at:\n{public_url}\n")
    print("Example API calls:")
    print(f"1. Analyze PR:")
    print(f"   curl -X POST '{public_url}/analyze-pr' \\")
    print(f"        -H 'Content-Type: application/json' \\")
    print(f"        -d '{json.dumps(example_request)}'")
    print(f"\n2. Check Status:")
    print(f"   curl '{public_url}/status/YOUR_TASK_ID'")
    print(f"\n3. Get Results:")
    print(f"   curl '{public_url}/results/YOUR_TASK_ID'\n")
except Exception as e:
    print(f"Error creating ngrok tunnel: {str(e)}")
    raise

# Run the FastAPI app
if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
