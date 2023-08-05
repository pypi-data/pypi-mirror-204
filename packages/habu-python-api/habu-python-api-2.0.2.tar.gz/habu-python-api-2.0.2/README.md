# habu-api

This is python package for Habu API. This follows the patterns defined at:
https://packaging.python.org/tutorials/packaging-projects/

#### Step 1
python3 -m pip install --upgrade build

#### Step 2
python3 -m build

#### Step 3
python3 -m pip install --upgrade twine

#### Step 4
python3 -m twine upload --repository pypi dist/* 

For loading to testpypi, use this:
python3 -m twine upload --repository testpypi dist/* 

#### Step 5
Relax and Enjoy!
