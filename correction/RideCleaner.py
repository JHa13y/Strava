import strava_common.Authorize as authorize
import datetime
from ActivityManager import ActivityManager;

"""I annoyingly forget to change rides to the correct bike, but always record my commuting using my vivoactive HR
This automatically flags them as commutes"""

username= "joshua_haley"
type ="Ride"
activities = []
start=datetime.datetime(2017,1,29)
device_name ='Garmin Vívoactive HR'

def main():
    """Manual Testing of Scrubbing"""
    client = authorize.get_authorized_client(username)
    cleaner = RideCleaner(client);
    athlete = client.get_athlete()
    argyle_id = None
    for b in athlete.bikes:
        if b.name == "Blue Argyle":
            argyle_id = b.id

    cleaner.change_bike(client, bike_id=argyle_id, device_name=device_name,after=start)
    cleaner.set_commutes(client, bike_id=argyle_id, device_name=device_name, after=start)


class RideCleaner:

    act_manager = None
    client = None

    def __init__(self, client):
        self.client = client
        self.act_manager = ActivityManager(client)

    def change_bike(self, bike_id, device_name, before=None, after=None):

        """Scrubs history by pulling down all activities.  It then will set any ride using the
         specified device to use the specified bike"""
        if bike_id is None:
            return
        acts = self.act_manager.get_activities(device_name=device_name, after=after, before=before);
        for act in acts:
            if act.device_name == device_name and act.gear_id != bike_id:
                self.act_manager.update_activity(act.id, gear_id=bike_id)


    def set_commutes(self, bike_id, device_name, before=None, after=None):
        """tags all rides using the specified bike and device to a commute"""
        acts = self.act_manager.get_activities(bike_id=bike_id, device_name=device_name, after=after, before=before, commute_filter=False)
        for act in acts:
            if act.device_name == device_name and act.commute == False:
                print("Updating to commute Activity: " + str(act))
                self.act_manager.update_activity(act.id, commute=True)


if __name__ == "__main__":
        main();