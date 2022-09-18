from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
from datetime import datetime
from operator import itemgetter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import glob
import os
import shutil
import csv

import pymongo
mongo_uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_uri) 
db = client["financialModellingPrepDB"]
collection = db["zacksScreener"]

PATH = "C:/Program Files (x86)/chromeWebDriver/chromedriver.exe"
# driver = webdriver.Chrome(PATH)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# driver.get('https://www.zacks.com/screening/stock-screener?icid=home-home-nav_tracking-zcom-main_menu_wrapper-stock_screener')

# driver.execute_script("window.scrollBy(0,200)")
# iframe = driver.find_element(By.XPATH, '//*[@id="screenerContent"]')
# driver.switch_to.frame(iframe)

# driver.maximize_window()
# time.sleep(2)

# time.sleep(2)

# mktcap = driver.find_element(By.ID, 'val_12010')
# # mktcap.click() 
# time.sleep(2)
# mktcap.send_keys("1000")

# time.sleep(2)

# mktcap_button = driver.find_element(By.XPATH, '//*[@id="regular"]/table/tbody/tr[9]/td/a')
# mktcap_button.click()

# time.sleep(2)
# driver.find_element(By.XPATH, '//*[@id="run_screen_result"]').click()

# time.sleep(2)
# driver.find_element(By.XPATH, '//*[@id="edit-view-tab"]').click()

# time.sleep(2)
# # click on 'company descriptors'
# driver.find_element(By.XPATH, '//*[@id="criteria_cat_11000"]/a').click()

# time.sleep(3)

# # driver.execute_script("window.scrollBy(0,300)")

# time.sleep(2)
# # click on exchange tickbox
# driver.find_element(By.XPATH, '//*[@id="editView11005"]').click()
# time.sleep(2)
# # click on 'month of fiscal yr end'
# driver.find_element(By.XPATH, '//*[@id="editView11020"]').click()
# time.sleep(2)
# # click on 'Sector'
# driver.find_element(By.XPATH, '//*[@id="editView11025"]').click()
# time.sleep(2)
# # click on 'Industry'
# driver.find_element(By.XPATH, '//*[@id="editView11030"]').click()

# time.sleep(2)
# # click on 'Price & Price Changes'
# driver.find_element(By.XPATH, '//*[@id="criteria_cat_14000"]/a').click()
# time.sleep(2)
# # click on 'Last Close'
# driver.find_element(By.XPATH, '//*[@id="editView14005"]').click()


# time.sleep(2)
# # click on 'EPS Surprise & Actuals'
# driver.find_element(By.XPATH, '//*[@id="criteria_cat_17000"]/a').click()
# time.sleep(2)
# # click on 'Last Yr's EPS (F0) Before NRI
# driver.find_element(By.XPATH, '//*[@id="editView17035"]').click()
# time.sleep(2)

# driver.switch_to.default_content()
# driver.execute_script("window.scrollBy(0,100)")
# driver.switch_to.frame(iframe)

# #click on 'Last Reported Fiscal Yr (yyyymm)'
# driver.find_element(By.XPATH, '//*[@id="editView17040"]').click()

# time.sleep(2)
# # click on '12mo Trailing EPS'
# driver.find_element(By.XPATH, '//*[@id="editView17045"]').click()

# time.sleep(2)
# # click on 'EPS Estimates'
# driver.find_element(By.XPATH, '//*[@id="criteria_cat_19000"]/a').click()


# driver.switch_to.default_content()
# driver.execute_script("window.scrollBy(0,160)")
# driver.switch_to.frame(iframe)

# time.sleep(2)
# # click on 'F1 Consensue Est.'
# driver.find_element(By.XPATH, '//*[@id="editView19055"]').click()

# time.sleep(2)
# # click on '# of Analysts in F1 Consensus'
# driver.find_element(By.XPATH, '//*[@id="editView19060"]').click()

# time.sleep(2)
# # click on 'F2 Consensue Est.'
# driver.find_element(By.XPATH, '//*[@id="editView19070"]').click()

# time.sleep(2)
# # click on '# of Analysts in F2 Consensus'
# driver.find_element(By.XPATH, '//*[@id="editView19075"]').click()

# driver.switch_to.default_content()
# driver.execute_script("window.scrollBy(0,-260)")
# driver.switch_to.frame(iframe)

# time.sleep(2)
# # click on 'Sales, Growth & Estimates'
# driver.find_element(By.XPATH, '//*[@id="criteria_cat_21000"]/a').click()

# time.sleep(2)
# # click on 'F(1) Consensus Sales Est. ($mil)'
# driver.find_element(By.XPATH, '//*[@id="editView21015"]').click()

# time.sleep(2)
# # click on 'Q(1) Consensus Sales Est. ($mil)'
# driver.find_element(By.XPATH, '//*[@id="editView21020"]').click()

# time.sleep(2)
# # click on 'Run Screen' button
# driver.find_element(By.XPATH, '//*[@id="run_screen_result"]').click()

# time.sleep(2)
# # click on CSV button
# driver.find_element(By.XPATH, '//*[@id="screener_table_wrapper"]/div[1]/a[1]').click()

# time.sleep(20)



list_of_files = glob.glob('C:/Users/Matthew/Downloads/*')
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
shutil.copy(latest_file, 'C:/Users/Matthew/Downloads/PTM_v2.0/Anton_Kreil_PTM_v2.0_Video/Documents-updated/Video 23 - zacks-custom-screen/zacks_downloads')
zacks_files = glob.glob('C:/Users/Matthew/Downloads/PTM_v2.0/Anton_Kreil_PTM_v2.0_Video/Documents-updated/Video 23 - zacks-custom-screen/zacks_downloads/*')
latest_zacks = max(zacks_files, key=os.path.getctime)
print(latest_zacks)

