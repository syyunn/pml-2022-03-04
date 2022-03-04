from db import PostgresqlManager


if __name__ == "__main__":
    pgm = PostgresqlManager()
    sql = """
    select * from legislators l 
        inner join sponsor s on (l.govtrack_id = s.govtrack_id)
    """
    df = pgm.execute_sql(sql, fetchall=True)
    pass
