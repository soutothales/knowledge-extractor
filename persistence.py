from config import supabase
import json

def save_analysis(record):
    resp = supabase.table("analyses").insert(record).execute()
    return resp.data[0]

def search_by_topic(topic):
    needle = json.dumps([topic])
    query = supabase.table("analyses").select("*") \
        .or_(f"topics.cs.{needle},keywords.cs.{needle}").execute()
    return query.data