rows = []
with open(latest_zacks, 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    # print(header)
    for row in csvreader:
        rows.append(row)
    print(len(rows))
    for r in rows:
        row = {}
        for i in range(len(header)):
            # print(header[i])
            if r[i] != '':
                row[header[i]] = r[i]
            if header[i] == "Market Cap (mil)":
                row['Mkt Cap'] = float(r[i])*1000000
                row.pop("Market Cap (mil)")
            elif header[i] == 'F1 Consensus Est.':
                row['F1 Consensus EPS Est'] = r[i]
                row.pop('F1 Consensus Est.')
            elif header[i] == 'F2 Consensus Est.':
                if r[i] != '':
                    row['F2 Consensus EPS Est'] = float(r[i])
                    row.pop('F2 Consensus Est.')
                else:
                    row['F2 Consensus EPS Est'] = r[i]
                    # row.pop('F2 Consensus Est.')
            elif header[i] == 'Month of Fiscal Yr End' or header[i] == 'Last Close' or header[i] == "Last Yr's EPS (F0) Before NRI" or header[i] == '12 Mo Trailing EPS' or header[i] == '# of Analysts in F1 Consensus' or header[i] == '# of Analysts in F2 Consensus' or header[i] == 'F(1) Consensus Sales Est. ($mil)' or header[i] == 'Q(1) Consensus Sales Est. ($mil)':
                if r[i] != '':
                    row[header[i]] = float(r[i])
                else:
                    row[header[i]] = r[i]
            else:
                row[header[i]] = r[i]
        # collection.insert_one(row)
        # print(row)
        # try:
        if row["Last Yr's EPS (F0) Before NRI"] != '':
            row["Last Yr's EPS (F0) Before NRI"] = float(row["Last Yr's EPS (F0) Before NRI"])
        if row["12 Mo Trailing EPS"] != '':
            row["12 Mo Trailing EPS"] = float(row["12 Mo Trailing EPS"])
        if row["F1 Consensus EPS Est"] != '':
            row["F1 Consensus EPS Est"] = float(row["F1 Consensus EPS Est"])
        mongo_item = {
            "Ticker": row["Ticker"],
            "zacksData": {
                "updatedAt": datetime.today().strftime("%d/%m/%Y"),
                "Company Name": row["Company Name"],
                # "Market Cap": float(row["Market Cap (mil)"]) * 1000000,
                "Mkt Cap": float(row["Mkt Cap"]),
                "Exchange": row["Exchange"],
                "Month of Fiscal Yr End": float(row["Month of Fiscal Yr End"]),
                "Sector": row["Sector"],
                "Industry": row["Industry"],
                "Last Close": float(row["Last Close"]),
                "Last Yr's EPS (F0) Before NRI": row["Last Yr's EPS (F0) Before NRI"],
                "Last Reported Fiscal Yr (yyyymm)": row["Last Reported Fiscal Yr  (yyyymm)"],
                "12 Mo Trailing EPS": row["12 Mo Trailing EPS"],
                "F1 Consensus Est": float(row["F1 Consensus EPS Est"]),
                "# of Analysts in F1 Consensus": float(row["# of Analysts in F1 Consensus"]),
                "F2 Consensus Est": float(row["F2 Consensus EPS Est"]),
                "# of Analysts in F2 Consensus": float(row["# of Analysts in F2 Consensus"]),
                "F(1) Consensus Sales Est. ($mil)": float(row["F(1) Consensus Sales Est. ($mil)"]),
                "Q(1) Consensus Sales Est. ($mil)": float(row["Q(1) Consensus Sales Est. ($mil)"]),
                "EG1": ((float(row["F1 Consensus EPS Est"]) - float(row["Last Yr's EPS (F0) Before NRI"])) / abs(float(row["Last Yr's EPS (F0) Before NRI"]))) * 100,
                "EG2": ((float(row["F2 Consensus EPS Est"]) - float(row["F1 Consensus EPS Est"])) / abs(float(row["F1 Consensus EPS Est"]))) * 100,
                "PE1": float(row["Last Close"]) / float(row["F1 Consensus EPS Est"]),
                "PE2": float(row["Last Close"]) / float(row["F2 Consensus EPS Est"]),
                "PEG1": float(row["Last Close"]) / float(row["F1 Consensus EPS Est"]) / (((float(row["F1 Consensus EPS Est"]) - float(row["Last Yr's EPS (F0) Before NRI"])) / abs(float(row["Last Yr's EPS (F0) Before NRI"]))) * 100),
                "PEG2": float(row["Last Close"]) / float(row["F2 Consensus EPS Est"]) / (((float(row["F2 Consensus EPS Est"]) - float(row["F1 Consensus EPS Est"])) / abs(float(row["F1 Consensus EPS Est"]))) * 100)
            }
        }
        # except:
        #     row["updatedAt"] = datetime.today().strftime("%d/%m/%Y")
        #     mongo_item = {
        #         "Ticker": row["Ticker"],
        #         "zacksData": row
        #     }

        # collection.insert_one(mongo_item)
        collection.find_one_and_update({"symbol": row["Ticker"]}, { "$set": { "zacksData": mongo_item["zacksData"] }}, upsert=True)
    
    # print(mongo_item)

# print((rows[0:2]))