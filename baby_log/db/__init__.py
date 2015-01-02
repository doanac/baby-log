import imp
import os

from baby_log.db.model import DBModel

_here = os.path.abspath(os.path.dirname(__file__))


def db_create(app, babies=[]):
    with DBModel.connect(app) as model:
        with app.open_resource('db/schema.sql', mode='r') as f:
            model._con.executescript(f.read())

        model.add_entry_type('bottle', True)
        model.add_entry_type('sleep', True)
        model.add_entry_type('tummy time', True)
        model.add_entry_type('wet diaper', False)
        model.add_entry_type('poop diaper', False)

        for baby in babies:
            model.add_baby(baby)


def db_migrate(app):
    with DBModel.connect(app) as db:
        db._execute(
            'CREATE TABLE IF NOT EXISTS migrations (name varchar(1024))')

        completed = db._execute('SELECT name from migrations')
        completed = [x[0] for x in completed]

        migrations = os.path.join(_here, 'migrations')
        for m in sorted(os.listdir(migrations)):
            if m.endswith('.py') and m not in completed:
                print('Migrating: ' + m)
                mod = imp.load_source('', os.path.join(migrations, m))
                mod.migrate(app, db)
                db._execute('INSERT INTO migrations values(?)', (m,))
            else:
                print('skipping %s' % m)
