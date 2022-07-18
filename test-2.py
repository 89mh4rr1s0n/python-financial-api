from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
from datetime import datetime
from operator import itemgetter

import pymongo
mongo_uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_uri) 
db = client["financialModellingPrepDB"]
collection = db["ismManufacturing"]

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromeWebDriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('https://www.prnewswire.com/news-releases/services-pmi-at-55-3-june-2022-services-ism-report-on-business-301580808.html')

time.sleep(3)

# nmi value
nmi_value = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[2]/div/div/table/tbody/tr[2]/td[2]/p/span')

# business activity values
bus_act_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[5]/p/span')
#                                              //*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[5]/p/span
bus_act_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[4]/p/span')
bus_act_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[3]/p/span')
bus_act_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[2]/p/span')

#new orders values
new_orders_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[5]/p/span')
#                                                 //*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[5]/p/span
new_orders_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[4]/p/span')
new_orders_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[3]/p/span')
new_orders_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[2]/p/span')

#employment values
employment_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[5]/p/span')
#                                                 //*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[5]/p/span
employment_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[4]/p/span')
employment_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[3]/p/span')
employment_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[2]/p/span')

#deliveries values
deliveries_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[5]/p/span')
#                                                 //*[@id="main"]/article/section/div/div/div[14]/div/div/table/tbody/tr[2]/td[5]/p/span
deliveries_faster = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[4]/p/span')
deliveries_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[3]/p/span')
deliveries_slower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[2]/p/span')

#inventories values
inventories_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[7]/div/div/table/tbody/tr[2]/td[5]/p/span')
inventories_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[7]/div/div/table/tbody/tr[2]/td[4]/p/span')
inventories_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[7]/div/div/table/tbody/tr[2]/td[3]/p/span')
inventories_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[7]/div/div/table/tbody/tr[2]/td[2]/p/span')

# prices values
prices_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[5]/p/span')
prices_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[4]/p/span')
prices_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[3]/p/span')
prices_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[2]/p/span')

# order backlog values
order_backlog_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[9]/div/div/table/tbody/tr[2]/td[5]/p/span')
order_backlog_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[9]/div/div/table/tbody/tr[2]/td[4]/p/span')
order_backlog_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[9]/div/div/table/tbody/tr[2]/td[3]/p/span')
order_backlog_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[9]/div/div/table/tbody/tr[2]/td[2]/p/span')

# exports values
exports_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[5]/p/span')
exports_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[4]/p/span')
exports_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[3]/p/span')
exports_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[2]/p/span')

# imports values
imports_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[5]/p/span')
imports_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[4]/p/span')
imports_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[3]/p/span')
imports_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[2]/p/span')

# inventory sentiment values
inv_sent_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[5]/p/span')
inv_sent_too_low = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[4]/p/span')
inv_sent_about_right = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[3]/p/span')
inv_sent_too_high = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[2]/p/span')

print(bus_act_index.text, type(bus_act_index.text))
print(bus_act_lower.text)
print(bus_act_same.text)
print(bus_act_higher.text)

# //*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[5]/p/span
# //*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[5]/p/span