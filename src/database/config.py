import streamlit as st
import os
from supabase import create_client, Client, ClientOptions
import httpx

# Fallback to env vars if secrets missing
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

# SSL workaround: disable verify for cert issues
http_client = httpx.Client(verify=False)

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options=ClientOptions(httpx_client=http_client)
)

SUPABASE_SERVICE_KEY = st.secrets.get("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_SERVICE_KEY")
supabase_admin: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY,
    options=ClientOptions(httpx_client=http_client)
)

def test_connection():
    """Test Supabase connection."""
    try:
        # Simple ping: try to select from a table (won't fail if tables don't exist)
        response = supabase.table("teachers").select("count").limit(1).execute()
        return True
    except Exception:
        return False

def ensure_tables():
    """Create required tables if missing using supabase_admin."""
    tables_sql = """
    CREATE TABLE IF NOT EXISTS teachers (
        id BIGSERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS students (
        id BIGSERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        face_embedding VECTOR(512),
        voice_embedding VECTOR(512),
        created_at TIMESTAMP DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS subjects (
        id BIGSERIAL PRIMARY KEY,
        subject_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        section TEXT,
        teacher_id BIGINT REFERENCES teachers(id),
        created_at TIMESTAMP DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS subject_students (
        id BIGSERIAL PRIMARY KEY,
        subject_id BIGINT REFERENCES subjects(id),
        student_id BIGINT REFERENCES students(id),
        UNIQUE(subject_id, student_id)
    );

    CREATE TABLE IF NOT EXISTS attendance_logs (
        id BIGSERIAL PRIMARY KEY,
        student_id BIGINT REFERENCES students(id),
        subject_id BIGINT REFERENCES subjects(id),
        timestamp TIMESTAMPTZ DEFAULT NOW(),
        is_present BOOLEAN NOT NULL
    );
    """
    try:
        supabase_admin.rpc('execute_sql', {'sql': tables_sql}).execute()
        return True
    except:
        return False

