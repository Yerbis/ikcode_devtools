#!/bin/bash

# Clean old builds
echo "Cleaning old builds..."
rm -rf dist build *.egg-info

# Build source and wheel distributions
echo "Building distributions..."
python3 setup.py sdist bdist_wheel

# Upload to PyPI via twine
echo "Uploading to PyPI..."
twine upload dist/*

echo "Done!"
