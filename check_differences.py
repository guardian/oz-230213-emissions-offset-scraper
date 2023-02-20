# %%
import pandas as pd 
import os 
import time 

from bs4 import BeautifulSoup as bs 

from dates import today_os_format, today_use_date, today, day_of_week

# today_use_date = '2023/02/19'


# %%

import smtplib
from email.mime.text import MIMEText
import os

def sendEmail(text, subject, to):
    
    EMAIL_ALERT_PASSWORD = os.environ['EMAIL_ALERT_PASSWORD']
    
    fromaddr = "alerts@nickevershed.com"
    recipients = ["josh.nicholas@theguardian.com"]
    
    msg = MIMEText(text, 'html')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = ", ".join(to)   
    server = smtplib.SMTP_SSL('mail.nickevershed.com', 465)
    server.login(fromaddr, EMAIL_ALERT_PASSWORD)
    text = msg.as_string()
    print("Sending email")
    server.sendmail(fromaddr, to, text)
    server.quit()
    print("Email sent")


# %%


diffs = pd.read_csv('data/has_changed.csv')
# 'EPBC Number', 'Stem', 'Url', 'Under Review', 'Scraped'

# %%


tods = diffs.loc[diffs['Scraped'] == today_use_date].copy()

lenno = len(tods)

if lenno > 0:

    texto = f"There were {lenno} changes to the offsets register today."

    sendEmail(texto,"Offsets register changes", ['josh.nicholas@theguardian.com'])

# %%


