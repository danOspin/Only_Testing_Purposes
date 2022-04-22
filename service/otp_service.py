from config.mongo_db import MongoApi
from model.otp_object import OtpObject
from flask import Response,Blueprint, json, request
import datetime
class OTPService():
    time_limit = 60
    otp_size = 4

    def __init__(self):
        self.data = {"database": "otp_database",
                     "collection": "otp_collection"}

        self.otp_object = OtpObject()

    def generate_otp(self, user):
        connection = MongoApi(self.data)
        self.otp_object.generate_otp(user,self.time_limit,self.otp_size)
        otp_json = self.otp_object.otp_json()
        response = connection.save_otp(otp_json)
        return {"user":self.otp_object.user_id,"created_date":self.otp_object.utc_to_local(self.otp_object.created_date),"expiring_date":self.otp_object.utc_to_local(self.otp_object.expiring_date),"otp":self.otp_object.otp_pass}

    def validate_otp(self, user,otp):
        connection = MongoApi(self.data)
        connection.get_otp_number()
        self.otp_object(user, self.time_limit, self.otp_size)

        #otp_json = self.otp_object.generate_otp(user,self.time_limit,self.otp_size)
        #response = connection.check_otp_number(otp_json, "Error al guardar en base de datos")
        #return response

    #traer lista de otp filtrado por usuario.
    def list_otp(self, user):
        connection = MongoApi(self.data)
        otp_json = connection.read_by_filter(user)
        response = connection.save_otp(otp_json, "Error al guardar en base de datos")
        return response

    #traer lista de otp filtrado por usuario.
    def check_status_otp(self, user):
        connection = MongoApi(self.data)
        has_valid_otp = connection.check_otp_number(user,datetime.datetime.utcnow())
        return has_valid_otp

    #encontrar otps de usuario seleccionado y traer el otp mayor a la fecha actual
    def find_latest_otp(self, user, otp):
        connection = MongoApi(self.data)
        otp_json = connection.get_otp_number(user,datetime.datetime.utcnow())
        if (otp==otp_json):
            print ("valido")
            return True
        else:
            print("invalido")
            return False

    def change_otp_values(self,data):
        new_size = int(data['otp_size'])
        new_time_limit = int(data['otp_size'])

        if (new_size > 4):
            self.otp_size = (data['otp_size'])

        if (new_time_limit > 30 and new_time_limit < 86400):
            self.otp_size = int(data['time_limit'])

