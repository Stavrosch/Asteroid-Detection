# Data Preparation

This repository relies on a few additional data files that are not distributed
with the code.  They need to be downloaded or generated and placed in the
locations shown below:
- `GUIs/Utilities/mpcorb_df.pkl`
- `GUIs/Utilities/astorb.dat`
- `GUIs/de421.bsp`

## Generating `mpcorb_df.pkl`

1. **Download the MPCORB catalogue**

   Visit the [Minor Planet Center MPCORB page](https://minorplanetcenter.net/iau/MPCORB.html) and download the latest `MPCORB.DAT.gz` file.  After downloading, decompress it so that you have `MPCORB.DAT` on disk.

2. **Convert to a DataFrame**

   Use the `skyfield` utilities to parse the file and save the result as a pickle:

   ```python
   from skyfield.data import mpc
   import pandas as pd

   df = mpc.load_mpcorb_dataframe('MPCORB.DAT')
   df.to_pickle('GUIs/Utilities/mpcorb_df.pkl')
   ```

   The resulting `mpcorb_df.pkl` should be placed in `GUIs/Utilities` so that modules like `quick_eph_window.py` can load it.

## Downloading astorb.dat

1. **Get the ASTORB catalogue**

   The asteroid orbital elements database can be downloaded from a direct link to the file:

   ```
   https://asteroid.lowell.edu/astorb/
   ```

2. **Place the file**

   Copy the resulting `astorb.dat` into `GUIs/Utilities`.  Scripts such as
   `ORB_EL_printer.py` and `TLE_printer.py` expect to find the catalogue in that
   directory.

## Downloading ephemeris de421.bsp

1. **Download the planetary ephemeris**

   JPL's DE421 ephemeris can be dowloaded using Skyfield library from:

   ```
   from skyfield.api import load
   planets = load('de421.bsp')
   print('Ready')
    ```
**This is already done by the script automatically and dowloaded only the first time.**


