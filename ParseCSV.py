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
xsize = [6.5 * (10**-9), 6.5 * (10**-9)] # convert nanometers to meters
ysize = [6.5 * (10**-9), 6.5 * (10**-9)] # convert nanometers to meters
foc = [3.6, 3.6] # meters

xpos = input['x_sat_eci'].values.tolist()
ypos = input['y_sat_eci'].values.tolist()
zpos = input['z_sat_eci'].values.tolist()

q0 = input['q0'].values.tolist()
q1 = input['q1'].values.tolist()
q2 = input['q2'].values.tolist()
q3 = input['q3'].values.tolist()

# this function converts a quaternion into euler angles (roll, pitch, yaw)
def quaternion_to_euler(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
        
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
        
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
        
    return roll_x, pitch_y, yaw_z # in radians

xrot1, yrot1, zrot1 = quaternion_to_euler(q0[0], q1[0], q2[0], q3[0])
xrot2, yrot2, zrot2 = quaternion_to_euler(q0[1], q1[1], q2[1], q3[1])

# x and y pixel count, leave blank for now, will eventually be photo resolution
xcount = ['', '']
ycount = ['', '']

# data for params.csv file
columns = ['filename', 'x position', 'y position', 'z position', 'x rotation',
           'y rotation', 'z rotation', 'x field of view', 'y field of view',
           'camera focal length', 'x pixel well size', 'y pixel well size',
           'UNIX timestamp', 'x pixel count', 'y pixel count']
output = [[filename[0], xpos[0], ypos[0], zpos[0], xrot1, yrot1, zrot1, xfov[0], yfov[0], foc[0], xsize[0], ysize[0], str(timestamp[0]), xcount[0], ycount[0]],
          [filename[1], xpos[1], ypos[1], zpos[1], xrot2, yrot2, zrot2, xfov[1], yfov[1], foc[1], xsize[1], ysize[1], str(timestamp[1]), xcount[1], ycount[1]]]

# create the params.csv file
params = pd.DataFrame(output, columns=columns)
params.to_csv('OutputCSV/params.csv', index=False)


