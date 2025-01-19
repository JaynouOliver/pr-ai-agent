from celery import Celery
from celery.utils.log import get_task_logger
from aiagent import process_and_analyze

logger = get_task_logger(__name__)

celery_app = Celery('pr_review')
celery_app.config_from_object('celery_config')

@celery_app.task(bind=True)
def analyze_pr_task(self, request_dict: dict):
    """
    Celery task.
    States:
    - PENDING 
    - STARTED
    - SUCCESS
    - FAILURE
    """
    try:
        logger.info(f"Starting analysis of PR #{request_dict['pr_number']} from {request_dict['repo_url']}")
        
        result = process_and_analyze(request_dict)
        logger.info("PR analysis completed successfully")
        return result
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error analyzing PR: {error_msg}")
        raise