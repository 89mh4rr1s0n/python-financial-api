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
man_hist_collection = db["ismManHist"]

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller as chromedriver
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
# driver = webdriver.Chrome(PATH)
chromedriver.install()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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
    # driver = webdriver.Chrome(PATH)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)
    man = driver.find_element(By.XPATH, "//*[contains(text(), 'manufacturing industries reported growth in') or contains(text(), ' reported growth in')]")
    new_orders = driver.find_element(By.XPATH, "//*[contains(text(), 'reported growth in new orders in')]")
    production = driver.find_element(By.XPATH, "//*[contains(text(), ' growth in production during ')]")
    employment = driver.find_element(By.XPATH, "//*[contains(text(), 'reported employment growth i') or contains(text(), 'industries to report employment growth')]")
    deliveries = driver.find_element(By.XPATH, "//*[contains(text(), 'reported slower supplier deliveries')]")
    inventories = driver.find_element(By.XPATH, "//*[contains(text(), ' reporting higher inventories i')]")
    customer_inventories = driver.find_element(By.XPATH, "//*[contains(text(), 'reported customers') or contains(text(), 'industries reporting customers')]")

    headline = driver.find_element(By.CSS_SELECTOR, ".detail-headline")
    headline_split = headline.text.split(";")
    headline_words = headline_split[1][1:len(headline_split[1])].split(" ")
    month_num = datetime.strptime(headline_words[0], '%B').month

    date = datetime(int(headline_words[1]), month_num, 1).strftime("%d/%m/%Y")
    period = headline_words[0] + " " + headline_words[1]

    pmi_value = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[2]/div/div/table/tbody/tr[2]/td[2]/p/span')

    # new orders values
    new_orders_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[2]/p/span')
    new_orders_same = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[3]/p/span')
    new_orders_lower = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[4]/p/span')
    new_orders_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[5]/p/span')
    new_orders_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[6]/p/span')

    # production values
    production_higher = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[2]/p/span')
    production_same = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[3]/p/span')
    production_lower = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[4]/p/span')
    production_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[5]/p/span')
    production_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[6]/p/span')


    # employment values
    employment_higher = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[2]/p/span')
    employment_same = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[3]/p/span')
    employment_lower = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[4]/p/span')
    employment_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[5]/p/span')
    employment_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[6]/p/span')


    # deliveries values
    deliveries_slower = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[2]/p/span')
    deliveries_same = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[3]/p/span')
    deliveries_faster = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[4]/p/span')
    deliveries_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[5]/p/span')
    deliveries_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[6]/p/span')


    # inventories values 
    inventories_higher = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[7]/div/div/table/tbody/tr[2]/td[2]/p/span')
    inventories_same = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[7]/div/div/table/tbody/tr[2]/td[3]/p/span')
    inventories_lower = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[7]/div/div/table/tbody/tr[2]/td[4]/p/span')
    inventories_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[7]/div/div/table/tbody/tr[2]/td[5]/p/span')
    inventories_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[7]/div/div/table/tbody/tr[2]/td[6]/p/span')


    # customer inventories values 
    customer_inventories_reporting = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[2]/p/span')
    customer_inventories_too_high = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[3]/p/span')
    customer_inventories_about_right = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[4]/p/span')
    customer_inventories_too_low = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[5]/p/span')
    customer_inventories_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[6]/p/span')
    customer_inventories_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[7]/p/span')


    # prices values 
    prices_higher = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[9]/div/div/table/tbody/tr[2]/td[2]/p/span')
    prices_same = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[9]/div/div/table/tbody/tr[2]/td[3]/p/span')
    prices_lower = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[9]/div/div/table/tbody/tr[2]/td[4]/p/span')
    prices_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[9]/div/div/table/tbody/tr[2]/td[5]/p/span')
    prices_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[9]/div/div/table/tbody/tr[2]/td[6]/p/span')


    # order backlog values
    order_backlog_reporting = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[2]/p/span')
    order_backlog_higher = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[3]/p/span')
    order_backlog_same = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[4]/p/span')
    order_backlog_lower = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[5]/p/span')
    order_backlog_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[6]/p/span')
    order_backlog_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[7]/p/span')


    # exports values 
    exports_higher = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[3]/p/span')
    exports_same = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[4]/p/span')
    exports_lower = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[5]/p/span')
    exports_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[6]/p/span')
    exports_reporting = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[2]/p/span')
    exports_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[11]/div/div/table/tbody/tr[2]/td[7]/p/span')


    # imports values 
    imports_higher = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[3]/p/span')
    imports_same = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[4]/p/span')
    imports_lower = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[5]/p/span')
    imports_net = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[6]/p/span')
    imports_reporting = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[2]/p/span')
    imports_index = driver.find_element(By.XPATH , '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[7]/p/span')

    

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

    ism_man = {
        "date": date,
        "value": float(pmi_value.text)
    }

    new_orders_dict = {
        "date": date,
        "% Higher": float(new_orders_higher.text),
        "% Same": float(new_orders_same.text),
        "% Lower": float(new_orders_lower.text),
        "Net": float(new_orders_net.text),
        "Index": float(new_orders_index.text),
    }

    production_dict = {
        "date": date,
        "% Higher": float(production_higher.text),
        "% Same": float(production_same.text),
        "% Lower": float(production_lower.text),
        "Net": float(production_net.text),
        "Index": float(production_index.text),
    }

    employment_dict = {
        "date": date,
        "% Higher": float(employment_higher.text),
        "% Same": float(employment_same.text),
        "% Lower": float(employment_lower.text),
        "Net": float(employment_net.text),
        "Index": float(employment_index.text),
    }

    deliveries_dict = {
        "date": date,
        "% Slower": float(deliveries_slower.text),
        "% Same": float(deliveries_same.text),
        "% Faster": float(deliveries_faster.text),
        "Net": float(deliveries_net.text),
        "Index": float(deliveries_index.text),
    }

    inventories_dict = {
        "date": date,
        "% Higher": float(inventories_higher.text),
        "% Same": float(inventories_same.text),
        "% Lower": float(inventories_lower.text),
        "Net": float(inventories_net.text),
        "Index": float(inventories_index.text),
    }

    customer_inventories_dict = {
        "date": date,
        "% Too High": float(customer_inventories_too_high.text),
        "% About Right": float(customer_inventories_about_right.text),
        "% Too Low": float(customer_inventories_too_low.text),
        "Net": float(customer_inventories_net.text),
        "% Reporting": float(customer_inventories_reporting.text),
        "Index": float(customer_inventories_index.text),
    }

    prices_dict = {
        "date": date,
        "% Higher": float(prices_higher.text),
        "% Same": float(prices_same.text),
        "% Lower": float(prices_lower.text),
        "Net": float(prices_net.text),
        "Index": float(prices_index.text),
    }

    order_backlog_dict = {
        "date": date,
        "% Higher": float(order_backlog_higher.text),
        "% Same": float(order_backlog_same.text),
        "% Lower": float(order_backlog_lower.text),
        "Net": float(order_backlog_net.text),
        "% Reporting": float(order_backlog_reporting.text),
        "Index": float(order_backlog_index.text),
    }

    exports_dict = {
        "date": date,
        "% Higher": float(exports_higher.text),
        "% Same": float(exports_same.text),
        "% Lower": float(exports_lower.text),
        "Net": float(exports_net.text),
        "% Reporting": float(exports_reporting.text),
        "Index": float(exports_index.text),
    }

    imports_dict = {
        "date": date,
        "% Higher": float(imports_higher.text),
        "% Same": float(imports_same.text),
        "% Lower": float(imports_lower.text),
        "Net": float(imports_net.text),
        "% Reporting": float(imports_reporting.text),
        "Index": float(imports_index.text),
    }

    ism_man_doc = man_hist_collection.find({"index": "ISM_MAN"})
    update = {"$push": {'data': {'$each': [ism_man], "$position": 0 }}}
    for doc in ism_man_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "ISM_MAN"}, update)

    new_orders_doc = man_hist_collection.find({"index": "NEW_ORDERS"})
    new_orders_update = {"$push": {'data': {'$each': [new_orders_dict], "$position": 0 }}}
    for doc in new_orders_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "NEW_ORDERS"}, new_orders_update)

    production_doc = man_hist_collection.find({"index": "PRODUCTION"})
    production_update = {"$push": {'data': {'$each': [production_dict], "$position": 0 }}}
    for doc in production_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "PRODUCTION"}, production_update)

    employment_doc = man_hist_collection.find({"index": "EMPLOYMENT"})
    employment_update = {"$push": {'data': {'$each': [employment_dict], "$position": 0 }}}
    for doc in employment_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "EMPLOYMENT"}, employment_update)

    deliveries_doc = man_hist_collection.find({"index": "DELIVERIES"})
    deliveries_update = {"$push": {'data': {'$each': [deliveries_dict], "$position": 0 }}}
    for doc in deliveries_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "DELIVERIES"}, deliveries_update)

    inventories_doc = man_hist_collection.find({"index": "INVENTORIES"})
    inventories_update = {"$push": {'data': {'$each': [inventories_dict], "$position": 0 }}}
    for doc in inventories_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "INVENTORIES"}, inventories_update)

    customer_inventories_doc = man_hist_collection.find({"index": "CUSTOMER_INVENTORIES"})
    customer_inventories_update = {"$push": {'data': {'$each': [customer_inventories_dict], "$position": 0 }}}
    for doc in customer_inventories_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "CUSTOMER_INVENTORIES"}, customer_inventories_update)

    prices_doc = man_hist_collection.find({"index": "PRICES"})
    prices_update = {"$push": {'data': {'$each': [prices_dict], "$position": 0 }}}
    for doc in prices_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "PRICES"}, prices_update)

    order_backlog_doc = man_hist_collection.find({"index": "ORDER_BACKLOG"})
    order_backlog_update = {"$push": {'data': {'$each': [order_backlog_dict], "$position": 0 }}}
    for doc in order_backlog_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "ORDER_BACKLOG"}, order_backlog_update)

    exports_doc = man_hist_collection.find({"index": "EXPORTS"})
    exports_update = {"$push": {'data': {'$each': [exports_dict], "$position": 0 }}}
    for doc in exports_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "EXPORTS"}, exports_update)

    imports_doc = man_hist_collection.find({"index": "IMPORTS"})
    imports_update = {"$push": {'data': {'$each': [imports_dict], "$position": 0 }}}
    for doc in imports_doc:
        dates = [x['date'] for x in doc['data']]
        if date not in dates:
            man_hist_collection.find_one_and_update({"index": "IMPORTS"}, imports_update)



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

