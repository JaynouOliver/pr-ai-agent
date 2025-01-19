from github_service import fetch_pr_data
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import json

# Pydantic models for API and analysis
class Issue(BaseModel):
    type: str
    line: int
    description: str
    suggestion: str

class File(BaseModel):
    name: str
    issues: List[Issue]

class Summary(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int

class AnalysisResult(BaseModel):
    files: List[File]
    summary: Summary

def process_github_pr(api_request):
    output_file = fetch_pr_data(api_request)
    return output_file

def analyze_json_data(file_path: str) -> Dict: 
    # Initialize FileReadTool with the specific JSON file
    file_read_tool = FileReadTool(file_path=file_path)
    
    agent = Agent(
        role="PR Review Expert",
        goal="Analyze GitHub Pull Request data and identify potential issues",
        backstory="""You are an expert code reviewer specializing in analyzing GitHub Pull Requests.
        Your task is to analyze the PR data and identify any potential issues, focusing on:
        - Code quality and best practices
        - Security concerns
        - Performance implications
        - Documentation completeness""",
        verbose=False,
        tools=[file_read_tool]
    )

    task = Task(
        description="""Analyze the GitHub Pull Request data and provide a detailed review.
        Focus on:
        1. Changed files and their impact
        2. Potential issues in the code
        3. Security and performance concerns
        4. Documentation completeness
        
        Format the output according to the AnalysisResult schema with files and issues.""",
        expected_output="A detailed PR analysis in the specified JSON format with files, issues, and summary.",
        agent=agent,
        output_json=AnalysisResult
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()
    if hasattr(result, 'tasks_output') and result.tasks_output: 
        task_output = result.tasks_output[0] 
        if hasattr(task_output, 'json_dict'):
            return task_output.json_dict
    return None

def process_and_analyze(api_request):
    try:
        file_path = fetch_pr_data(api_request)
        raw_result = analyze_json_data(file_path)
        analysis_result = AnalysisResult(**raw_result)
        return json.dumps(analysis_result.model_dump(), indent=2)
    except Exception as e:
        raise Exception(f"Error analyzing PR: {str(e)}")

if __name__ == "__main__":
    api_request = {
        "repo_url": "https://github.com/fossasia/eventyay-video",
        "pr_number": 304
    }
    
    try:
        result = process_and_analyze(api_request)
        print(result)  # This will now print nicely formatted JSON
    except Exception as e:
        print("Error:", e)
