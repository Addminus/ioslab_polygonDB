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
    build: ../Polygon-db/  
    depends_on:  
      - postgis  
      
      
  _replace the build path!_ 
