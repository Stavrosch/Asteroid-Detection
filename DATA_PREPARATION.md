This repository relies on a few additional data files that are not distributed
with the code.  They need to be downloaded or generated and placed in the
locations shown below:
- `GUIs/Utilities/mpcorb_df.pkl`
- `GUIs/Utilities/astorb.dat`
- `GUIs/de421.bsp` This file is added automatically

## Download the MPCORB catalogue

   Visit the [Minor Planet Center MPCORB page](https://minorplanetcenter.net/iau/MPCORB.html) and download the latest `MPCORB.DAT.gz` file. 
  
- **Convert to a pickle DataFrame & Removing Lines**
  
  After extracting the MPCORB.DAT.gz and placing the MPCORB.DAT in the utilities folder. Run the script 

   ```
   python pickler.py
   ```
   inside the Utilities folder :

   The resulting `mpcorb_df.pkl` should be already placed in `GUIs/Utilities`.

## Downloading astorb.dat

1. **Get the ASTORB catalogue**

   The asteroid orbital elements database can be downloaded from a direct link to the file:

   ```
   https://asteroid.lowell.edu/astorb/
   ```

2. **Place the file**

   Copy the resulting `astorb.dat` into `GUIs/Utilities`.
## Downloading ephemeris de421.bsp

1. **Download the planetary ephemeris**

   JPL's DE421 ephemeris can be dowloaded using Skyfield library from:

   ```
   from skyfield.api import load
   planets = load('de421.bsp')
   print('Ready')
    ```
**This is already done by the script automatically and dowloaded only the first time.**


