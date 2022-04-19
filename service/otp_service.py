from config.mongo_db import MongoApi
from model.otp_object import OtpObject
from flask import Response,Blueprint, json, request

class OTPService():
    time_limit = 60
    otp_size = 4

    def __init__(self):
        self.data = {"database": "otp_database",
                     "collection": "otp_collection"}

        self.otp_object = OtpObject()

    def generate_otp(self, user):
        otp_json = self.otp_object.generate_otp(user,self.time_limit,self.otp_size)
        response = self.save(otp_json, "Error al guardar en base de datos")
        return response

    def validate_otp(self, user):
        otp_json = self.otp_object.generate_otp(user,self.time_limit,self.otp_size)
        response = self.read_by_filter(otp_json, "Error al guardar en base de datos")
        return response

    #traer lista de otp filtrado por usuario.
    def list_otp(self, user):
        otp_json = MongoApi.read_by_filter(user)
        response = self.save(otp_json, "Error al guardar en base de datos")
        return response

    #traer lista de otp filtrado por usuario.
    def change_status_otp(self, user):
        otp_json = MongoApi.read_by_filter(user)
        response = self.save(otp_json, "Error al guardar en base de datos")
        return response

    #encontrar otps de usuario seleccionado y traer el otp mayor a la fecha actual
    def find_latest_otp(self, user):
        otp_json = MongoApi.read_by_filter(user)
        response = self.save(otp_json, "Error al guardar en base de datos")
        return response

    def change_otp_values(self,data):
        new_size = int(data['otp_size'])
        new_time_limit = int(data['otp_size'])

        if (new_size > 4):
            self.otp_size = (data['otp_size'])

        if (new_time_limit > 30 and new_time_limit < 86400):
            self.otp_size = int(data['time_limit'])

