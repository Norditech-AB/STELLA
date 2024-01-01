#!/bin/bash

# Define the file that contains the list of files and folders to remove
CLEAR_FILES=".clear_files"

# Check if the .clear_files exists
if [[ ! -f $CLEAR_FILES ]]; then
    echo "The file $CLEAR_FILES does not exist."
    exit 1
fi

# Read the .clear_files and remove each entry
while IFS= read -r line || [[ -n "$line" ]]; do
    # Check if line is not empty and not a comment
    if [[ -n $line && ! $line =~ ^#.* ]]; then
        rm -rf "$line"
        if [ $? -eq 0 ]; then
            echo "Removed $line"
        else
            echo "Failed to remove $line"
        fi
    fi
done < "$CLEAR_FILES"

echo "Cleanup completed."
