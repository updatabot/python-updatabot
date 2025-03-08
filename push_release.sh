#!/bin/bash


# Check there are no uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "Uncommitted changes found"
    exit 1
fi

# Get the version from the pyproject.toml file
VERSION_TAG=v$(grep "^version = " pyproject.toml | cut -d'"' -f2)

if [ -z "$VERSION_TAG" ]; then
    echo "No version found in pyproject.toml"
    exit 1
fi

echo "VERSION_TAG=\"$VERSION_TAG\""
# Ask for confirmation before proceeding
read -p "Proceed with release? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Release cancelled"
    exit 1
fi

echo "Pushing tag $VERSION_TAG to origin"
git tag $VERSION_TAG
git push origin $VERSION_TAG

echo "Creating release on GitHub"
gh release create $VERSION_TAG --generate-notes

echo "Done"