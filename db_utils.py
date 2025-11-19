# db_utils.py
import pandas as pd
from sqlalchemy import create_engine
from config import DB_URL

def run_query(sql):
    """
    SQL문을 실행하고 DataFrame으로 결과를 반환합니다.
    DB 연결 오류 시에는 빈 DataFrame을 반환합니다.
    """
    try:
        engine = create_engine(DB_URL)
        df = pd.read_sql(sql, engine)
        return df
    except Exception as e:
        print(f"⚠️ DB 연결 오류: {e}")
        return pd.DataFrame()
