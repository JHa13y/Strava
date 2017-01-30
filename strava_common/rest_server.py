
from flask import Flask
from flask import request

code = "null"


def setup_server():
    app = Flask(__name__)


    @app.route('/authorized', methods=['GET'])
    def authorized():
        global code
        code = request.args.get('code', '')
        return "Authorized!"

    @app.route('/code', methods=['GET'])
    def get_code():
        return str(code)

    app.run(debug=False)

if __name__ == "__main__":
    setup_server()