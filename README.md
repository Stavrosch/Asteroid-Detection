# Asteroid-Detection

Toolkit created as part of an MSc thesis on automatic asteroid detection.
The repository contains a set of graphical utilities for analysing FITS
images, tracking known asteroids and plate solving observations.  The main
entry point is a simple launcher window that opens the available tools.

## Requirements

- **Python**: version 3.11 or later is recommended.
- **Dependencies** (installable with `pip`):
  `astropy`, `astroquery`, `pandas`, `skyfield`, `matplotlib`, `customtkinter`,
  `Pillow`, `requests` and optionally `pwi4_client` for telescope control.
  Plate solving can use either `astroquery.astrometry_net` with an Astrometry.net
  API key or a local installation of `astrometry.net`.

### Installation

1. Clone this repository.
2. Install the required packages, for example:

   ```bash
   pip install astropy astroquery pandas skyfield matplotlib customtkinter Pillow requests
   ```

## Data files

Some modules expect a pre-generated Minor Planet Center database in
`GUIs/Utilities/mpcorb_df.pkl`.  If this file is not present, download the
`mpcorb.dat` catalogue from the MPC and convert it into a pandas DataFrame saved
at this location.

## Running

Launch the application with:

```bash
python GUIs/GUI_main.py
```

The window provides buttons to track asteroids, perform plate solving and run
the asteroid detection tool.

### Plate solving

Plate solving requires either a valid Astrometry.net API key (for the online
solver) or a working local installation of `astrometry.net`.  Configure these
before using the plate solving window.

