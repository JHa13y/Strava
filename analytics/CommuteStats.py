"""
Calculates the amount of commuting done during the specified year and give you a few interesting stats about that
"""

import strava_common.Authorize as authorize
import datetime, sys, argparse
from ActivityManager import ActivityManager;




car_co2_cost=271
bike_co2_cost=21
class CommuteCalculator:
    """
    Class to calculate commuting stats for a single year.
    """
    def __init__(self, username, start, finish = None):
        self.username= username
        self.activities = []
        self.start = start
        self.finish = finish
        self.client = authorize.get_authorized_client(username)
        self.act_manager = ActivityManager(self.client)
        self.athlete = self.client.get_athlete()
        self.bike_distance_breakdown = {}
        self.bikes = {}
        self.bike_distance_breakdown["other"] = 0
        for b in self.athlete.bikes:
            self. bikes[b.id] = b.name
            self.bike_distance_breakdown[b.id] = 0

    def run_stats(self):
        self.acts = self.act_manager.get_activities(after=self.start, before=self.finish, commute_filter=True);

        self.total_distance = 0  ##In Meters
        for act in self.acts:
            self.total_distance += act.distance._num
            if act.gear_id in self.bike_distance_breakdown:
                self. bike_distance_breakdown[act.gear_id] += act.distance._num
            else:
                self.bike_distance_breakdown["other"] += act.distance._num

        self.d_km = self.total_distance / 1000;
        self.d_miles = self.d_km * 0.621371;

    def print(self):
        print("*************************************************************************************")
        print(
            "You commuted " + '{:6.2f}'.format(self.d_miles) + " miles (or " + '{:6.2f}'.format(self.d_km) + " km) since " + str(
                self.start))
        co2_Saved = ((car_co2_cost - bike_co2_cost) * self.d_km) * 0.00220462
        print("You reduced your C02 foot print by " + '{:6.2f}'.format(co2_Saved) + " lbs!")
        print("You used the following gear to commute: ")

        for b in self.athlete.bikes:
            if b.id in self.bike_distance_breakdown:
                if self.bike_distance_breakdown[b.id] < 1:
                    continue
                dist = self.bike_distance_breakdown[b.id] / 1000.0 * 0.621371;
                print('{:6.2f}'.format(dist) + " miles on " + self.bikes[b.id])
        dist = self.bike_distance_breakdown["other"] / 1000.0 * 0.621371;
        print('{:6.2f}'.format(dist) + " miles on Other")

    def get_miles(self):
        return self.d_miles

    def print_comparison(self, other, monthly=False):
        print("By this time last year you had commuted: " + '{:6.2f}'.format(other.get_miles()) + " By this time in the year")

    @staticmethod
    def print_references():
        print("Data Source: https://ecf.com/sites/ecf.com/files/ECF_CO2_WEB.pdf")
        print("Script Source: https://github.com/JHa13y/Strava")


def main(username, compare=False):
    now = datetime.datetime.now()
    year = now.year
    start = datetime.datetime(year, 1, 1)
    c=CommuteCalculator(username, start)
    c.run_stats()
    if not compare:
        c.print()

    if compare:
        finish = datetime.datetime(year-1, now.month, now.day, now.hour, now.minute)
        start2 = datetime.datetime(year-1, 1, 1)
        c2 = CommuteCalculator(username,start=start2, finish=finish)
        c2.run_stats()
        c.print()
        c.print_comparison(c2)

    CommuteCalculator.print_references()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculates Commuting stats for the year and C02 savings')
    parser.add_argument('username')
    parser.add_argument("-c", "--compare",action="store_true", help='Runs a comparison to how far along you were compared to last year')
    args= parser.parse_args()

    main(args.username, args.compare)