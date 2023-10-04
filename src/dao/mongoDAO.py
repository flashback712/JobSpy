from pymongo import MongoClient


class MongoDBHelper:
    def __init__(self,
                 connection_host="mongodb://mongos.mongos:73hck*euuDyU!JXikCTV@172.31.57.134:27017",
                 database_name='indeed'):
        self.client = MongoClient(connection_host)
        self.database = self.client[database_name]

    def disconnect(self):
        if self.client is not None:
            self.client.close()
            self.client = None
            self.database = None

    def insert_one(self, collection_name, data):
        collection = self.database[collection_name]
        result = collection.insert_one(data)
        return result.inserted_id

    def insert_all(self, data_list, collection_name='job_detail'):
        collection = self.database[collection_name]
        result = collection.insert_many(data_list)
        print(f'{len(data_list)} rows inserted into [{collection}].')
        return result.inserted_ids

    def find(self, collection_name, query):
        collection = self.database[collection_name]
        return collection.find(query)
