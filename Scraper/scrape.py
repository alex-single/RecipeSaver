from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc 
#setup the driver

driver = uc.Chrome()

def ingredients_available_walmart(url):
    driver.get(url)
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys("milk")
    search_bar.send_keys(Keys.RETURN)
    
    time.sleep(10)


def get_ingredients_from_url(url):
    driver.get(url)
    

if __name__ == "__main__":
    ingredients_available_walmart("https://www.walmart.com")