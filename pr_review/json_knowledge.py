from crewai import Agent, Task, Crew
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from pydantic import BaseModel
from typing import List

# Define the output structure
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

# Create a JSON knowledge source
json_source = JSONKnowledgeSource(
    file_paths=["data.json"]
)

# Create an agent with the JSON knowledge source
agent = Agent(
    role="Data Analyst",
    goal="Analyze data from the JSON source",
    backstory="You are an expert in analyzing JSON data.",
    verbose=True,
    knowledge_sources=[json_source]
)

# Create a task for the agent
task = Task(
    description="Analyze the data from the JSON source and provide insights.",
    expected_output="A detailed analysis of the JSON data with key insights in the specified JSON format.",
    agent=agent,
    output_json=AnalysisResult
)

# Create a crew with the agent and task
crew = Crew(
    agents=[agent],
    tasks=[task]
)

# Run the crew
result = crew.kickoff()

print(result)