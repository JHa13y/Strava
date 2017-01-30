from stravalib.client import Client
import strava_common.Authorize as authorize
import datetime

username= "joshua_haley"
start=datetime.datetime(2017,1,1,0,0,0)
type ="Ride"
activities = []

def main():
    global activities
    client = authorize.get_authorized_client(username)
    athlete = client.get_athlete()
    print("{id} ".format(id=athlete.username))
    get_activities(client)

    f = open_file()
    print_records(f, activities)


def get_activities(client):
    global activities
    acts = client.get_activities(after=start)
    for activity in acts:
        print(activity)
        if activity.type == type:
            activities.append(activity)

def open_file():
    print("Not yet Implemented")

def print_records(file, activities):
    print("Not yet Implemented")

if __name__ == "__main__":
        main()