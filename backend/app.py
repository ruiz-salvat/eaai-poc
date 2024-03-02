from flask import Flask, request
from flask_cors import CORS
import json


app = Flask(__name__)


def __get_next_id():
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()
    id_list = list(map(lambda x: x['id'], data['items']))
    max_id = max(id_list)
    return max_id + 1


@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET': # TODO: sort by date asc
        with open('data.json', 'r') as f:
            data = json.load(f)
            return data
    
    elif request.method == 'POST':
        f = open('data.json', 'r')
        data = json.load(f)
        f.close()
        
        next_id = __get_next_id()
        new_item = request.json
        new_item['id'] = next_id
        data['items'].append(new_item)

        with open('data.json', 'w') as f:
            json.dump(data, f)
        return 'Ok'

    return ''


@app.route('/item/<id>', methods=['GET', 'DELETE'])
def item(id):
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()
    
    item_list = list(filter(lambda x: x['id'] == int(id), data['items']))
    if len(item_list) < 1:
        return 'Item not found'

    if request.method == 'GET':    
        item = item_list[0]
        return item
    
    elif request.method == 'DELETE':
        data['items'] = list(filter(lambda x: x['id'] != int(id), data['items']))
        with open('data.json', 'w') as f:
            json.dump(data, f)
        return 'Ok'

    return ''


CORS(app)