import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import glob

data_prefix = "backup/data_"
data_files = glob.glob(f"{data_prefix}*.json")

dfs = []
for file in data_files:
    data = pd.read_json(file)
    timestamp = np.datetime64(file.removeprefix(data_prefix).removesuffix(".json").replace('_', '-')) .astype(object)
    data['datum'] = timestamp
    dfs.append(data)

df = pd.concat(dfs, ignore_index=True)
df.set_index('datum', inplace=True)

plt.figure(figsize=(15, 10))
df.groupby('player')['elo'].plot(legend=True)
plt.savefig("static/images/elo_history.png")