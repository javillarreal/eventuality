from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import graphene
from flask_graphql import GraphQLView

# set up app
app = Flask(__name__)
app.config.from_object("project.config.Config")
app.debug = True

# set up database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .apps.event.models.category import Category

from .apps.event.schema import Query as eventQuery

class Query(eventQuery):
    pass

schema = graphene.Schema(query=Query)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

@app.route("/")
def hello_world():
    return jsonify(hello="world")
