from stravalib.client import Client
import strava_common.Authorize as authorize
import datetime, sys

username= "joshua_haley"

type ="Ride"
activities = []
bikes = None

def main(year, month, day):
    global activities, bikes
    client = authorize.get_authorized_client(username)
    athlete = client.get_athlete()
    bikes = {}
    for bike in athlete.bikes:
        bikes[bike.id] = bike.name
    print("{id} ".format(id=athlete.username))
    start = datetime.datetime(year, month, day, 0, 0, 0)
    get_activities(client,start)
    write_file()


def get_activities(client, start):
    global activities
    acts = client.get_activities(after=start)
    for activity in acts:
        print(activity)
        if activity.type == type:
            activities.append(activity)

def write_file():
    with open("activities.csv", "w", encoding="utf16") as f:
        f.write("RideName, Date, Distance (m), Avg Speed(m/s), Gear\n")
        for act in activities:
            name = act.name
            date = act.start_date_local
            speed = act.average_speed.num
            distance = act.distance.num
            if act.gear_id in bikes:
                gear = bikes[act.gear_id]
            else:
                gear = "Other"
            f.write("{},{},{},{}, {}\n".format(name, date, distance,speed, gear))




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify the year and optionally the month and day in the form YYYY MM DD")
    now = datetime.datetime.now()
    year = now.year
    month = 1
    day = 1
    if len(sys.argv) >= 2:
        year = int(sys.argv[1])
    if len(sys.argv) >= 3:
        month = int(sys.argv[2])
    if len(sys.argv) >= 4:
        day = int(sys.argv[3])
    main(year, month, day)