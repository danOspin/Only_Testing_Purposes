from flask import Response, Blueprint, json, request

from service.user_service import UserService
from service.otp_service import OTPService

app_user = Blueprint('app_user', __name__)
user_service = UserService()
otp_service = OTPService()


@app_user.route('/user', methods=['GET'])
def get_all_users():  # put application's code here
    return Response(response=json.dumps(user_service.get_all()), status=200,
                    mimetype='application/json')


@app_user.route('/user', methods=['POST'])
def save_user():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error":
                                                 "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    if 'key' not in data or data['key'] not in data['Document']:
        return Response(response=json.dumps({"Error":
                                                 "Key not configured"}),
                        status=400,
                        mimetype='application/json')
    try:
        response = user_service.save(data, "Ya existe un usuario para los datos suministrados")
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')
    except Exception as e:
        return Response(response=json.dumps({"message": str(e)}),
                        status=409,
                        mimetype='application/json')


@app_user.route('/user', methods=['PUT'])
def update_user():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    response = user_service.update(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app_user.route('/user', methods=['DELETE'])
def delete_user():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    response = user_service.delete(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app_user.route('/user/byfilter', methods=['POST'])
def get_users_by_filter():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error":
                                                 "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    response = user_service.get_all_by_filter(data['Filter'])
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app_user.route('/user/generate_otp', methods=['POST'])
def generate_otp_per_user():
    data = request.json
    if data is None or data == {} or 'user_id' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    # TODO: Validar que usuario exista
    if not otp_service.has_active_otp(data['user_id']):
        response = otp_service.generate_otp(data['user_id'])
    else:
        response = {"message": "Ya hay otro otp generado"}
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app_user.route('/user/validate_otp', methods=['PUT'])
def validate_otp_per_user():
    data = request.json
    if data is None or data == {} or ('user_id' or 'otp') not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    # TODO: Validamos que usuario exista
    # llamamos al generador de otp y mandamos id
    response = otp_service.validate_otp(data['user_id'], data['otp'])
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app_user.route('/user/list_otp', methods=['GET'])
def list_otp_per_user():
    data = request.json
    if data is None or data == {} or 'user_id' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    response = user_service.generate_otp(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app_user.route('/user/showotp', methods=['GET'])
def get_otp_per_users():  # put application's code here
    return Response(response=json.dumps(user_service.get_all()), status=200,
                    mimetype='application/json')

@app_user.route('/admin/config_otp_values', methods=['PUT'])
def change_otp_values():
    data = request.json
    if data is None or data == {} or ('time_limit' and 'char_limit') not in data:
        return Response(response=json.dumps({"Error": "Ingrese parametros de configuración"}),
                        status=400,
                        mimetype='application/json')
    response = otp_service.change_otp_values(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')
