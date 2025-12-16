# import os
# from datetime import datetime
# from supabase import create_client

# supabase = create_client(
#     os.getenv("SUPABASE_URL"),
#     os.getenv("SUPABASE_KEY")
# )

# async def create_session(session_id: str, user_id: str = None):
#     supabase.table("sessions").insert({
#         "session_id": session_id,
#         "user_id": user_id
#     }).execute()

# async def log_event(session_id: str, role: str, content: str):
#     supabase.table("session_events").insert({
#         "session_id": session_id,
#         "role": role,
#         "content": content
#     }).execute()

# async def fetch_history(session_id: str):
#     res = supabase.table("session_events") \
#         .select("role, content") \
#         .eq("session_id", session_id) \
#         .order("created_at") \
#         .execute()

#     return [{"role": r["role"], "content": r["content"]} for r in res.data]

# async def fetch_full_conversation(session_id: str):
#     res = supabase.table("session_events") \
#         .select("role, content") \
#         .eq("session_id", session_id) \
#         .order("created_at") \
#         .execute()

#     return "\n".join(f"{r['role']}: {r['content']}" for r in res.data)

# async def finalize_session(session_id: str, summary: str):
#     supabase.table("sessions").update({
#         "summary": summary,
#         "end_time": datetime.utcnow()
#     }).eq("session_id", session_id).execute()


import os
from datetime import datetime
from supabase import create_client

# Initialize Supabase Client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

async def create_session(session_id: str, user_id: str = None):
    """
    Creates a new session. 
    If the session_id already exists, it does nothing (prevents the crash).
    """
    # FIX: Changed .insert() to .upsert() with ignore_duplicates=True
    supabase.table("sessions").upsert(
        { "session_id": session_id, "user_id": user_id },
        on_conflict="session_id", 
        ignore_duplicates=True
    ).execute()

async def log_event(session_id: str, role: str, content: str):
    """Logs a single message event to the database."""
    supabase.table("session_events").insert({
        "session_id": session_id,
        "role": role,
        "content": content
    }).execute()

async def fetch_history(session_id: str):
    """Fetches chat history as a list of dictionaries."""
    res = supabase.table("session_events") \
        .select("role, content") \
        .eq("session_id", session_id) \
        .order("created_at") \
        .execute()

    return [{"role": r["role"], "content": r["content"]} for r in res.data]

async def fetch_full_conversation(session_id: str):
    """Fetches chat history formatted as a string."""
    res = supabase.table("session_events") \
        .select("role, content") \
        .eq("session_id", session_id) \
        .order("created_at") \
        .execute()

    return "\n".join(f"{r['role']}: {r['content']}" for r in res.data)

async def finalize_session(session_id: str, summary: str):
    """Updates the session with a summary and end time."""
    # Note: .isoformat() is required to fix the datetime serialization error
    supabase.table("sessions").update({
        "summary": summary,
        "end_time": datetime.utcnow().isoformat()
    }).eq("session_id", session_id).execute()