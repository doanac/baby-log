from flask import render_template

from baby_log import app
from baby_log.db import DBModel


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/babies/<string:name>/')
def baby(name):
    with DBModel.connect(app) as db:
        baby = db.get_baby(name)
        args = {
            'baby_id': baby.id,
            'baby_name': baby.name,
            'entry_types': list(db.entry_types()),
        }
        return render_template('baby.html', **args)
