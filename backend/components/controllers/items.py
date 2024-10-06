from components.services import JSONItemService
from flask import request, Blueprint, jsonify
from authlib.integrations.flask_oauth2 import current_token
from components.oauth import require_oauth


items_controller = Blueprint('ItemsController', __name__, template_folder='controllers')
json_item_service = JSONItemService()


@items_controller.route('/items', methods=['GET', 'POST'])
@require_oauth()
def items():
    user = current_token.user

    print('\nuser', flush=True)
    print(user, flush=True)
    print(user.id, flush=True)
    print(user.username, flush=True)

    if request.method == 'GET':
        return jsonify(json_item_service.get_user_items('items', user.id))
    
    new_item = request.json
    new_item['user_id'] = user.id

    return jsonify(json_item_service.create_item('items', new_item))


@items_controller.route('/item/<id>', methods=['GET', 'DELETE'])
def item(id):
    if request.method == 'GET':
        return json_item_service.get_item('items', id)
    
    elif request.method == 'DELETE':
        return json_item_service.delete_item('items', id)

    return ''