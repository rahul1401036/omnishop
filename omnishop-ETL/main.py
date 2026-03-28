import pandas as pd
import os
import logging

from extract import extract_data
from transform import transform_data
from load import load_data, get_sample

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# STEP 1: EXTRACT
logging.info("Starting data extraction...")
combined_df = extract_data()

# Save combined CSV
os.makedirs("combined_data", exist_ok=True)
combined_df.to_csv("combined_data/combined_data.csv", index=False)

logging.info("Data combined and saved")


# STEP 2: TRANSFORM
logging.info("Starting data cleaning...")
cleaned_df = transform_data(combined_df)


# STEP 3: LOAD TO DATABASE
logging.info("Loading data to database...")
engine = load_data(cleaned_df)


# STEP 4: CREATE HOURLY FILES
os.makedirs("hourly_data", exist_ok=True)

for hour, group in cleaned_df.groupby('hour'):
    logging.info(f"Processing data for hour: {hour}")

    hour_str = hour.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"hourly_data/data_{hour_str}.csv"

    group.to_csv(file_name, index=False)

logging.info("Hourly CSV files created successfully!")


# STEP 5: SAMPLE DATA
sample_data = get_sample(engine)

logging.info("Sample data from DB:")
logging.info(sample_data)