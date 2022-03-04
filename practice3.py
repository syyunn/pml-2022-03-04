import pandas as pd
from db import PostgresqlManager


if __name__ == "__main__":
    df = pd.read_csv('/Users/suyeolyun/legislators.csv')
    pgm = PostgresqlManager()
    create_table = """
    CREATE TABLE legislators (govtrack_id text, last_name text, first_name text, gender text)
    """
    pgm.execute_sql(create_table, commit=True)
    pgm.copy_from(df=df, table="legislators", commit=True)
    pass

