# %%
from sudulunu.helpers import pp, make_num, dumper, rand_delay
import pandas as pd 
import os 
import time 

from bs4 import BeautifulSoup as bs 

# %%
## Set dates

import datetime
import pytz

today = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane"))

today_os_format = today.strftime('%Y%m%d')
today_use_date = today.strftime('%Y/%m/%d')

print(today_os_format)

# %%
### Setup selenium

from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

chrome_options = Options()
# chrome_options.add_argument("--headless")

driver = webdriver.Firefox(options=chrome_options)


# %%
### Paths and stuff

urlo = 'https://epbcpublicportal.awe.gov.au/offsets-register/'
out_path = 'data/register_raw'

### Set the current folder

full_path = '/Users/josh_nicholas/Repos/oz-230213-emissions-offset-scraper/'

os.chdir(full_path)

# %%

### Check if a folder exists for the current date

folds = os.listdir(out_path)

print(folds)

if today_os_format not in folds:
    os.mkdir(f"{out_path}/{today_os_format}")

new_out_path = f"{out_path}/{today_os_format}"


# %%

driver.get(urlo)

time.sleep(15)

# %%

for nummer in range(0, 3):

    time.sleep(15)

    if nummer not in os.listdir(new_out_path):

        sauce = driver.page_source

        soup = bs(sauce, 'html.parser')


        rows = soup.find_all('tr')[1:]

        print(rows)

        # https://epbcpublicportal.awe.gov.au/offsets-register/offset-detail/?id=9299af79-0275-ed11-81ac-000d3ae0929c

        # bows = rows[:2]
        bows = rows.copy()

        dicto = {}

        for row in bows:
            # print(row)
            teeds = row.find_all('td')

            # print(teeds[0])
            # print(teeds[0].text)

            epbc_num = teeds[0].text
            urlo = 'https://epbcpublicportal.awe.gov.au' + teeds[0].a['href']
            # print(urlo)

            dicto[epbc_num] = urlo

        # print(rows[0])
        # print(dicto)


        tabs = pd.read_html(sauce)[0]
        # 'EPBC Number. sort descending', 'Project. sort descending', 'Offset Name. sort descending', 
        # 'Project Approval Date. sort descending', 'Project Approval Expiry Date. sort descending', 
        # 'Approval Holder. sort descending'

        rename = {}

        for col in tabs.columns.tolist():
            rename[col] = col.replace('. sort descending', '')

        print(rename)

        tabs.rename(columns=rename, inplace=True)
        columns = tabs.columns.tolist()

        tabs['Url'] = tabs[columns[0]]
        tabs.replace({'Url': dicto}, inplace=True)

        tabs['Scraped'] = today_use_date

        tabs['Project Approval Date'] = pd.to_datetime(tabs['Project Approval Date'], format="%d/%m/%Y")
        tabs['Scraped'] = pd.to_datetime(tabs['Scraped'], format="%Y/%m/%d")
        tabs['Project Approval Expiry Date'] = pd.to_datetime(tabs['Project Approval Expiry Date'], format="%d/%m/%Y")

        dumper(f"{new_out_path}", f"{nummer}", tabs)


        pp(tabs)

        # driver.quit()

        rand_delay(10)

        button = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/div/div/div[2]/div[7]/div/ul/li[12]/a').click()



        print("One round down")
# driver.quit()