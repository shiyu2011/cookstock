#!/bin/bash
# Define paths
REPO_PATH="/home/rxm/cookstock"
TODAY=$(date +%Y-%m-%d)

# Navigate to the repository
cd "$REPO_PATH" || exit

# Add, commit, and push changes
git add .
git commit -m "Update results for $TODAY"
git push origin main  # Replace 'main' with your branch name if different

echo "Results updated for $TODAY."

