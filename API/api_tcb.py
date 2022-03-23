from flask import Flask, jsonify, request
import ast
from werkzeug.security import check_password_hash
from hashlib import sha256
from config import AUTH_param, CONFIDENTIALITY, INTEGRITY

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'my-secret-key'


@app.route('/get', methods=['GET'])
def get_data():
    return "<h1>Peticion GET<h1>"


@app.route('/post', methods=['POST'])
def post_data():
    secret = 'ClaveSecreta'

    if request.method == 'POST':
        body = request.get_data()
        if body is None:
            return 'The body is null', 400
        else:
            body = body.decode()
            msg_dict = ast.literal_eval(body)
            if CONFIDENTIALITY == 1:
                pass
            if INTEGRITY == 1:
                pass
            if AUTH_param == 1:
                identity_auth(msg_dict, secret)

            return 'ACK', 400
        return 'A POST has been received', 400
    else:
        return 'A GET has been received', 400


def identity_auth(msg_dict, secret):
    h = sha256()
    h.update(bytes(msg_dict['id']+secret, 'utf-8'))
    hash_compare = h.hexdigest()
    if(hash_compare == msg_dict['hash']):
        print('Autenticado')
    else:
        print('Autenticación incorrecta')


app.run(host='0.0.0.0')
