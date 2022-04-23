from.generic_service import GenericService

class UserService(GenericService):
    def __init__(self):
        super().__init__("otp_test","otp_collection","user")

    def generate_otp(self,data):
        self.otp_controller.generate_otp(data)
        #Verificar si usuario existe (o un nivel más arriba)
        return {"otp":"1234","time":"15/04/2022:7:00pm"}