import os
import streamlit as st
from dotenv import load_dotenv
import urllib.parse

# Load local .env (for local dev)
load_dotenv()

# 1️⃣ OpenAI Key
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

# 2️⃣ PostgreSQL 연결 정보 (Streamlit Cloud 우선 → 로컬 백업)
PG_HOST = st.secrets.get("PG_HOST", os.getenv("PG_HOST"))
PG_PORT = st.secrets.get("PG_PORT", os.getenv("PG_PORT", "5432"))
PG_DATABASE = st.secrets.get("PG_DATABASE", os.getenv("PG_DATABASE"))
PG_USER = st.secrets.get("PG_USER", os.getenv("PG_USER"))
PG_PASSWORD = st.secrets.get("PG_PASSWORD", os.getenv("PG_PASSWORD"))
PG_SSLMODE = st.secrets.get("PG_SSLMODE", os.getenv("PG_SSLMODE", "require"))

# 3️⃣ 비밀번호 URL 인코딩
PG_PASSWORD_ENC = urllib.parse.quote_plus(PG_PASSWORD or "")

# 4️⃣ 최종 연결 URL
DB_URL = f"postgresql://{PG_USER}:{PG_PASSWORD_ENC}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}?sslmode=require"
