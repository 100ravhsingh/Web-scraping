import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Setting proxy

# proxy = {
#     "https": "http://95.66.151.101:8080"
# }

# use for loop for scraping all pages

final = pd.DataFrame()
for j in range(1, 3):
# Getting URL
    webpage = requests.get('https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage={}'.format(j)).text
    soup = BeautifulSoup(webpage, 'lxml')

# Fetching Data
# Considering The Whole Data
    company = soup.find_all('div', class_='product')

# Storing Data
    price = []
    title = []
    stocks = []
    manufacturer = []

    for i in company:
        try:
            price.append(i.find('span', class_='price').text.strip())
        except:
            price.append(np.nan)

        try:
            title.append(i.find('a', class_='catalog-item-name').text.strip())
        except:
            title.append(np.nan)

        try:
            stocks.append(i.find('span', class_='status').text.strip())
        except:
            stocks.append(np.nan)

        try:
            manufacturer.append(i.find('a', class_='catalog-item-brand').text.strip())
        except:
            manufacturer.append(np.nan)

# Creating Dataframe For All The Pages
    d = {'Price (in dollar)': price,
         'Title': title,
         'Stock status': stocks,
         'Manufacturer': manufacturer,
         }
    df = pd.DataFrame(d)

# Changing the types of all object
    df['Price (in dollar)'] = df['Price (in dollar)'].str.replace('$', '').astype(float)
    df['Stock status']=df['Stock status'].replace('Out of Stock', 0).replace('In Stock', 1).astype(bool)

# Converting Data into Json
    final = final.append(df.to_json('Data.json'), ignore_index=True)
