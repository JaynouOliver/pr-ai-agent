import os
import re
from dotenv import load_dotenv

def extract_github_url(api_request):
    repo_url = api_request.get("repo_url", "")
    pr_number = api_request.get("pr_number", "")
    
    # Extract owner and repo from URL
    pattern = r"https://github\.com/([^/]+)/([^/]+)"
    match = re.match(pattern, repo_url)
    
    if not match:
        raise ValueError("Invalid GitHub URL format")
        
    owner, repo = match.groups()
    return owner, repo, pr_number

def fetch_pr_data(api_request, output_file=None):
    """Fetch PR data from GitHub API and save to file
    
    Args:
        api_request: Dictionary containing repo_url and pr_number
        output_file: Optional path to save the PR data. If None, generates a path
    
    Returns:
        str: Path to the saved JSON file
    """
    # Load environment variables
    load_dotenv()
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        raise ValueError("GitHub token not found in environment variables")
    
    # Extract GitHub details
    owner, repo, pr_number = extract_github_url(api_request)
    
    # Construct API URL
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    
    # Generate output file path if not provided
    if output_file is None:
        # Ensure knowledge directory exists
        os.makedirs("knowledge", exist_ok=True)
        output_file = f"knowledge/pr_{owner}_{repo}_{pr_number}.json"

    curl_command = f"curl -L \
  -H \"Accept: application/vnd.github+json\" \
  -H \"Authorization: Bearer {github_token}\" \
  -H \"X-GitHub-Api-Version: 2022-11-28\" \
  {api_url} > {output_file}"

    os.system(curl_command)
    return output_file

if __name__ == "__main__":
    api_request = {
        "repo_url": "https://github.com/elizaOS/agent-twitter-client",
        "pr_number": 52
    }

    try:
        file_path = fetch_pr_data(api_request)
        print(file_path)
    except Exception as e:
        print("Error:", e)
