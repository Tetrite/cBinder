# cBinder
C bindings generator for Python using cffi

# Develop
Assuming python version >= 3.6:
python -m venv venv  # to create virtual environment
source venv/bin/activate  # to activate venv within shell
pip -r requirements.txt  # to install requirements

# Running example
python main.py -f "$(pwd)/test_library" -d "$(pwd)/test_library/Release"
