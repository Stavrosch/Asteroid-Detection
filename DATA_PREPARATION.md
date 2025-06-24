# Data Preparation

This repository relies on some additional data files that are not distributed with the code.  The most important is `mpcorb_df.pkl`, a pandas DataFrame containing orbital elements for known minor planets.

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

