import pandas as pd
import glob
import logging

def extract_data():
    files = glob.glob("source_data/*.csv")
    df_list = []

    for file in files:
        try:
            df = pd.read_csv(file)
            df_list.append(df)
        except Exception as e:
            logging.error(f"Error reading {file}: {e}")

    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df