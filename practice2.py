from db import PostgresqlManager

if __name__ == "__main__":
    pgm = PostgresqlManager()
    sql1 = """
    select * from phonebook
    """
    select = pgm.execute_sql(sql1, fetchall=True)
    pass


