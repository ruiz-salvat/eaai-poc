from flask import request, Blueprint, jsonify
from authlib.integrations.flask_oauth2 import current_token
from components.utils import require_oauth


users_controller = Blueprint('UsersController', __name__, template_folder='controllers')


@users_controller.route('/user')
@require_oauth()
def user_profile():
    # if Token model has `.user` foreign key
    user = current_token.user
    return jsonify(user)