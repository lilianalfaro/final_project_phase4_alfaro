from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db


app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment variable

# Register Blueprints
from app.blueprints.safety_observations import safety_observations
from app.blueprints.employees import employees
from app.blueprints.actions import actions
from app.blueprints.dashboard import dashboard
from app.blueprints.reports import reports
# from app.blueprints.runners import runners

app.register_blueprint(safety_observations)
app.register_blueprint(employees)
app.register_blueprint(dashboard)
app.register_blueprint(reports)
app.register_blueprint(actions)


from . import routes

@app.before_request
def before_request():
    g.db = get_db()

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)