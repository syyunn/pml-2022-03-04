import pandas as pd
import datetime
import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

df = pd.read_csv("./FARA_All_Registrants.csv", encoding_errors='ignore')
df = df.where(pd.notnull(df), None)  # replace all nan values to None
df.columns = df.columns.str.lower()


def format_datetime(date_str):
    if date_str:
        datetime_format = "%m/%d/%Y"
        datetime_obj = datetime.datetime.strptime(date_str, datetime_format)
        return datetime_obj
    else:
        return date_str


# convert date string to python default datetime obj
df["registration date"] = df["registration date"].apply(lambda x: format_datetime(x))
df["termination date"] = df["termination date"].apply(lambda x: format_datetime(x))

# clean-out first/end whitespaces
df["zip"] = df["zip"].apply(lambda x: x.strip() if x else x)
df["address 2"] = df["address 2"].apply(lambda x: x.strip() if x else x)

# write df on db
load_dotenv('../.env')

host = os.getenv(f"HOST")
port = os.getenv(f"PORT")
database = os.getenv(f"DATABASE")
username = os.getenv(f"USERNAME")
password = os.getenv(f"PASSWORD")

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
df.to_sql(name='registrants', con=engine, index=False, if_exists='replace')


if __name__ == "__main__":
    pass
