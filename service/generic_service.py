from config.mongo_db import MongoApi

class GenericService:
    def __init__(self,database,collection,type):
        self.data = {"database":database,
                         "collection":collection}
        self.type = type

    def get_all(self):
        connection = MongoApi(self.data)
        response = connection.read_by_filter({"type":self.type})
        return response

    def save(self,data,message):
        connection = MongoApi(self.data)
        key = data['key']
        validation = connection.read_by_filter({key:data['Document'][key]})
        if(len(validation)>0):
            raise Exception(message)
        data['Document']['type']=self.type
        response = connection.write(data)
        return response

    def update(self, data):
        self.data['Filter']=data['Filter']
        self.data['DataToBeUpdated'] = data['DataToBeUpdated']
        connection = MongoApi(self.data)
        response = connection.update()
        return response

    def delete(self, data):
        connection = MongoApi(self.data)
        response = connection.delete(data)
        return response

    def get_all_by_filter(self,filter):
        connection = MongoApi(self.data)
        response = connection.read_by_filter(filter)
        return response

