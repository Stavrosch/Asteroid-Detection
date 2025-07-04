# Asteroid-Detection v1.0.0

Toolkit created as part of an MSc thesis on automatic asteroid detection. The repository contains a set of graphical utilities for analysing FITS images, tracking known asteroids and plate solving observations.
![Asteroid-Detection Demo](demo.gif) 

## Requirements

- **Python**: version 3.11 or later is recommended.
  
- **Windows** & **WSL** (WSL needeed to run astrometry.net locally, for online Plate Solving, not needed)
  
- **Dependencies** (installable with `pip`):
  `astropy`, `astroquery`, `pandas`, `skyfield`, `matplotlib`, `customtkinter`,
  `Pillow`, `requests` and optionally `pwi4_client` for telescope control.
  
- **Plate Solving**
    - **Online**: API key & astrometry.net account
    - **Local**: WSL to run a local installation of `astrometry.net`

- **Track Asteroid** requires the asteroid pickled files. See [DATA_PREPARATION.md](DATA_PREPARATION.md).

## Installation

  - Clone the repository
  - Install dependencies
        
        pip install -r requirements.txt  # (if you have a requirements file)

  - Set up plate-solving:

     - Online (Astrometry.net API):
         - Get an API key from https://nova.astrometry.net/api_help
         - Add it to GUIs/Utilities/ps_API.py (line 23).

     - Local (WSL):
         - Follow astrometry.net’s build guide.
    
                https://astrometry.net/doc/build.html#build

  - Set up data files
      - Several tools depend on a pickled catalogue of minor planet orbits named `GUIs/Utilities/mpcorb_df.pkl` and others. This file is not included in the repository.
        See [DATA_PREPARATION.md](DATA_PREPARATION.md) for instructions on downloading the MPCORB catalogue from the Minor Planet Center and generating the pickle.
## Running

Launch the application by running inside the GUIs folder:

```
python GUI_main.py
```
