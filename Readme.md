Project setup instructions

creat venv with python 3.10
install crew ai from crew ai docs 

or pip install -r requirements.txt

cd into the crew ai directory

# In terminal 1
source venv/bin/activate  # or however you activate your virtual environment
(#start redis server)
redis-server
celery -A tasks worker --loglevel=INFO

# In terminal 2
source venv/bin/activate  # or however you activate your virtual environment
uvicorn main:app --reload --port 8000

API documentation

curl -X POST "http://localhost:8000/analyze-pr" -H "Content-Type: application/json" -d '{"repo_url": "https://github.com/NixOS/nixpkgs", "pr_number": 350177}'

Result - {"task_id":"508ae882-027c-4812-a905-020f5b8bf27a"}

http://localhost:8000/status/508ae882-027c-4812-a905-020f5b8bf27a

Result - {"task_id":"508ae882-027c-4812-a905-020f5b8bf27a","status":"completed"}

http://localhost:8000/results/508ae882-027c-4812-a905-020f5b8bf27a

