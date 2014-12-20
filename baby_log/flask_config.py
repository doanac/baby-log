import os

DEBUG = False
DBNAME = 'production.db'

if os.environ.get('DEBUG') == '1':
    DEBUG = True
    DBNAME = 'tmp.db'
