import os

_here = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
DBNAME = 'production.db'

if os.environ.get('DEBUG') == '1':
    DEBUG = True
    DBNAME = 'tmp.db'

DBNAME = os.path.join(_here, '../', DBNAME)

REPORT_TYPES = {
    'bottle': [
        {
            'name': 'most_recent',
            'label': 'Last bottle',
        },
        {
            'name': 'per_day',
            'label': 'Bottles per day',
            'days': 3,
        },
        {
            'name': 'long_interval',
            'duration': 5 * 60 * 60,  # 5 hours in seconds
        }
    ]
}
