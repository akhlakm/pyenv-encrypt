#!/usr/bin/env bash
setup() {
    pip install --upgrade pip
    pip install --upgrade twine build
}

publish() {
    python -m build
    python -m twine upload dist/*
}

version() {
    # current version
    grep version pyproject.toml
    read -p "new version string? " NEW_VERSION
    sed -i "s/\(version = \"\)[^\"]*\"/\1$NEW_VERSION\"/" pyproject.toml
}

tag() {
    # create a new git tag using the pyproject.toml version
    # and push the tag to origin
    version=$(sed -n 's/version = "\(.*\)"/\1/p' file.txt)
    git tag v$version && git push origin v$version
}

clean() {
    /bin/rm -rf dist *.egg-info
}

"$@"
