# ioslab_polygonDB

###### Setup

add this to the docker-compose:

postgis:  
    image: kartoza/postgis  
    environment:  
      - POSTGRES_USER=docker  
      - POSTGRES_PASS=docker  
    ports:  
      - 25432:5432  
  populator:  
    build: _replace with path to polygon generator Dockerfile_  
    depends_on:  
      - postgis  
      
      
      
      
      
 ###### Polygon generator
 
The polygon generator generates a raster based on a starting gps-point.
Starting from the chosen point it generates the raster by incrementing the lat and lon coordinates of the gps-point, therefore the start gps point is the lower left corner of the generated raster.  
The parameters of the raster generation can be changed in the script.

Based on the resulting raster polygons are then created and parsed into the WKT-Format.
These WKT-Polygons are then uploaded to the postgis database.
  
  
  
  
