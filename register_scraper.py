# %%
# from sudulunu.helpers import pp, make_num, dumper, rand_delay
import pandas as pd 
import os 
import time 

from bs4 import BeautifulSoup as bs 

from dates import today_os_format, today_use_date, today, day_of_week

print("\n#### Scraping offsets register table\n\n")

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
### Setup selenium

from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Firefox(options=chrome_options)


# %%
### Paths and stuff

urlo = 'https://epbcpublicportal.awe.gov.au/offsets-register/'
out_path = 'data/register_raw'

### Set the current folder

# full_path = '/Users/josh_nicholas/Repos/oz-230213-emissions-offset-scraper/'

# os.chdir(full_path)

# %%

### Check if a folder exists for the current date

folds = os.listdir(out_path)

# print("folds: ", folds)

if today_os_format not in folds:
    os.mkdir(f"{out_path}/{today_os_format}")

new_out_path = f"{out_path}/{today_os_format}"

# %%

driver.get(urlo)

# time.sleep(15)

# %%

### Reverse the date order 
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Project Approval Date"]'))) 
button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Project Approval Date"]').click()
rand_delay(10)
# print("Reverse order clicko")
button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Project Approval Date"]').click()
# print("Reverse order clicko")


skipped = 0

rangeo = 11

if day_of_week == 5:
    rangeo = 131


# for nummer in range(1, 10):
# for nummer in range(1, 131):
    # time.sleep(5)

for nummer in range(1, rangeo):

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, f"{nummer}")))

    if f"{nummer}.csv" not in os.listdir(new_out_path):

        # time.sleep(15)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, f"{nummer}")))

        sauce = driver.page_source

        soup = bs(sauce, 'html.parser')


        rows = soup.find_all('tr')[1:]

        # print(rows)

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

        # print(tabs.columns.tolist())

        if len(tabs) >= 1:

            rename = {}

            for col in tabs.columns.tolist():
                rename[col] = col.replace('. sort descending', '').replace('. sort ascending', '').strip()

            # print(rename)

            tabs.rename(columns=rename, inplace=True)
            columns = tabs.columns.tolist()

            tabs['Url'] = tabs[columns[0]]
            tabs.replace({'Url': dicto}, inplace=True)

            tabs['Scraped'] = today_use_date

            tabs['Project Approval Date'] = pd.to_datetime(tabs['Project Approval Date'], format="%d/%m/%Y")
            tabs['Scraped'] = pd.to_datetime(tabs['Scraped'], format="%Y/%m/%d")
            tabs['Project Approval Expiry Date'] = pd.to_datetime(tabs['Project Approval Expiry Date'], format="%d/%m/%Y")

            # tabs['Stem'] = tabs['EPBC Number'].str.replace("/", "_")

            dumper(f"{new_out_path}", f"{nummer}", tabs)


            # pp(tabs)

            # print(f"Just finished {nummer}...")

            # driver.quit()
        
        else: 
            print("\n\nBROKEN\n\n")
            break

        # rand_delay(5)
    else:
        # print("Skipped table page ", nummer)
        skipped += 1

### This was how I was selecting the next button before (xpath), however it doesn't remain consistent throughout

    # button = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/div/div/div[2]/div[7]/div/ul/li[12]/a').click()
    
### Selecting the button based on the link text value (the page number)    
    
    rand_delay(10)
    button_num = nummer + 1
    button = driver.find_element(By.LINK_TEXT, f"{button_num}").click()
    # button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Next page"]').click()
    # print("Clicko")

print("Skipped: ", skipped)

driver.quit()

