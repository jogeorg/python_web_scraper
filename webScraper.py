# -*- coding: utf-8 -*-

# ENV setup

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Get webpage request and extract domain name

url = 'https://www.census.gov/programs-surveys/popest.html'
urlChopped = url.split('/')
domain = str(urlChopped[2])
page = requests.get(url)

# Set local variables for later calls

soup = BeautifulSoup(page.content, 'html.parser')
a = soup.find_all('a', href=True)
slash = re.compile("/")
octothorpe = re.compile("#")
urls = pd.DataFrame(columns=[])

# Scrape the webpage and export links to CSV

for link in a:
    if slash.match(link.get('href')):
        urls = urls.append(pd.Series('https://' + domain + link.get('href')), ignore_index=True).drop_duplicates()
    elif octothorpe.match(link.get('href')):
        print("I found",link.get('href'),"and removed it")
    else:
        urls = urls.append(pd.Series(link.get('href')), ignore_index=True).drop_duplicates()
    
urls.to_csv('urls.csv', sep=',', header=None)
print('I completed successfully')