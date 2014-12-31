import datetime

from flask import render_template

import dateutil.parser

from baby_log import app
from baby_log.db import DBModel


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/babies/<string:name>/')
def baby(name):
    with DBModel.connect(app) as db:
        baby = db.get_baby(name)
        bot = [x['id'] for x in db.entry_types() if x['label'] == 'bottle'][0]
        days_ago = DBModel.now() - datetime.timedelta(days=3)
        count = 0
        for e in db.entries():
            if e['entry_type'] == bot:
                started = e['started']
                if dateutil.parser.parse(started) > days_ago:
                    count += 1
        args = {
            'baby_id': baby.id,
            'baby_name': baby.name,
            'entry_types': list(db.entry_types()),
            'bottles_per_day': float(count) / 3.0
        }
        return render_template('baby.html', **args)


@app.route('/babies/<string:name>/entry/<int:id>/')
def baby_entry(name, id):
    with DBModel.connect(app) as db:
        entry = db.get_entry(id)
        entry_type = [x['label'] for x in db.entry_types()
                      if x['id'] == entry['entry_type']][0]
        started = dateutil.parser.parse(entry['started'])
        ended = entry['ended']
        if ended:
            ended = dateutil.parser.parse(ended).isoformat()
        else:
            ended = ''  # so it doesn't show as "None"
        baby = db.get_baby(name)
        args = {
            'baby_id': baby.id,
            'baby_name': baby.name,
            'entry_type': entry_type,
            'entry_id': id,
            'started': started.isoformat(),
            'ended': ended,
        }
        return render_template('entry.html', **args)
