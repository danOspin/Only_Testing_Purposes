from config.mongo_db import MongoApi
from model.otp_object import OtpObject
from flask import Response,Blueprint, json, request

class OTPService():
    time_limit = 60
    otp_size = 4

    def __init__(self):
        self.data = {"database": "otp_database",
                     "collection": "otp_collection"}

        self.otp_controller = OtpObject()

    def generate_otp(self, user):
        otp_json = self.otp_controller.generate_otp(user,self.time_limit,self.otp_size)
        response = self.save(otp_json, "Error al guardar en base de datos")
        return response

    def save(self, data, message):
        connection = MongoApi(self.data)
        """key = data['key']
            validation = connection.read_by_filter({key: data['Document'][key]})
            if (len(validation) > 0):
                raise Exception(message)"""
        response = connection.write(data)
        return response
