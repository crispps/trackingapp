import psycopg2
import psycopg2.extras


def get_dsn() -> str:
    with open("data/password.txt", "r") as f:
        password = f.read().strip()
    return f"postgresql://postgres.bvnzdjoabugzrbfhytsn:{password}@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"


class Database:
    def __init__(self, db_path: str = None, dsn: str = None, **kwargs):

        self.dsn = dsn or get_dsn()
        self.kwargs = kwargs
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(self.dsn, **self.kwargs)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute(self, query: str, params: tuple = ()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"[DB ERROR] execute: {e} | query: {query} | params: {params}")
            raise

    def fetchone(self, query: str, params: tuple = ()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            print(f"[DB ERROR] fetchone: {e} | query: {query} | params: {params}")
            raise

    def fetchall(self, query: str, params: tuple = ()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"[DB ERROR] fetchall: {e} | query: {query} | params: {params}")
            raise

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()