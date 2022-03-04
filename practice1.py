from db import PostgresqlManager

if __name__ == "__main__":
    pgm = PostgresqlManager()
    sql1 = """
    CREATE TABLE phonebook(phone text, name text, address text);
    """
    pgm.execute_sql(sql1, commit=True)

    sql2 = """
    INSERT INTO phonebook(phone, name, address) VALUES ('+1 875 856 0403', 'Suyeol Yun', '224 Albany St, Cambridge, MA')
    """
    pgm.execute_sql(sql2, commit=True)



