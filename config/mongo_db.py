from pymongo import MongoClient

class MongoApi:
    def __init__(self,data):
        self.client= MongoClient("mongodb://localhost:5002")
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data=data

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item !='_id' } for data in documents]
        return output

    def write(self, data):
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfull',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfull' if response.modified_count > 0 else "No se ha ejecutado ninguna actualización."}
        return output

    def delete(self, data):
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Documento no encontrado."}
        return output

    def read_by_filter(self,filter):
        documents = self.collection.find(filter)
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def save_otp(self, data, message):
        connection = MongoApi(self.data)
        """key = data['key']
            validation = connection.read_by_filter({key: data['Document'][key]})
            if (len(validation) > 0):
                raise Exception(message)"""
        response = connection.write(data)
        return response