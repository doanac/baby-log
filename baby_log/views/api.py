import datetime

import dateutil.parser

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


def _reporting_loop(report_types, data, entry):
    entry_type = data['entry_types'][entry['entry_type']]
    reports = report_types.get(entry_type)
    if not reports:
        return

    started = dateutil.parser.parse(entry['started'])
    days_ago = data.get('days_ago')

    for r in reports:
        if r['name'] == 'most_recent':
            mr = data.get('most_recent_' + entry_type)
            if not mr or mr < started:
                data['most_recent_' + entry_type] = started
        elif r['name'] == 'per_day':
            if not days_ago:
                days_ago = DBModel.now() - datetime.timedelta(days=r['days'])
                data['days_ago'] = days_ago
            count = data.get('days_count_' + entry_type, 0)
            if started > days_ago:
                count += 1
                data['days_count_' + entry_type] = count
        elif r['name'] == 'long_interval':
            last_entry = data.get('previous_' + entry_type)
            if last_entry:
                if (last_entry - started).total_seconds() > r['duration']:
                    entry['long_interval'] = True
            data['previous_' + entry_type] = started
        else:
            raise ValueError('Invalid report type: ' + r['name'])


def _report_summary(report_types, data):
    report = {}
    for entry_type, reports in report_types.items():
        for r in reports:
            if r['name'] == 'most_recent':
                key = 'most_recent_' + entry_type
                report[r['label']] = data[key].isoformat()
            elif r['name'] == 'per_day':
                key = 'days_count_' + entry_type
                report[r['label']] = float(data[key]) / r['days']
    return report


def _baby_entries(db, id):
    entries = []
    report_types = app.config.get('REPORT_TYPES')
    data = {'entry_types': {x['id']: x['label'] for x in db.entry_types()}}
    for e in db.entries(baby=id):
        if report_types:
            _reporting_loop(report_types, data, e)
        entries.append(e)
    return jsonify(
        {'entries': entries, 'reports': _report_summary(report_types, data)})


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


@app.route('/api/v1/babies/<int:baby>/entries/<int:id>/', methods=['DELETE'])
def baby_entry_delete(baby, id):
    with DBModel.connect(app) as db:
        db.delete_entry(id)
        return jsonify({})
