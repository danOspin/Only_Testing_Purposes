from flask import Flask, jsonify
import json
from controller.user_controller import app_user


app = Flask(__name__)
app.register_blueprint(app_user)

@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return 'Hello World!'



if __name__ == '__main__':
    app.run()
