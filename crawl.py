from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# create a new instance of the Firefox driver
driver = webdriver.Firefox()

salt_class = 'saltInfo DrugHeader__meta-value___vqYM0'
manufacturer_class = 'DrugHeader__meta-title___22zXC'
count_info_class = 'style__countInfo___sVIyR'
product_link_class = 'style__product-link___1hWpa'
one_product_xpath = '/html/body/div[3]/div[1]/div/div/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/a'

df = pd.read_excel(r'data/drugs.xlsx')

salts = ['' for _ in range(len(df['manufacturer']))]
name_on_website = ['' for _ in range(len(df['manufacturer']))]


def save_progress():
    df['salt'] = salts
    df['name_on_website'] = name_on_website
    df.to_excel(r'data/new.xlsx', index=False)


for i in range(len(df['manufacturer'])):
    m = df['manufacturer'][i]
    d = df['drug'][i]
    driver.get("https://www.1mg.com/search/all?name=" + d)
    count_info = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, count_info_class)))
    count = int(count_info.text.split()[0].replace(',', ''))
    if count == 0:
        salts[i] = 'not found'
        name_on_website[i] = 'not found'
        continue
    elif count == 1:
        product = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, one_product_xpath)))
    else:
        try:
            product = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, product_link_class)))
        except:
            salts[i] = 'not found'
            name_on_website[i] = 'not found'
            continue
    driver.get(product.get_attribute('href'))
    try:
        salt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div[2]/div/div/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[2]/div[2]/a'))).text
    except:
        salt = 'not found'
    try:
        name = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/div/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div[1]/h1').text
    except:
        name = 'not found'
    salts[i] = salt
    name_on_website[i] = name
    print(salts)
    print(name_on_website)
    if i % 10 == 0:
        save_progress()
