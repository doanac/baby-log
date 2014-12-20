
import flask

app = flask.Flask(__name__)

import baby_log.db
import baby_log.views.api
import baby_log.views.ui
