import requests
from bs4 import BeautifulSoup
import pyperclip  # Make sure to install this library using `pip install pyperclip`

# Define the target URL
url = input("Enter the URL of the page: ")

# User-Agent header to mimic a browser
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

# Fetch the webpage
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Copy the prettified HTML to the clipboard
    prettified_html = soup.prettify()
    pyperclip.copy(prettified_html)
    
    print("HTML has been copied to your clipboard. You can paste it here.")
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
