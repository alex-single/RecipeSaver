from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_store_names(zip):
    url = f"https://www.google.com/maps/search/grocery+store+in+{zip}"
    driver = webdriver.Chrome()  b  
    driver.get(url)
    
    time.sleep(5)  
    
    stores = []
    elements = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
    for element in elements:
        aria_label = element.get_attribute("aria-label")
        if aria_label:
            stores.append(aria_label)
    
    driver.quit()
    return stores

print(get_store_names(input('Enter zipcode: ')))