#!/bin/bash

# Define base paths and file types for optimization
BASE_DIR="/home/rxm/cookstock/"
RESULTS_DIR="/home/rxm/cookstock/results"
TODAY=$(date +'%Y-%m-%d')
BRANCH="main"

# Change to the repository directory
cd "$BASE_DIR" || { echo "Failed to navigate to cookstock directory"; exit 1; }


# Load the user profile to ensure environment variables are loaded
source ~/.bashrc

# Initialize Conda

# Set paths explicitly (replace `/path/to/conda` with the actual path if necessary)
export PATH="/home/rxm/miniconda3/bin:$PATH"
eval "$(conda shell.bash hook)"

# step -1: pull changes from GitHub
#echo "Pulling changes from GitHub..."
#git pull origin "$BRANCH"


## Step 0: remove folders older than 2 days
# Get today's date in seconds since the epoch
today=$(date +%s)

# Loop through each folder in the RESULTS_DIR
for dir in "$RESULTS_DIR"/*; do
    # Check if it's a directory and if its name matches the YYYY-MM-DD format
    if [ -d "$dir" ]; then
        folder_name=$(basename "$dir")

        # Validate the folder name as a date in the format YYYY-MM-DD
        if [[ $folder_name =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            # Convert the folder name (date) to seconds since the epoch
            folder_date=$(date -d "$folder_name" +%s 2>/dev/null)

            # Check if the conversion was successful (date was valid)
            if [ $? -eq 0 ]; then
                # Calculate the age in days
                age=$(( (today - folder_date) / 86400 ))

                # If the folder is older than 2 days, remove it
                if [ $age -gt 2 ]; then
                    echo "Removing folder: $dir (Age: $age days)"
                    rm -rf "$dir"
                fi
            else
                echo "Skipping invalid date folder: $folder_name"
            fi
        else
            echo "Skipping folder with invalid format: $folder_name"
        fi
    fi
done
git add -u  

## Step 1: activate cookStock environment
conda activate cookStock

## Step 2: first run auto.py to update README.md based on previous results
#python $BASE_DIR/auto.py

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

