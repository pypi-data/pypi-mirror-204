#!/bin/sh

rm -rf dist &&
. venv/bin/activate &&
python3 -m build &&
twine upload --repository testpypi dist/* &&
pip3 install --force-reinstall jsonclass &&
python3 tests/test.py &&
twine upload dist/*
