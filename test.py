#!/usr/bin/env python

from baby_log import app
from baby_log.db import DBModel


def main():
    with DBModel.connect(app) as db:
        #baby = db.add_baby('miles')
        #print 'baby id', baby
        baby = 1
        entry = db.get_entry_type('bottle')

        #db.add_entry(baby, entry)
        for entry in db.entries(baby=1):
            print entry
        db.entries(baby=1, id=2)
        #db.entries(baby=1)
        #db.entries(order='ASC')


if __name__ == '__main__':
    main()
