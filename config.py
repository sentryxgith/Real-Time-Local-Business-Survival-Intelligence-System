import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

DB_NAME = "business_data.db"

RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"

DEFAULT_LOCATION = {
    "lat": 23.0225,
    "lon": 72.5714
}