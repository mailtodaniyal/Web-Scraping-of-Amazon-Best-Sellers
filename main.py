from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver as per your configuration
webdriver_service = Service("/path/to/chromedriver")

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Function to extract product data
def get_product_data(product):
    try:
        title = product.find_element(By.CSS_SELECTOR, "span.a-text-normal").text
    except:
        title = None
    try:
        brand = product.find_element(By.CSS_SELECTOR, "span.a-size-base-plus.a-color-base").text
    except:
        brand = None
    try:
        price = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
    except:
        price = None
    try:
        link = product.find_element(By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href")
    except:
        link = None
    try:
        image = product.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
    except:
        image = None
    return {"Title": title, "Brand": brand, "Price": price, "Link": link, "Image": image}

# Initialize an empty list to store product data
product_list = []

# URL of the Amazon Best Sellers in Women's Western Wear Tops
url = "https://www.amazon.in/gp/bestsellers/apparel/1968326031"

# Open the URL
driver.get(url)
time.sleep(2)  # Let the page load

# Loop through the pages
while True:
    # Find all product elements on the page
    products = driver.find_elements(By.CSS_SELECTOR, "div.zg-grid-general-faceout")
    for product in products:
        data = get_product_data(product)
        product_list.append(data)
        if len(product_list) >= 200:  # Stop if we have enough products
            break
    if len(product_list) >= 200:
        break
    # Try to find the 'Next' button to go to the next page
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li.a-last a")
        next_button.click()
        time.sleep(2)  # Let the page load
    except:
        break  # No more pages

# Close the driver
driver.quit()

# Create a DataFrame from the list
df = pd.DataFrame(product_list)

# Save the DataFrame to a CSV file
df.to_csv("amazon_womens_western_wear_tops.csv", index=False)

print("Scraping completed. Data saved to 'amazon_womens_western_wear_tops.csv'.")
