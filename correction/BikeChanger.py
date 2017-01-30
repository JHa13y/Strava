import strava_common.Authorize as authorize

"""I annoyingly forget to change rides to the correct bike, but always record my commuting using my vivoactive HR
This automatically flags them as commutes"""

username= "joshua_haley"
type ="Ride"
activities = []

def main():
    client = authorize.get_authorized_client(username)
    athlete = client.get_athlete()
    print("{id} ".format(id=athlete.username))
    get_activities(client)

def get_activities(client):
        global activities
        acts = client.get_activities()
        for activity in acts:
            print(activity)
            if activity.type == type:
                activities.append(activity)

if __name__ == "__main__":
        main();