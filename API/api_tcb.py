from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/get', methods=['GET'])
def get_data():
    return "<h1>Peticion GET<h1>"


@app.route('/post', methods=['POST'])
def post_data():
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            return 'The body is null', 400
        else:
            print(body)
            return 'body full', 400
        return 'A POST has been received', 400
    else:
        return 'A GET has been received', 400


app.run(host='0.0.0.0')
