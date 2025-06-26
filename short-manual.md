## Track Asteroid / Observable Objects
Provides two tabs:

- “Whats Observable?” – queries JPL’s service for observable asteroids given location, date/time, elevation limit, magnitude range, and object type.

- “Track Asteroid” – displays ephemeris data for a specified asteroid and plots its altitude path.
## Plate Solver

Plate Solves FITS images via Astrometry.net or a local installation of Astrometry.net and writes a wsc object in the header.

**If using Astrometry.net, set your API key in GUIs/Utilities/ps_API.py around line 21.
The local solve requires to locally install astrometry.net independently.**

## Asteroid Detection

Select a FITS file and magnitude threshold.

Runs detection (calls functions in Utilities/detector.py), marking possible asteroids and allowing generation of an MPC-formatted report.

If no asteroid is found lower the threshold and if there are too many detections do the opposite. 
Use the report button to generate an 80 collumn format report.
