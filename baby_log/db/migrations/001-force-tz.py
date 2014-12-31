#!/usr/bin/env python

import dateutil.parser
import pytz


def migrate(app, db):
    us_central = pytz.timezone('US/Central')
    for e in db.entries():
        d = dateutil.parser.parse(e['started'])
        updated = False
        if not d.tzinfo:
            e['started'] = d.replace(
                tzinfo=us_central).astimezone(pytz.utc).isoformat()
            updated = True
        d = e.get('ended')
        if d:
            d = dateutil.parser.parse(d)
            if not d.tzinfo:
                e['ended'] = d.replace(
                    tzinfo=us_central).astimezone(pytz.utc).isoformat()
                updated = True
        if updated:
            db.update_entry(e['id'], e)
