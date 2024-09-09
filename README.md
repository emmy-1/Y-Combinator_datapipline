### Y Combinator Data Pipeline

**Project Overview:**
The Y Combinator Data Pipeline is an automated ETL (Extract, Transform, Load) solution designed to extract company information from Y Combinator's API, transform the data into a structured format, and load it into a Snowflake data warehouse for analysis and reporting. This pipeline leverages Apache Airflow for orchestration, dbt for data transformation, and Python for data extraction and processing.

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
