from flask import jsonify, request

from baby_log import app
from baby_log.db import DBModel


@app.route('/api/v1/entry_types/', methods=['GET'])
def entry_types():
    with DBModel.connect(app) as db:
        types = list(db.entry_types())
        return jsonify({'entry_types': types})


@app.route('/api/v1/babies/', methods=['GET'])
def babies_list():
    with DBModel.connect(app) as db:
        babies = list(db.babies())
        return jsonify({'babies': babies})


def _baby_entries(db, id):
    entries = list(db.entries(baby=id))
    return jsonify({'entries': entries})


@app.route('/api/v1/babies/<int:id>/entries/', methods=['GET'])
def baby_entries_by_id(id):
    with DBModel.connect(app) as db:
        return _baby_entries(db, id)


@app.route('/api/v1/babies/<string:name>/entries/', methods=['GET'])
def baby_entries_by_name(name):
    with DBModel.connect(app) as db:
        return _baby_entries(db, db.get_baby(name).id)


@app.route('/api/v1/babies/<int:id>/entries/', methods=['POST'])
def baby_entry_create_by_id(id):
    with DBModel.connect(app) as db:
        id = db.add_entry(**request.json)
        resp = jsonify({})
        resp.status_code = 201
        resp.headers['Location'] = 'todo_' + str(id)
        return resp


@app.route('/api/v1/babies/<int:baby>/entries/<int:id>/', methods=['PATCH'])
def baby_entries_update(baby, id):
    with DBModel.connect(app) as db:
        db.update_entry(id, request.json)
        return jsonify({})
