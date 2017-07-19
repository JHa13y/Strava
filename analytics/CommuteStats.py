import strava_common.Authorize as authorize
import datetime
from ActivityManager import ActivityManager;

"""I annoyingly forget to change rides to the correct bike, but always record my commuting using my vivoactive HR
This automatically flags them as commutes"""

username= "joshua_haley"
type ="Ride"
activities = []
start=datetime.datetime(2017,1,1)
device_name ='Garmin Vívoactive HR'
car_co2_cost=271
bike_co2_cost=21

def main():

    """Manual Testing of Scrubbing"""
    client = authorize.get_authorized_client(username)
    act_manager = ActivityManager(client)
    athlete = client.get_athlete()
    bike_distance_breakdown ={}
    bikes={}
    for b in athlete.bikes:
        bikes[b.id] = b.name
        bike_distance_breakdown[b.id] = 0

    acts = act_manager.get_activities(after=start, commute_filter=True);

    total_distance=0 ##In Meters
    for act in acts:
        total_distance += act.distance._num
        bike_distance_breakdown[act.gear_id] += act.distance._num

    d_km = total_distance/1000;
    d_miles = d_km * 0.621371;

    print("*************************************************************************************")
    print("You commuted " + '{:6.2f}'.format(d_miles) + " miles (or " +'{:6.2f}'.format(d_km) +" km) since " + str(start))
    co2_Saved = ((car_co2_cost - bike_co2_cost) * d_km) * 0.00220462
    print("You reduced your C02 foot print by " + '{:6.2f}'.format(co2_Saved) + " lbs!")
    print("You used the following gear to commute: ")

    for b in athlete.bikes:
        dist = bike_distance_breakdown[b.id]/1000.0 * 0.621371;
        print('{:6.2f}'.format(dist) + " miles on " + bikes[b.id])

    print("Data Source: https://ecf.com/sites/ecf.com/files/ECF_CO2_WEB.pdf")
    print("Script Source: https://github.com/JHa13y/Strava")

if __name__ == "__main__":
    main();