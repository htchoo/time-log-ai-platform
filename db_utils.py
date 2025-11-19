# db_utils.py
import pandas as pd
from sqlalchemy import create_engine
from config import DB_URL

def run_query(sql: str):
    """
    SQL문을 실행하고 DataFrame으로 결과를 반환합니다.
    DB 연결 오류 시에는 빈 DataFrame을 반환합니다.
    """
    try:
        # SSL 모드 적용을 명시적으로 강제 (Neon 요구사항)
        engine = create_engine(
            DB_URL,
            connect_args={"sslmode": "require"},
            pool_pre_ping=True  # 비활성 세션 자동 감지
        )

        df = pd.read_sql(sql, engine)
        engine.dispose()  # 연결 자원 정리
        return df

    except Exception as e:
        print(f"⚠️ DB 연결 오류: {e}")
        return pd.DataFrame()
