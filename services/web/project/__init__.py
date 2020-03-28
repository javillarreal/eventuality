from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .apps.events.models.category import Category

@app.route("/")
def hello_world():
    return jsonify(hello="world")
