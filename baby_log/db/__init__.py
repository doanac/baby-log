from baby_log.db.model import DBModel


def db_create(app, babies=[]):
    with DBModel.connect(app) as model:
        with app.open_resource('db/schema.sql', mode='r') as f:
            model._con.executescript(f.read())

        model.add_entry_type('bottle', True)
        model.add_entry_type('sleep', True)
        model.add_entry_type('wet-diaper', False)
        model.add_entry_type('poop-diaper', False)

        for baby in babies:
            model.add_baby(baby)
