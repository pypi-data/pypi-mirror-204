#!/bin/sh

. venv/bin/activate &&
pip3 install . &&
python3 tests/test.py &&
python3 -m build &&
twine upload dist/* &&
pip3 install jsonclass &&
python3 tests/test.py
