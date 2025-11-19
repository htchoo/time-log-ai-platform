import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
# from sql_agent import generate_sql, summarize_result  # ⛔ summarize_result 임시 비활성화
from sql_agent import generate_sql
from db_utils import run_query


# 페이지 기본 설정
st.set_page_config(page_title="Time Log 분석 플랫폼", layout="wide")

st.title("📊 Time Log AI 분석 플랫폼")
st.markdown("AI 기반으로 자연어 질의 → SQL 생성 → 결과 → 시각화까지 자동화된 분석 플랫폼")

# --- 사용자 입력 영역 ---
user_query = st.text_area("🔍 질의 입력", placeholder="예: 2025년도 차승우의 타임로그 작성 트렌드를 월단위로 보여줘")

if st.button("분석 실행"):
    if user_query.strip() == "":
        st.warning("질의를 입력하세요.")
    else:
        try:
            # --- Step 1: SQL 생성 ---
            with st.spinner("🔧 SQL 생성 중..."):
                sql = generate_sql(user_query)
            st.code(sql, language="sql")

            # --- Step 2: DB 쿼리 실행 ---
            with st.spinner("📡 PostgreSQL에서 데이터 조회 중..."):
                df = run_query(sql)

            if df.empty:
                st.warning("데이터가 없습니다. 쿼리 조건을 확인하세요.")
            else:
                # --- Step 3: 원본 테이블 표시 ---
                st.subheader("📋 쿼리 결과")
                st.dataframe(df)

                # --- Step 4: 시각화 ---
                time_columns = [col for col in ["year", "mm", "year_wkprd2"] if col in df.columns]

                if time_columns:
                    st.subheader("📈 트렌드 시각화")
                    time_col = time_columns[0]

                    # period 컬럼 생성
                    if "year" in df.columns and "mm" in df.columns:
                        df["period"] = df["year"].astype(str) + "-" + df["mm"].astype(str)
                    elif "year" in df.columns:
                        df["period"] = df["year"].astype(str)
                    elif "year_wkprd2" in df.columns:
                        df["period"] = df["year_wkprd2"]
                    else:
                        df["period"] = df.index.astype(str)

                    # 시각화용 수치 컬럼 감지
                    numeric_cols = df.select_dtypes(include=["float", "int"]).columns
                    if len(numeric_cols) > 0:
                        metric = numeric_cols[-1]  # 마지막 수치 컬럼 사용
                        fig, ax = plt.subplots(figsize=(10, 4))
                        ax.plot(df["period"], df[metric], marker="o")
                        ax.set_title(f"{metric} Trend")
                        ax.set_xlabel("Period")
                        ax.set_ylabel(metric)
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                    else:
                        st.info("시각화 가능한 수치형 컬럼이 없습니다.")
                else:
                    st.info("트렌드 분석에 필요한 시간 컬럼이 존재하지 않습니다.")

                # --- Step 5: 결과 요약 (비활성화) ---
                # with st.spinner("🧠 결과 요약 중..."):
                #     summary = summarize_result(user_query, df)
                # st.subheader("🧾 분석 요약")
                # st.write(summary)

        except Exception as e:
            st.error(f"⚠️ 오류 발생: {e}")
