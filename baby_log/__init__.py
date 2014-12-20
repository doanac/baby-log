
import flask

app = flask.Flask(__name__)
app.config.from_object('baby_log.flask_config')

import baby_log.db
import baby_log.views.api
import baby_log.views.ui
