import argparse
from ActivityManager import ActivityManager
import strava_common.Authorize as authorize

def main(args):
    client = authorize.get_authorized_client(args.username)
    act_manager = ActivityManager(client)
    act = act_manager.get_detailed_activity(args.activity_id)
    stream = client.get_effort_streams(args.activity_id, 'cadence')
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Utility to print bike id and sensor ids for an activity')
    parser.add_argument('username')
    parser.add_argument('activity_id')
    args= parser.parse_args()
    main(args)