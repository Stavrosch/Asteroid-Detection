# Asteroid-Detection

Toolkit created as part of an MSc thesis on automatic asteroid detection. The repository contains a set of graphical utilities for analysing FITS images, tracking known asteroids and plate solving observations.

## Requirements

- **Python**: version 3.11 or later is recommended.
- **Windows**
- **Dependencies** (installable with `pip`):
  `astropy`, `astroquery`, `pandas`, `skyfield`, `matplotlib`, `customtkinter`,
  `Pillow`, `requests` and optionally `pwi4_client` for telescope control.
- **Plate Solving** can use either `astroquery.astrometry_net` with an Astrometry.net API key (add it to `GUIs/Utilities/ps_API.py` line 23) or a local installation of `astrometry.net`.
- **Track Asteroid** requires the asteroid pickled files. See [DATA_PREPARATION.md](DATA_PREPARATION.md).

### Installation

1. Clone this repository.
2. Install the required packages, for example:

   ```bash
   pip install astropy astroquery pandas skyfield matplotlib customtkinter Pillow requests
   ```
3. Install data files

## Data files

Several tools depend on a pickled catalogue of minor planet orbits named `GUIs/Utilities/mpcorb_df.pkl` and others. This file is not included in the repository.
See [DATA_PREPARATION.md](DATA_PREPARATION.md) for instructions on downloading the MPCORB catalogue from the Minor Planet Center and generating the pickle.
## Running

Launch the application by running inside the GUIs folder:

```
python GUI_main.py
```
