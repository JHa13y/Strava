import strava_common.Authorize as authorize
import datetime
import ActivityManager;

"""I annoyingly forget to change rides to the correct bike, but always record my commuting using my vivoactive HR
This automatically flags them as commutes"""

username= "joshua_haley"
type ="Ride"
activities = []
start=datetime.datetime(2016,1,1)
device_name ='Garmin Vívoactive HR'

def main():
    """Manual Testing of Scrubbing"""
    client = authorize.get_authorized_client(username)
    athlete = client.get_athlete()
    argyle_id = None
    for b in athlete.bikes:
        if b.name == "Blue Argyle":
            argyle_id = b.id

    #change_bike(client, bike_id=argyle_id, device_name=device_name,after=start)
    set_commutes(client, bike_id=argyle_id, device_name=device_name, after=start)


def change_bike(client, bike_id, device_name, before=None, after=None):
    """Scrubs history by pulling down all activities.  It then will set any ride using the
     specified device to use the specified bike"""
    if bike_id is None:
        return
    acts = ActivityManager.get_activities(client, device_name=device_name, after=after, before=before);
    for act in acts:
        if act.device_name == device_name:
            client.update_activity(act.id, gear_id=bike_id)


def set_commutes(client, bike_id, device_name, before=None, after=None):
    """tags all rides using the specified bike and device to a commute"""
    acts = ActivityManager.get_activities(client, bike_id=bike_id, device_name=device_name, after=after, before=before, commute_filter=False)
    for act in acts:
        if act.device_name == device_name and act.commute == False:
            print("Updating to commute Activity: " + str(act))
            client.update_activity(act.id, commute=True)


if __name__ == "__main__":
        main();