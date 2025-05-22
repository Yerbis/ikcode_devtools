#!/bin/bash

# Check if the user provided the old and new names
if [ "$#" -ne 2 ]; then
    echo "Usage: ./rename.sh <old_name> <new_name>"
    exit 1
fi

OLD_NAME=$1
NEW_NAME=$2

echo "Renaming package from $OLD_NAME to $NEW_NAME..."

# Rename the folder
if [ -d "$OLD_NAME" ]; then
    mv "$OLD_NAME" "$NEW_NAME"
    echo "Folder renamed from $OLD_NAME to $NEW_NAME."
else
    echo "Error: Directory $OLD_NAME does not exist."
    exit 1
fi

# Find and replace all occurrences of the old name within files
echo "Updating imports and references..."
find . -type f -name "*.py" -exec sed -i "s/$OLD_NAME/$NEW_NAME/g" {} +

# Update setup.py package name
if [ -f setup.py ]; then
    sed -i "s/name='$OLD_NAME'/name='$NEW_NAME'/" setup.py
    sed -i "s/packages=\['$OLD_NAME'\]/packages=\['$NEW_NAME'\]/" setup.py
    echo "Updated setup.py with the new package name."
else
    echo "Error: setup.py not found."
    exit 1
fi

# Commit changes if using Git
if [ -d .git ]; then
    git add .
    git commit -m "Renamed package from $OLD_NAME to $NEW_NAME"
    echo "Committed changes to Git."
fi

echo "Package renamed successfully!"
