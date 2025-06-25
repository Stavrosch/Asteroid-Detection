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

3. **Updating the file**

   Periodically refresh the file by repeating the steps above with a newer `MPCORB.DAT`.

## Downloading astorb.dat

1. **Get the ASTORB catalogue**

   The asteroid orbital elements database can be downloaded from either the
   [Minor Planet Center](https://minorplanetcenter.net/) or the
   [Jet Propulsion Laboratory](https://ssd.jpl.nasa.gov/tools/sbdb_query.html).
   A direct link to the file is available from JPL's FTP service:

   ```bash
   wget https://ssd.jpl.nasa.gov/ftp/ssd/nearby/astorb/astorb.dat.gz
   gunzip astorb.dat.gz
   ```

2. **Place the file**

   Copy the resulting `astorb.dat` into `GUIs/Utilities`.  Scripts such as
   `ORB_EL_printer.py` and `TLE_printer.py` expect to find the catalogue in that
   directory.

## Downloading ephemeris de421.bsp

1. **Download the planetary ephemeris**

   JPL's DE421 ephemeris can be retrieved from the NAIF repository:

   ```bash
   wget https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de421.bsp
   ```

2. **Install the kernel**

   Save the downloaded `de421.bsp` file in the `GUIs` folder.  The
   `quick_eph_window.py` module loads it with `load('de421.bsp')`, so keeping the
   file alongside the GUI scripts ensures it is found at runtime.


