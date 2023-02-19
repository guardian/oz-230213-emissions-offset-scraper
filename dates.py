
# %%
## Set dates

import datetime
import pytz

today = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane"))


day_of_week = today.weekday()
# print("Today is: ", day_of_week)

today_os_format = today.strftime('%Y%m%d')
today_use_date = today.strftime('%Y/%m/%d')

yest = datetime.datetime.now() - datetime.timedelta(days=1)

yest = yest.astimezone(pytz.timezone("Australia/Brisbane"))


yest_os_format = yest.strftime('%Y%m%d')
yest_use_date = yest.strftime('%Y/%m/%d')

# print(yest_os_format)


# %%
