# %%
import pandas as pd 
import os 
# pd.set_option("display.max_rows", 100)

from sudulunu.helpers import pp, make_num, dumper
# from sudulunu.helpers import rand_delay, unique_in_col, null_in_col
# from sudulunu.helpers import combine_from_folder

fillo = ''
#%%

data = pd.read_csv(fillo)

# %%

df = data.copy()

pp(df)

#%%