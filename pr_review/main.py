from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from models import PRRequest, TaskResponse, TaskStatusResponse, AnalysisTaskResponse, TaskStatus, AnalysisResult
from tasks import analyze_pr_task, celery_app
import json

app = FastAPI(title="PR Review API")

@app.post("/analyze-pr", response_model=TaskResponse)
async def analyze_pr(request: PRRequest):
    """
    Start a PR analysis task
    """
    try:
        task = analyze_pr_task.delay(request.model_dump())
        return TaskResponse(task_id=task.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_status(task_id: str):
    """
    Get the status of a PR analysis task
    """
    try:
        task = AsyncResult(task_id, app=celery_app)
        
        # Map Celery states to our TaskStatus enum
        status_map = {
            'PENDING': TaskStatus.PENDING,
            'STARTED': TaskStatus.PROCESSING,
            'SUCCESS': TaskStatus.COMPLETED,
            'FAILURE': TaskStatus.FAILED
        }
        
        return TaskStatusResponse(
            task_id=task_id,
            status=status_map.get(task.status, TaskStatus.PENDING)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{task_id}", response_model=AnalysisTaskResponse)
async def get_results(task_id: str):
    """
    Get the results of a PR analysis task
    """
    try:
        task = AsyncResult(task_id, app=celery_app)
        
        if task.failed():
            return AnalysisTaskResponse(
                task_id=task_id,
                error=str(task.result)
            )
            
        if not task.ready():
            raise HTTPException(
                status_code=404,
                detail="Task results not ready yet"
            )
            
        result = task.result
        if isinstance(result, str):
            result = json.loads(result)
            
        # Convert the result to AnalysisResult
        analysis_result = AnalysisResult(**result)
            
        return AnalysisTaskResponse(
            task_id=task_id,
            result=analysis_result
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
