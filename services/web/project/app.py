import graphene
from project import settings
from flask import Flask, jsonify, render_template, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sockets import Sockets
from graphene_file_upload.flask import FileUploadGraphQLView
from graphql_ws.gevent import GeventSubscriptionServer
from flask_graphql import GraphQLView
from flask_cors import CORS


# set up app
app = Flask(__name__)
app.config.from_object("project.config.Config")
app.debug = True

# CORS
CORS(app)

# Sockets
sockets = Sockets(app)

# set up database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)


from .apps.event.models.event import Event, EventPromoter
from .apps.event.models.eventCategory import EventCategory
from .apps.promoter.models.promoter import Promoter, PromoterUser
from .apps.user.models.user import User

from .apps.event.schema import EventQuery, EventMutation, EventSubscription
from .apps.promoter.schema import PromoterMutation, PromoterQuery
from .apps.user.schema import UserQuery, UserMutation


class Query(EventQuery, UserQuery, PromoterQuery):
    pass


class Mutation(UserMutation, PromoterMutation, EventMutation):
    pass


class Subscription(EventSubscription):
    pass


# schema definition
schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)

# graphql base url with file uploads upport
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # to have the GraphiQL interface
    )
)

# graphql subscriptions endpoint setup
subscription_server = GeventSubscriptionServer(schema)
app.app_protocol = lambda environ_path_info: 'graphql-ws'


@sockets.route('/subscriptions')
def echo_socket(ws):
    subscription_server.handle(ws)
    return [] 


# auth route rules
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


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    print('subscriptions!')
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
