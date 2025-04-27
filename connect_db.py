import os
import psycopg2
from psycopg2 import  OperationalError
from dotenv import load_dotenv

load_dotenv()


class ConnectDB:
    def __init__(self) -> None:
        try:
            self.dbhost = os.environ["DBHOST"]
            self.dbname = os.environ["DBNAME"]
            self.password = os.environ["PASSWORD"]
            self.dbuser = os.environ["DBUSER"]
            self.sslmode = os.environ["SSLMODE"]
        except KeyError as e:
            raise RuntimeError(f"Missing environment variable: {str(e)}")

    def get_connection_uri(self) -> str:
        db_uri = f"""
            host={self.dbhost}
            dbname={self.dbname}
            user={self.dbuser}
            password={self.password}
            sslmode={self.sslmode}
        """
        return db_uri

    def get_connection(self):
        try:
            conn = psycopg2.connect(self.get_connection_uri())
            return conn
        except OperationalError as e:
            raise RuntimeError(f"Database connection error: {e}")


def main():
    try:
        connect_db = ConnectDB()
        conn = connect_db.get_connection()
        cursor = conn.cursor
        print("✅ Connection successful")
        print(f"conn type: {type(conn)}")
        print(f"cursor type: {type(cursor)}")
    except Exception as e:
        print(f"❌ Error occurred: {e}")


if __name__ == "__main__":
    main()
