from skyfield.data import mpc
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
mpcorb_dat_path = os.path.join(script_dir, 'MPCORB.DAT')
output_pkl_path = os.path.join(script_dir, 'mpcorb_df.pkl')

with open(mpcorb_dat_path, 'r') as f:
    for line_num, line in enumerate(f):
        if line.startswith('--------'):
            break

with open(mpcorb_dat_path, 'rb') as f:
    for _ in range(line_num + 1):
        next(f)
    df = mpc.load_mpcorb_dataframe(f)

os.makedirs(os.path.dirname(output_pkl_path), exist_ok=True)
df.to_pickle(output_pkl_path)
print(f"Successfully saved MPCORB data to {output_pkl_path}")

print("\nVerification:")

if os.path.exists(output_pkl_path):
    print(f"✔ Pickle file exists at {output_pkl_path}")
    print(f"File size: {os.path.getsize(output_pkl_path) / 1024:.2f} KB")
else:
    print(f"✖ Pickle file not found at {output_pkl_path}")
    exit(1)

try:
    loaded_df = pd.read_pickle(output_pkl_path)
    print("✔ Successfully loaded the pickle file")
except Exception as e:
    print(f"✖ Failed to load pickle file: {e}")
    exit(1)

if df.equals(loaded_df):
    print("✔ Original and loaded DataFrames match")
else:
    print("✖ Original and loaded DataFrames differ")
    exit(1)

print("\nSample data from the DataFrame:")
print(f"Total objects: {len(df)}")
print("\nFirst 5 objects:")
print(df.head())
print("\nRandom 5 objects:")
print(df.sample(5))

if len(df.select_dtypes(include='number').columns) > 0:
    print("\nBasic statistics:")
    print(df.describe())