import random
print("hello world")
import MakeSpaceTower
# import hypar
# Import the classes we'll need.

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC
#from aecSpace.Geometry import aecGeometry
import itertools

import shapely
from shapely.geometry import Point


u"""
A base class for creating sample points located in a given region of interest,
i.e. polygon.
"""

from shapely.geometry import Polygon

class PolygonPointSampler(object):

    def __init__(self, polygon = ''):
        u"""
        Initialize a new PolygonPointSampler object using the specified polygon
        object (as allocated by Shapely). If no polygon is given a new empty
        one is created and set as the base polygon.
        """
        if polygon:
            self.polygon = polygon
        else:
            self.polygon = Polygon()
        self.samples = list()
        self.sample_count = 0
        self.prepared = False

    def add_polygon(self, polygon):
        u"""
        Add another polygon entity to the base polygon by geometrically unifying
        it with the current one.
        """
        self.polygon = self.polygon.union(polygon)
        self.prepared = False

    def print_samples(self):
        u"""
        Print all sample points using their WKT representation.
        """
        for sample_pt in self.samples:
            print(sample_pt)

    def prepare_sampling(self):
        u"""
        Prepare the actual sampling procedure by splitting up the specified base
        polygon (that may consist of multiple simple polygons) and appending its
        compartments to a dedicated list.
        """
        self.src = list()
        if hasattr(self.polygon, 'geoms'):
            for py in self.polygon:
                self.src.append(py)
        else:
            self.src.append(self.polygon)
        self.prepared = True

    def perform_sampling(self):
        u"""
        Create a stub for the actual sampling procedure.
        """
        raise NotImplementedError

def floatrange(start, stop, step):
    while start < stop:
        yield start
        start += step

class RegularGridSampler(PolygonPointSampler):
    def __init__(self, polygon = '', x_interval = 610, y_interval = 610):
        super(RegularGridSampler, self).__init__(polygon)
        self.x_interval = x_interval
        self.y_interval = y_interval

    def perform_sampling(self):
        u"""
        Perform sampling by substituting the polygon with a regular grid of
        sample points within it. The distance between the sample points is
        given by x_interval and y_interval.
        """
        if not self.prepared:
            self.prepare_sampling()
        ll = self.polygon.bounds[:2]
        ur = self.polygon.bounds[2:]
        low_x = int(ll[0]) / self.x_interval * self.x_interval
        upp_x = int(ur[0]) / self.x_interval * self.x_interval + self.x_interval
        low_y = int(ll[1]) / self.y_interval * self.y_interval
        upp_y = int(ur[1]) / self.y_interval * self.y_interval + self.y_interval
        
        for x in floatrange(low_x, upp_x, self.x_interval):
            for y in floatrange(low_y, upp_y, self.y_interval):
                p = Point(x, y)
                if p.within(self.polygon):
                    self.samples.append(p)




spaces = MakeSpaceTower.makeSpaceTower()
#print(spaces)
'''
poly_boundary =[]

for x in spaces:
    poly_boundary.append (x.boundary)
#print(spaces)
#print(poly_boundary)
print(poly_boundary)
'''
def difflayout(space):
    mysampler = RegularGridSampler()
    mysampler.add_polygon(space.boundary)
    mysampler.perform_sampling()
    allpoints = []
    for p in mysampler.samples:
        newpoint = (p.x, p.y, space.center_ceiling.z)
        allpoints.append(newpoint)
    return allpoints

print(difflayout(spaces[0]))
        
    #    mysampler.print_samples()
    #poly_test = poly_boundary[0]