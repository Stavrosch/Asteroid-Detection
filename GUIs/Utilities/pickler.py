from skyfield.data import mpc
import pandas as pd

with open('Utilities/MPCORB.DAT', 'rb') as f:
    df = mpc.load_mpcorb_dataframe(f)
df.to_pickle('Utilities/mpcorb_df.pkl')