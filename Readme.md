# PR-AI-Agent: Intelligent Pull Request Analysis System

## System Architecture

![Untitled-2025-01-21-0215](https://github.com/user-attachments/assets/331de60a-d920-4ac7-bc27-1bcc5c0f5aa7)

## Overview

PR-AI-Agent is a sophisticated automated code review system that leverages AI to analyze GitHub Pull Requests. Built with a focus on scalability and reliability, it provides detailed insights into code quality, security vulnerabilities, performance implications, and documentation completeness.

## Key Features

- **Asynchronous Processing**: Handle multiple PR reviews simultaneously
- **Scalable Architecture**: Each component can be scaled independently
- **Real-time Status Updates**: Track review progress through API endpoints
- **Detailed Analysis**: Comprehensive code review covering multiple aspects
- **Persistent Storage**: Reliable task and result management
- **Error Handling**: Robust retry mechanisms and error recovery

## Technical Stack

### Core Components
- **Web Framework**: FastAPI
  - Async support for high performance
  - Built-in OpenAPI documentation
  - Type validation with Pydantic

- **Task Queue**: Celery
  - Distributed task processing
  - Automatic retries
  - Task monitoring

- **Message Broker & Cache**: Redis
  - Fast in-memory operations
  - Persistent task queue
  - Result caching

## Setup Instructions

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/pr-ai-agent.git
   cd pr-ai-agent
   ```

2. **Environment Setup**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Unix
   # or
   .venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. **Start Services**
   ```bash
   # Start Redis
   redis-server

   # Start Celery Worker
   celery -A tasks worker --loglevel=info

   # Start FastAPI Server
   uvicorn main:app --reload
   ```

## API Usage Examples

### 1. Submit PR for Analysis
```bash
curl -X POST "http://localhost:8000/analyze-pr" -H "Content-Type: application/json" -d '{"repo_url": "https://github.com/NixOS/nixpkgs", "pr_number": 350177}'
```

Example Response:
<img width="755" alt="Screenshot 2025-01-20 at 8 38 06 AM" src="https://github.com/user-attachments/assets/7eb94fc5-a0e5-497d-9b53-3f0b08c6b2a2" />

### 2. Check Analysis Status
```bash
http://localhost:8000/status/508ae882-027c-4812-a905-020f5b8bf27a
```

Example Response:
<img width="755" alt="Screenshot 2025-01-20 at 8 38 18 AM" src="https://github.com/user-attachments/assets/1483dba2-ed16-4b79-87dc-063a67f828dd" />

### 3. Get Analysis Results
```bash
http://localhost:8000/results/508ae882-027c-4812-a905-020f5b8bf27a
```

Example Response:
<img width="755" alt="Screenshot 2025-01-20 at 8 38 35 AM" src="https://github.com/user-attachments/assets/43ebcb63-6600-4684-95f2-6c1cb17c8147" />

Example JSON Response:
```json
{
    "task_id": "201c58f9-599b-42ef-a798-52caa0b4d1ea",
    "result": {
        "files": [{
            "name": "merged--generated--merge-conflict",
            "issues": [{
                "type": "Code Quality",
                "line": 0,
                "description": "Presence of auto-generated code conflicting with custom code.",
                "suggestion": "Review and resolve the merge conflict manually to ensure all necessary functionalities are intact."
            }, {
                "type": "Documentation Completeness",
                "line": 0,
                "description": "Lack of inline comments and documentation for complex logic.",
                "suggestion": "Include comments explaining the purpose and usage of critical sections of the code."
            }]
        }],
        "summary": {
            "total_files": 1,
            "total_issues": 2,
            "critical_issues": 1
        }
    },
    "error": null
}
```

## Future Roadmap

1. **Enhanced Analysis**
   - Custom analysis rules
   - Language-specific checks
   - Team-specific preferences

2. **Integration Features**
   - GitHub webhook support
   - CI/CD pipeline integration
   - Slack notifications

3. **Performance Optimizations**
   - Response caching
   - Task prioritization
   - Resource optimization

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
