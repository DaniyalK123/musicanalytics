This component is responsible for extracting data from various music-related APIs, cleaning the data, and storing it in Parquet format in Google Cloud Storage.

To run the data ingestion process, follow these steps:

1. Set up and configure the API keys for Spotify, MusicBrainz, and the Billboard Charts.
2. Configure the environment variables for GCP credentials, BigQuery project ID, dataset name, GCS bucket name, and GCS path.
3. Install the required Python libraries using `pip install -r requirements.txt`.
4. Run the data extraction script with `python data_extraction.py`.