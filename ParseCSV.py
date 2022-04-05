# this file converts the PlanetAPI.csv to params.csv

import pandas as pd
import csv
import math

input = pd.read_csv(
    r'InputCSV/frame_index.csv')

filename = pd.DataFrame(input, columns=['name'])
timestamp = pd.DataFrame(input, columns=['datetime'])

for i in timestamp.index:
    row = timestamp['datetime'][i]
    print(row)

xfov = 2.8 * (math.pi/180) # convert deg to rad
yfov = 2.8 * (math.pi/180) # convert deg to rad
xsize = 6.5 # nanometers
ysize = 6.5 # nanometers
foc = 3.6 # meters



columns = ['filename', 'x position', 'y position', 'z position', 'x rotation',
           'y rotation', 'z rotation', 'x field of view', 'y field of view',
           'camera focal length', 'x pixel well size', 'y pixel well size',
           'UNIX timestamp', 'x pixel count', 'y pixel count']
output = []

# create the params.csv file
#with open('/Users/ellemiekevankints/Desktop/SSRL/PlanetAPI/PlanetAPI/OutputCSV/params.csv', 'w', encoding='UTF8', newline='') as params:
    # create the csv writer
    #writer = csv.writer(params)
    
    # write a row to the csv file
    #writer.writerow(columns)
    
    # write the output data
    #writer.writerown(output)
    

