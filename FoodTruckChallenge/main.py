#!/usr/bin/env python3
from DataHandling import areaBoundaries
from QuadTree import *
#from FoodTruckChallenge import *

boundary = areaBoundaries()
qtree = QuadTree(boundary)

buildQuadTree