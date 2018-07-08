import os, sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from core import main
from model.models import *

if __name__ == '__main__':
    main.run()