import strava_common.Authorize as authorize
import datetime
from ActivityManager import ActivityManager;

"""I annoyingly forget to change rides to the correct bike, but always record my commuting using my vivoactive HR
This automatically flags them as commutes"""

username= "joshua_haley"
type ="Ride"
activities = []
start=datetime.datetime(2017,1,1)


def main():

    """Manual Testing of Scrubbing"""
    client = authorize.get_authorized_client(username)
    act_manager = ActivityManager(client)
    athlete = client.get_athlete()

    century_in_meters=160934
    metric_in_meters = 100000

    acts = act_manager.get_activities(after=start, distance_min=metric_in_meters);
    count =1;
    print("Century (>100mi) Stats since: " + str(start))
    acts.reverse()
    for act in acts:
        distance= act.distance._num / 1000 * 0.621371;
        if distance >= 100:
            print(str(count) +": distance: " + '{:6.2f}'.format(distance) + " miles on Event: " + act.name + " " + str(act.start_date_local))
            count = count +1

    count = 1


    print("*********************************************************************")
    print("Metric Centuries (>=62mi and <100mi) Stats since: " + str(start))
    for act in acts:
        distance = act.distance._num / 1000 * 0.621371
        if distance < 100:
            print(str(count) + ": distance: " + '{:6.2f}'.format(distance) + " miles on Event: " + act.name + " " + str(
                act.start_date_local))
            count = count + 1

    print("Script Source: https://github.com/JHa13y/Strava")




if __name__ == "__main__":
    main();