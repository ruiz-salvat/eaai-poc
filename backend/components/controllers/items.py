from components.services import JSONItemService
from flask import request, Blueprint


items_controller = Blueprint('ItemsController', __name__, template_folder='controllers')
json_item_service = JSONItemService()


@items_controller.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET': # TODO: sort by date asc
        return json_item_service.get_all_items('items')
    
    elif request.method == 'POST':
        new_item = request.json
        return json_item_service.create_item('items', new_item)

    return ''


@items_controller.route('/item/<id>', methods=['GET', 'DELETE'])
def item(id):
    if request.method == 'GET':
        return json_item_service.get_item('items', id)
    
    elif request.method == 'DELETE':
        return json_item_service.delete_item('items', id)

    return ''