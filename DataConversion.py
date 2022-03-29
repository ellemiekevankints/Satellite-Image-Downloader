# this file converts API metdata from SkySat Videos into the SSRLCV params.csv format 

import os
import json
import urllib.request
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

# pass in API key
os.environ['PL_API_KEY']='PLAK75f5a3397deb4421b656652e0c7ecd8c'

# setup the API key from the `PL_API_KEY` environment variable
PLANET_API_KEY = os.getenv('PL_API_KEY')
item_type = "PSScene3Band"

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

# get images acquired within a date range
date_range_filter = {
  "type": "DateRangeFilter",
  "field_name": "acquired",
  "config": {
    "gte": "2021-03-22T00:00:00.000Z",
    "lte": "2022-03-22T00:00:00.000Z"
  }
}

# only get images which have <50% cloud coverage
cloud_cover_filter = {
  "type": "RangeFilter",
  "field_name": "cloud_cover",
  "config": {
    "lte": 0.5
  }
}

# combine our geo, date, cloud filters
combined_filter = {
  "type": "AndFilter",
  "config": [geometry_filter, date_range_filter, cloud_cover_filter]
}

# API request object
search_request = {
  "item_types": [item_type], 
  "filter": combined_filter
}

# fire off the POST request
search_result = \
  requests.post(
    'https://api.planet.com/data/v1/quick-search',
    auth=HTTPBasicAuth(PLANET_API_KEY, ''),
    json=search_request)

# extract image IDs only
image_ids = [feature['id'] for feature in search_result.json()['features']]

# for demo purposes, just grab the first image ID
id0 = image_ids[0]
id0_url = 'https://api.planet.com/data/v1/item-types/{}/items/{}/assets'.format(item_type, id0)

# returns JSON metadata for assets in this ID
result = \
  requests.get(
    id0_url,
    auth=HTTPBasicAuth(PLANET_API_KEY, '')
  )
  
# we want the 'visual_xml' asset
links = result.json()[u"visual_xml"]["_links"]
self_link = links["_self"]
activation_link = links["activate"]

# request activation of the 'visual_xml' asset
activate_result = \
  requests.get(
    activation_link,
    auth=HTTPBasicAuth(PLANET_API_KEY, '')
  )
  
  # in order to download an assent, we first have to activate it
activation_status_result = \
  requests.get(
    self_link,
    auth=HTTPBasicAuth(PLANET_API_KEY, '')
  )

# check to see that the status of the asset is "active"
print(activation_status_result.json()["status"])
print()

# now we can download the image
download_link = activation_status_result.json()["location"]

# move generated metadata file to the associated folder
print(urllib.request.urlretrieve(download_link, 
                                 '/Users/ellemiekevankints/Desktop/SSRL/PlanetAPI/PlanetAPI/XMLfiles/metadata.xml'))
print()

# parse metadata
tree = ET.parse(
  '/Users/ellemiekevankints/Desktop/SSRL/PlanetAPI/PlanetAPI/XMLfiles/metadata.xml'
)
root = tree.getroot()

# dictionary of namespaces
ns = {
    'opt' : 'http://earth.esa.int/opt',
    'eop' : 'http://earth.esa.int/eop',
    'ps' : 'http://schemas.planet.com/ps/v1/planet_product_metadata_geocorrected_level'
}

# the goal tag
tag = '{' + ns['ps'] + '}Acquisition'

# retrieve specified metadata
for elem in root.iter(tag):
    viewAng = elem.find('ps:spaceCraftViewAngle', ns)
    azimAng = elem.find('ps:azimuthAngle', ns)
    print(viewAng.tag + ': ' + viewAng.text)
    print(azimAng.tag + ': ' + azimAng.text)
  

