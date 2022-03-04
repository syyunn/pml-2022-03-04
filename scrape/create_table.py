from db import PostgresqlManager

pgm = PostgresqlManager(dotenv_path='../.env')
sql = """
CREATE TABLE company(name text, url text);
"""
pgm.execute_sql(sql, commit=True)

if __name__ == "__main__":
    pass
