# %%
# from sudulunu.helpers import pp, make_num, dumper, rand_delay
import pandas as pd 
import os 
import time 

import difflib
# duffer = difflib.Differ()

from bs4 import BeautifulSoup as bs 

from dates import today_os_format, today_use_date, today
# from dates import yest_os_format, yest_use_date

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


print("#### Scraping individual pages")

# %%

scraped_path = f'data/register_combined/combined.csv'
out_path = 'data/projects_raw/backup'

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


# %%

### Load in the dataset

df = pd.read_csv(scraped_path)
'EPBC Number', 'Project', 'Offset Name', 'Project Approval Date', 
'Project Approval Expiry Date', 'Approval Holder', 'Url', 'Scraped'

df.drop_duplicates(subset=['Url'], inplace=True)

# pp(df)



# %%

def dump_text(stringo, pathos, stem):
    with open(f"{pathos}/{stem}.txt", "w") as writer:
        writer.write(stringo)

def already_done(stemmo, pathos):
    inner = os.listdir(pathos)
    inner = [x.strip(".txt") for x in inner]
    # print("Inner", inner)

    if stemmo in inner:
        return True
    else:
        return False

# %%

records = []
has_changed = []

old_changed = pd.read_csv('data/has_changed.csv')
# old_changed.drop(columns={"Changed"}, inplace=True)

# df = df[:1]

for index,row in df.iterrows():

    texto = ''

    urlo = row['Url']
    nummer = row['EPBC Number'].replace("/", "_")

    if already_done(nummer, new_out_path) == True:
        # print("Skipped")
        continue
    else:

        ### Grab the previous data:

        old = ''

        with open(f'data/projects_raw/latest/{nummer}.txt', 'r') as reader:
            old = reader.read()

        dump_text(old, f'data/projects_raw/previous', nummer)

        # print(old)
        # print(urlo)

        driver.get(urlo)

        # time.sleep(10)

        # print("Start")
        # start = time.process_time()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="customTab"]/li[2]/a')))
        # print("That took: ", time.process_time() - start)

        driver.find_element(By.XPATH, '//*[@id="customTab"]/li[2]/a').click()

        # print("Clicko")

        # time.sleep(5)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@data-name="tab_2_section_1"]')))
        rand_delay(5)
        sauce = driver.page_source

        soup = bs(sauce, 'html.parser')

        # content = soup.find_all(id='mainContent')
        content = soup.find_all(attrs={'data-name':'tab_2_section_1'})

        content = [x.text for x in content]

        for x in content:
            texto += '\n\n'
            texto += x.strip()
            # print(x.strip())
            texto += '\n\n'   

        dump_text(texto, 'data/projects_raw/latest', nummer)

        dump_text(texto, f'data/projects_raw/backup/{today_os_format}', nummer)



        ### This is going to check whether the "Offset Sites" is stil "Under Review" as a boolean and save it as a csv

        review = soup.find(attrs={'aria-label':'Under review'})
        # review = soup.find(attrs={'aria-label':'Under reasdfasdf'})
        review_ouput = True

        if review == None:
            review_ouput = False
        
        record = {'EPBC Number': row['EPBC Number'], 'Stem': nummer, "Url": urlo, "Under Review": review_ouput, 'Scraped': today_use_date}

        records.append(record)

        old_review = pd.read_csv('data/projects_raw/Under review.csv')

        inter = pd.DataFrame.from_records(records)

        tog = pd.concat([old_review, inter])
        tog.drop_duplicates(subset=['EPBC Number', 'Scraped'], inplace=True)

        dumper('data/projects_raw', "Under review", tog)


        if texto != old:

            ### This is just updating the change csv
            print(f"{nummer} has changed!")
            changed = {'EPBC Number': row['EPBC Number'], 'Stem': nummer, "Url": urlo, "Under Review": review_ouput, 'Scraped': today_use_date}
            has_changed.append(changed)
            changer = pd.DataFrame.from_records(has_changed)
            change_dump = pd.concat([old_changed, changer])
            change_dump.drop_duplicates(subset=['EPBC Number', 'Scraped'], inplace=True)
            dumper('data', 'has_changed', change_dump)

            ### Want to save the differences somewhere

            # duff = duffer.compare(texto, old)
            # dufference = ''.join(duff)

            duff = difflib.ndiff(old.splitlines(), texto.splitlines())
            dufference = '\n'.join(list(duff))

            dump_text(dufference, f'data/projects_raw/differences', f"{today_os_format}_{nummer}")



        # else:
        #     # print("IT HASN'T CHANGED")

        #     continue



        # print("Reivew", review)
        donezo = len(os.listdir(f'data/projects_raw/backup/{today_os_format}'))
        if donezo % 20 == 0:
            print(f"{donezo}/{len(df)}")
        rand_delay(10)

# %%


driver.quit()

#customTab > li:nth-child(2) > a

# <a class="nav-link" href="div[data-name='tab_sites']" data-toggle="tab" aria-expanded="false">Offset Sites</a>