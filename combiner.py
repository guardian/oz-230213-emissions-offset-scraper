# %%
# from sudulunu.helpers import pp, make_num, dumper, rand_delay
import pandas as pd 
import os 

from dates import today_os_format, today_use_date, today

# %%
#### Import functions

def dumper(path, name, frame):
    with open(f'{path}/{name}.csv', 'w') as f:
        frame.to_csv(f, index=False, header=True)

def rand_delay(num):
  import random 
  import time 
  rando = random.random() * num
#   print(rando)
  time.sleep(rando)


# print(today_os_format)

scrape_path = f'data/register_raw/{today_os_format}'

out_path = 'data/register_combined'

# %%

def combine_from_folder(pathos):
  
  listo = []
  
  fillos = os.listdir(pathos)
  fillos = [pathos + "/" + x for x in fillos if x != '.DS_Store']

  for fillo in fillos:
    inter = pd.read_csv(fillo)

    listo.append(inter)

  cat = pd.concat(listo)

  return cat

# %%

old = combine_from_folder(f"{out_path}/backup")
dumper(out_path, "previous", old)
# pp(old)


# %%

# if f"{today_os_format}.csv" not in os.listdir(out_path):

new = combine_from_folder(scrape_path)
dumper(out_path, "latest", new)

# %%

tog = pd.concat([new, old])
tog['Scraped'] = pd.to_datetime(tog['Scraped'])

tog['Offset Name'] = tog['Offset Name'].str.strip()

tog.sort_values(by=['Scraped'], ascending=True, inplace=True)
tog.drop_duplicates(subset=['EPBC Number', 'Offset Name'], inplace=True)

dumper(f"{out_path}/backup", today_os_format, tog)
dumper(out_path, "combined", tog)


