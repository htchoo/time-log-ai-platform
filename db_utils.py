# db_utils.py
import pandas as pd
import time
from sqlalchemy import create_engine
from config import DB_URL

def run_query(sql: str, retries: int = 3, delay: int = 3) -> pd.DataFrame:
    """
    SQL문을 실행하고 DataFrame으로 결과를 반환합니다.
    DB 연결 실패 시 자동 재시도 로직을 포함합니다.

    Parameters
    ----------
    sql : str
        실행할 SQL 문
    retries : int
        최대 재시도 횟수 (기본 3회)
    delay : int
        재시도 간격(초)

    Returns
    -------
    pandas.DataFrame
        SQL 실행 결과
    """

    for attempt in range(1, retries + 1):
        try:
            # ✅ SSL 모드 명시 + 연결 자동 감지
            engine = create_engine(
                DB_URL,
                connect_args={"sslmode": "require"},
                pool_pre_ping=True  # 비활성 세션 자동 감지
            )

            # ✅ SQL 실행
            df = pd.read_sql(sql, engine)
            engine.dispose()  # 연결 자원 정리

            # ✅ 결과 로그
            print(f"✅ SQL 실행 성공 (시도 {attempt}/{retries}) — 결과 행 수: {len(df)}")
            return df

        except Exception as e:
            print(f"⚠️ DB 연결 오류 (시도 {attempt}/{retries}): {e}")

            # Neon DB가 Idle일 경우 깨우기 시간 확보
            if attempt < retries:
                print(f"⏳ {delay}초 후 재시도 중...")
                time.sleep(delay)
            else:
                print("❌ 모든 재시도 실패 — 빈 DataFrame 반환")
                return pd.DataFrame()
