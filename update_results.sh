#!/bin/bash

# Define base paths and file types for optimization
RESULTS_DIR="/home/rxm/cookstock/results"
TODAY=$(date +'%Y-%m-%d')
BRANCH="main"

# Step 1: Install Git LFS if not already installed
if ! git lfs --version &> /dev/null; then
    echo "Installing Git LFS..."
    git lfs install
fi

# Step 2: Track large files (e.g., JPEG images) with Git LFS
echo "Tracking large files with Git LFS..."
git lfs track "*.jpg" "*.jpeg" "*.png" "*.json"
git add .gitattributes

# Step 3: Compress/Optimize images
echo "Optimizing images in $RESULTS_DIR..."
find "$RESULTS_DIR" -type f -name "*.jpg" -exec jpegoptim {} \;
find "$RESULTS_DIR" -type f -name "*.png" -exec optipng {} \;

# Step 4: Add changes to Git
echo "Staging changes..."
git add .

# Step 5: Commit changes with today's date in the commit message
echo "Committing changes..."
git commit -m "Update results for $TODAY"

# Step 6: Perform Git garbage collection and pruning
echo "Cleaning up repository..."
git gc --aggressive
git prune

# Step 7: Push changes to GitHub
echo "Pushing to GitHub on branch $BRANCH..."
git push origin "$BRANCH"

echo "Update completed successfully."

