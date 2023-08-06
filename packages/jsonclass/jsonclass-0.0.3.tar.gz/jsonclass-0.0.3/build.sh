#!/bin/sh

rm -rf dist &&
. venv/bin/activate &&
python3 -m build &&
twine upload --repository testpypi dist/* &&
pip3 install --index-url https://test.pypi.org/simple/ jsonclass &&
python3 tests/test.py &&
twine upload dist/*
