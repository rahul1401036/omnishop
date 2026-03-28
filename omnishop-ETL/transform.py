import pandas as pd

def transform_data(combined_df):

    cleaned_df = combined_df.copy()

    # Remove missing values
    cleaned_df = cleaned_df.dropna()

    # Remove duplicates
    cleaned_df = cleaned_df.drop_duplicates()

    # Convert event_time to datetime
    cleaned_df['event_time'] = pd.to_datetime(cleaned_df['event_time'] , errors='coerce')

    # Clean event_type
    cleaned_df['event_type'] = cleaned_df['event_type'].str.strip().str.lower()

    # Remove invalid rows
    cleaned_df = cleaned_df[cleaned_df['event_type'] != ""]

    # Create hour column
    cleaned_df['hour'] = cleaned_df['event_time'].dt.floor('h')

    return cleaned_df