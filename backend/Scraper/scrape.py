from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc 
from bs4 import BeautifulSoup as bs
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
'''
setup the driver
driver = uc.Chrome()

'''
headers = {"User-Agent": "Mozilla/5.0"}

publix = False
walmart = False
kroger = False
wholeFoods = False
aldi = False



def get_ingredients_from_url(url):
    
    
    
    
    parts = url.split(".")
    domain = parts[1]
    
    #allrecipes https://www.allrecipes.com/
    if domain == 'allrecipes' :
        #driver.get(url)
        response = requests.get(url, headers=headers)
    
        # Check if the request was successful
        if response.status_code != 200:
            print("Failed to fetch the page")
            return None

        # Parse the HTML content
        soup = bs(response.text, 'html.parser')
        recipeDetails = soup.find_all('ul', class_ = 'mm-recipes-structured-ingredients__list')
        ingredients = []
    
        for item in recipeDetails:
            list_items = item.find_all('li', class_='mm-recipes-structured-ingredients__list-item')
            for list_item in list_items:
                name = list_item.find('span', attrs={'data-ingredient-name': 'true'}).text.strip()
                ingredients.append(name)
                
                #note to self ^^ strip after commas on the stupid shit

                
        cleaned_ingredients = []
        for ingredient in ingredients:
            if ',' in ingredient:
                clean_ingredient = ingredient.split(',')
                cleaned_ingredients.append(clean_ingredient[0])
            else:
                cleaned_ingredients.append(ingredient)
    
    
    
    
        
    
    return cleaned_ingredients 



def get_store_names(zip):
    url = f"https://www.google.com/maps/search/grocery+store+in+{zip}"
    driver = webdriver.Chrome()  
    driver.get(url)
    
    time.sleep(3)  
    
    stores = set()
    #doesnt work
    
    left_panel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
    # Identify the scrollable results panel on the left

    for i in range(20):
        elements = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
        
        
        for element in elements:
            aria_label = element.get_attribute("aria-label")
            driver.execute_script("arguments[0].scrollTop += 100;", left_panel)
            
            if aria_label and aria_label not in stores:
                stores.add(aria_label)
            
            
    
    global publix, walmart, kroger, wholeFoods, aldi
    publix = any("Publix" in store for store in stores)
    walmart = any("Walmart" in store for store in stores)
    kroger = any("Kroger" in store for store in stores)
    wholeFoods = any("Whole Foods" in store for store in stores)
    aldi = any("ALDI" in store for store in stores)
            
        
        
    
            
    driver.quit()
    return stores

def human_typing(element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(.125, .3))


#
def walmart_login(user, password):
    url = f"https://www.walmart.com/account/login"
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-infobars")  
    driver = uc.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"})
    driver.get(url)
    time.sleep(3)
    
    email_box = driver.find_element(By.NAME, "Email Address")
    human_typing(email_box, user)
    email_box.send_keys(Keys.RETURN)
    time.sleep(1)
    
    pass_box = driver.find_element(By.XPATH, '/html/body/div/div[1]/section/form/div[1]/div/input')
    human_typing(pass_box, password)
    pass_box.send_keys(Keys.RETURN)
    time.sleep(30)

def walmart_items(ingredients, zip):
    url = f"https://www.walmart.com"
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-infobars")  
    driver = uc.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"})
    driver.get(url)
    time.sleep(5)
    
    #put in zip
    but1 = driver.find_element(By.XPATH, '/html/body/div/div[1]/span/header/section/div/div/div[1]/button/div')
    but1.click()
    time.sleep(.5)
    but2 = driver.find_element(By.XPATH, '/html/body/div/div[1]/span/header/section/div/div/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/button')
    but2.click()
    time.sleep(2)
    
            
        
    areaSearch = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/input')
    for i in range(6):areaSearch.send_keys(Keys.BACK_SPACE)
    human_typing(areaSearch, zip)
    time.sleep(3)
    save_but1 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div/div[3]/div/button')
    save_but1.click()
    time.sleep(2)
    search_bar = driver.find_element(By.XPATH, '/html/body/div/div[1]/span/header/form/div/input')
    time.sleep(2)
    for ingredient in ingredients:
        pass
    
    
    driver.quit()


if __name__ == "__main__":
    walmart_items("a", '36527')