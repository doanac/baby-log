import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)

from baby_log import app as application
