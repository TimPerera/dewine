import sys
import os

project_root = os.path.join(os.path.abspath(os.path.dirname('__file__')),'src')
sys.path.append(project_root)

from src.config.connection import create_session
