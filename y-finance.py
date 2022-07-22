from itertools import count
from locale import currency
import yfinance as yf
import investpy
from datetime import datetime
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

# driver.get('https://www.investing.com/economic-calendar/building-permits-25')

driver.get('https://www.investing.com/economic-calendar/michigan-consumer-sentiment-320')

# popup_close = driver.find_element(By.CLASS_NAME, "popupCloseIcon largeBannerCloser")
# popup_close.click()

# time.sleep(3)

# search = driver.find_element(By.CLASS_NAME, "searchText arial_12 lightgrayFont js-main-search-bar")

# expand_history = driver.find_element(By.CLASS_NAME, "showMoreReplies block")
time.sleep(2)
for x in range(400):
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
        # element = WebDriverWait(driver, 10).until(
        # EC.element_to_be_clickable((By.XPATH, '//div[contains(@id,"showMoreHistory")]/a')))

        # if element:
        #     element.click()
        # else:
        #     print('')


        # if driver.find_element(By.CLASS_NAME, "showMoreReplies").is_displayed():
        #     driver.find_element(By.CLASS_NAME, "showMoreReplies").click()

        if driver.find_element(By.XPATH, '//div[contains(@id,"showMoreHistory")]/a').is_displayed():
            driver.find_element(By.XPATH, '//div[contains(@id,"showMoreHistory")]/a').click()
    except:
        print("finished expanding historical data")

time.sleep(2)
hist_data = []
# hist_table = driver.find_element(By.CLASS_NAME, "historyTab")
# table_rows = hist_table.find_elements(By.CSS_SELECTOR, 'tr')
# dates = hist_table.find_elements(By.CSS_SELECTOR, 'td:first-child')
# actuals = hist_table.find_elements(By.CSS_SELECTOR, 'td:nth-child(3) > span')
# forecasts = hist_table.find_elements(By.CSS_SELECTOR, 'td:nth-child(4)')
# previous = hist_table.find_elements(By.CSS_SELECTOR, 'td:nth-child(5)')
# print(len(table_rows))

# dates = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr/td[1]')
# times = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr/td[2]')

# rows without speaks
# //*[@id="fullColumn"]/div/div[6]/div[3]/div/a[not(descendant::span[contains(text(), "Speaks")])]

# //*[@id="fullColumn"]/div/div[6]/div[3]/div/a[not(descendant::span[contains(text(), "Speaks")]) and not(descendant::span[contains(text(), "Election")]) and not(descendant::span[contains(text(), "FOMC")]) and not(descendant::span[contains(text(), "Testifies")])    ] 


# "FOMC"  "Testifies"

# find table with historical data and exclude premliminary rows

series_description = driver.find_element(By.XPATH, '//div[@id="overViewBox"]/div[contains(@class, "left")]')
country = driver.find_element(By.XPATH, '//div[@id="overViewBox"]/div[contains(@class, "right")]/div[2]/span[2]/i[@title]')
curr = driver.find_element(By.XPATH, '//div[@id="overViewBox"]/div[contains(@class, "right")]/div[3]/span[2]')
importance = driver.find_elements(By.XPATH, '//div[@id="overViewBox"]/div[contains(@class, "right")]//i[contains(@class, "grayFullBullishIcon")]')

dates = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr[not(descendant::span[contains(@class, "smallGrayP")])]/td[1]')
actuals = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr[not(descendant::span[contains(@class, "smallGrayP")])]/td[3]')
forecasts = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr[not(descendant::span[contains(@class, "smallGrayP")])]/td[4]')
previous = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr[not(descendant::span[contains(@class, "smallGrayP")])]/td[5]')

# dates = hist_table.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr/td[1]')
# times = hist_table.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr/td[2]')

print('country', country.get_attribute('title'))

def convert_string(str):
    if "M" in str:
        num = str.replace('M', '')
        return float(num) * 1000000
    elif "K" in str:
        num = str.replace('K', '')
        return float(num) * 1000
    elif "B" in str:
        num = str.replace('B', '')
        return float(num) * 1000000000
    elif "T" in str:
        num = str.replace('T', '')
        return float(num) * 1000000000000
    elif "%" in str:
        num = str.replace('%', '')
        return float(num)
    elif str == ' ':
        return str
    else:
        return float(str)

monthly = False
same_month = False

# still need to handle the "x + 1" error for the last iteration of the loop where it is not available -- on linne 122 -- next_date_string
# also i think i can change the clickable element to expand the table back to the xpath selectors

for x in range(len(dates)):
    date_string = dates[x].text.split(" ")
    next_date_string = dates[x + 1].text.split(" ")
    next_next_date_string = dates[x + 2].text.split(" ")
    year = int(date_string[2])
    rep_month = datetime.strptime(date_string[0], '%b').month
    rep_day = int(date_string[1].strip(','))
    reported = datetime(year, rep_month, rep_day)

    date = datetime(year, rep_month, 1)


    if "(" in date_string[-1] and x == 0:
        month = datetime.strptime(date_string[-1].replace("(", "").replace(")", ""), '%b').month
        next_month = datetime.strptime(next_date_string[-1].replace("(", "").replace(")", ""), '%b').month
        next_next_month = datetime.strptime(next_date_string[-1].replace("(", "").replace(")", ""), '%b').month
        if month == 1 and next_month == 12 and next_next_month == 11 or next_month == month -1 and next_next_month == month -2:
            monthly = True

        if date_string[-1].replace("(", "").replace(")", "") == date_string[0]:
            # date = datetime(year, month, 1)
            same_month = True
        elif date_string[-1].replace("(", "").replace(")", "") != date_string[0] and monthly == True:
            if datetime.strptime(next_date_string[0], '%b').month == 12:
                date = datetime(year -1, datetime.strptime(next_date_string[0], '%b').month, 1)
            else:
                date = datetime(year, datetime.strptime(next_date_string[0], '%b').month, 1)
                
    else:
        prev_date_string = dates[x + 1].text.split(" ")
        previous = dates[x - 1].text.split(" ")
        if monthly == True and same_month == False:
            if datetime.strptime(next_date_string[0], '%b').month == 12:
                date = datetime(year -1, datetime.strptime(next_date_string[0], '%b').month, 1)
            else:
                date = datetime(year, datetime.strptime(prev_date_string[0], '%b').month, 1)
        elif monthly == True and same_month == True:
            if datetime.strptime(date_string[0], '%b').month == datetime.strptime(previous[0], '%b').month:
                date = datetime(year, datetime.strptime(date_string[0], '%b').month -1, 1)
            else:
                date = datetime(year, datetime.strptime(date_string[0], '%b').month, 1)

    item = {
        'date reported': reported.strftime("%d/%m/%Y"),
        'date': date.strftime("%d/%m/%Y"),
        'value': convert_string(actuals[x].text),
        'forecast': convert_string(forecasts[x].text)
    }
    print(item, monthly, date_string[-1].replace("(", "").replace(")", ""), date_string[0], datetime.strptime(next_date_string[0], '%b').month, same_month)
    # print("val", convert_string(actuals[x].text))

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

