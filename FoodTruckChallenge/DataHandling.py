from QuadTree import *
# from FoodTruckChallenge.QuadTree import Point, Boundary, QuadTree

import pandas as pd

# TODO: implement convertion between (lat,lon) to (X,Y) coordinates
def coordToXY(lat, lon):
    pass

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
    return Boundary(center, width, height)

def buildDataSet():
    # import file using relative path
    dataset = pd.read_csv('Mobile_Food_Facility_Permit.csv')
    
    # data treatment: for PoC just remove unwanted X,Y coordinates
    # TODO: improve this in the future (remove duplicates, etc)
    cleanDataset = dataset.dropna(subset = ["X", "Y"])

    return cleanDataset

