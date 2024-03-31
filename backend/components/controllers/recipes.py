from components.services import JSONItemService
from flask import request, Blueprint


recipes_controller = Blueprint('RecipesController', __name__, template_folder='controllers')
json_item_service = JSONItemService()


@recipes_controller.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'GET':
        return json_item_service.get_all_items('recipes')
    
    elif request.method == 'POST':
        new_item = request.json
        return json_item_service.create_item('recipes', new_item)

    return ''


@recipes_controller.route('/recipe/<id>', methods=['GET', 'DELETE'])
def recipe(id):
    if request.method == 'GET':
        return json_item_service.get_item('recipes', id)
    
    elif request.method == 'DELETE':
        return json_item_service.delete_item('recipes', id)

    return ''