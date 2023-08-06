#!/bin/sh

rm -rf dist
. venv/bin/activate

python3 -m build &&
twine upload --repository testpypi dist/* &&
sleep 2 &&
pip3 install --upgrade --index-url https://test.pypi.org/simple/ jsonclass &&
python3 tests/test.py
