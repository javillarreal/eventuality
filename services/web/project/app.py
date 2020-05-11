import graphene
from project import settings
from flask import Flask, jsonify, render_template, request
from flask_jwt_extended import JWTManager, create_access_token
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

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)


from .apps.event.models.event import Event
from .apps.event.models.eventCategory import EventCategory
from .apps.event.models.eventPromoter import EventPromoter
from .apps.promoter.models.promoter import Promoter
from .apps.promoter.models.prromoterUser import PromoterUser
from .apps.user.models.user import User

from .apps.event.schema import EventQuery
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


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    if not user.check_password(password):
        return jsonify({"msg": "Password incorrect"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


@app.route("/")
def hello_world():
    return render_template('index.html')
