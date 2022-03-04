import pandas as pd
from db import PostgresqlManager


if __name__ == "__main__":
    df = pd.read_csv('/Users/suyeolyun/sponsor.csv', dtype=str)
    pgm = PostgresqlManager()
    create_table = """
    CREATE TABLE sponsor(bill_id text, govtrack_id text, sponsor_title text);
    """
    pgm.execute_sql(create_table, commit=True)
    pgm.copy_from(df=df, table="sponsor", commit=True)
    pass
