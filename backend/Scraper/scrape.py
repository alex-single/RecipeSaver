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
   
    
if __name__ == "__main__":
    u = input("Enter url: ")
    if u != None:
        print(get_ingredients_from_url(u))
        