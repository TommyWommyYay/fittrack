import sys
import os

# Add the backend directory to sys.path so `app` package is importable when
# running pytest from the backend directory.
sys.path.insert(0, os.path.dirname(__file__))
