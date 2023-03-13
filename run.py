
# %%
import os 
import pathlib
pathos = pathlib.Path(__file__).parent
os.chdir(pathos)
# print(pathos)
# print("Current path: ", os.getcwd())

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

# %%

try:

  import register_scraper

except:

  rand_delay(5)

import combiner

rand_delay(5)

import fix_broken_links

import individual_scraper

rand_delay(5)

from dates import day_of_week

if day_of_week == 6:
    import cleanup_old

import check_differences

