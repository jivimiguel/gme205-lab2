from spatial import Point
from spatial import PointSet

p = Point("A", 121.0, 14.6)
print(p.id, p.lon, p.lat)
print(p.to_tuple())

r = Point("B", 120.6, 16.4)
print(p.distance_to(r))

q = Point("X", 999, 14)
print(q.id, q.lon, q.lat)

ps = PointSet.from_csv("data/points.csv")
print(ps)
print("Count:", ps.count())

bbox = ps.bbox()
print("Bbox:", (min_lon, min_lat, max_lon, max_lat))

pois = ps.filter_by_tag("POI")
print("POIs:", pois.count())