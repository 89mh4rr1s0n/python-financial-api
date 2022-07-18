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
collection = db["ismServices"]

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

serv_ind_list = [
    'Accommodation & Food Services',
    'Agriculture, Forestry, Fishing & Hunting',
    'Arts, Entertainment & Recreation',
    'Construction',
    'Educational Services',
    'Finance & Insurance',
    'Health Care & Social Assistance',
    'Information',
    'Management of Companies & Support Services',
    'Mining',
    'Other Services',
    'Professional, Scientific & Technical Services',
    'Public Administration',
    'Real Estate, Rental & Leasing',
    'Retail Trade',
    'Transportation & Warehousing',
    'Utilities',
    'Wholesale Trade',
]

PATH = "C:\Program Files (x86)\chromeWebDriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('https://www.prnewswire.com/news/institute-for-supply-management/')

time.sleep(3)

man_links = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Services ISM® Report On Business®')

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
        for ind in range(len(serv_ind_list)):
            if serv_ind_list[ind] in growth:
                i = {
                    'industry': serv_ind_list[ind],
                    'index': growth.find(serv_ind_list[ind])
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
        for ind in range(len(serv_ind_list)):
            if serv_ind_list[ind] in contraction:
                i = {
                    'industry': serv_ind_list[ind],
                    'index': contraction.find(serv_ind_list[ind])
                }
                contraction_a.append(i.copy())
        contraction_sorted = sorted(contraction_a, key=itemgetter('index'), reverse=False)
        for i in contraction_sorted:
            contraction_arr.append(i["industry"])

    series_data = []

    for x in range(len(serv_ind_list)):
        if serv_ind_list[x] in growth_arr:
            item = {
                'industry': serv_ind_list[x],
                'direction': 'Growth',
                'rank': len(growth_arr) - ( growth_arr.index(serv_ind_list[x]) )
            }
            series_data.append(item.copy())
        elif serv_ind_list[x] in contraction_arr:
            item = {
                'industry': serv_ind_list[x],
                'direction': 'Contraction',
                'rank': 0 - ( len(contraction_arr) - ( contraction_arr.index(serv_ind_list[x]) ) )
            }
            series_data.append(item.copy())
        else:
            item = {
                'industry': serv_ind_list[x],
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
    nmi = driver.find_element(By.XPATH, "//*[contains(text(), 'services industries reporting growth in') or contains(text(), 'non-manufacturing industries reporting growth')]")
    business_activity = driver.find_element(By.XPATH, "//*[contains(text(), 'in business activity')]")
    new_orders = driver.find_element(By.XPATH, "//*[contains(text(), 'of new orders in ')]")
    employment = driver.find_element(By.XPATH, "//*[contains(text(), 'increase in employment')]")
    deliveries = driver.find_element(By.XPATH, "//*[contains(text(), 'slower deliveries in ')]")
    inventories = driver.find_element(By.XPATH, "//*[contains(text(), 'increase in inventories in ')]")

    headline = driver.find_element(By.CSS_SELECTOR, ".detail-headline")
    if ";" in headline.text:
        headline_split = headline.text.split(";")
        headline_words = headline_split[1][1:len(headline_split[1])].split(" ")
        month_num = datetime.strptime(headline_words[0], '%B').month

        date = datetime(int(headline_words[1]), month_num, 1).strftime("%d/%m/%Y")
        period = headline_words[0] + " " + headline_words[1]
        # nmi_value = headline_split[0][len(headline_split[0])-5: len(headline_split[0]) -1]
    else:
        headline_split = headline.text.split("%")
        headline_words = headline_split[1][1:len(headline_split[1])].split(" ")
        month_num = datetime.strptime(headline_words[0], '%B').month

        date = datetime(int(headline_words[1]), month_num, 1).strftime("%d/%m/%Y")
        period = headline_words[0] + " " + headline_words[1] 
        # nmi_value = headline_split[0][len(headline_split[0])-5: len(headline_split[0]) -1]

    # nmi value
    # nmi_value = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[2]/div/div/table/tbody/tr[2]/td[2]/p/span')

    if len(driver.find_elements(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[5]/p/span')) > 0:

        nmi_value = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[2]/div/div/table/tbody/tr[2]/td[2]/p/span')
        
        # business activity values
        bus_act_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[5]/p/span')
        bus_act_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[4]/p/span')
        bus_act_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[3]/p/span')
        bus_act_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[2]/td[2]/p/span')

        #new orders values
        new_orders_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[5]/p/span')
        new_orders_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[4]/p/span')
        new_orders_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[3]/p/span')
        new_orders_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[4]/div/div/table/tbody/tr[2]/td[2]/p/span')

        #employment values
        employment_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[5]/p/span')
        employment_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[4]/p/span')
        employment_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[3]/p/span')
        employment_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[5]/div/div/table/tbody/tr[2]/td[2]/p/span')

        #deliveries values
        deliveries_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[6]/div/div/table/tbody/tr[2]/td[5]/p/span')
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

    else:

        nmi_value = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[3]/div/div/table/tbody/tr[4]/td[2]/p/span')

        # business activity values
        bus_act_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[5]/p/span')
        bus_act_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[4]/p/span')
        bus_act_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[3]/p/span')
        bus_act_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[8]/div/div/table/tbody/tr[2]/td[2]/p/span')

        #new orders values
        new_orders_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[5]/p/span')
        new_orders_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[4]/p/span')
        new_orders_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[3]/p/span')
        new_orders_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[10]/div/div/table/tbody/tr[2]/td[2]/p/span')

        #employment values
        employment_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[5]/p/span')
        employment_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[4]/p/span')
        employment_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[3]/p/span')
        employment_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[12]/div/div/table/tbody/tr[2]/td[2]/p/span')

        #deliveries values
        deliveries_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[14]/div/div/table/tbody/tr[2]/td[5]/p/span')
        deliveries_faster = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[14]/div/div/table/tbody/tr[2]/td[4]/p/span')
        deliveries_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[14]/div/div/table/tbody/tr[2]/td[3]/p/span')
        deliveries_slower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[14]/div/div/table/tbody/tr[2]/td[2]/p/span')

        #inventories values
        inventories_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[16]/div/div/table/tbody/tr[2]/td[5]/p/span')
        inventories_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[16]/div/div/table/tbody/tr[2]/td[4]/p/span')
        inventories_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[16]/div/div/table/tbody/tr[2]/td[3]/p/span')
        inventories_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[16]/div/div/table/tbody/tr[2]/td[2]/p/span')

        # prices values
        prices_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[18]/div/div/table/tbody/tr[2]/td[5]/p/span')
        prices_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[18]/div/div/table/tbody/tr[2]/td[4]/p/span')
        prices_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[18]/div/div/table/tbody/tr[2]/td[3]/p/span')
        prices_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[18]/div/div/table/tbody/tr[2]/td[2]/p/span')

        # order backlog values
        order_backlog_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[20]/div/div/table/tbody/tr[2]/td[5]/p/span')
        order_backlog_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[20]/div/div/table/tbody/tr[2]/td[4]/p/span')
        order_backlog_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[20]/div/div/table/tbody/tr[2]/td[3]/p/span')
        order_backlog_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[20]/div/div/table/tbody/tr[2]/td[2]/p/span')

        # exports values
        exports_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[22]/div/div/table/tbody/tr[2]/td[5]/p/span')
        exports_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[22]/div/div/table/tbody/tr[2]/td[4]/p/span')
        exports_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[22]/div/div/table/tbody/tr[2]/td[3]/p/span')
        exports_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[22]/div/div/table/tbody/tr[2]/td[2]/p/span')

        # imports values
        imports_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[24]/div/div/table/tbody/tr[2]/td[5]/p/span')
        imports_lower = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[24]/div/div/table/tbody/tr[2]/td[4]/p/span')
        imports_same = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[24]/div/div/table/tbody/tr[2]/td[3]/p/span')
        imports_higher = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[24]/div/div/table/tbody/tr[2]/td[2]/p/span')

        # inventory sentiment values
        inv_sent_index = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[26]/div/div/table/tbody/tr[2]/td[5]/p/span')
        inv_sent_too_low = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[26]/div/div/table/tbody/tr[2]/td[4]/p/span')
        inv_sent_about_right = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[26]/div/div/table/tbody/tr[2]/td[3]/p/span')
        inv_sent_too_high = driver.find_element(By.XPATH, '//*[@id="main"]/article/section/div/div/div[26]/div/div/table/tbody/tr[2]/td[2]/p/span')
    # series_info = {
    #     'series': 'ISM Manufacturing Report On Business',
    #     'date': date,
    #     'period': period
    # }

    # data.append(series_info)

    get_ind_rankings(nmi.text, 'non-manufacturing')
    get_ind_rankings(business_activity.text, 'business activity')
    get_ind_rankings(new_orders.text, 'new orders')
    get_ind_rankings(employment.text, 'employment')
    get_ind_rankings(deliveries.text, 'deliveries')
    get_ind_rankings(inventories.text, 'inventories')

    values = {
        'NMI Index': float(nmi_value.text),
        'Business Activity': {
            '% Higher': float(bus_act_higher.text),
            '% Same': float(bus_act_same.text),
            '% Lower': float(bus_act_lower.text),
            'Index': float(bus_act_index.text)
        },
        'New Orders': {
            '% Higher': float(new_orders_higher.text),
            '% Same': float(new_orders_same.text),
            '% Lower': float(new_orders_lower.text),
            'Index': float(new_orders_index.text)
        },
        'Employment': {
            '% Higher': float(employment_higher.text),
            '% Same': float(employment_same.text),
            '% Lower': float(employment_lower.text),
            'Index': float(employment_index.text)
        },
        'Deliveries': {
            '% Slower': float(deliveries_slower.text),
            '% Same': float(deliveries_same.text),
            '% Faster': float(deliveries_faster.text),
            'Index': float(deliveries_index.text)
        },
        'Inventories': {
            '% Higher': float(inventories_higher.text),
            '% Same': float(inventories_same.text),
            '% Lower': float(inventories_lower.text),
            'Index': float(inventories_index.text)
        },
        'Prices': {
            '% Higher': float(prices_higher.text),
            '% Same': float(prices_same.text),
            '% Lower': float(prices_lower.text),
            'Index': float(prices_index.text)
        },
        'Order Backlog': {
            '% Higher': float(order_backlog_higher.text),
            '% Same': float(order_backlog_same.text),
            '% Lower': float(order_backlog_lower.text),
            'Index': float(order_backlog_index.text)
        },
        'Exports': {
            '% Higher': float(exports_higher.text),
            '% Same': float(exports_same.text),
            '% Lower': float(exports_lower.text),
            'Index': float(exports_index.text)
        },
        'Imports': {
            '% Higher': float(imports_higher.text),
            '% Same': float(imports_same.text),
            '% Lower': float(imports_lower.text),
            'Index': float(imports_index.text)
        },
        'Inventory Sentiment': {
            '% Too High': float(inv_sent_too_high.text),
            '% About Right': float(inv_sent_about_right.text),
            '% Too Low': float(inv_sent_too_low.text),
            'Index': float(inv_sent_index.text)
        }
    }

    mongo_item = {
        '_id': 'ism-services-' + headline_words[0].lower() + "-" + headline_words[1],
        'series': 'ISM Services Report On Business',
        'date': date,
        'period': period,
        'values': values,
        'sectors': data
    }

    check = collection.count_documents({'_id': 'ism-services-' + headline_words[0].lower() + "-" + headline_words[1]})

    print(check)

    if check == 0:
        collection.insert_one(mongo_item)

    driver.quit()

for link in links:
    get_ism_data(link)