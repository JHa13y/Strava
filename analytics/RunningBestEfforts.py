import strava_common.Authorize as authorize
import datetime, sys
from ActivityManager import ActivityManager;

"""I annoyingly forget to change rides to the correct bike, but always record my commuting using my vivoactive HR
This automatically flags them as commutes"""

username= "joshua_haley"


def main():
    start = datetime.datetime(2009, 1, 1)
    client = authorize.get_authorized_client(username)
    act_manager = ActivityManager(client)
    athlete = client.get_athlete()
    best_efforts ={}
    type = "Run"
    acts = act_manager.get_activities(type=type, after=start)
    for act in acts:
        if act.best_efforts is not None:
            for effort in act.best_efforts:
                dist = str(effort.name)
                name = str(act.start_date) + " " + act.name
                value = str(effort.elapsed_time)
                seconds = effort.elapsed_time.seconds
                if dist not in best_efforts:
                    best_efforts[dist]= []
                best_efforts[dist].append([name, value, seconds])

    for key in best_efforts.keys():
        print("Printing Top 5 Efforts for: " + key + " since " + str(start))
        efforts = best_efforts[key]
        sorted_efforts = sorted(efforts, key =lambda tup: tup[2])
        count =0;
        while count <5 and count < len(sorted_efforts):
            print(str(count+1) + ": " + sorted_efforts[count][1] + " -" + sorted_efforts[count][0])
            count += 1
        print("******************************************")
        print("")


    print("Script Source: https://github.com/JHa13y/Strava")

if __name__ == "__main__":
    main()