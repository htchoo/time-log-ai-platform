import psycopg2
import pandas as pd
from config import PG_CONFIG

def run_query(sql: str) -> pd.DataFrame:
    conn = psycopg2.connect(**PG_CONFIG)
    try:
        df = pd.read_sql(sql, conn)
        return df
    finally:
        conn.close()
