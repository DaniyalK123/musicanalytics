# Music Data Transformation with DBT

This component is responsible for transforming and modeling the music data using dbt (Data Build Tool) to create fact and dimension tables in a BigQuery data warehouse.

To run the dbt transformations, follow these steps:

1. Install dbt using `pip install dbt`.
2. Configure the `profiles.yml` file with the BigQuery project ID, dataset name, and service account keyfile path.
3. Set the environment variables for the BigQuery project ID, dataset name, and service account keyfile path.
4. Run the dbt transformations with the following commands:
   - `dbt deps`
   - `dbt seed`
   - `dbt run`
   - `dbt test`