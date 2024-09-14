from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def scrape_y_combinator(url):  # Corrected function name
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    driver.implicitly_wait(10)  # Set an implicit wait for 10 seconds to allow elements to load
    time.sleep(10)  # Wait for 10 seconds to allow the page to load

    previous_count = 0  # Initialize previous count of companies found
    current_count = 0  # Initialize current count of companies found
    page_delay = 5  # Set the delay between page scrolls to 5 seconds

    company_details = [["name", "Description", "Location", "tags"]]  # Initialize with a list of column names

    while True:
        # Scroll to the bottom of the page to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(page_delay)  # Wait for new content to load

        html = driver.page_source  # Get the HTML content of the page
        soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML with BeautifulSoup
        current_count = len(soup.find_all('a', class_="_company_86jzd_338"))
        if current_count == previous_count:
            break  # Exit loop if no new companies are found
        previous_count = current_count
        print(f"Found {current_count} companies")

    # Extract details for each company found
    for element in soup.find_all('a', class_="_company_86jzd_338"):
        title = element.find('span', class_="_coName_86jzd_453").text  # Get company description
        description = element.find('span', class_="_coDescription_86jzd_478").text
        location = element.find('span', class_="_coLocation_86jzd_469").text  # Get company location
        # Ensure we are only getting tags related to the current company
        tags = ",".join([tag.text for tag in element.find_all('span', class_="pill _pill_86jzd_33") if tag])  # Filter to ensure only valid tags are included
        company_details.append([title, description, location, tags])  # Append data as a list

    driver.close()  # Close the driver after scraping

    # Create DataFrame after collecting all data
    df = pd.DataFrame(company_details[1:], columns=company_details[0])  # Use the first element as column names
    return df


def copy_to_snowflake(df):
    import pandas as pd
    import snowflake.connector
    import os
    from dotenv import load_dotenv
    from snowflake.connector.pandas_tools import write_pandas

    # Load environment variables from .env file
    load_dotenv()

    # Get environment variables
    connection_details = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
    connection_details.cursor().execute("USE SCHEMA YC_Companies.RawYc_companies")
    success, nchunks, nrows, _ = write_pandas(conn = connection_details, df = df, table_name="COMPAINES",
                                               database ="YC_COMPANIES", schema="RAWYC_COMPANIES", auto_create_table=True,overwrite=True)
    return success , nchunks, nrows, _    
# Call the function with the URL and store the returned DataFrame
df = scrape_y_combinator("https://www.ycombinator.com/companies")  # Store the returned DataFrame
copy_to_snowflake(df)  # Pass the DataFrame to the copy function