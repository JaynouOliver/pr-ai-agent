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

<img width="755" alt="Screenshot 2025-01-20 at 8 38 06 AM" src="https://github.com/user-attachments/assets/7eb94fc5-a0e5-497d-9b53-3f0b08c6b2a2" />


Result - {"task_id":"508ae882-027c-4812-a905-020f5b8bf27a"}

http://localhost:8000/status/508ae882-027c-4812-a905-020f5b8bf27a

<img width="755" alt="Screenshot 2025-01-20 at 8 38 18 AM" src="https://github.com/user-attachments/assets/1483dba2-ed16-4b79-87dc-063a67f828dd" />


Result - {"task_id":"508ae882-027c-4812-a905-020f5b8bf27a","status":"completed"}
<img width="755" alt="Screenshot 2025-01-20 at 8 38 35 AM" src="https://github.com/user-attachments/assets/43ebcb63-6600-4684-95f2-6c1cb17c8147" />

http://localhost:8000/results/508ae882-027c-4812-a905-020f5b8bf27a

Example response - 
{"task_id":"201c58f9-599b-42ef-a798-52caa0b4d1ea","result":{"files":[{"name":"merged--generated--merge-conflict","issues":[{"type":"Code Quality","line":0,"description":"Presence of auto-generated code conflicting with custom code.","suggestion":"Review and resolve the merge conflict manually to ensure all necessary functionalities are intact."},{"type":"Documentation Completeness","line":0,"description":"Lack of inline comments and documentation for complex logic.","suggestion":"Include comments explaining the purpose and usage of critical sections of the code."}]}],"summary":{"total_files":1,"total_issues":2,"critical_issues":1}},"error":null}
