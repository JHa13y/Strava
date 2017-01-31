from stravalib.client import Client
from flask import Flask
from flask import request
import multiprocessing
import webbrowser
import requests
import time


def get_authorized_client(username):
    client= Client()
    token = get_access_token(username, client)
    client.access_token = token
    return client

def get_access_token(username, client):
    #TODO: Lookup Cached Result
    server_thread = multiprocessing.Process(target=setup_server)
    server_thread.start()

    authorize_url = client.authorization_url(client_id=13057, scope="write", redirect_uri='http://127.0.0.1:5000/authorized')

    webbrowser.open(authorize_url);
    time.sleep(2)
    code = b'No Authorized'
    while code == b'No Authorized':
        try:
            response = requests.get("http://127.0.0.1:5000/code")
            if response.status_code == 200:
                code = response.content
        except requests.exceptions.HTTPError:
            print("waiting for code")


    server_thread.terminate()

    access_token = client.exchange_code_for_token(client_id=13057,
                                                  client_secret='b48d4a0be5e16f97b4e52060252afe4e5bf1293f',
                                                  code=code)

    #TODO: Save Client access Token
    return access_token


def setup_server():
    app = Flask(__name__)
    code = "No Authorized"

    @app.route('/authorized', methods=['GET'])
    def authorized():
        nonlocal code
        code = request.args.get('code', '')
        return "Authorized!"

    @app.route('/code', methods=['GET'])
    def get_code():
        return str(code)

    app.run(debug=False)

if __name__ == "__main__":
    setup_server()