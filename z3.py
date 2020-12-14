import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import numpy as np
import pandas as pd
import regex as re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

chromedriver = "/usr/local/bin/chromedriver" # path to the chromedriver executable
chromedriver = os.path.expanduser(chromedriver)
print('chromedriver path: {}'.format(chromedriver))
sys.path.append(chromedriver)
driver = webdriver.Chrome(chromedriver)

zillow_url = 'https://www.zillow.com/homes/Altoona,-IA_rb/'

driver.get(zillow_url)
ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)
wait = WebDriverWait(driver, 30, ignored_exceptions=ignored_exceptions)

maininfo = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "list-card")))
print(len(maininfo))
def get_page_info(listdata, pagelistlength):   #pagelistlength is maininfo variable
    for i in range(len(pagelistlength)):

        article_path = '/html/body/div[1]/div[5]/div/div[1]/div/div[1]/ul/li[1]/article'
        article_list = list(article_path)
        article_list[-10] = str(i + 1)
        article_path = ''.join(article_list)
        print('before click party')
        try:
            clickinfo = wait.until(EC.presence_of_all_elements_located((By.XPATH, article_path)))
            print('got clickable page?')
            clickinfo[0].click()
            time.sleep(3)
            maininfo = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ds-summary-row")))
            listdata.append(maininfo[0].text)
            address = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ds-address-container")))
            listdata.append(address[0].text)
            time.sleep(2)
            lotsize = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ds-home-fact-list")))
            listdata.append(lotsize[0].text)
            time.sleep(3)
            try:

                backbutton = wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div[6]/div/div[1]/div/button")))  # /html/body/div[1]/div[6]/div/div[1]/div/button

                backbutton[0].click()
                print('regular back used')
            except:
                try:
                    backbutton = wait.until(EC.presence_of_all_elements_located((By.ID, "mobile-back-link")))
                    backbutton[0].click()
                    print('mobile link used')
                except:
                    print('back button didnt work')

        except:
            print('main not working')
            break
        print('length of listdata is: ',len(listdata))
    print('through a page')
    return listdata
data = []
while True:

    try:
        altoonainfo = get_page_info(data,  maininfo)
        nextpagebutton = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="grid-search-results"]/div[2]/nav/ul/li[3]/a')))
        nextpagebutton[0].click()
        if len(altoonainfo) < 3:
            break
    except:
        print('next page button didnt work')
        break
print('we downloaded it')
driver.quit()


if len(data) > 3:
    datadf = pd.DataFrame(data)
    datadf.to_csv('altoonazillowfullinfo.csv')




