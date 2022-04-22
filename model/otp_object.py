import string
import datetime
import random


class OtpObject():
    def __init__(self):
        self.user_id = None
        self.created_date = datetime.datetime.utcnow()
        self.expiring_date = datetime.datetime.utcnow()
        self.otp_pass = ""
        self.used = False
        self.time_limit = 60
        self.otp_size = 4

    def generate_pass(self, user, time_limit,otp_size):
        #Se limitan dígitos para caso de 4 caracteres.
        random_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        if (otp_size==4):
            random_chars = string.digits

        self.otp_pass = ''.join([random.choice(random_chars)
                                 for n in range(otp_size)])
        print("Código generado "+self.otp_pass)
        self.created_date = datetime.datetime.utcnow()
        print(self.created_date)
        self.expiring_date = self.created_date + datetime.timedelta(0,time_limit)
        print(self.expiring_date)
        self.user_id = user

    def generate_otp(self,user,time_limit,otp_size):
        self.generate_pass(user,time_limit,otp_size)
        return self.otp_json()

    def otp_json(self):
        otp_to_json = {}
        otp_to_json['user_id']=self.user_id
        otp_to_json['created_date']=self.created_date
        otp_to_json['expiring_date'] = self.expiring_date
        otp_to_json['otp_pass'] = self.otp_pass
        otp_to_json['used'] = self.used
        otp_to_json['type'] = "otp"
        return {'Document': otp_to_json}

    def utc_to_local(self, utc_dt):
        return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
