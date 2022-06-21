from turtle import color
from FoodTruckChallenge.QuadTree import *
# from FoodTruckChallenge.QuadTree import Point, Boundary, QuadTree

import pandas as pd
import matplotlib.pyplot as plt
import utm

# def coordToXY(lat, lon):
#     #//Calculates x based on cos of average of the latitudes
#     x, y, zone, ut = utm.from_latlon(lat, lon)
#     return x, y

def buildDataStructure(dataset):
    # create Quadtree with boundaries defined by the input dataset
    boundary = defineAreaBoundary(dataset)
    qtree = QuadTree(boundary)

    #iterates over dataset adding points to the QuadTree
    dataset = dataset.reset_index()  # make sure indexes pair with number of rows
    for index, row in dataset.iterrows():
        point = Point(row['X'], row['Y'], row['locationid'])
        qtree.insert(point)

    return qtree

def defineAreaBoundary(dataset):
    # Get minimun and maximun values from dataset to define Area boundaries
    minX = dataset.X.min()
    maxX = dataset.X.max()
    minY = dataset.Y.min()
    maxY = dataset.Y.max()

    xc = (minX + maxX)/2
    yc = (minY + maxY)/2
    center = Point(xc, yc, None) 

    height = (maxY - yc)
    width = (maxX - xc)

    # print("x1: ", minX)
    # print("x2: ", maxX)
    # print("y1: ", minY)
    # print("y2: ", maxY)

    # print("---")
    # print("xc: ", xc)
    # print("yc: ", yc)
    return Boundary(center, width, height)


dataset = pd.read_csv('Mobile_Food_Facility_Permit.csv')
cleanDataset = dataset.dropna(subset = ["X", "Y"])

qtree = buildDataStructure(cleanDataset)
print("---")
print(qtree.boundary.center.x, qtree.boundary.center.y , qtree.boundary.width, qtree.boundary.height)

dataset.plot.scatter(x="X", y="Y")
plt.scatter(x=qtree.boundary.center.x, y=qtree.boundary.center.y, color="red")
#ax.scatter(x=qtree.boundary.center.x, y=qtree.boundary.center.y, color="red")

pointOfInterest = Point(6013916.72, 2117244.027)
range = Range(pointOfInterest, 1000)
pointsNearby = qtree.queryRange(range)
print(len(pointsNearby))
fig, ax = plt.subplots()
qtree.draw(ax)
range.draw(ax)

ax.scatter(x = pointOfInterest.x, y = pointOfInterest.y, color="red", alpha=1)

for p in pointsNearby:
    ax.scatter(x = p.x, y = p.y, color="green", alpha=1)

plt.show()