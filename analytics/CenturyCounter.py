import strava_common.Authorize as authorize
from stravalib import unithelper
import datetime, sys
from ActivityManager import ActivityManager;

"""I annoyingly forget to change rides to the correct bike, but always record my commuting using my vivoactive HR
This automatically flags them as commutes"""

username= "joshua_haley"
type ="Ride"
activities = []


def main(year, month, day):
    """Manual Testing of Scrubbing"""
    start = datetime.datetime(year, month, day)
    if month != 1 and day != 1:
        print("Assuming only single year stats!")
        end = datetime.datetime(year, 12, 31)
    else:
        end = datetime.datetime.now()
    client = authorize.get_authorized_client(username)
    act_manager = ActivityManager(client)
    athlete = client.get_athlete()
    total_road = 0
    total_virtual = 0
    metric_in_meters = 100000
    acts = client.get_activities(after=start, before=end)
    for act in acts:
        if act.external_id is not None:
            if "trainerroad" in act.external_id or "zwift" in act.external_id:
                total_virtual += unithelper.miles(act.distance).get_num()
            elif act.type == 'Ride':
                total_road += unithelper.miles(act.distance).get_num()
        elif act.type == 'Ride':
            total_road += unithelper.miles(act.distance).get_num()

    print("Stats for Period from {} to {}".format(start, end))
    print("Outside distance: " + '{:6.2f}'.format(total_road))
    print("Virtual distance: " + '{:6.2f}'.format(total_virtual))

    #acts = act_manager.get_activities(after=start, distance_min=metric_in_meters);
    count =1;
    print("Century (>100mi) Stats since: " + str(start))
    #acts.reverse()
    for act in acts:
        distance= unithelper.miles(act.distance).get_num()
        if distance >= 100:
            print(str(count) +": distance: " + '{:6.2f}'.format(distance) + " miles on Event: " + act.name + " " + str(act.start_date_local))
            count = count +1

    count = 1


    print("*********************************************************************")
    print("Metric Centuries (>=62mi and <100mi) Stats since: " + str(start))
    for act in acts:
        distance = unithelper.miles(act.distance).get_num()
        if 62 <= distance < 100:
            print(str(count) + ": distance: " + '{:6.2f}'.format(distance) + " miles on Event: " + act.name + " " + str(
                act.start_date_local))
            count = count + 1

    print("Script Source: https://github.com/JHa13y/Strava")



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
    main(year, month, day)