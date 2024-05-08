from google.protobuf.gtfs_realtime_pb2 import * 
import collections, geopy.geocoders, sqlite3
messageFeed = FeedMessage()
conn = sqlite3.connect('marta_schedule.sqlite')
conn.row_factory = sqlite3.Row
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


with open('vehiclepositions.pb',"rb") as f:
    messageFeed.ParseFromString(f.read())
sql = 'INSERT INTO real_time_vehicles VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'
for e in messageFeed.entity:
    vehicleTripRecord = VehicleTripUpdate(e)
    cur.execute(sql,vehicleTripRecord.getTuple())
    #if e.vehicle is not None and int(rte_id) <= 21622:
    #print(e,file=open("marta_real_trips.txt","a"))
address_string = '4266 Roswell Rd NE Atlanta, GA 30342'
geolocator = geopy.geocoders.Nominatim(user_agent='marta-real-time')
loc = geolocator.geocode(address_string)

def get_nearby_stops(l: geopy.location.Location, rng: float):
    """rng denoted in degrees of lat/long"""
    lower_latitude = l.latitude - rng
    upper_latitude =  l.latitude + rng
    lower_longitude = l.longitude - rng
    upper_longitude = l.longitude + rng
    stop_sql = \
    f'''SELECT stop_id, stop_code, stop_name, stop_lat, stop_lon 
    FROM stops 
    WHERE CAST(stop_lat AS NUMERIC) BETWEEN {lower_latitude} AND {upper_latitude} 
    AND CAST(stop_lon AS NUMERIC) BETWEEN {lower_longitude} AND {upper_longitude}'''
    return stop_sql
stop_sql = get_nearby_stops(loc,0.005)
cur.execute(stop_sql)
stops = cur.fetchall()
print(stops[:10])
route_id_sql = f'''SELECT DISTINCT route_id FROM ((trips 
INNER JOIN stop_times ON trips.trip_id = stop_times.trip_id )
INNER JOIN stops ON stop_times.stop_id = stops.stop_id) WHERE stops.stop_id = ?'''
chosen_stop_id = stops[0]['stop_id']
cur.execute(route_id_sql, (chosen_stop_id,))
route = cur.fetchall()
vehicle_position_sql = '''
SELECT vehicle_id, route_id, position_latitude, position_longitude, vehicle_label
FROM real_time_vehicles
WHERE route_id = ? '''
cur.execute(vehicle_position_sql,(route[0]['route_id'],))
vehicles = cur.fetchall()
conn.close()
import folium
def draw_map():
    base_map = folium.Map(tiles='CartoDB positron',location= (loc.latitude, loc.longitude), zoom_start=13)
    radius = 10
    for veh in vehicles:
        folium.CircleMarker(
            location=[veh["position_latitude"],veh["position_longitude"]],
            radius=radius,
            color="green",
            stroke=False,
            fill=True,
            fill_opacity=0.6,
            opacity=1,
            popup="{} pixels".format(radius),
            tooltip=veh["vehicle_label"],
        ).add_to(base_map)
    for stop in stops:
        folium.CircleMarker(
            location=[stop["stop_lat"],stop["stop_lon"]],
            radius=radius,
            color="cornflowerblue",
            stroke=False,
            fill=True,
            fill_opacity=0.6,
            opacity=1,
            popup="{} pixels".format(radius),
            tooltip=stop["stop_name"],
        ).add_to(base_map)
    base_map.save('base_map.html')
draw_map()
"""
import requests
BASE_URL = 'https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/vehicle'
pb_file = requests.get(BASE_URL)
"""
#messages I care about have a Trip, Vehicle, and Position
#create csv loader to make sqlite database of marta schedule



