class Database:
    host = None
    port = None
    database = None
    user = None
    password = None
    conn = None

    def __init__(self, **kwargs):
        from dotenv import load_dotenv
        import os

        dotenv_path = kwargs.get("dotenv_path") or ".env"
        load_dotenv(dotenv_path)

        self.host = os.getenv(f"HOST")
        self.port = os.getenv(f"PORT")
        self.database = os.getenv(f"DATABASE")
        self.user = os.getenv(f"USERNAME")
        self.password = os.getenv(f"PASSWORD")

        assert (
            self.host and self.port and self.database and self.user and self.password
        ) is not None, "One or more configuration for DB are missing."


class PostgresqlManager(Database):
    import pandas as pd

    def __init__(self, dotenv_path=".env"):
        super().__init__(dotenv_path=dotenv_path)

    def create_connection(self, reuse_connection: bool = False):
        import psycopg2
        import logging

        if (self.host and self.port and self.database and self.user and self.password) is None:
            print('One more of configuration for Database are None')
            return None

        try:
            if reuse_connection and self.conn is not None:
                return self.conn

            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )

            if reuse_connection:
                self.conn = conn

            return conn

        except Exception as e:
            logging.error(e)
            return e

    def execute_sql(self, sql, conn=None, reuse_connection=False, parameters=None, commit=False, fetchall=False,
                    include_columns=False):
        _conn = conn or self.create_connection(reuse_connection)
        cursor = _conn.cursor()

        if parameters is isinstance(parameters, (tuple, list)):
            parameters = tuple([
                parameter.strip() if isinstance(parameter, str) else parameter
                for parameter in parameters
            ])

        cursor.execute(sql, parameters)

        if commit:
            _conn.commit()  # to write on db, commit() is required.

        if fetchall:
            if include_columns:
                return [desc[0] for desc in cursor.description], cursor.fetchall()  # return rows in list
            else:
                return cursor.fetchall()

    def copy_from(self, df: pd.DataFrame, table: str, conn=None, reuse_connection=False, commit=False):
        import psycopg2.extras
        import logging

        try:
            df_columns = list(df)
            columns = ",".join(df_columns)
            values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

            _conn = conn or self.create_connection(reuse_connection)
            cursor = _conn.cursor()

            sql = "INSERT INTO {} ({}) {}".format(table, columns, values)

            psycopg2.extras.execute_batch(cursor, sql, df.values)
            if commit:
                _conn.commit()  # to write on db, commit() is required.

        except Exception as e:
            logging.error(e)
            return e

    @staticmethod
    def convert_fetchall_to_pd(data: list):
        import pandas as pd
        import numpy as np
        return pd.DataFrame(np.array(data))

    def __del__(self):
        self.conn and self.conn.close()


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



