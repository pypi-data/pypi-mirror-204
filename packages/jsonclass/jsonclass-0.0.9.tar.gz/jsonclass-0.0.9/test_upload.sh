#!/bin/sh

rm -rf dist
. venv/bin/activate

pip3 uninstall -y jsonclass &&
pip3 install . &&
python3 tests/test.py &&
python3 -m build &&
twine upload --repository testpypi dist/* &&
pip3 uninstall -y jsonclass &&
pip3 install --index-url https://test.pypi.org/simple/ jsonclass &&
python3 tests/test.py &&
echo ">> DONE <<"
