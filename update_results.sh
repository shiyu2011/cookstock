#!/bin/bash

# Define base paths and file types for optimization
BASE_DIR="/home/rxm/cookstock/"
RESULTS_DIR="/home/rxm/cookstock/results"
TODAY=$(date +'%Y-%m-%d')
BRANCH="main"


## Step 0: remove folders older than 3 days
echo "Removing deleted files..."
find $RESULTS_DIR -type d -ctime +3 -exec rm -rf {} \;  
git add -u  

## Step 1: activate cookStock environment
conda activate cookStock

## Step 2: first run auto.py to update README.md based on previous results
python $BASE_DIR/auto.py

## Step 3: run cookStockPipeline.py to update results
python $BASE_DIR/batch/cookStockPipeline.py

## Step 4: set up git LFS
if ! git lfs --version &> /dev/null; then
    echo "Installing Git LFS..."
    git lfs install
fi

## Step 5: rerun auto.py to update README.md based on new results
python $BASE_DIR/auto.py

## Step 6: deactivate cookStock environment
conda deactivate

## Step 7: track large files with Git LFS
echo "Tracking large files with Git LFS..."
git lfs track "*.jpg" "*.jpeg" "*.png" "*.json"
git add .gitattributes

## Step 8: optimize images
echo "Optimizing images in $RESULTS_DIR..."
find "$RESULTS_DIR" -type f -name "*.jpg" -exec jpegoptim {} \;
find "$RESULTS_DIR" -type f -name "*.png" -exec optipng {} \;

## Step 9: stage changes
echo "Staging changes..."
git add .

# Step 10: commit changes
echo "Committing changes..."
git commit -m "Update results for $TODAY"

## Step 11: clean up repository
echo "Cleaning up repository..."
git gc --aggressive
git prune

## Step 12: push changes to GitHub
echo "Pushing to GitHub on branch $BRANCH..."
git push origin "$BRANCH"

echo "Update completed successfully."

