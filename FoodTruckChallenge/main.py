#!/usr/bin/env python3

import DataHandling as dataHandling
import QuadTree as qtree

import PySimpleGUI as sg
import numpy as np
import random as rd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
def createCanvas(canvasWindow, figure):
    canvas = FigureCanvasTkAgg(figure, canvasWindow)
    canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
    return canvas


def searchForPoints(db, pointOfInterest, ax):
    # clear plot for the new search
    ax.clear()

    # define a range for search in the Area
    # TODO: Improve radius definition (maybe user input)
    pointsNearby = []
    radius = 1000
    range = qtree.Range(pointOfInterest, radius)

    # From requirement, we want at least 5 options for foodtruck
    # so in case the specified range does not contain such number, increase the 
    # range radius so extra points can be retrieved.
    while (len(pointsNearby) < 5):
        range = qtree.Range(pointOfInterest, radius)
        if not db.boundary.intersects(range):
            break
        pointsNearby = db.queryRange(range)
        radius = radius+1000

    # plot the database points
    db.draw(ax)

    # plot the range being searched
    range.draw(ax)

    # plot the points within the range 
    for p in pointsNearby:
        ax.scatter(x = p.x, y = p.y, color="green", alpha=1)
        
    # plot the point of interest, as a reference
    ax.scatter(x = pointOfInterest.x, y = pointOfInterest.y, color="red", alpha=1)

    return pointsNearby

# plot a single point in the Canvas, keeping axes fixed
# just an utility function for better visualization
def plotSinglePoint(boundary, x, y, ax):
    ax.clear()
    ax.scatter(x, y, color="red")
    plt.xlim([boundary.center.x-boundary.width,boundary.center.x+boundary.width])
    plt.ylim([boundary.center.y-boundary.height,boundary.center.y+boundary.height])
            
# Generates a random coordinate (X,Y) based on the Dataset Boundaries 
def generateRandomCoord(boundary, window, values, ax):
    values['X'] = rd.uniform(boundary.center.x - boundary.width, boundary.center.x + boundary.width)
    values['Y'] = rd.uniform(boundary.center.y - boundary.height, boundary.center.y + boundary.height)
    window['X'].Update(values['X'])
    window['Y'].Update(values['Y'])

    plotSinglePoint(boundary,float(values['X']), float(values['Y']), ax)


# User interface
def buildGUI():
    graphColumn = [
        [sg.Text("FoodTruck Graph")],
        [sg.Canvas(key="CANVAS")],
    ]
    searchColumn = [
        [sg.Text("FoodTruck Search. Please, enter your location.")],
        [sg.Text("Location:")],
        [sg.Text('X', size=(5, 1)), sg.InputText(key='X')],
        [sg.Text('Y', size=(5, 1)), sg.InputText(key='Y')],
        [sg.Button("Search"), sg.Button("Get Location"), sg.Text("(Generates a random location within the map)", font="Helvetica 12")],
        [sg.Multiline("", size=(75,10), key='result', font="Helvetica 12")],
    ]
    layout = [
        [
            sg.Column(searchColumn),
            sg.VSeparator(),
            sg.Column(graphColumn),
        ]
    ]
    window = sg.Window("FoodTruckChallenge", layout, location=(0,0), finalize=True, element_justification="center", font="Helvetica 18",)
    
    return window

# Update Result text information with the list of points retrieved
# points are displayed in ascending order based on distance from the point of interest
def updateResult(dataSet, pointOfInterest, pointsNearby, window):
    
    # sort results by distance from the point of interest
    pointsNearby.sort(key = lambda x: x.distanceFromOther(pointOfInterest))
    
    if len(pointsNearby) == 0:
        result = "area is out of range. no foodtrucks nearby"
    elif len(pointsNearby) < 5:
        result = "just a few (" + str(len(pointsNearby)) + ") foodtrucks nearby"
    else:
        result = "found " + str(len(pointsNearby)) + " foodtrucks nearby"

    # fetch point information in dataset and print it to user.
    for p in pointsNearby:
        result += "\nId: " + str(p.locationId)
        result += "\t\tName: " + dataSet.loc[dataSet['locationid'] == p.locationId]['Applicant'].to_string(index=False)
        result += "\t\t\tDistance: " + "{0:.3f}".format(p.distanceFromOther(pointOfInterest))
         
    window['result'].Update(result)


def main():
    # full Dataset: Pandas Dataset storing all information of each foodTruck
    foodTruckDataset = dataHandling.buildDataSet()

    # city Boundary: reference to the area in which points exist
    cityBoundary = dataHandling.defineAreaBoundary(foodTruckDataset)

    # dataStructure: stores QuadTree with points,
    # . points have only coordinates (X,Y) and locationId for each truck
    # . extra data can be queried based on locationId 
    foodTruckDB = dataHandling.buildDataStructure(foodTruckDataset)

    # build FoodTruck GUI
    window = buildGUI()

    # graph plot configuration
    fig = plt.figure(figsize=(5,4), dpi=100)
    ax = fig.add_subplot(111)
    foodTruckGraph = createCanvas(window["CANVAS"].TKCanvas, fig)

    
    while True:
        event, values = window.read()
        if event == "Search":
            pointOfInterest = qtree.Point(float(values['X']), float(values['Y']))
            pointsNearby = searchForPoints(foodTruckDB, pointOfInterest, ax)
            foodTruckGraph.draw()
            updateResult(foodTruckDataset, pointOfInterest, pointsNearby, window)
        if event == "Get Location":
            generateRandomCoord(cityBoundary, window, values, ax)
            foodTruckGraph.draw()
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    main()