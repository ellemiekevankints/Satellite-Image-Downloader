# this file converts API metdata from SkySat Videos into the SSRLCV params.csv format 

import os
import json
import requests
from requests.auth import HTTPBasicAuth

# pass in API key
os.environ['PL_API_KEY']='PLAK75f5a3397deb4421b656652e0c7ecd8c'

# setup the API key from the `PL_API_KEY` environment variable
PLANET_API_KEY = os.getenv('PL_API_KEY')
item_type = "SkySatVideo"

# setup a session
session = requests.Session()

# authenticate session with username and password
session.auth = (PLANET_API_KEY, "")

# define an AOI bounding box
geojson_geometry = {
  "type": "Polygon",
  "coordinates": [
    [ 
      [-83.38846206665039, 33.920286634865164],
      [-83.35086822509766, 33.920286634865164],
      [-83.35086822509766, 33.95916582840359],
      [-83.38846206665039, 33.95916582840359],
      [-83.38846206665039, 33.920286634865164]
    ]
  ]
}

# get images that overlap with our AOI 
geometry_filter = {
  "type": "GeometryFilter",
  "field_name": "geometry",
  "config": geojson_geometry
}

# API request object
search_request = {
  "item_types": [item_type] ,
  "filter": geometry_filter
}

# fire off the POST request
search_result = \
  requests.post(
    'https://api.planet.com/data/v1/quick-search',
    auth=HTTPBasicAuth(PLANET_API_KEY, ''),
    json=search_request)
  
# returns metadata for all of the videos within out AOI that match our filters
print(json.dumps(search_result.json(), indent=1))
print()

# extract image IDs only
image_ids = [feature['id'] for feature in search_result.json()['features']]
print(image_ids)
print()