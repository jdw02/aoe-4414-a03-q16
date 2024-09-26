# sez_to_ecef.py
#
# Usage: python3 script_name.py arg1 arg2 ...
#  Text explaining script usage
# Parameters:
#  arg1: description of argument 1
#  arg2: description of argument 2
#  ...
# Output:
#  A description of the script output
#
# Written by: Jayden Warren
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import sys # argv
import math
import numpy #matrix math

# "constants"
e_E = 0.081819221456
r_E_km = 6378.1363

# helper functions
def calc_denom(ecc,lat_rad):
    return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

## function description
    # def calc_denom(ecc,lat_rad):
        #Shortcut for the denominator found in CE and SE equations

# initialize script arguments
o_lat_deg = float('nan') # Origin Latitude in Degrees
o_lon_deg = float('nan') # Origin Longitude in Degrees
o_hae_km = float('nan') # Origin Height above ellipsoid in km
s_km = float('nan') # South Coordinate
e_km = float('nan') # East Coordinate
z_km = float('nan') # Zenith Corrdinate

# parse script arguments
if len(sys.argv)==7:
    o_lat_deg = float(sys.argv[1])
    o_lon_deg = float(sys.argv[2])
    o_hae_km  = float(sys.argv[3])
    s_km = float(sys.argv[4])
    e_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
else:
    print(\
     'Usage: '\
     'py sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
    )
    exit()

o_lat_rad = math.radians(o_lat_deg)
o_lon_rad = math.radians(o_lon_deg)

# write script below this line

## sez to ecef conversion matrices
R_y = numpy.array([[math.sin(o_lat_rad), 0,math.cos(o_lat_rad)], 
                   [0.0,1.0,0.0],
                   [-math.cos(o_lat_rad),0,math.sin(o_lat_rad)]]) 
R_z = numpy.array([[math.cos(o_lon_rad),-math.sin(o_lon_rad),0],
                   [math.sin(o_lon_rad), math.cos(o_lon_rad),0],
                   [0.0,0.0,1.0]]) 
sez_origin = numpy.array([[s_km],
                          [e_km],
                          [z_km]]) 
first_rotation = R_y.dot(sez_origin)
# second rotation is SEZ vector
second_rotation = R_z.dot(first_rotation) 
sez_vector = second_rotation

## llh to ecef conversions 
denom = calc_denom(e_E,o_lat_rad)
C_E = r_E_km/denom
r_x_km = (C_E+o_hae_km)*math.cos(o_lat_rad)*math.cos(o_lon_rad)
r_y_km = (C_E+o_hae_km)*math.cos(o_lat_rad)*math.sin(o_lon_rad)
r_z_km = (C_E*(1-e_E**2)+o_hae_km)*math.sin(o_lat_rad)
# llh to ecef vector before puting in terms of sez origin
llh_to_ecef_vector = numpy.array([[r_x_km],
                           [r_y_km],
                           [r_z_km]])
# add ecef to sez vector to get final ecef vector of the plane
ecef_vector = numpy.add(sez_vector,llh_to_ecef_vector)
ecef_x_km = ecef_vector[0]
ecef_y_km = ecef_vector[1]
ecef_z_km = ecef_vector[2]

# Printing outputs
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)
