from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

default_args = {
    "email": ['eobayomi2@gmail.com'],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def scrape_y_combinator(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    driver.implicitly_wait(10)  # Set an implicit wait for 10 seconds to allow elements to load
    time.sleep(10)  # Wait for 10 seconds to allow the page to load

    previous_count = 0
    current_count = 0
    page_delay = 5

    company_details = [["name", "Description", "Location", "tags"]]

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(page_delay)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        current_count = len(soup.find_all('a', class_="_company_86jzd_338"))
        if current_count == previous_count:
            break
        previous_count = current_count
        print(f"Found {current_count} companies")

    for element in soup.find_all('a', class_="_company_86jzd_338"):
        title = element.find('span', class_="_coName_86jzd_453").text
        description = element.find('span', class_="_coDescription_86jzd_478").text
        location = element.find('span', class_="_coLocation_86jzd_469").text
        tags = ",".join([tag.text for tag in element.find_all('span', class_="pill _pill_86jzd_33") if tag])
        company_details.append([title, description, location, tags])

    driver.quit()

    df = pd.DataFrame(company_details[1:], columns=company_details[0])
    return df

def copy_to_snowflake(df):
    import snowflake.connector
    import os
    from dotenv import load_dotenv
    from snowflake.connector.pandas_tools import write_pandas

    load_dotenv()

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
    success, nchunks, nrows, _ = write_pandas(conn=connection_details, df=df, table_name="COMPAINES",
                                              database="YC_COMPANIES", schema="RAWYC_COMPANIES", auto_create_table=True, overwrite=True)
    return success, nchunks, nrows, _

def run_scraper():
    url = "https://www.ycombinator.com/companies"
    data_set = scrape_y_combinator(url)
    return data_set

def load_data(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='Extract_data')
    copy_to_snowflake(df)

with DAG(
    'Y_combinator_extract_load',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    description='This DAG extracts data from the Y Combinator website and loads it into a Snowflake database',
    schedule='@daily',
    catchup=False,
    tags=["Y_combinator"],
) as dag:

    extract_load_data = PythonOperator(task_id='Extract_data', python_callable=run_scraper)
    load_to_snowflake = PythonOperator(task_id='load_to_snowflake', python_callable=load_data, provide_context=True)

    extract_load_data >> load_to_snowflake