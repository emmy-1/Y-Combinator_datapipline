![download](https://github.com/user-attachments/assets/a90e21d3-d2a3-45fe-980e-d5e92fd53ee5)

Y Combinator DataPipline
========                                    
The Y Combinator Data Pipeline is an automated ETL (Extract, Transform, Load) solution designed to extract company information from Y Combinator's API, transform the data into a structured format, and load it into a Snowflake data warehouse for analysis and reporting. This pipeline leverages Apache Airflow for orchestration, dbt for data transformation, snowflake for data warehousing, and Python for data extraction and processing.


![Ycombinator - page 1](https://github.com/user-attachments/assets/b7ccb650-f923-43cc-80d2-58bc35be1ebb)

**Key Features:**
- **Data Extraction**: Utilizes Python-based scripts to fetch real-time data from Y Combinator startup directory, including YC companies by industry, region, company size, and more.
- **Data Transformation**: Implements data cleaning and transformation processes to ensure the data is structured, consistent, and ready for analysis. This includes handling missing values, normalizing data formats, and enriching datasets with additional information.
- **Data Loading**: Loads the transformed data into a Snowflake data warehouse, enabling efficient querying and analysis.
- **Orchestration**: Uses Apache Airflow to schedule and manage the workflow, ensuring that data extraction, transformation, and loading tasks are executed in the correct order and at specified intervals.
- **Modular Design**: The pipeline is designed with modular components, allowing for easy updates and maintenance. Utility functions for data processing are separated into dedicated files for better organization and reusability.
- **Monitoring and Alams**: The system includes email notifications triggered after successful or failed events.

**Use Cases:**
- Analyze startup trends and funding patterns over time.
- Generate reports on Y Combinator's portfolio companies for stakeholders.
- Provide insights into the performance and growth of startups within the Y Combinator ecosystem.

**Technologies Used:**
- **Python**: For data extraction and processing.
- **Apache Airflow**: For workflow orchestration.
- **dbt**: For data transformation and modeling.
- **Snowflake**: For data storage and analytics.

## Project Structure

The project is organized as follows:

- `dags/`: Contains the Airflow DAGs and related scripts.
  - `dbt/`: Contains dbt project files and configurations.
    - `analyses/`: Directory for dbt analysis files.
    - `logs/`: Directory for dbt log files.
    - `macros/`: Directory for dbt macro files.
    - `seeds/`: Directory for dbt seed files.
    - `snapshots/`: Directory for dbt snapshot files.
    - `tests/`: Directory for dbt test files.
    - `dbt_project.yml`: dbt project configuration file.
- `logs/`: Directory for general log files.
- `.astro/`: Astronomer configuration files.
- `.gitignore`: Git ignore file.
- `LICENSE`: License file.
- `README.md`: Project documentation file.
- `requirements.txt`: Python dependencies file.

## Getting Started

### Prerequisites

- Docker
- Python 3.8+
- Apache Airflow
- dbt
- Snowflake account

Deploy Your Project Locally
===========================

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/y-combinator-datapipeline.git
   cd y-combinator-datapipeline
   ```

2. Start Airflow on your local machine:
   ```sh
   astro dev start
   ```

   This command will spin up 4 Docker containers on your machine, each for a different Airflow component:
   - Postgres: Airflow's Metadata Database
   - Webserver: The Airflow component responsible for rendering the Airflow UI
   - Scheduler: The Airflow component responsible for monitoring and triggering tasks
   - Triggerer: The Airflow component responsible for triggering deferred tasks

3. Verify that all 4 Docker containers were created by running:
   ```sh
   docker ps
   ```

   Note: Running `astro dev start` will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either stop your existing Docker containers or change the port.

4. Access the Airflow UI for your local Airflow project:
   Open your browser and go to [http://localhost:8080/](http://localhost:8080/) and log in with 'admin' for both your Username and Password.

   You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

## :mag_right: Explanation of the DAGs

<details>
    <summary> Y_combinator_extract_load </summary>
  

This DAG (Directed Acyclic Graph) is designed to extract data from the Y Combinator website and load it into a Snowflake database. Here's a breakdown of what it does:

1. **Scrape Data**: The `scrape_y_combinator` function uses Selenium and Beautiful Soup to scrape company details from the Y Combinator website.
2. **Load Data to Snowflake**: The `copy_to_snowflake` function takes the scraped data and loads it into a Snowflake database.
3. **DAG Definition**: The DAG is defined to run weekly, starting from January 1, 2023. It has two tasks:
   - `Extract_data`: Runs the `run_scraper` function to scrape data.
   - `load_to_snowflake`: Runs the `load_data` function to load the scraped data into Snowflake.
</details>

<details>
 <summary> dbt_dag </summary>
  
This DAG is designed to run dbt (data build tool) models on the data loaded into Snowflake. Here's a breakdown:

1. **Profile Configuration**: Configures the connection to Snowflake using user credentials.
2. **DBT DAG Definition**: Defines a dbt DAG that runs daily, starting from September 10, 2023. It uses the profile configuration to connect to Snowflake and execute dbt models.
</details>


## :mag_right: Explanation of dbt models

<details>
    <summary> YCslivertable.sql </summary>

### YCslivertable SQL Transformation

This SQL code creates a view or table called `YCslivertable` from a source table named `COMPAINES` in the `Y_Combinator` schema. The transformation is done in two steps using Common Table Expressions (CTEs).

## First CTE: `transformation`

This CTE performs the following transformations:

1. Renames the "name" column to "company".
2. Creates a "value_proposition" column from the "Description" column, replacing empty strings with 'Unspecified'.
3. Splits the "Location" column into city, state, and country, using default values when parts are missing.
4. Splits the "tags" column into batch, customer_type, industry, and additional_info.
5. Keeps the original "tags" column as other_info.

## Second CTE: `updated_transformation`

This CTE further refines the data by:

1. Keeping most columns from the first transformation.
2. Modifying the "industry" column:
   - If the industry is 'Travel', it appends 'Leisure and Tourism'.
   - If the industry is 'Engineering', it appends 'Product and Design'.
   - Otherwise, it keeps the original industry value.

## Final SELECT Statement

The final SELECT statement chooses specific columns from the `updated_transformation` CTE to include in the final output.

## Key Points

- This transformation cleans and structures data from the Y Combinator companies database.
- It handles missing or empty values by providing default values like 'Unspecified', 'Remote', or 'World'.
- The code splits compound fields (Location and tags) into separate columns for easier analysis.
- It standardizes some industry names by appending additional information.
</details>

<details>
    <summary> S24_batch</summary>
    This dbt model filters the Y Combinator silver table to include only companies from the S24 batch.

  ### Details
- Selects all columns from `YCslivertable`
- Filters for records where `batch` is 'S24'
  *Note*
- S24 represents the Summer 2024 Y Combinator cohort
  </details>

  
<details>
    <summary> NigeriaYCcompanines</summary>
    This dbt model filters the Y Combinator silver table to include only companies from Nigeria.

  ### Details
- Select all columns from `YCslivertable`
- Filters for records where `batch` is 'Nigeria'
  </details>
## Learning Outcomes
I Must say this has been a very insight full project for me as it allowed me work with tools i have not worked before e.g snowflake and selenium. Some of the most important concept used here were given as comments posted on my previuus project.[Check out this Reddit comment](https://www.reddit.com/r/dataengineering/comments/1fbynu7/comment/lmoe0zx/?context=3)

The core problem with my previous project was the mistake of combining tasks during the extract phase. Instead of just extracting the data, transformations were also applied at the same time.This resulted in a fragile pipeline that couldn’t rebuild historical data if the original sources were no longer available. The "T" (transformation) sneaking into the early stages caused data to be altered before being saved in its raw form, which is risky because once the source is gone, you can't easily reproduce the untransformed data





