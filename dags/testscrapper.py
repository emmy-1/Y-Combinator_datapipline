from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from utils.function import get_html_content
from utils.function import find_text,find_html
from bs4 import BeautifulSoup
import time
import pandas as pd


def scrpae_y_combinator(url):
    # Set up Chrome options for headless browsing and page load strategy
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.page_load_strategy = 'none'
    # Initialize the Chrome driver with the specified options
    driver = Chrome(options=options) 
    
    driver.implicitly_wait(10)# Set an implicit wait for 10 seconds to allow elements to load
    driver.get(url)# Navigate to the specified URL
    time.sleep(10)# Wait for 10 seconds to allow the page to load

    previous_count = 0 # Initialize previous count of companies found
    current_count = 0 # Initialize current count of companies found
    page_delay = 5 # Set the delay between page scrolls to 5 seconds


    while True:
        # Scroll to the bottom of the page to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(page_delay)# Wait for new content to load

        html = driver.page_source# Get the HTML content of the page
        soup = BeautifulSoup(html, 'html.parser') # Parse the HTML with BeautifulSoup
        current_count = len(soup.find_all('a', class_="_company_86jzd_338"))
        if current_count == previous_count:
            break  # Exit loop if no new companies are found
        previous_count = current_count
        print(f"Found {current_count} companies")

        company_details = [["name", "Description", "Location", "tags"]]  # Initialize with a list of column names
    # Extract details for each company found
    for element in soup.find_all('a', class_="_company_86jzd_338"):
        title = element.find('span', class_="_coName_86jzd_453").text # Get company description
        description = element.find('span', class_="_coDescription_86jzd_478").text
        location = element.find('span', class_="_coLocation_86jzd_469").text  # Get company location
        # Ensure we are only getting tags related to the current company
        tags = ",".join([tag.text for tag in element.find_all('span', class_="pill _pill_86jzd_33") if tag])  # Filter to ensure only valid tags are included
        company_details.append([title, description, location, tags])  # Append data as a list

    driver.close()  # Close the driver after scraping

    # Create DataFrame after collecting all data
    df = pd.DataFrame(company_details[1:], columns=company_details[0])  # Use the first element as column names
    df.to_csv('company_details.csv', index=False)

# Call the function with the URL
scrpae_y_combinator("https://www.ycombinator.com/companies")