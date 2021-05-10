import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

driver.get("https://mastercard.wd1.myworkdayjobs.com/CorporateCareers")

time.sleep(3)
previous_height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(2)

    new_height  = driver.execute_script('return document.body.scrollHeight')

    if new_height == previous_height:
        break
    previous_height = new_height

src = driver.page_source
soup = BeautifulSoup(src,'lxml')

parsed_content = soup.find_all('div', {'class': 'WB5F WP4F'})

item_list=[]

for i in parsed_content:
    name = i.find('div', {'class': 'gwt-Label WJBP WCAP'}).text.strip()
    details = i.find('span',{'class':'gwt-InlineLabel WEAG WD5F'}).text.strip()
    id_ = i.find('div', {'class': 'gwt-Label WJBP WCAP'}).get("id")
    x_path = '//*[@id="{}"]'.format(id_)
    button = driver.find_element_by_xpath(x_path)
    actions = ActionChains(driver)
    actions.context_click(button).perform()
    time.sleep(2)
    url_xpath = driver.find_elements_by_xpath('/html/body/div[6]/div[1]/div/table/tbody/tr[2]/div')
    url = url_xpath[0].get_attribute("data-clipboard-text")

    items={
        'job_post':name,
        'details':details,
        'x_path':x_path,
        'url':url,
    }

    item_list.append(items)

df = pd.DataFrame(item_list)
df.to_csv("master_card_test.csv")
