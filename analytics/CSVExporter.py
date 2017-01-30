from stravalib.client import Client
import strava_common.Authorize as authorize
import datetime

username= "joshua_haley"
start=datetime.datetime(2017,1,1,0, 0, 0)


def main():
    client = authorize.get_authorized_client(username)
    athlete = client.get_athlete()
    print("{id} ".format(id=athlete.username))
    activities = client.get_activities(after=start)
    for activity in activities:
        print(activity)

def open_file():
    print("Not yet Implemented")

def print_record():
    print("Not yet Implemented")

if __name__ == "__main__":
        main()