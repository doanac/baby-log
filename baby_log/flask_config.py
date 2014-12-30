import os

_here = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
DBNAME = 'production.db'

if os.environ.get('DEBUG') == '1':
    DEBUG = True
    DBNAME = 'tmp.db'

DBNAME = os.path.join(_here, '../', DBNAME)
