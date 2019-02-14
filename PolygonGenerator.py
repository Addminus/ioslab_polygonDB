#52.560, 13.417
#Adding or substracting to the last decimal point changes rastersize in reasonable level

import sys
import psycopg2
from postgis import LineString
from postgis.psycopg import register
import time
from random import randint
import json

# time.sleep(10)

#declare Default starting values
# startLon = 52.503  #y in 2d
# startLat = 13.350 #x in 2d
startLat = 52.453
startLon = 13.290

increment = 0.005
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
        newPoint = [newLon, newLat]
        xArray.append(newPoint)
    pointMatrix.append(xArray)
print("point matrix : " + str(pointMatrix))

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
                # polyWKT = "POLYGON ([(%s; %s; %s; %s; %s)])"%(cornerBL, cornerBR, cornerTL, cornerTR, cornerBL)
                polyWKT = "POLYGON ([(%s; %s; %s; %s; %s)])"%(cornerBL, cornerTL, cornerTR, cornerBR, cornerBL)
                polyWKT = polyWKT.replace("[", "")
                polyWKT = polyWKT.replace("]", "")
                polyWKT = polyWKT.replace(",", "")
                polyWKT = polyWKT.replace(";", ",")
                polyWKTList.append(polyWKT)
                print(polyWKT)


#write polygons to postgis
print("connecting to db")
connected = False
while not connected:
    try:
        connection = psycopg2.connect(host="postgis", port="5432", database="gis", user="docker", password="docker")
        connected = True
    except psycopg2.Error as e:
        print("error while trying to connect to database, retrying...")
        time.sleep(1)
print("connected to db, starting to insert polygons...")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS berlin_polygons")
cursor.execute("CREATE TABLE berlin_polygons (id SERIAL PRIMARY KEY, outline GEOGRAPHY, pollution INTEGER NOT NULL)")
cursor.execute("CREATE INDEX polygon_index ON berlin_polygons USING GIST(outline)")
connection.commit()

for string in polyWKTList:
    ranPoll = randint(1, 10)
    cursor.execute("INSERT INTO berlin_polygons (outline,pollution) VALUES (ST_PolygonFromText('{0}'), {1})".format(string,ranPoll))
connection.commit()

cursor.execute("UPDATE berlin_polygons SET outline=ST_Buffer(outline, 0.0)")
connection.commit()

cursor.execute("SELECT COUNT(id) from berlin_polygons")
print("database populated, number of polygons : " + str(cursor.fetchone()))

# export to json file
# jsonGeom = {
#     "type": "GeometryCollection",
#     "geometries": []
# }
# for geo in cursor:
#     jsonGeom["geometries"].append(json.loads(geo[0]))

# f = open("demofile.json", "w")

# f.write(json.dumps(jsonGeom, separators=(',',':')))
# print(json.dumps(jsonGeom, separators=(',',':')))
# print("bye :)")