from sudulunu.helpers import rand_delay

import register_scraper

rand_delay(5)

import combiner

rand_delay(5)

import individual_scraper

rand_delay(5)

from dates import day_of_week

if day_of_week == 6:
    import cleanup_old

