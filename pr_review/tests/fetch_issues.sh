#!/bin/bash

# Load environment variables from .env file
source .env

# GitHub API URL
url="https://api.github.com/repos/browser-use/browser-use/pulls/229/files"

# Make the API request and save the response to pr_files.json
curl -H "Accept: application/vnd.github.v3+json" \
     -H "Authorization: Bearer $GITHUB_TOKEN" \
     $url -o pr_files.json

echo "✅ PR files saved to pr_files.json"
