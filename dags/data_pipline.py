from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from testscrapper import scrape_y_combinator, copy_to_snowflake



def run_scraper():
    url = "https://www.ycombinator.com/companies"
    data_set = scrape_y_combinator(url)
    return data_set

def load_data(**kwargs):
    ti = kwargs['ti']  # Get the task instance
    df = ti.xcom_pull(task_ids='Extract_data')  # Pull the DataFrame from XCom
    copy_to_snowflake(df)  # Pass the DataFrame to the copy function 



with DAG(
    'Y_combinator_extract_load',
    default_args ={
        "email": ['eobayomi2@gmail.com'],
        "email_on_failure": True,
        "email_on_retry": True,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    start_date = datetime(2023,1,1),
    description = 'This Dag main goal is to extract data from the Y_combinator website and directly load the data into a snowflake database',
    schedule ='@daily', catchup = False):

    extract_load_data = PythonOperator(task_id = 'Extract_data', python_callable = run_scraper )
    load_to_snowflake = PythonOperator(task_id= 'load_to_snowflake', python_callable = load_data, provide_context=True)

    extract_load_data >> load_to_snowflake
    