from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from config import OPENAI_API_KEY
import os
import pandas as pd

# ------------------------------
# 🔹 환경 설정
# ------------------------------
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# 공용 LLM 인스턴스 (매번 초기화 방지 → 성능 개선)
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm = ChatOpenAI(model="gpt-4o", temperature=0)


# ------------------------------
# 🔹 SQL 생성 함수
# ------------------------------
def generate_sql(user_query: str) -> str:
    """
    사용자의 자연어 질의를 SQL로 변환합니다.
    """
    try:
        # SQL 프롬프트 템플릿 로드
        with open("prompts/sql_prompt.txt", "r", encoding="utf-8") as f:
            template = f.read()

        prompt = PromptTemplate(
            input_variables=["user_query"],
            template=template + "\n\nUser Query: {user_query}"
        )

        # RunnableSequence 구성
        chain = RunnableSequence(prompt | llm)
        response = chain.invoke({"user_query": user_query})

        # 결과 추출
        sql = response.content if hasattr(response, "content") else str(response)
        return sql.strip("```sql").strip("```").strip()
    except Exception as e:
        return f"-- SQL 생성 중 오류 발생: {str(e)}"


# ------------------------------
# 🔹 결과 요약 함수 (임시 비활성화)
# ------------------------------
# def summarize_result(user_query: str, df: pd.DataFrame) -> str:
#     """
#     SQL 실행 결과를 요약하여 자연어로 설명합니다.
#     """
#     try:
#         if df is None or df.empty:
#             return "⚠️ 데이터가 없습니다."
#
#         # 결과 샘플
#         sample_data = df.head(10).to_string(index=False)
#
#         # 요약용 프롬프트
#         summary_prompt = f"""
#         사용자가 다음 질의를 수행했습니다:
#         "{user_query}"
#
#         결과 데이터의 일부는 다음과 같습니다:
#         {sample_data}
#
#         위 결과를 기반으로 주요 패턴, 이상치, 또는 인사이트를 한국어로 간결하게 요약해 주세요.
#         """
#
#         # LLM 호출
#         response = llm.invoke(summary_prompt)
#         summary = response.content if hasattr(response, "content") else str(response)
#
#         return summary.strip()
#
#     except Exception as e:
#         return f"요약 생성 중 오류 발생: {str(e)}"


# ------------------------------
# 🔹 테스트 실행 (직접 실행 시만 동작)
# ------------------------------
if __name__ == "__main__":
    test_query = "2025년도 차승우의 타임로그 작성 트렌드를 월단위로 보여줘"
    sql = generate_sql(test_query)
    print("🧠 생성된 SQL:\n", sql)

    # 가짜 데이터프레임 예시 (테스트용)
    dummy_df = pd.DataFrame({
        "year": [2025, 2025, 2025],
        "mm": [1, 2, 3],
        "total_duration": [12.5, 8.3, 15.2]
    })

    # summary = summarize_result(test_query, dummy_df)
    # print("\n📝 요약 결과:\n", summary)
