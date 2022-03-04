import pandas as pd
from db import PostgresqlManager


if __name__ == "__main__":
    pgm = PostgresqlManager()
    create_table = """
    select * from legislators l inner join sponsor s on (l.govtrack_id = s.govtrack_id)
    """
    pgm.execute_sql(create_table, fetchall=True)
    pass
