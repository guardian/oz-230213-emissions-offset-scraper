# from sudulunu.helpers import rand_delay


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

import register_scraper

rand_delay(5)

import combiner

rand_delay(5)

import individual_scraper

rand_delay(5)

from dates import day_of_week

if day_of_week == 6:
    import cleanup_old

import check_differences