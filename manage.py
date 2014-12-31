#!/usr/bin/env python
import argparse

import dateutil.parser

from baby_log import app
from baby_log.db import db_create, db_migrate, DBModel


def _migrate(args):
    db_migrate(app)


def _create_db(args):
    db_create(app, args.baby)


def _run(args):
    app.run(args.host, args.port)


def _add_entry(args):
    with DBModel.connect(app) as db:
        baby = db.get_baby(args.baby)
        if not args.entry_type.isdigit():
            id = [x['id'] for x in db.entry_types()
                  if x['label'] == args.entry_type]
            args.entry_type = id[0]
        args.started = dateutil.parser.parse(args.started)
        if args.ended:
            args.ended = dateutil.parser.parse(args.ended)
        db.add_entry(baby.id, args.entry_type, args.started, args.ended)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Manage baby-log application')

    sub = parser.add_subparsers(title='Commands', metavar='')
    p = sub.add_parser('create-db', help='Create database.')
    p.add_argument('baby', nargs='+')
    p.set_defaults(func=_create_db)

    p = sub.add_parser('migrate', help='Run db migrations')
    p.set_defaults(func=_migrate)

    p = sub.add_parser('runserver', help='Run webserver')
    p.add_argument('--host', default='0.0.0.0')
    p.add_argument('-p', '--port', type=int, default=8000)
    p.set_defaults(func=_run)

    p = sub.add_parser('add-entry', help='Add an entry')
    p.add_argument('-b', '--baby', required=True)
    p.add_argument('-e', '--entry-type', required=True)
    p.add_argument('-S', '--started', required=True)
    p.add_argument('-E', '--ended', required=False)
    p.set_defaults(func=_add_entry)

    args = parser.parse_args()
    args.func(args)
