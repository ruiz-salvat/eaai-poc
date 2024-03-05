from flask import Flask, request
from flask_cors import CORS
import json


app = Flask(__name__)


def __get_next_id(key):
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()
    id_list = list(map(lambda x: x['id'], data[key]))
    try:
        max_id = max(id_list)
        return max_id + 1
    except:
        return 0


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
        
        next_id = __get_next_id('items')
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


@app.route('/recipies', methods=['GET', 'POST'])
def recipies():
    if request.method == 'GET': # TODO: sort by date asc
        with open('data.json', 'r') as f:
            data = json.load(f)
            return data['recipies']
    
    elif request.method == 'POST':
        f = open('data.json', 'r')
        data = json.load(f)
        f.close()
        
        next_id = __get_next_id('recipies')
        new_item = request.json
        new_item['id'] = next_id
        data['recipies'].append(new_item)

        with open('data.json', 'w') as f:
            json.dump(data, f)
        return 'Ok'

    return ''


@app.route('/recipie/<id>', methods=['GET', 'DELETE'])
def recipie(id):
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()
    
    item_list = list(filter(lambda x: x['id'] == int(id), data['recipies']))
    if len(item_list) < 1:
        return 'Item not found'

    if request.method == 'GET':    
        item = item_list[0]
        return item
    
    elif request.method == 'DELETE':
        data['recipies'] = list(filter(lambda x: x['id'] != int(id), data['recipies']))
        with open('data.json', 'w') as f:
            json.dump(data, f)
        return 'Ok'

    return ''


CORS(app)