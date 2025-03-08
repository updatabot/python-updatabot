#!/bin/bash

# Must be in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Must be in a virtual environment"
    exit 1
fi

# Build the package
rm -rf dist
python3 -m build

# Upload the package to PyPI
python3 -m twine upload dist/* --verbose