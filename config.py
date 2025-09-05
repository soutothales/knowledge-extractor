import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
DEFAULT_LOCALE = os.getenv("DEFAULT_LOCALE", "en")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
