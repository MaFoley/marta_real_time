from google.protobuf.gtfs_realtime_pb2 import * 
import collections,sqlite3
messageFeed = FeedMessage()
conn = sqlite3.connect('marta_schedule.sqlite')
cur = conn.cursor()

class VehicleTripUpdate:
    def __init__(self,entity):
        self._vehicle_label = entity.vehicle.vehicle.label
        self._vehicle_id = entity.vehicle.vehicle.id
        self._trip_id = entity.vehicle.trip.trip_id
        self._route_id = entity.vehicle.trip.route_id
        self._direction_id = entity.vehicle.trip.direction_id
        self._trip_start_date = entity.vehicle.trip.start_date
        self._position_latitude = entity.vehicle.position.latitude
        self._position_longitude = entity.vehicle.position.longitude
        self._position_bearing = entity.vehicle.position.bearing
        self._position_speed = entity.vehicle.position.speed
        self._timestamp = entity.vehicle.timestamp
        self._occupancy_status = entity.vehicle.occupancy_status
    def getTuple(self):
        return (self._vehicle_label
                ,self._vehicle_id
                ,self._trip_id
                ,self._route_id
                ,self._direction_id
                ,self._trip_start_date
                ,self._position_latitude
                ,self._position_longitude
                ,self._position_bearing
                ,self._position_speed
                ,self._timestamp
                ,self._occupancy_status)


with open('tripupdates.pb',"rb") as f:
    messageFeed.ParseFromString(f.read())
sql = 'INSERT INTO real_time_vehicles VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'
for e in messageFeed.entity:
    vehicleTripRecord = VehicleTripUpdate(e)
    cur.execute(sql,vehicleTripRecord.getTuple())
    #if e.vehicle is not None and int(rte_id) <= 21622:
    #print(e,file=open("marta_real_trips.txt","a"))
Location = collections.namedtuple('Location',['latitude','longitude'])
loc = Location(33.871590,-84.381127)

stop_sql = \
'''SELECT stop_id, stop_code, stop_name, stop_lat, stop_lon
FROM stops
WHERE stop_lat - 33.871590 BETWEEN -0.005 AND 0.005
AND stop_lon - -84.381127 BETWEEN -0.005 AND 0.005'''
cur.execute(stop_sql)
stops = cur.fetchall()
print(stops[:10])
conn.close()
"""

import requests
BASE_URL = 'https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/vehicle'
pb_file = requests.get(BASE_URL)
"""
#messages I care about have a Trip, Vehicle, and Position
#create csv loader to make sqlite database of marta schedule



