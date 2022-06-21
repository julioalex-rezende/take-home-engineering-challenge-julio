import math
from matplotlib.patches import Rectangle, Circle

# Point: 
# . stores only X,Y coordinates and its locationID
# . For extra information, dataset can be queried based on ID 
class Point:
    def __init__(self, x, y, userData = None):
        self.x = x
        self.y = y
        self.locationId = userData

    # calculates the Euclidian distance from 2 points
    def distanceFromOther(self, point):
        return math.dist([self.x, self.y], [point.x, point.y])

# Boundary:
# . defines the Rectangle area in which points will be located.
# . a reference center point, and width/height information
class Boundary:
    def __init__(self, center, width, height):
        self.center = center
        self.width = width
        self.height = height

    # check if a point is within the boundary
    def containsPoint(self, point):
        return (
            point.x >= self.center.x - self.width and
            point.x <= self.center.x + self.width and
            point.y >= self.center.y - self.height and
            point.y <= self.center.y + self.height
        )        

    # checks whether a specific range somehow intersects the boundary
    def intersects(self, range):
        return not (
            self.center.x + self.width < range.center.x - range.radius or
            self.center.x - self.width > range.center.x + range.radius or
            self.center.y + self.height < range.center.y - range.radius or
            self.center.y - self.height > range.center.y + range.radius
        )

# Range:
# . An Circular area centered in a reference point
class Range:
    def __init__(self, center, r = 1):
        self.center = center
        self.radius = r

    # check if a point is within the range boundary 
    def containsPoint(self, point):
        return ( self.center.distanceFromOther(point) < self.radius )

    # plot the range in a reference plot
    def draw(self, referencePlot):
        referencePlot.add_patch(Circle((self.center.x, self.center.y), self.radius, edgecolor="green", facecolor="none"))
        


# QuadTree:
# . A tree data structure which can be divided into 4 new leaves
# . Each leave/branch will have its own capacity
# . if capacity is full, a new division is made
# . when adding a point, the quadrant is checked if the point belongs to it
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

    # add a point to the tree
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

        # recursive incursion to respective quadrants
        if self.northWest.insert(point):
            return True
        if self.northEast.insert(point):
            return True
        if self.southWest.insert(point):
            return True
        if self.southEast.insert(point):
            return True
    
        # point was not added. (shall never happen)
        return False
    
    # divide a leave, creating 4 new ones based on their geometrical location
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

    # Search for points within a Range in the QuadTree
    def queryRange(self, range):
        foundPoints = []
        if not self.boundary.intersects(range):
            return foundPoints # empty array in case of no interception

        # get points in this quadrant
        for p in self.points:
            if range.containsPoint(p):
                foundPoints.append(p)

        # recursively get points in inner quadrants
        if self.divided:
            foundPoints = foundPoints + self.northWest.queryRange(range)
            foundPoints = foundPoints + self.northEast.queryRange(range)
            foundPoints = foundPoints + self.southWest.queryRange(range)
            foundPoints = foundPoints + self.southEast.queryRange(range)

        return foundPoints

    # plot the QuadTree and its points
    def draw(self, referencePlot):
        x = self.boundary.center.x - self.boundary.width
        y = self.boundary.center.y - self.boundary.height

        # quadrant boundary
        referencePlot.add_patch(Rectangle((x, y), self.boundary.width*2, self.boundary.height*2, edgecolor="black", facecolor="none"))

        # all points in this quadrant
        for p in self.points:
            referencePlot.scatter(x = p.x, y = p.y, color="blue", alpha=1)

        # recursively plots inner quadrants
        if self.divided:
            self.northWest.draw(referencePlot)
            self.northEast.draw(referencePlot)
            self.southWest.draw(referencePlot)
            self.southEast.draw(referencePlot)

