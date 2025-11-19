import os
import streamlit as st
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DATABASE = os.getenv("PG_DATABASE", "postgres")
PG_USER = os.getenv("PG_USER", "postgres")

PG_PASSWORD_ENC = urllib.parse.quote_plus(os.getenv("PG_PASSWORD", ""))

DB_URL = f"postgresql://{PG_USER}:{PG_PASSWORD_ENC}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
