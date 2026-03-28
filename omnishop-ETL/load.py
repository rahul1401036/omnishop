import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def load_data(cleaned_df):

    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    cleaned_df.to_sql(
        name="events",
        con=engine,
        if_exists="append",
        index=False
    )

    return engine


def get_sample(engine):
    df = pd.read_sql("SELECT * FROM events LIMIT 10;", engine)
    return df