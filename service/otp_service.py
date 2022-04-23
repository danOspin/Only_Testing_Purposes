from config.mongo_db import MongoApi
from model.otp_object import OtpObject
from flask import Response, Blueprint, json, request
import datetime


class OTPService:
    time_limit = 180
    otp_size = 4

    def __init__(self):
        self.data = {"database": "otp_database",
                     "collection": "otp_collection"}
        self.otp_object = OtpObject()

    def generate_otp(self, user):
        connection = MongoApi(self.data)
        self.otp_object.generate_otp(user, self.time_limit, self.otp_size)
        otp_json = self.otp_object.otp_json()
        response = connection.save_otp(otp_json)
        return {"user": self.otp_object.user_id,
                "created_date": self.otp_object.utc_to_local(self.otp_object.created_date),
                "expiring_date": self.otp_object.utc_to_local(self.otp_object.expiring_date),
                "otp": self.otp_object.otp_pass}

    def validate_otp(self, user, otp):
        connection = MongoApi(self.data)
        response = connection.otp_validation(user, datetime.datetime.utcnow(), otp)
        # Aquí devolver 3 casos. vencido, incorrecto y correcto.
        if (response['Status'] == 'Successfull'):
            output = {'Message': 'OTP Validado correctamente'}
        elif (response['Status'] == 'Expired'):
            output = {'Message': 'OTP Expiró. Genere uno nuevo.'}
        elif (response['Status'] == 'Invalid'):
            output = {'Message': 'Mantenimiento.'}
        # otp_json = self.otp_object.generate_otp(user,self.time_limit,self.otp_size)
        # response = connection.check_otp_number(otp_json, "Error al guardar en base de datos")
        return output

    # traer lista de otp filtrado por usuario.
    def list_otp(self, user):
        connection = MongoApi(self.data)
        otp_json = connection.read_by_filter(user)
        response = connection.save_otp(otp_json, "Error al guardar en base de datos")
        return response

    # traer lista de otp filtrado por usuario.
    def has_active_otp(self, user):
        connection = MongoApi(self.data)
        otp_object_obtained = connection.active_otp_per_user(user, datetime.datetime.utcnow())
        if (otp_object_obtained == []):
            return False
        else:
            return True

    def show_otp_per_user(self, user):
        connection = MongoApi(self.data)
        otp_object_obtained = connection.active_otp_per_user(user, datetime.datetime.utcnow())
        if (otp_object_obtained == []):
            return False
        else:
            return True

    # encontrar otps de usuario seleccionado y traer el otp mayor a la fecha actual
    def find_latest_otp(self, user, otp):
        connection = MongoApi(self.data)
        otp_json = connection.get_otp_number(user, datetime.datetime.utcnow())
        if (otp == otp_json):
            print("valido")
            return True
        else:
            print("invalido")
            return False

    def change_otp_values(self, data):
        if 'otp_size' in data:
            new_size = int(data['otp_size'])
        if 'time_limit' in data:
            new_time_limit = int(data['time_limit'])
        if (new_size > 4):
            self.otp_size = new_size
        if (new_time_limit > 30 and new_time_limit < 86400):
            self.time_limit = new_time_limit
        return {
            'Message': 'Parameters for otp_size: {0} and for time_limit: {1}'.format(self.otp_size, self.time_limit)}
