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
driver = webdriver.Chrome(PATH)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.prnewswire.com/news-releases/manufacturing-pmi-at-53-june-2022-manufacturing-ism-report-on-business-301579263.html')
time.sleep(2)

man = driver.find_element(By.XPATH, "//*[contains(text(), 'manufacturing industries reported growth in')]")
new_orders = driver.find_element(By.XPATH, "//*[contains(text(), 'reported growth in new orders in')]")

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

man_split = man.text.split(".")
growth = man_split[0]
growth_split = growth.split(":")
growth_inds = growth_split[1]
growth_arr = growth_inds.split(";")
growth_arr = [i.lstrip() for i in growth_arr]
growth_arr_copy = growth_arr.copy()
last_growth = growth_arr_copy[len(growth_arr_copy)-1]
growth_arr.pop()
growth_arr.append(last_growth[4:len(last_growth)])
print(growth_arr)
print(len(growth_arr))
contraction = man_split[1]
contraction_split = contraction.split(":")
contraction_inds = contraction_split[1]
contraction_arr = contraction_inds.split(";")
contraction_arr = [i.lstrip() for i in contraction_arr]
contraction_arr_copy = contraction_arr.copy()
last_contraction = contraction_arr_copy[len(contraction_arr_copy)-1]
contraction_arr.pop()
contraction_arr.append(last_contraction[4:len(last_contraction)])
print(contraction_arr)
print(len(contraction_arr))

data_arr = []

for x in range(len(man_ind_list)):
    if man_ind_list[x] in growth_arr:
        item = {
            'industry': man_ind_list[x],
            'direction': 'Growth',
            'rank': growth_arr.index(man_ind_list[x]) + 1
        }
        data_arr.append(item.copy())
    elif man_ind_list[x] in contraction_arr:
        item = {
            'industry': man_ind_list[x],
            'direction': 'Contraction',
            'rank': ( 18 - len(contraction_arr) ) + contraction_arr.index(man_ind_list[x]) + 1
        }
        data_arr.append(item.copy())
    else:
        item = {
            'industry': man_ind_list[x],
            'direction': 'Neutral',
            'rank': 0
        }
        data_arr.append(item.copy())

print(data_arr)
print(len(data_arr))