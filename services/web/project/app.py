import graphene
from project import settings
from authlib.integrations.flask_client import OAuth
from flask import Flask, jsonify, render_template
from flask_graphql import GraphQLView
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from six.moves.urllib.parse import urlencode

# set up app
app = Flask(__name__)
app.config.from_object("project.config.Config")
app.debug = True


# set up database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from .apps.event.models.category import Category
from .apps.event.schema import EventQuery

from .apps.user.models.user import User
from .apps.user.schema import UserQuery, UserMutation


class Query(EventQuery, UserQuery):
    pass


class Mutation(UserMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # to have the GraphiQL interface
    )
)


@app.route("/")
def hello_world():
    return render_template('index.html')
