from stravalib.client import Client
import strava_common.common as common
import requests
import webbrowser

def main():
    client = Client()
    authorize_url = client.authorization_url(client_id=13057, redirect_uri='http://127.0.0.1:5000/authorized')

    webbrowser.open(authorize_url);
    code ="null"
    while code =="null":
        print("waiting for code")
        response = requests.get("http://localhost:5000/code")
        if response.status_code == 200:
            code = response.content

    access_token = client.exchange_code_for_token(client_id=13057,
                                                  client_secret='b48d4a0be5e16f97b4e52060252afe4e5bf1293f',
                                                  code=code)

    # Now store that access token somewhere (a database?)
    client.access_token = access_token
    athlete = client.get_athlete()
    print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))

def open_file():
    print("Not yet Implemented")

def print_record():
    print("Not yet Implemented")

if __name__ == "__main__":
        main()