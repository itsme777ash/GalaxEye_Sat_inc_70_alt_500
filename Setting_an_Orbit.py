from sgp4.api import Satrec, WGS72
from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite
import numpy as np
import matplotlib.pyplot as plt

ts = load.timescale()
minutes = np.arange(0,200,0.1)  #monitorning the ground track for 200 minutes
times   = ts.utc(2021, 7, 30, 10, minutes)

#Substituted orbital elements from gmat
satrec = Satrec()
satrec.sgp4init(
    WGS72,           # gravity model
    'i',             # 'a' = old AFSPC mode, 'i' = improved mode
    7,               # satnum: Satellite number
    26144.4166667,       # epoch: days since 1949 December 31 00:00 UT
    2.8098e-05,      # bstar: drag coefficient (/earth radii)
    6.969196665e-13, # ndot: ballistic coefficient (revs/day)
    0.0,             # nddot: second derivative of mean motion (revs/day^3)
    0,       # ecco: eccentricity
    0, # argpo: argument of perigee (radians)
    1.22173, # inclo: inclination (radians)
    1.16937, # mo: mean anomaly (radians)
    0.0664050067, # no_kozai: mean motion (radians/minute)
    1.0472, # nodeo: right ascension of ascending node (radians)
)

#Created a satellite element and used geocentric to get it's location wrt geocentric coordinate system
sat = EarthSatellite.from_satrec(satrec, ts)
geocentric = sat.at(times)
subsat = geocentric.subpoint()

#Plotted latitude vs Longitude graph for the ground track of the satellite
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(1, 1, 1)
ax.set(xlim=(-180,180),ylim = (-90,90))

ax.plot([-180,180],[60,60])
ax.plot([0,0],[-80,80])
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.scatter(subsat.longitude.degrees, subsat.latitude.degrees,
            color='red',s=3)
plt.show()
print('Satellite number:', sat.model.satnum)
print('Epoch:', sat.epoch.utc_jpl())