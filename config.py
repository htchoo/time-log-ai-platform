import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

PG_CONFIG = {
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
    "dbname": os.getenv("PG_DATABASE"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
}

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
