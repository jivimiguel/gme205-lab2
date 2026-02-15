import math
import csv
from typing import Iterable, List, Optional, Tuple

class Point:
    def __init__(self, id, lon, lat, name=None, tag=None):
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 abd 90")
        
        self.id = id
        self.lon = lon
        self.lat = lat
        self.name = name
        self.tag = tag

# -------------------------------------------------------------------------------
# Instance methods (behavior belongs to the object)
# -------------------------------------------------------------------------------
    def to_tuple(self) -> tuple[float, float]:
        """
        Return the coordinate as a (lon, lat) tuple,
        """
        return (self.lon, self.lat)
    
    def distance_to(self, other):
        return Point.haversine_m(self.lon, self.lat, other.lon, other.lat)

    # -------------------------------------------------------------------------------
    # Static method (pure spatial math)
    # ---------------------------------------------------------------------------
    @staticmethod
    def harvesine_m(
        lon1: float, lat1: float, lon2: float, lat2: float
    ) -> float:
        """
        Compute the Harvensine distance between two lon/lat pairs in meters.

        Static method because it does not depent on object state
        """
        R = 6_371_000.0 # Earth radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlamba = math.radians(lon2 -lon1)
        
        a = (
            math.sin(dphi / 2) ** 2
            + mat.cos(phi1)
            * math.cos(phi2)
            * math.sin(dlambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    # ----------------------------------------------------------------------------
    # Class method (constructing objects from data)
    # ----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row):
        return cls(
            id=str(row["id"]),
            lon=float(row["lon"]),
            lat=float(row["lat"]),
            name=row.get("name"),
            tag=row.get("tag"),
        )    
    
    def is_poi(self):
        return (self.tag or "").lower() == "poi"

# --------------------------------------------------------------------------------
# Designing a PountSet Spatial Collection
# --------------------------------------------------------------------------------
class PointSet:
    def __init__(self, points):
        self.points = points
    
    @classmethod
    def from_csv(cls, path):
        """
        Red a CSV file and construct a PointSet.
        """
        points = []
        with open(path, newline ="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    p = Point.fromrow(row)
                    points.append(p)
                except ValueError:
                    continue
        return cls(points)
    
    def count(self) -> int:
        """
        Return number of points in the set.
        """
        return len(self._points)
    
    def bbox(self):
        """
        Return (min_lon, min_lat, max_lon, max_lat) for the collection.
        """
        lons = [p.lon for p in self._points]
        lats = [p.lat for p in self._poins]
        return (min(lons), min(lats), max(lons), max(lats))
    
    def filter_by_tag(self, tag):
        """
        Return a New PointSet containing only points with the given tag without mutating the original set.
        """
        tag_lower = (tag or "").lower()
        subset = [p for p in self.points if (p.tag or "").lower() == tag_lower]
        return PointSet(subset)
        