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
from selenium.webdriver import ActionChains
import pandas as pd

'''
setup the driver
driver = uc.Chrome()

'''
USER_AGENTS = [
    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
]

publix = False
walmart = False
kroger = False
wholeFoods = False
aldi = False


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

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
    url = "https://www.walmart.com"
    user_agent = random.choice(USER_AGENTS)

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")

    # Initialize Chrome driver with undetected_chromedriver's options
    driver = uc.Chrome(options=options)
    
    driver.get(url)
    # Modify navigator.webdriver flag to prevent detecti
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
    search_bar = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/span/header/form/div/input')

    time.sleep(2)
    for ingredient in ingredients:
        human_typing(search_bar, str(ingredient))
        time.sleep(5)
    
    driver.quit()
   
def publix_items(ingredients, zip):
    url = f"https://www.publix.com/"
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-infobars")  
    #chrome_options.add_argument("--headless")  # Enable headless mode
    driver = uc.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"})
    driver.get(url)
    time.sleep(1)
    
    time.sleep(2)  # Wait for popup to appear
    try:
        # Switch to the permission popup and click "Block"
        driver.execute_cdp_cmd('Browser.grantPermissions', {
            'origin': 'https://www.publix.com',
            'permissions': []
        })
        driver.execute_cdp_cmd('Browser.setPermission', {
            'origin': 'https://www.publix.com',
            'permission': {'name': 'geolocation'},
            'setting': 'denied'
        })
    except Exception as e:
        print("Could not handle location popup:", str(e))
        
    wait = WebDriverWait(driver, 10)
    
    findstore = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/header/div[1]/div/div[2]/div/div/div[2]/div/div/button')))
    findstore.click()
    
    storefind = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/header/div[1]/div/div[2]/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[1]/form/input')))
    storefind.send_keys(zip)
    
    
    confirmbut = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/header/div[1]/div/div[2]/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[1]/form/button')))
    confirmbut.click()
    
    #get back to this later bc it making me mad
    choosestore = wait.until(EC.element_to_be_clickable((By.ID,'choose_1400')))
    choosestore.click()
    time.sleep(3)
    curbside = wait.until(EC.element_to_be_clickable((By.ID, 'deliveryCurbside')))
    curbside.click()
    time.sleep(2)
    proceed = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/header/div[1]/div/div[4]/div/div[3]/div/div/button[2]')))
    proceed.click()
    
    #need to fix location
    time.sleep(5)
    try:
        # Try multiple selector strategies
        pickup_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "e-1pmzhru")))
        pickup_button.click()
    except:
        try:
            # Try by XPath looking for the text content
            pickup_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'e-1pmzhru') or .//span[contains(text(), 'Pickup')]]")))
            driver.execute_script("arguments[0].click();", pickup_button)
        except:
            try:
                # Try finding by the SVG parent button
                pickup_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//svg[@width='24' and @height='24']]")))
                driver.execute_script("arguments[0].click();", pickup_button)
            except Exception as e:
                print(f"Could not click pickup button: {e}")
                # Continue anyway as the page might still work
    
    time.sleep(2)  # Wait for any modal or page update after clicking
    
    try:
        # Try by class name
        confirm_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "e-u5hdv")))
        confirm_button.click()
    except:
        try:
            # Try by XPath looking for the text "Confirm"
            confirm_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'e-u5hdv') or .//span[text()='Confirm']]")))
            driver.execute_script("arguments[0].click();", confirm_button)
        except:
            try:
                # Try finding by button type and class combination
                confirm_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[@type='submit'][.//span[contains(@class, 'e-e2f3my')]]")))
                driver.execute_script("arguments[0].click();", confirm_button)
            except Exception as e:
                print(f"Could not click confirm button: {e}")
    
    time.sleep(2)  # Wait for confirmation to process
    
    time.sleep(2)
    searchbar = wait.until(EC.presence_of_element_located((By.ID, "search-bar-input")))
    # Dictionary to store ingredient prices
    ingredient_prices = {}
    
    for i in range(len(ingredients)):
        # Wait for search bar to be clickable
        searchbar = wait.until(EC.element_to_be_clickable((By.ID, "search-bar-input")))
        
        # Clear any existing text first
        searchbar.clear()
        time.sleep(1)  # Short wait after clearing
        
        # Type new search
        searchbar.send_keys(ingredients[i])
        searchbar.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Wait for results
        
        # Clear the searchbar using JavaScript
        driver.execute_script("arguments[0].value = '';", searchbar)
        
        # Wait for page to load and get results
        page_source = driver.page_source
        soup = bs(page_source, 'html.parser')
        
        # Find all price spans
        item_info = soup.find_all('span', class_='screen-reader-only')
        
        price_spans = []
        try:
            for _ in range(min(5, len(item_info))):  # Take either 5 or all available items
                price_spans.append(item_info[_])
        except IndexError:
            print(f"Found fewer than 5 results for {ingredients[i]}")
            
            
        # Extract and clean prices for this ingredient
        prices = []
        for span in price_spans:
            price_text = span.text
            if 'Current price:' in price_text:
                try:
                    # Remove 'Current price: $' and any text after numbers (like 'each (estimated)')
                    price_str = price_text.replace('Current price: $', '')
                    # Split on space and take first part (the number)
                    price_str = price_str.split()[0]
                    # Convert to float
                    price = float(price_str)
                    prices.append(price)
                except (ValueError, IndexError):
                    # Skip prices that can't be converted
                    continue
        
        # Store prices for this ingredient (only if we found any)
        if prices:
            ingredient_prices[ingredients[i]] = prices
            print(f"Prices for {ingredients[i]}: {prices}")
    
    print("\nAll ingredient prices:")
    for ingredient, prices in ingredient_prices.items():
        print(f"{ingredient}: {prices}")
    
    # Create a dictionary to store the maximum number of options
    max_options = max(len(prices) for prices in ingredient_prices.values())
    
    # Create a dictionary for the DataFrame
    df_data = {
        ingredient: prices + [None] * (max_options - len(prices))  # Pad with None for missing prices
        for ingredient, prices in ingredient_prices.items()
    }
    
    # Create DataFrame with ingredients as columns
    df = pd.DataFrame(df_data)
    
    # Add option numbers as index
    df.index = [f'Option {i+1}' for i in range(max_options)]
    
    # Print the DataFrame
    
    # Optionally save to CSV

if __name__ == "__main__":
   publix_items(get_ingredients_from_url(input("ENTER URL: ")), "36527")
    
   