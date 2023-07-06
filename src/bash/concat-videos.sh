#!/bin/bash

# Directory containing the videos
dir="/Volumes/RICO_III/SNFTM/concat"

# Output file
output="/Volumes/RICO_III/SNFTM/concat.mp4"

# Temporary file for storing the list of videos to concatenate
list=$(mktemp)


# Find all mp4 files in the directory, sort them, then add them to the list
for f in $(ls "$dir"/*.mp4 | sort); do
    echo "file '$f'"
    echo "file '$f'" >> "$list"
done

# Output the contents of the list
echo "List of files to concatenate:"
cat "$list"

# Use ffmpeg to concatenate the videos
ffmpeg -f concat -safe 0 -i "$list" -c copy "$output"

# Remove the temporary file
rm "$list"