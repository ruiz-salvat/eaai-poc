import pymongo
import json


class JSONItemService():

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://root:pass@mongodb:27017/')
        self.db = self.client['mongodb_groceries']

    def get_user_items(self, key, user_id):
        collection = self.db[key]
        return list(collection.find({'user_id': user_id}, {'_id': 0}))

    def get_item(self, key, user_id, id):
        item_list = list(filter(lambda x: x['id'] == int(id), self.data[key]))
        if len(item_list) < 1:
            return {'error': 'Item not found'}
        
        item = item_list[0]
        return item

    def create_item(self, key, new_item):
        collection = self.db[key]
        collection.insert_one(new_item)
        del new_item['_id']
        return new_item

    def update_item(self, key, user_id, id, new_item):
        pass

    def delete_item(self, key, user_id, id):
        self.data[key] = list(filter(lambda x: x['id'] != int(id), self.data[key]))
        with open('data.json', 'w') as f:
            json.dump(self.data, f)
        return True


class AIService():

    def __init__(self):
        pass