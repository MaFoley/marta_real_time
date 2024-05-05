DROP TABLE IF EXISTS routes;
CREATE TABLE routes(
    route_id PRIMARY KEY,
    agency_id,
    route_short_name,
    route_long_name,
    route_desc,
    route_type,
    route_url,
    route_color,
    route_text_color
);
CREATE INDEX routes_pk on routes (route_id);
DROP TABLE IF EXISTS trips;
CREATE TABLE trips(
    route_id REFERENCES routes(route_id),
    service_id,
    trip_id PRIMARY KEY,
    trip_headsign,
    trip_short_name,
    direction_id,
    block_id,
    shape_id,
    wheelchair_accessible,
    bikes_allowed
);
CREATE INDEX trips_pk on trips (trip_id);
DROP TABLE IF EXISTS stops;
CREATE TABLE stops(
    stop_id PRIMARY KEY,
    stop_code,
    stop_name,
    stop_desc,
    stop_lat,
    stop_lon,
    zone_id,
    stop_url,
    location_type,
    parent_station,
    stop_timezone,
    wheelchair_boarding
);
CREATE INDEX stops_pk on stops (stop_id);
DROP TABLE IF EXISTS stop_times;
CREATE TABLE stop_times(
    trip_id,
    arrival_time,
    departure_time,
    stop_id,
    stop_sequence,
    stop_headsign,
    pickup_type,
    drop_off_type,
    shape_dist_traveled,
    timepoint
);
CREATE INDEX stop_times_rel on stop_times (trip_id, stop_id);
DROP TABLE IF EXISTS real_time_vehicles;
CREATE TABLE real_time_vehicles(
    vehicle_label,
    vehicle_id,
    trip_id REFERENCES trip(trip_id),
    route_id REFERENCES route(route_id),
    direction_id,
    trip_start_date,
    position_latitude,
    position_longitude,
    position_bearing,
    position_speed,
    update_timestamp,
    occupancy_status
);
CREATE INDEX real_time_vehicles_pk on real_time_vehicles (vehicle_label);