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

man_ind_list = [
    'Apparel, Leather & Allied Products',
    'Furniture & Related Products',
    'Wood Products',
    'Fabricated Metal Products',
    'Machinery',
    'Computer & Electronic Products',
    'Transportation Equipment',
    'Plastics & Rubber Products',
    'Paper Products',
    'Chemical Products',
    'Petroleum & Coal Products',
    'Primary Metals',
    'Textile Mills',
    'Electrical Equipment, Appliances & Components',
    'Food, Beverage & Tobacco Products',
    'Miscellaneous Manufacturing',
    'Nonmetallic Mineral Products',
    'Printing & Related Support Activities'
]

PATH = "C:\Program Files (x86)\chromeWebDriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('https://www.prnewswire.com/news/institute-for-supply-management/')

time.sleep(3)

man_links = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Manufacturing ISM® Report On Business®')

links = []

for link in man_links:
    links.append(link.get_attribute('href'))

for l in links:
    print(l)
    

driver.quit()

data = []

def get_ind_rankings(text, series_name):
    man_split = text.split(".")

    growth = man_split[0]
    if ":" in growth:
        growth_split = growth.split(":")
        growth_inds = growth_split[len(growth_split) - 1]
        growth_arr = growth_inds.split(";")
        growth_arr = [i.lstrip() for i in growth_arr]
        growth_arr_copy = growth_arr.copy()
        last_growth = growth_arr_copy[len(growth_arr_copy)-1]
        growth_arr.pop()
        growth_arr.append(last_growth[4:len(last_growth)])
    else:
        growth_a = []
        growth_arr = []
        for ind in range(len(man_ind_list)):
            if man_ind_list[ind] in growth:
                i = {
                    'industry': man_ind_list[ind],
                    'index': growth.find(man_ind_list[ind])
                }
                growth_a.append(i.copy())
        growth_sorted = sorted(growth_a, key=itemgetter('index'), reverse=False)
        for i in growth_sorted:
            growth_arr.append(i["industry"])

    contraction = man_split[1]
    if ":" in contraction:
        contraction_split = contraction.split(":")
        contraction_inds = contraction_split[len(contraction_split) - 1]
        contraction_arr = contraction_inds.split(";")
        contraction_arr = [i.lstrip() for i in contraction_arr]
        contraction_arr_copy = contraction_arr.copy()
        last_contraction = contraction_arr_copy[len(contraction_arr_copy)-1]
        contraction_arr.pop()
        contraction_arr.append(last_contraction[4:len(last_contraction)])
    else:
        contraction_a = []
        contraction_arr = []
        for ind in range(len(man_ind_list)):
            if man_ind_list[ind] in contraction:
                i = {
                    'industry': man_ind_list[ind],
                    'index': contraction.find(man_ind_list[ind])
                }
                contraction_a.append(i.copy())
        contraction_sorted = sorted(contraction_a, key=itemgetter('index'), reverse=False)
        for i in contraction_sorted:
            contraction_arr.append(i["industry"])

    series_data = []

    for x in range(len(man_ind_list)):
        if man_ind_list[x] in growth_arr:
            item = {
                'industry': man_ind_list[x],
                'direction': 'Growth',
                'rank': len(growth_arr) - ( growth_arr.index(man_ind_list[x]) )
            }
            series_data.append(item.copy())
        elif man_ind_list[x] in contraction_arr:
            item = {
                'industry': man_ind_list[x],
                'direction': 'Contraction',
                'rank': 0 - ( len(contraction_arr) - ( contraction_arr.index(man_ind_list[x]) ) )
            }
            series_data.append(item.copy())
        else:
            item = {
                'industry': man_ind_list[x],
                'direction': 'Neutral',
                'rank': 0
            }
            series_data.append(item.copy())

    series = {
        "name": series_name,
        "data": series_data
    }

    data.append(series.copy())

def get_ism_data(link):
    data.clear()
    driver = webdriver.Chrome(PATH)
    driver.get(link)
    man = driver.find_element(By.XPATH, "//*[contains(text(), 'manufacturing industries reported growth in') or contains(text(), ' reported growth in')]")
    new_orders = driver.find_element(By.XPATH, "//*[contains(text(), 'reported growth in new orders in')]")
    production = driver.find_element(By.XPATH, "//*[contains(text(), ' growth in production during ')]")
    employment = driver.find_element(By.XPATH, "//*[contains(text(), 'industries reported employment growth i') or contains(text(), 'industries to report employment growth')]")
    deliveries = driver.find_element(By.XPATH, "//*[contains(text(), 'reported slower supplier deliveries')]")
    inventories = driver.find_element(By.XPATH, "//*[contains(text(), ' reporting higher inventories i')]")
    customer_inventories = driver.find_element(By.XPATH, "//*[contains(text(), 'reported customers') or contains(text(), 'industries reporting customers')]")

    headline = driver.find_element(By.CSS_SELECTOR, ".detail-headline")
    headline_split = headline.text.split(";")
    headline_words = headline_split[1][1:len(headline_split[1])].split(" ")
    month_num = datetime.strptime(headline_words[0], '%B').month

    date = datetime(int(headline_words[1]), month_num, 1).strftime("%d/%m/%Y")
    period = headline_words[0] + " " + headline_words[1]

    # series_info = {
    #     'series': 'ISM Manufacturing Report On Business',
    #     'date': date,
    #     'period': period
    # }

    # data.append(series_info)

    get_ind_rankings(man.text, 'manufacturing')
    get_ind_rankings(new_orders.text, 'new orders')
    get_ind_rankings(production.text, 'production')
    get_ind_rankings(employment.text, 'employment')
    get_ind_rankings(deliveries.text, 'deliveries')
    get_ind_rankings(inventories.text, 'inventories')
    get_ind_rankings(customer_inventories.text, 'customer inventories')

    mongo_item = {
        '_id': 'ism-man-' + headline_words[0].lower() + "-" + headline_words[1],
        'series': 'ISM Manufacturing Report On Business',
        'date': date,
        'period': period,
        'data': data
    }

    check = collection.count_documents({'_id': 'ism-man-' + headline_words[0].lower() + "-" + headline_words[1]})

    print(check)

    if check == 0:
        collection.insert_one(mongo_item)

    driver.quit()

# get_ism_data('https://www.prnewswire.com/news-releases/manufacturing-pmi-at-60-7-december-2020-manufacturing-ism-report-on-business-301200432.html')
for link in links:
    get_ism_data(link)

# print(json.dumps(data, indent=4))

