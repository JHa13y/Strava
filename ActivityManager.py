import datetime
import pickle, argparse, os
import strava_common.Authorize as authorize
from stravalib.model import Activity
import copy

"""This module should get (and cache) activities from Strava"""

pickle_url = "../data/"

class ActivityManager:
    client = None
    activities_cache ={}
    # activities_cache['after'] = str(datetime.datetime(3000, 1, 1))
    # activities_cache['before'] = str(datetime.datetime(1900, 1, 1))

    def __init__(self, client):
        self.client = client
        self.athlete = self.client.get_athlete().username
        #Load Activity Cache from Pickle
        try:
            self.activities_cache = pickle.load(open(self.get_pickle_file(), "rb"))
        except:
            print("Issue reading activity cache for user: " + self.athlete + ". Has their activities been serialized?")

    def get_pickle_file(self):
        return pickle_url + self.athlete + ".pickle"


    def clear_cache(self):
        """
            Deletes the Local Cache file of activities
        """
        filename = self.get_pickle_file()
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("Sorry, I can not remove %s file." % filename)
        pass

    def serialize_activities_cache(self):
        """
        Saves Local cache out to file system, overwriting if necissary
        """
        if not os.path.exists(pickle_url):
            os.makedirs(pickle_url)
        filename = self.get_pickle_file()
        pickle.dump(self.activities_cache, open(filename, "wb"))
        pass


    def get_activities(self, before=None, after=None, bike_id=None, device_name = None, type = "Ride", commute_filter = None, distance_min=None):
        """Returns all activities within the specified time range for an optionally specified bike"""
        #TODO: Figure out a way to not relookup existing activities
        # old_before = datetime.datetime.strptime(self.activities_cache["before"])
        # old_after = datetime.datetime.strptime(self.activities_cache["before"])
        activities = []
        if before is None:
            before = datetime.datetime.now()
        if after is None:
            after = datetime.datetime(2009,1,1)
        acts = self.client.get_activities(after=after, before=before)
        for activity in acts:
            if activity.type == type and (bike_id is None or activity.gear_id == bike_id):
                if (commute_filter is True and activity.commute is True) or commute_filter is None or (commute_filter is False and activity.commute is False):
                    if distance_min is None or activity.distance.num > distance_min:
                        act = self.get_detailed_activity(activity.id)
                        #TODO: This is the spot where I would cache a resol
                        if device_name is None or act.device_name == device_name:
                            activities.append(act)
        self.serialize_activities_cache()
        return activities

    def get_detailed_activity(self, activity_id):
        #TODO:This is the spot for caching and retrieving cached results...
        #act = self.activities_cache.get(activity_id)
        #if act is None:
        act = self.client.get_activity(activity_id)
        #    self.activities_cache[act.id] = act.to_dict()
        # else:
        #     act= Activity.deserialize(act)
        return act


    def update_activity(self, activity_id, name=None, activity_type=None,
                            private=None, commute=None, trainer=None, gear_id=None,
                            description=None):
        """Alias of the client updater so we can locally track changes to activities as well"""
        #TODO: Update local cached copy
        act = self.get_detailed_activity(activity_id)

        if name is not None:
            act.name =name
        if activity_type is not None:
            act.activity_type= activity_type
        if commute is not None:
            act.commute = commute
        if private is not None:
            act.private = private
        if trainer is not None:
            act.trainer = trainer
        if gear_id is not None:
            act.gear_id = gear_id
        if description is not None:
            act.description = description

        self.activities_cache[activity_id] = act

        self.client.update_activity(activity_id=activity_id, name=name, activity_type=activity_type, private=private,
                               commute=commute, trainer=trainer, gear_id=gear_id, description=description)

def clear(username):
    client = authorize.get_authorized_client(username)
    act_manager = ActivityManager(client)
    act_manager.clear_cache()

def populate(username):
    client = authorize.get_authorized_client(username)
    act_manager = ActivityManager(client)
    act_manager.get_activities(before = datetime.datetime.now(), after= datetime.datetime(1900, 1,1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clear/Populate full activity cache of the specified user')
    parser.add_argument('username')
    parser.add_argument("-u", "--username",dest="username", help='Which User Name?')
    parser.add_arguments("-c", "--clear_cache", action="store_true", help="Clears the Cache")
    parser.add_arguments("-p", "--populate_cache", action="store_true", help="Loads the Cache with all history")
    args= parser.parse_args()
    if args.clear_cache and args.populate_cache:
        print("You've selected conflicting options, please only pick one")
    elif args.clear_cache:
        clear(args.username)
    elif args.populate:
        populate(args.username)