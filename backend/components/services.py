import json


class JSONItemService():

    def __init__(self):
        f = open('data.json', 'r')
        self.data = json.load(f)
        f.close()

    def __get_next_id(self, key):
        f = open('data.json', 'r')
        data = json.load(f)
        f.close()
        id_list = list(map(lambda x: x['id'], data[key]))
        try:
            max_id = max(id_list)
            return max_id + 1
        except:
            return 0

    def get_all_items(self, key):
        return self.data[key]

    def get_item(self, key, id):
        item_list = list(filter(lambda x: x['id'] == int(id), self.data[key]))
        if len(item_list) < 1:
            return {'error': 'Item not found'}
        
        item = item_list[0]
        return item

    def create_item(self, key, new_item):
        next_id = self.__get_next_id(key)
        new_item['id'] = next_id
        self.data[key].append(new_item)

        with open('data.json', 'w') as f:
            json.dump(self.data, f)
        return new_item

    def update_item(self, key, item):
        pass

    def delete_item(self, key, id):
        self.data[key] = list(filter(lambda x: x['id'] != int(id), self.data[key]))
        with open('data.json', 'w') as f:
            json.dump(self.data, f)
        return {'msg': 'success'}


class AIService():

    def __init__(self):
        pass