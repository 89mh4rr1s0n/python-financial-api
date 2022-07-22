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

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

currencies = [
    'USD',
    'GBP'
]

driver.get('https://www.investing.com/search/?q=USD&tab=ec_event')

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

time.sleep(6)

result_links = driver.find_elements(By.XPATH, '//*[@id="fullColumn"]/div/div[6]/div[3]/div/a[not(descendant::span[contains(text(), "Speaks")]) and not(descendant::span[contains(text(), "Election")]) and not(descendant::span[contains(text(), "FOMC")]) and not(descendant::span[contains(text(), "Testifies")]) and (descendant::span[2][contains(text(), "USD")])  ]')

# result_links = driver.find_elements(By.XPATH, '//*[@id="fullColumn"]/div/div[6]/div[3]/div/a[not(descendant::span[contains(text(), "Speaks")]) and not(descendant::span[contains(text(), "Election")]) and not(descendant::span[contains(text(), "FOMC")]) and not(descendant::span[contains(text(), "Testifies")]) and (descendant::span[@class="second", contains(text(), "USD")]) ]')

links = []

for link in result_links:
    links.append(link.get_attribute('href'))

print(json.dumps(links, indent=4))
print(len(links))