from itertools import count
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
opts = Options()
opts.add_argument("user-agent=fobar")
import time

import pymongo
mongo_uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_uri) 
db = client["financialModellingPrepDB"]
collection = db["investingMacroData"]

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

PATH = "C:\Program Files (x86)\chromeWebDriver\chromedriver.exe"

driver = webdriver.Chrome(chrome_options=opts, service=Service(ChromeDriverManager().install()))

currencies = [
    'USD',
    'GBP'
]

driver.get('https://www.investing.com/search/?q=USD&tab=ec_event')

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

time.sleep(6)

result_links = driver.find_elements(By.XPATH, '//*[@id="fullColumn"]/div/div[6]/div[3]/div/a[not(descendant::span[contains(text(), "Speaks")]) and not(descendant::span[contains(text(), "Election")]) and not(descendant::span[contains(text(), "FOMC")]) and not(descendant::span[contains(text(), "Testifies")]) and (descendant::span[2][contains(text(), "USD")])  ]')

links = []

for link in result_links:
    links.append(link.get_attribute('href'))

print(len(links))
print(links[0])

time.sleep(1)

driver.quit()

time.sleep(1)

def get_hist_series(url):
    hist_data = []
    hist_data.clear()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(2)
    for x in range(400):
        try:
            driver.find_element(By.XPATH, '//div[contains(@id,"showMoreHistory")]/a').click()
        except:
            print("finished expanding historical data")

    time.sleep(2)

    series_name = driver.find_element(By.XPATH, '//*[@id="leftColumn"]/h1')
    series_description = driver.find_element(By.XPATH, '//div[@id="overViewBox"]/div[contains(@class, "left")]')
    country = driver.find_element(By.XPATH, '//div[@id="overViewBox"]/div[contains(@class, "right")]/div[2]/span[2]/i[@title]')
    curr = driver.find_element(By.XPATH, '//div[@id="overViewBox"]/div[contains(@class, "right")]/div[3]/span[2]')
    importance = driver.find_elements(By.XPATH, '//div[@id="overViewBox"]/div[contains(@class, "right")]//i[contains(@class, "grayFullBullishIcon")]')

    series_name = series_name.text
    series_description = series_description.text
    country = country.get_attribute('title')
    curr = curr.text
    importance = len(importance)

    print(series_name, type(series_name))

    dates = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr[not(descendant::span[contains(@class, "smallGrayP")])]/td[1]')
    actuals = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr[not(descendant::span[contains(@class, "smallGrayP")])]/td[3]')
    forecasts = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr[not(descendant::span[contains(@class, "smallGrayP")])]/td[4]')
    previous = driver.find_elements(By.XPATH, '//div[contains(@class, "historyTab")]/table/tbody/tr[not(descendant::span[contains(@class, "smallGrayP")])]/td[5]')

    # print('country', country.get_attribute('title'))

    def convert_string(strng):
        if "M" in strng:
            num = strng.replace('M', '').replace(',', '')
            return float(num) * 1000000
        elif "K" in strng:
            num = strng.replace('K', '').replace(',', '')
            return float(num) * 1000
        elif "B" in strng:
            num = strng.replace('B', '').replace(',', '')
            return float(num) * 1000000000
        elif "T" in strng:
            num = strng.replace('T', '').replace(',', '')
            return float(num) * 1000000000000
        elif "%" in strng:
            num = strng.replace('%', '').replace(',', '')
            return float(num)
        elif strng == ' ':
            return strng.replace(',', '')
        else:
            return float(strng)

    monthly = False
    same_month = False

    for x in range(len(dates) -2):
        date_string = dates[x].text.split(" ")
        if x <= len(dates) -3:
            next_date_string = dates[x + 1].text.split(" ")
            next_next_date_string = dates[x + 2].text.split(" ")
        year = int(date_string[2])
        rep_month = datetime.strptime(date_string[0], '%b').month
        rep_day = int(date_string[1].strip(','))
        reported = datetime(year, rep_month, rep_day)

        date = reported

        if "(" in date_string[-1] and x == 0:
            month = datetime.strptime(date_string[-1].replace("(", "").replace(")", ""), '%b').month
            next_month = datetime.strptime(next_date_string[-1].replace("(", "").replace(")", ""), '%b').month
            next_next_month = datetime.strptime(next_next_date_string[-1].replace("(", "").replace(")", ""), '%b').month
            if month == 1 and next_month == 12 and next_next_month == 11 or next_month == month -1 and next_next_month == month -2:
                monthly = True

            if date_string[-1].replace("(", "").replace(")", "") == date_string[0]:
                same_month = True
            elif date_string[-1].replace("(", "").replace(")", "") != date_string[0] and monthly == True:
                if datetime.strptime(next_date_string[0], '%b').month == 12:
                    date = datetime(year -1, datetime.strptime(next_date_string[0], '%b').month, 1)
                else:
                    date = datetime(year, datetime.strptime(next_date_string[0], '%b').month, 1)
                    
        else:
            previous = dates[x - 1].text.split(" ")
            if monthly == True and same_month == False:
                if datetime.strptime(next_date_string[0], '%b').month == 12:
                    date = datetime(year -1, datetime.strptime(next_date_string[0], '%b').month, 1)
                else:
                    date = datetime(year, datetime.strptime(next_date_string[0], '%b').month, 1)
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

        hist_data.append(item.copy())

    mongo_item = {
        '_id': country.lower().replace(' ', '-') + '-' + series_name.lower().replace(' ', '-'),
        'country': country,
        'currency': curr,
        'series name': series_name,
        'importance': importance,
        'description': series_description,
        'historical': hist_data,
    }

    collection.insert_one(mongo_item)

    driver.quit()

for link in links[1:10]:
    get_hist_series(link)
        # print(item, monthly, date_string[-1].replace("(", "").replace(")", ""), date_string[0], datetime.strptime(next_date_string[0], '%b').month, same_month)
