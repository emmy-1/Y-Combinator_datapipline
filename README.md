![download](https://github.com/user-attachments/assets/a90e21d3-d2a3-45fe-980e-d5e92fd53ee5)

Y Combinator DataPipline
========                                    
The Y Combinator Data Pipeline is an automated ETL (Extract, Transform, Load) solution designed to extract company information from Y Combinator's API, transform the data into a structured format, and load it into a Snowflake data warehouse for analysis and reporting. This pipeline leverages Apache Airflow for orchestration, dbt for data transformation, snowflake for data warehousing, and Python for data extraction and processing.

**Key Features:**
- **Data Extraction**: Utilizes a Python-based API client to fetch real-time data on startups, founders, and funding rounds from Y Combinator.
- **Data Transformation**: Implements data cleaning and transformation processes to ensure the data is structured, consistent, and ready for analysis. This includes handling missing values, normalizing data formats, and enriching datasets with additional information.
- **Data Loading**: Loads the transformed data into a Snowflake data warehouse, enabling efficient querying and analysis.
- **Orchestration**: Uses Apache Airflow to schedule and manage the workflow, ensuring that data extraction, transformation, and loading tasks are executed in the correct order and at specified intervals.
- **Modular Design**: The pipeline is designed with modular components, allowing for easy updates and maintenance. Utility functions for data processing and API interactions are separated into dedicated files for better organization and reusability.
- **Testing and Validation**: Includes unit tests to validate the functionality of each component, ensuring data integrity and reliability throughout the pipeline.

**Use Cases:**
- Analyze startup trends and funding patterns over time.
- Generate reports on Y Combinator's portfolio companies for stakeholders.
- Provide insights into the performance and growth of startups within the Y Combinator ecosystem.

**Technologies Used:**
- **Python**: For data extraction and processing.
- **Apache Airflow**: For workflow orchestration.
- **dbt**: For data transformation and modeling.
- **Snowflake**: For data storage and analytics.

Deploy Your Project Locally
===========================

1. Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

2. Verify that all 4 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://www.astronomer.io/docs/astro/deploy-code/

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support.
