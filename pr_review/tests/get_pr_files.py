import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Run the shell script
os.system("bash fetch_issues.sh")

# Print a message
print("✅ Shell script executed. Check pr_files.json for the output.")
