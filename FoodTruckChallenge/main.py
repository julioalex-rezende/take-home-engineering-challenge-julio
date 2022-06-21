#!/usr/bin/env python3
from tkinter import Scrollbar
import DataHandling as dataHandling
import QuadTree as qtree

from distutils.command.build import build
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

# plot
def searchForPoints(db, pointOfInterest, ax):
    ax.clear()

    pointsNearby = []
    radius = 1000
    range = qtree.Range(pointOfInterest, radius)

    while (len(pointsNearby) < 5):
        range = qtree.Range(pointOfInterest, radius)
        if not db.boundary.intersects(range):
            break
        print("trying with range = ", radius)
        pointsNearby = db.queryRange(range)
        radius = radius+1000

    db.draw(ax)
    range.draw(ax)
    for p in pointsNearby:
        ax.scatter(x = p.x, y = p.y, color="green", alpha=1)
        
    ax.scatter(x = pointOfInterest.x, y = pointOfInterest.y, color="red", alpha=1)

    return pointsNearby

def plotSinglePoint(boundary, x, y, ax):
    ax.clear()
    ax.scatter(x, y, color="red")
    plt.xlim([boundary.center.x-boundary.width,boundary.center.x+boundary.width])
    plt.ylim([boundary.center.y-boundary.height,boundary.center.y+boundary.height])
            

def generateRandomCoord(boundary, window, values, ax):
    values['X'] = rd.uniform(boundary.center.x - boundary.width, boundary.center.x + boundary.width)
    values['Y'] = rd.uniform(boundary.center.y - boundary.height, boundary.center.y + boundary.height)
    window['X'].Update(values['X'])
    window['Y'].Update(values['Y'])

    plotSinglePoint(boundary,float(values['X']), float(values['Y']), ax)



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

def updateResult(dataSet, pointOfInterest, pointsNearby, window):
    
    # sort results by distance from the point of interest
    pointsNearby.sort(key = lambda x: x.distanceFromOther(pointOfInterest))
    
    if len(pointsNearby) == 0:
        result = "area is out of range. no foodtrucks nearby"
        window['result'].Update(result)
        return
    elif len(pointsNearby) < 5:
        result = "just a few (" + str(len(pointsNearby)) + ") foodtrucks nearby"
    else:
        result = "found " + str(len(pointsNearby)) + " foodtrucks nearby"
    
    print(dataSet.loc[dataSet['locationid'] == pointsNearby[0].locationId]['Applicant'])

    for p in pointsNearby:
        result += "\nId: " + str(p.locationId)
        result += "\t\tName: " + dataSet.loc[dataSet['locationid'] == p.locationId]['Applicant'].to_string(index=False)
        result += "\t\t\tDistance: " + "{0:.3f}".format(p.distanceFromOther(pointOfInterest))
        
 
    window['result'].Update(result)

    pass

def main():
    # full Dataset: Pandas Dataset storing all information of each foodTruck
    foodTruckDataset = dataHandling.buildDataSet()
    cityBoundary = dataHandling.defineAreaBoundary(foodTruckDataset)
    # dataStructure: stores QuadTree with points, that have the coordinates (X,Y) and locationId for each truck
    foodTruckDB = dataHandling.buildDataStructure(foodTruckDataset)

    # build FoodTruck GUI
    window = buildGUI()
    # fig = matplotlib.figure.Figure(figsize=(5,4), dpi=100)
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