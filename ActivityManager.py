import datetime

"""This module should get (and cache) activities from Strava"""


class ActivityManager:
    client = None
    activities_cache ={}

    def __init__(self, client):
        self.client = client

    def get_activities(self, before=None, after=None, bike_id=None, device_name = None, type = "Ride", commute_filter = None, distance_min=None):
        """Returns all activities within the specified time range for an optionally specified bike"""
        #TODO: Cache this result...
        activities = []
        if before is None:
            before = datetime.datetime.now()
        if after is None:
            after = datetime.datetime(2009,1,1)
        acts = self.client.get_activities(after=after, before=before)
        for activity in acts:
            print("Processing Activity: " + str(activity))
            if activity.type == type and (bike_id is None or activity.gear_id == bike_id):
                if (commute_filter is True and activity.commute is True) or commute_filter is None or (commute_filter is False and activity.commute is False):
                    if distance_min is None or activity.distance.num > distance_min:
                        act = self.get_detailed_activity(activity.id)
                        #TODO: This is the spot where I would cache a resol
                        if device_name is None or act.device_name == device_name:
                            activities.append(act)
        return activities

    def get_detailed_activity(self, activity_id):
        #TODO:This is the spot for caching and retrieving cached results...
        act = self.activities_cache.get(activity_id)
        if act is None:
            act = self.client.get_activity(activity_id)
            self.activities_cache[act.id] = act
        return act


    def update_activity(self, activity_id, name=None, activity_type=None,
                            private=None, commute=None, trainer=None, gear_id=None,
                            description=None):
        """Alias of the client updater so we can locally track changes to activities as well"""
        #TODO: Update local cached copy
        act = self.activities_cache[activity_id]

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

        self.client.update_activity(activity_id=activity_id, name=name, activity_type=activity_type, private=private,
                               commute=commute, trainer=trainer, gear_id=gear_id, description=description)