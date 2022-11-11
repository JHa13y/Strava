import strava_common.Authorize as authorize
import datetime, sys
from ActivityManager import ActivityManager;

"""I annoyingly forget to change rides to the correct bike, but always record my commuting using my vivoactive HR
This automatically flags them as commutes"""

username= "joshua_haley"
type ="Ride"
activities = []
device_name ='Garmin fēnix 5 Plus'


def main(year, month, day):
    """Manual Testing of Scrubbing"""
    start = datetime.datetime(year, month, day)
    client = authorize.get_authorized_client(username)
    cleaner = RideCleaner(client);
    athlete = client.get_athlete()
    argyle_id = None
    for b in athlete.bikes:
        if b.name == "Blue Argyle":
            argyle_id = b.id

    cleaner.change_bike(bike_id=argyle_id, device_name=device_name,after=start)
    cleaner.set_commutes(bike_id=argyle_id, device_name=device_name, after=start)
def fix_trainer(year, month, day):
    """Manual Testing of Scrubbing"""
    device_name ='Zwift'
    start = datetime.datetime(year, month, day)
    client = authorize.get_authorized_client(username)
    cleaner = RideCleaner(client)
    athlete = client.get_athlete()
    bike_id = None
    for b in athlete.bikes:
        if b.name == "Basement POS":
            bike_id = b.id
            break

    cleaner.change_bike(bike_id=bike_id, device_name=device_name,after=start)

def fix_fl_rides(year, month, day):
    """Manual Testing of Scrubbing"""
    device_name = None
    start = datetime.datetime(year, month, day)
    client = authorize.get_authorized_client(username)
    cleaner = RideCleaner(client)
    athlete = client.get_athlete()
    bike_id = None
    for b in athlete.bikes:
        if b.name == "Scwinn World Traveler":
            bike_id = b.id
            break

    cleaner.change_bike(bike_id=bike_id, device_name=device_name,after=start, state='Florida')

class RideCleaner:

    act_manager = None
    client = None

    def __init__(self, client):
        self.client = client
        self.act_manager = ActivityManager(client)

    def change_bike(self, bike_id, device_name, before=None, after=None, state=None):

        """Scrubs history by pulling down all activities.  It then will set any ride using the
         specified device to use the specified bike"""
        if bike_id is None:
            return
        acts = self.act_manager.get_activities(device_name=device_name, after=after, before=before, state=state);
        update =False
        for act in acts:
            if (act.device_name == device_name or device_name == None) and act.gear_id != bike_id:
                self.act_manager.update_activity(act.id, gear_id=bike_id)
                update = True
        if update:
            self.act_manager.serialize_activities_cache()


    def set_commutes(self, bike_id, device_name, before=None, after=None):
        """tags all rides using the specified bike and device to a commute"""
        acts = self.act_manager.get_activities(bike_id=bike_id, device_name=device_name, after=after, before=before, commute_filter=False)
        for act in acts:
            if act.device_name == device_name and act.commute == False:
                print("Updating to commute Activity: " + str(act))
                self.act_manager.update_activity(act.id, commute=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify the year and optionally the month and day in the form YYYY MM DD")
    year=None
    month=1
    day=1
    if len(sys.argv) >= 2:
        year = int(sys.argv[1])
    if len(sys.argv) >= 3:
        month = int(sys.argv[2])
    if len(sys.argv) >= 4:
        day = int(sys.argv[3])
    fix_trainer(year, month, day)
    #fix_fl_rides(year, month, day)
