# Take Home Engineering Challenge

## Project Decisions

### Language - Python
- The candidate is **NOT** familiar with the selected language, but he considered the benefits it could bring to the solution and decided for choosing it. It was a great opportunity to also learn/become familiar with it. Therefore, though the solution works, there may be better ways of doing some of the considered steps.
- Python was the language of choice, as it is well-known for quick PoC code and its comunity collaboration making it possible to import libraries that could help the solution.
- Python also offers an easy way to plot data, characteristic that turned out to be pretty useful during validation and visualization of results
- The candidate is familiar with Database concepts, and had a short experience with Pandas Dataset in the past. He considered this as a good option for the data handling and decided for implementing it in Python.

### Dataset - Pandas
- Pandas provides useful functionalities for data handling, and a easy API for importing data.
- Data querying is also pretty straightforward (disregarding the learning curve with syntax). Therefore the Data Structure selected for this solution does not need to store every information that belongs to the foodtrucks. By storing just the foodTrucks' ids, any query can be made to the database in a post-process stage (after the points have been searched). This reduces memory consumption from the Data structure and the query is performed only to the relevant points.

### Data Structure: QuadTree
- First idea that comes to mind is to calculate distance between a point and all the others, sort the result by distance and return the result. Though this solution works, it does not scale well. Given that each search would require O(n) computations, increasing the number of queries would result into O(n2).
- QuadTree search require O(log n) computation, which will work better for the scalability scenario.
	- There is an overhead on building and adding items to the QuadTree. However the benefit on the search is a reason worthy having this overhed.
	- Additionally, Since it's expected that the dataset wouldn't change as frequently, this overhead would be experienced only once (or when we have a dataset uptdate). The number of requests is expected to be considerably higher than the dataset update.
	- Searching the QuadTree looking for ranges of intersection alsos avoid unecessary calculations of points outside those boundaries.
- Working together with Pandas Dataset, the QuadTree stores only the point location and its ID. Extra information can be queried through Pandas 

## Requirements

A python 3.7 or later installation
pip install --upgrade pandas
pip install matplotlib
pip install PySimpleGUI

a _requirements.txt_ file is included in the repository.
Packages can be installed by running the following command:

    - pip install -r requirements.txt

To run the program. call the main.py file from terminal using _python3_ command
	- python3 main.py

## Use Flow

There are 3 core steps in this project flow:
	- DataSet creation/Data Preparation
	- Construction of the QuadTree and Points Insertion
	- Querying the QuadTree for points within an specified range.
The 2 first steps are done only once, when the program starts.
- **Dataset Creation**

Dataset Creation is the process of loading the CSV file into a pandas dataset. This dataset is available during the whole program and any information about a foodTruck can be retrieved based on its respective locationId.
Some cleanup is performed to this dataset to avoid unwanted points. More on this can be done in future releases.

- **Quadtree construction and Points Insertion**

The QuadTree was designed as a squared region having a reference center point and boundaries(width and height) using the loaded dataset.
As its boundaries are the loaded dataset, we can assert that all points will be within these limits.
Points are then loaded one-by-one to the QuadTree. When inserting a point in a Quadrant, bound-checking is performed, therefore a point is only inserted in the quadrant in which it belongs
In case a quadrant reaches full capacity, it is then subdivided into 4 new quadrants. Each quadrant is also a QuadTree.
At the end, the entire tree is created, and the subdivisions are made only at the points that have required an extra space.

- **Querying the QuadTree for points within a range**

By user input (either by writing or generating a random (X,Y) coordinate), a range is created as a Circular region having the point of interest as reference and a default radius of 1000 (this number was an arbitrary decision for this project). 
Before the query itself, the point of interest is plotted in red just as a visual aid for the user to see where in the chart the point will be located.
The QuadTree is then queried to fetch all points within the intersection between itself and the circular range.
	- In case this intersection returns less than 5 points (project requirement), a new range is created with an bigger radius (increment of 1000 'units') until we get 5 (or more) points.
	- in case the range and tree do not intersect, the point of interest is out-of-bounds, so it does not return any points
	
The result from the query is an array of Points. And the final output is this array sorted by ascending distance from the Point of Interest.
The GUI displays a list of points with their IDs, Names and Distances. This can be expanded to fetch other data (looking into Pandas dataset)
The GUI also plots the entire area. with the points scattered around the plot (blue dots), the QuadTree subdivisions (black rectangles), the Point of Interest (red dot) and the Range queried (green circle.). It also plots the resulting points within the range as green dots.


## Trade-offs/Limitations
### Data Units/Measurements
- The dataset provides latitude-longitude coordinates, and also (X,Y) coordinates. This project considers the (X,Y) coordinates only, and a translation must be done so (lat,lon) can be used. This is one of the enhancements proposed.
- Distances between points were also considered as (X,Y) coordinates. The values displayed are the Euclidian distance between 2 points. Conversion to Miles/Km is a nice improvement for future releases
- These information, however, do not block the algorithm evaluation and it's a matter of applying the right conversion formulas to present the intended values.

### Data Cleanup
- only a simple cleanup was made to the dataset. which is to remove points that do not have their respective (X,Y) direction.
- More can be made, such as outliers and duplicates removal, if that is expected from the dataset.
- As each entry has it's locationId attribute, they were all considered as different points regardless of the extra information held.

### GUI
- A quite simple GUI was elaborated just for the purpose of presenting the results.
- no error handling was made on to prevent user to add wrong information to input fields
- The button "Get Location" was added to allow random locations within the boundary to be selected, as a way of quick testing the tool and visualize results. To test an out-of-boundary value, user must change the fields to something greater than the boundary (such as gererating a random location and adding one digit to one of the coordinate points)
- The result TextArea just lists the retrieved points ascending by distance, as an example that any data can be retrieved having the point locationId. To provide a more comprehensive information, this can be reviewed and/or extra methods can be added to this API

## Testing
- Validation for this project was made through visualization of the Area/Points being plotted.
- The chart presented by the GUI gives a good view of the algorithm being applied
- When running, we can experience some delay while plotting the result data. This was not expected since the dataset is not considerably big. Investigation is needed to check whether is a regular drawning bottleneck or if the algorithm has a missing bit.
- Unfortunately, no unit test was made for this project so far. This is also a enhancement proposal.

## Proposed Improvements
- Generate unit tests to validate data structure (quadTree)
- convert units to use real Coordinates based on (lat,lon)
- Improve GUI, adding error handlings as well as mouse interaction to select a point
- make use of APIs such as Google Maps to enhance user experience
- convert "Get Location" button flow into a actual location retrieving algorithm
- Increment result adding more relevant information for each foodtruck (Depending on requirements)
- Remove some hard coded code (quadTree capacity, range radius), providing parametrization and/or allowing user to decide 