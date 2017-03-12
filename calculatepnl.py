import glob
import os
import pandas as pd
import numpy as np

pnl = {}

latest_history = max(glob.iglob('archive/*.txt'), key=os.path.getctime)

print('Pulling the latest order history: ' + latest_history)

df = pd.read_csv(latest_history, names = ['symbol', 'side', 'quantity', 'price'])

df['total'] = df.quantity * df.price

df_grp = df.groupby(['side'], as_index=False).sum()

df_output = df_grp[['side', 'total']]

s = np.asscalar(df_output.loc[df_output['side'] == 'S']['total'].values)
b = np.asscalar(df_output.loc[df_output['side'] == 'B']['total'].values)

print('PnL: ' + str(s-b))
