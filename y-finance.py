import yfinance as yf
import investpy
import datetime
import json
import requests
from bs4 import BeautifulSoup
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromeWebDriver\chromedriver.exe"
# driver = webdriver.Chrome(PATH)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.investing.com/economic-calendar/construction-pmi-44')

# popup_close = driver.find_element(By.CLASS_NAME, "popupCloseIcon largeBannerCloser")
# popup_close.click()

# time.sleep(3)

# search = driver.find_element(By.CLASS_NAME, "searchText arial_12 lightgrayFont js-main-search-bar")

# expand_history = driver.find_element(By.CLASS_NAME, "showMoreReplies block")
time.sleep(2)
for x in range(100):
    # time.sleep(1)
    # try:
    #     table = driver.find_element(By.CLASS_NAME, "historyTab")
    #     print(len(table.find_elements(By.CLASS_NAME, "showMoreReplies")))
    #     if len(table.find_elements(By.CLASS_NAME, "showMoreReplies")) != 0:
    #         table.find_element(By.CLASS_NAME, "showMoreReplies").click()
    #     # expand_table = WebDriverWait(table, 5).until(
    #     #     EC.presence_of_element_located((By.CLASS_NAME, "showMoreReplies"))
    #     # )
    #     # expand_table.click()
    # except:
    #     driver.quit()
    try:
        if driver.find_element(By.CLASS_NAME, "showMoreReplies").is_displayed():
            driver.find_element(By.CLASS_NAME, "showMoreReplies").click()
    finally:
        print("finished expanding historical data")

time.sleep(2)
hist_data = []
hist_table = driver.find_element(By.CLASS_NAME, "historyTab")
table_rows = hist_table.find_elements(By.CSS_SELECTOR, 'tr')
dates = hist_table.find_elements(By.CSS_SELECTOR, 'td:first-child')
actuals = hist_table.find_elements(By.CSS_SELECTOR, 'span')
forecasts = hist_table.find_elements(By.CSS_SELECTOR, 'td:nth-child(4)')
previous = hist_table.find_elements(By.CSS_SELECTOR, 'td:nth-child(5)')

print(len(table_rows))

for x in actuals:
    print(x.text)

# for x in table_rows:
#     print(x.find_element(By.CSS_SELECTOR, 'td').text)
    # print(x.text)

# time.sleep(1)
# expand_history.click()
# time.sleep(1)
# expand_history.click()

# atkr = yf.Ticker("ATKR")

# opt = atkr.option_chain('2022-07-15')

# 20220715

# print(opt.calls)

# gspc = yf.Ticker("^GSPC")

# for 1min interval the max period is one week (5d)
# hist = gspc.history(period="5d", interval="1m")
# hist = gspc.history(period="max", interval="1wk")
# print(hist)

# data = investpy.get_bond_historical_data(bond='U.S. 10Y', from_date='01/01/1950', to_date=datetime.datetime.today().strftime("%d/%m/%Y"))
# data = investpy.get_bond_recent_data(bond='Argentina 3Y')
# print(data)

# return a list of available government bonds
# print(investpy.get_bonds_list())

# return recent data of a bond
# print(investpy.get_bond_recent_data('U.S. 10Y'))


# return todays date formatted to a specific format
# print(datetime.datetime.today().strftime("%d/%m/%Y"))

# print(atkr.quarterly_financials)

# url = 'https://www.investing.com/economic-calendar/construction-pmi-44'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Referer': 'https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173'}
# data = requests.get(url)


# soup = BeautifulSoup(data.text, "lxml")
# data = soup

# def web_content_div(web_content, class_path):
#     web_content_div = web_content.find_all('div', {'class': class_path})
    
#     tdata = web_content_div[0].find_all('td')
    
#     return tdata

# def get_data():
#     data = web_content_div(soup, 'historyTab')
#     return data

# print(get_data())

# uncomment this to print all data:
# print( json.dumps(data, indent=4) )
# print(soup)

# for candle in data['candles']:
#     t = datetime.datetime.fromtimestamp(candle[0] // 1000)
#     print('{!s:<20} {:<10} {:<10} {:<10}'.format(t, *candle[1:]))

