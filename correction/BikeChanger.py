import strava_common.Authorize as authorize
import datetime

"""I annoyingly forget to change rides to the correct bike, but always record my commuting using my vivoactive HR
This automatically flags them as commutes"""

username= "joshua_haley"
type ="Ride"
activities = []
start=datetime.datetime(2016,1,1,0,0,0)
device_name ='Garmin Vívoactive HR'
argyle_id=""

def main():
    client = authorize.get_authorized_client(username)
    athlete = client.get_athlete()
    global argyle_id
    for b in athlete.bikes:
        if b.name == "Blue Argyle":
            argyle_id = b.id

    print("{id} ".format(id=athlete.username))
    get_activities(client)
    for act in activities:
        print("processing:" + str(act))
        if act.device_name == device_name:
            if act.gear_id != argyle_id:
                client.update_activity(act.id, gear_id=argyle_id)




def get_activities(client):
        global activities
        acts = client.get_activities(after=start)
        for activity in acts:
            print(activity)
            if activity.type == type and activity.gear_id != argyle_id:
                act = client.get_activity(activity.id)
                activities.append(act)

if __name__ == "__main__":
        main();