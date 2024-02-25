from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)

@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        with open('data.json', 'r') as f:
            data = json.load(f)
            return data
    elif request.method == 'POST':
        f = open('data.json', 'r')
        data = json.load(f)
        f.close()
        data['items'].append(request.json)
        with open('data.json', 'w') as f:
            json.dump(data, f)

    return ''

@app.route('/item/<id>', methods=['GET', 'DELETE'])
def item(id):
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()
    
    item_list = list(filter(lambda x: x['id'] == int(id), data['items']))
    if len(item_list) < 1:
        return 'Item not found'
    item = item_list[0]

    if request.method == 'GET':
        return item
    elif request.method == 'DELETE':
        return 'Ok'

    return ''

CORS(app)