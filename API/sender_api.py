import requests
import json
from credentials import identity_hash


def main():

    msg = 'Mensaje de prueba'
    data = {'msg': msg}
    hash_id = identity_hash('1')
    data['id'] = '1'
    data['hash'] = hash_id
    resp = requests.post('http://127.0.0.1:5000/post', data=json.dumps(data))
    print(resp.content)


def get():
    requests.get('http://127.0.0.1:5000/get', headers={'host': 'example.com'})


if __name__ == '__main__':
    main()
    """ url = '127.0.0.0:5000'
    url = url + '/post'
    data = '{"name": "Mauro"}'
    data = "'" + data + "'"
    cont_type = "Content-type: application/json"
    cont_type = "'" + cont_type + "'"
    out = sp.check_output(['curl', '-H', cont_type,
                           '-X', 'POST', '-d', data, url])
    print(out)
    """
