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
'''
setup the driver
driver = uc.Chrome()

'''
headers = {"User-Agent": "Mozilla/5.0"}



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
    
    time.sleep(5)  
    
    stores = []
    #doesnt work
    scroll_pause_time = 3
    max_attempts = 10
    attempts = 0

    # Identify the scrollable results panel on the left
    scrollable_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]')

    while attempts < max_attempts:
        elements = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
        for element in elements:
            aria_label = element.get_attribute("aria-label")
            if aria_label and aria_label not in stores:
                stores.append(aria_label)
        
        
        left_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
        )

        # Scroll the left panel
        scroll_pause_time = 2
        for i in range(20):  # Adjust range to control the number of scrolls
            driver.execute_script("arguments[0].scrollTop += 500;", left_panel)
            time.sleep(scroll_pause_time)

            
            
            attempts += 1
    
            
    driver.quit()
    return stores
    


def scroll_left_panel(zip_code):
    url = f"https://www.google.com/maps/search/grocery+store+in+{zip_code}"
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # Wait for the results panel to load
        left_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
        )

        # Scroll the left panel
        scroll_pause_time = 2
        for i in range(20):  # Adjust range to control the number of scrolls
            driver.execute_script("arguments[0].scrollTop += 300;", left_panel)
            time.sleep(scroll_pause_time)

        print("Scrolling complete.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scroll_left_panel(36527)