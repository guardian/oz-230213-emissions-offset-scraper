# %%
import os 
import datetime
import pytz
from dates import today_os_format, today_use_date, today
import shutil

# %%
# ## Create some dummy data
# for i in range(0, 51):
#     start = datetime.datetime.strptime("20230101", '%Y%m%d')
#     today = start + datetime.timedelta(days=i)
#     today = today.astimezone(pytz.timezone("Australia/Brisbane"))

#     today_os_format = today.strftime('%Y%m%d')
#     today_use_date = today.strftime('%Y/%m/%d')

#     os.mkdir(f"testo/{today_os_format}")

# %%

def keep_seventh(pathos):
    folds = os.listdir(pathos)
    folds = [x for x in folds if x != '.DS_Store']

    remove = []

    for datto in folds:
        dayo = datetime.datetime.strptime(datto, '%Y%m%d').weekday()
        if dayo != 4:
            remove.append(datto)

    for datto in remove:
        print("Removing: ", datto)
        shutil.rmtree(f"{pathos}/{datto}")


keep_seventh('data/projects_raw/backup')

keep_seventh('data/register_raw')

# %%

