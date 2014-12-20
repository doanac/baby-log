import datetime
import collections
import contextlib
import sqlite3

DATABASE = 'tmp.db'

Baby = collections.namedtuple(
    'Baby', ['id', 'name'])


class DBModel(object):
    def __init__(self, connection):
        self._con = connection

    @staticmethod
    @contextlib.contextmanager
    def connect(app, autocommit=True):
        con = None
        try:
            con = sqlite3.connect(DATABASE)
            yield DBModel(con)
            if autocommit:
                con.commit()
        finally:
            if con:
                con.close()

    def _execute(self, stmt, params=None):
        if params:
            return self._con.cursor().execute(stmt, params)
        return self._con.cursor().execute(stmt)

    def add_baby(self, name):
        cmd = 'INSERT INTO babies(name) values(?)'
        return self._execute(cmd, (name,)).lastrowid

    def get_baby(self, name):
        row = self._execute(
            'SELECT id,name from babies where name=?', (name,)).fetchone()
        if not row:
            raise LookupError('No such baby: ' + name)
        return Baby(row[0], row[1])

    def babies(self):
        stmt = 'SELECT id,name from babies'
        for row in self._execute(stmt):
            yield({'id': row[0], 'name': row[1]})

    def add_entry_type(self, label, supports_duration):
        cmd = 'INSERT INTO entry_type(label, supports_duration) values(?,?)'
        return self._execute(cmd, (label, supports_duration)).lastrowid

    def entry_types(self):
        stmt = 'SELECT id,label,supports_duration from entry_type'
        for row in self._execute(stmt):
            yield({'id': row[0], 'label': row[1], 'supports_duration': row[2]})

    def add_entry(self, baby, entry_type, started=None, ended=None):
        cmd = 'INSERT INTO entries(baby, entry_type, started, ended) ' \
              'values(?,?,?,?)'
        if started is None:
            started = datetime.datetime.now()
        return self._execute(cmd, (baby, entry_type, started, ended)).lastrowid

    def stop_last_entry(self, baby, entry_type):
        ended = datetime.datetime.now()
        stmt = ('UPDATE entries SET ended=? '
                'WHERE baby=? and entry_type=? and '
                ' (ended is null or ended="") '
                'ORDER BY started DESC LIMIT 1')
        return self._execute(stmt, (ended, baby, entry_type)).rowcount == 1

    def entries(self, order='DESC', order_by='started', **kwargs):
        stmt = 'SELECT id,baby,entry_type,started,ended from entries '
        if kwargs:
            stmt += 'WHERE '
            stmt += 'AND '.join(['%s=:%s ' % (x, x) for x in kwargs.keys()])

        stmt += 'ORDER by %s %s' % (order_by, order)
        for row in self._execute(stmt, kwargs):
            yield {'id': row[0], 'baby': row[1], 'entry_type': row[2],
                   'started': row[3], 'ended': row[4]}
