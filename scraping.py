# Sample One: Scraping Earnings Calendar Information, Estimates, and Results from ZACKS and creating dataframe

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

url = 'http://zacks.thestreet.com/tools/earnings_announcements_company.php'

table_css_selector = 'table.bordered:nth-child(2)' #This comes from the browser's dev tools, Right click on table data on web page, Inspect Element -> Find Table Containing Data <td> or the rows of the table you want on the web page -> Right Click, Copy CSS Select

tickers = ['JPM', 'BAC', 'C', 'WFC', 'KEY', 'HBAN', 'FITB', 'PNC']

# Can also pass in set list of tickers from another source or combine with scraping S&P 500 list from sample two.
# symbols = pd.read_csv(r'E:\Python Programs\SP500\tickers for macrotrendsnet2.csv')
# tickers = symbols['Ticker'].tolist()

df_earnings_announcements = pd.DataFrame()

for ticker in tickers:
    print(ticker)
    time.sleep(2)
    payload = {
        'ticker': ticker
    }
    r = requests.post(url, params = payload)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.select(table_css_selector) #CSS Selector copied from the Browser's Dev Tools
    df_append = pd.read_html(str(table))[0]
    df_append.columns = df_append.iloc[0] #first row of the table is the column names
    df_append.drop(df_append.index[0], inplace=True) #drop the column names
    df_append['ticker'] = ticker
    # df_append.dropna(subset=['Reported'], inplace=True)
    df_earnings_announcements = df_earnings_announcements.append(df_append)

# Sample Two: Scraping List of Current S&P 500 Constituents from Wikipedia

import pandas as pd
import requests
import bs4 as bs

resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, features="lxml")
table = soup.find('table', {'wikitable sortable'})
tickers = []
names = []
sectors = []
industries = []
for row in table.find_all('tr')[1:]:
    ticker = row.find_all('td')[0].text.replace('\n','')
    tickers.append(ticker)
    name = row.find_all('td')[1].text.replace('\n','')
    names.append(name)
    sector = row.find_all('td')[3].text.replace('\n','')
    sectors.append(sector)
    industry = row.find_all('td')[4].text.replace('\n','')
    industries.append(industry)

df_tickers = pd.DataFrame(tickers)
df_tickers.rename(columns={0: "ticker"}, inplace=True)
df_names = pd.DataFrame(names)
df_names.rename(columns={0: "name"}, inplace=True)
df_sectors = pd.DataFrame(sectors)
df_sectors.rename(columns={0: "sector"}, inplace=True)
df_industry = pd.DataFrame(industries)
df_industry.rename(columns={0: "industry"}, inplace=True)
df_merged = pd.concat([df_tickers, df_names, df_sectors, df_industry], axis=1)
df_merged.to_csv(r'\data\tickers.csv', index=False)