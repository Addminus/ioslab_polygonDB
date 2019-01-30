#52.560, 13.417
#Adding or substracting to the last decimal point changes rastersize in reasonable level

import sys
import psycopg2
from postgis import LineString
from postgis.psycopg import register
import time

time.sleep(5)

#declare Default starting values
startLon = 52.509  #y in 2d
startLat = 13.376 #x in 2d
increment = 0.001 
rasterCount = 50
pointMatrix = []


print("Polygon generation is starting")

#create gps raster
for y in range(0, rasterCount):
    xArray = []
    newLon = startLon
    if y is 0:
        pass
    else:
        newLon = startLon + (y * increment)
    for x in range(0, rasterCount):
        newLat = startLat + ( x* increment)
        newPoint =[newLon, newLat]
        xArray.append(newPoint)
    pointMatrix.append(xArray)


#create polygons from raster for postgis db
polyWKTList = []
for (yIndex, xArray) in enumerate(pointMatrix):
    if(yIndex is len(pointMatrix)-1):  
        pass
    else: 
        for (xIndex, point) in enumerate(xArray):
            if(xIndex is len(xArray)-1):  
                pass
            else: 
                cornerBL = pointMatrix[yIndex][xIndex]
                cornerBR = pointMatrix[yIndex][xIndex + 1]
                cornerTL = pointMatrix[yIndex + 1][xIndex]
                cornerTR = pointMatrix[yIndex + 1][xIndex + 1]
                polyWKT = "POLYGON ([(%s; %s; %s; %s; %s)])"%(cornerBL, cornerBR, cornerTL, cornerTR, cornerBL)
                polyWKT = polyWKT.replace("[", "")
                polyWKT = polyWKT.replace("]", "")
                polyWKT = polyWKT.replace(",", "")
                polyWKT = polyWKT.replace(";", ",")
                polyWKTList.append(polyWKT)


#write polygons to postgis
connection = psycopg2.connect(host="postgis", port="5432", database="gis", user="docker", password="docker")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS berlin_polygons")
cursor.execute("CREATE TABLE berlin_polygons (id SERIAL PRIMARY KEY, outline GEOGRAPHY)")
cursor.execute("CREATE INDEX polygon_index ON berlin_polygons USING GIST(outline)")
connection.commit()
for string in polyWKTList:
    print(string)
    cursor.execute("INSERT INTO berlin_polygons (outline) VALUES (ST_PolygonFromText('{}'))".format(string))



cursor.execute("SELECT ST_AsText(outline) FROM berlin_polygons")
for geo in cursor:
    print(geo)

