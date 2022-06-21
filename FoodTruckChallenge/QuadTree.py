import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

class Point:
    def __init__(self, x, y, userData = None):
        self.x = x
        self.y = y
        self.locationId = userData

    def distanceFromOther(self, point):
        return math.dist([self.x, self.y], [point.x, point.y])


class Boundary:
    def __init__(self, center, width, height):
        self.center = center
        self.width = width
        self.height = height

    def containsPoint(self, point):
        return (
            point.x >= self.center.x - self.width and
            point.x <= self.center.x + self.width and
            point.y >= self.center.y - self.height and
            point.y <= self.center.y + self.height
        )        

    def intersects(self, range):
        return not (
            self.center.x + self.width < range.center.x - range.radius or
            self.center.x - self.width > range.center.x + range.radius or
            self.center.y + self.height < range.center.y - range.radius or
            self.center.y - self.height > range.center.y + range.radius
        )

class Range:
    def __init__(self, center, r = 1):
        self.center = center
        self.radius = r

    def containsPoint(self, point):
        return ( self.center.distanceFromOther(point) < self.radius )

    def draw(self, referencePlot):
        referencePlot.add_patch(Circle((self.center.x, self.center.y), self.radius, edgecolor="green", facecolor="none"))
        


class QuadTree:    
    def __init__(self, boundary, capacity = 1):
        self.points = []
        self.capacity = capacity
        self.boundary = boundary
        self.northWest = None
        self.northEast = None
        self.southWest = None
        self.southEast = None
        self.divided = False

    def insert(self, point):
        #Ignore points that do not belong in this quadrant
        if not self.boundary.containsPoint(point):
            return False # object cannot be added in this quadrant
        
        # If there is space in this quad tree and is yet not divided, add point here
        if (len(self.points) < self.capacity) and (not self.divided):
            self.points.append(point)
            return True
    
        # Otherwise, subdivide and then add the point to whichever node will accept it
        if not self.divided:
            self.subdivide()

        if self.northWest.insert(point):
            return True
        if self.northEast.insert(point):
            return True
        if self.southWest.insert(point):
            return True
        if self.southEast.insert(point):
            return True
    
        # point was not added. (shall never happen)
        # print("error inserting")
        # print("error inserting - point: ", point.x, point.y)
        return False
    

    def subdivide(self):
        xc = self.boundary.center.x
        yc = self.boundary.center.y
        h = self.boundary.height
        w = self.boundary.width
        nw = Boundary(Point(xc - w/2, yc + h/2), w/2, h/2)
        ne = Boundary(Point(xc + w/2, yc + h/2), w/2, h/2)
        sw = Boundary(Point(xc - w/2, yc - h/2), w/2, h/2)
        se = Boundary(Point(xc + w/2, yc - h/2), w/2, h/2)
        
        self.northWest = QuadTree(nw, self.capacity)
        self.northEast = QuadTree(ne, self.capacity)
        self.southWest = QuadTree(sw, self.capacity)
        self.southEast = QuadTree(se, self.capacity)
        self.divided = True

    def queryRange(self, range):
        foundPoints = []
        if not self.boundary.intersects(range):
            return foundPoints # empty array

        # get points in this quadrant
        for p in self.points:
            if range.containsPoint(p):
                foundPoints.append(p)

        # get points in inner quadrants
        if self.divided:
            foundPoints = foundPoints + self.northWest.queryRange(range)
            foundPoints = foundPoints + self.northEast.queryRange(range)
            foundPoints = foundPoints + self.southWest.queryRange(range)
            foundPoints = foundPoints + self.southEast.queryRange(range)

        return foundPoints

    def draw(self, referencePlot):
        x = self.boundary.center.x - self.boundary.width
        y = self.boundary.center.y - self.boundary.height

        # quadrant boundary
        referencePlot.add_patch(Rectangle((x, y), self.boundary.width*2, self.boundary.height*2, edgecolor="black", facecolor="none"))
        
        # center point - REMOVE
        #referencePlot.scatter(x=self.boundary.center.x, y=self.boundary.center.y, color="black")

        # all points in this quadrant
        for p in self.points:
            referencePlot.scatter(x = p.x, y = p.y, color="blue", alpha=1)

        if self.divided:
            self.northWest.draw(referencePlot)
            self.northEast.draw(referencePlot)
            self.southWest.draw(referencePlot)
            self.southEast.draw(referencePlot)

