from components.services import JSONItemService
from flask import request, Blueprint


plans_controller = Blueprint('PlansController', __name__, template_folder='controllers')
json_item_service = JSONItemService()


@plans_controller.route('/plans', methods=['GET', 'POST'])
def plans():
    if request.method == 'GET': # TODO: sort by date asc
        return json_item_service.get_all_items('plans')
    
    elif request.method == 'POST':
        new_item = request.json
        return json_item_service.create_item('plans', new_item)

    return ''


@plans_controller.route('/plan/<id>', methods=['GET', 'DELETE'])
def plan(id):
    if request.method == 'GET':
        return json_item_service.get_item('plans', id)
    
    elif request.method == 'DELETE':
        return json_item_service.delete_item('plans', id)

    return ''