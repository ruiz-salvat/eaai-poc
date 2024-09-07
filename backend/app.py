from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from components.models import init_db
from components.controllers.authorization import authorization_controller
from components.controllers.items import items_controller
from components.controllers.recipes import recipes_controller
from components.controllers.plans import plans_controller
from components.controllers.users import users_controller
from components.oauth import CurrentServer


init_db()
app = Flask(__name__)
CurrentServer.init(app)
app.register_blueprint(authorization_controller)
app.register_blueprint(users_controller)
app.register_blueprint(items_controller)
app.register_blueprint(recipes_controller)
app.register_blueprint(plans_controller)
app.secret_key = 'secret'
api = Api(app)


# TODO remove
@app.route('/api_key', methods=['GET'])
def get_api_key():
    f = open('api_key.txt', 'r')
    key = f.read()
    f.close()
    return key


CORS(app)