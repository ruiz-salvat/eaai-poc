from components.services import JSONItemService
from flask import request, Blueprint, jsonify
from authlib.integrations.flask_oauth2 import current_token


items_controller = Blueprint('ItemsController', __name__, template_folder='controllers')
json_item_service = JSONItemService()


@items_controller.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        return jsonify(json_item_service.get_all_items('items'))
    
    new_item = request.json
    return jsonify(json_item_service.create_item('items', new_item))


@items_controller.route('/item/<id>', methods=['GET', 'DELETE'])
def item(id):
    if request.method == 'GET':
        return json_item_service.get_item('items', id)
    
    elif request.method == 'DELETE':
        return json_item_service.delete_item('items', id)

    return ''