# this file converts the PlanetAPI.csv to params.csv

import pandas as pd
import datetime
import math
import time

input = pd.read_csv(
    r'InputCSV/frame_index.csv')

filename = input['name'].values.tolist()

# convert datetime string to UNIX timestamp
timestamp = input['datetime'].values.tolist()
for i in range(len(timestamp)):
    unixtime = time.mktime(datetime.datetime.strptime(timestamp[i], '%Y-%m-%dT%H:%M:%SZ').timetuple())
    unixtime = int(unixtime)
    timestamp[i] = unixtime

xfov = [2.8 * (math.pi/180), 2.8 * (math.pi/180)] # convert deg to rad
yfov = [2.8 * (math.pi/180), 2.8 * (math.pi/180)] # convert deg to rad
xsize = [6.5, 6.5] # nanometers
ysize = [6.5, 6.5] # nanometers
foc = [3.6, 3.6] # meters

xpos = input['x_sat_eci'].values.tolist()
ypos = input['y_sat_eci'].values.tolist()
zpos = input['z_sat_eci'].values.tolist()

# still need x, y, z rotation and x, y pixel count
xrot = ['', '']
yrot = ['', '']
zrot = ['', '']
xcount = ['', '']
ycount = ['', '']

columns = ['filename', 'x position', 'y position', 'z position', 'x rotation',
           'y rotation', 'z rotation', 'x field of view', 'y field of view',
           'camera focal length', 'x pixel well size', 'y pixel well size',
           'UNIX timestamp', 'x pixel count', 'y pixel count']
output = [[filename[0], xpos[0], ypos[0], zpos[0], xrot[0], yrot[0], zrot[0], xfov[0], yfov[0], foc[0], xsize[0], ysize[0], timestamp[0], xcount[0], ycount[0]],
          [filename[1], xpos[1], ypos[1], zpos[1], xrot[1], yrot[1], zrot[1], xfov[1], yfov[1], foc[1], xsize[1], ysize[1], timestamp[1]], xcount[1], ycount[1]]

# create the params.csv file
params = pd.DataFrame(output, columns=columns)
params.to_csv('/Users/ellemiekevankints/Desktop/SSRL/PlanetAPI/PlanetAPI/OutputCSV/params.csv', index=False)


