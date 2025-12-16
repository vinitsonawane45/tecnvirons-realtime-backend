import os
from openai import AsyncOpenAI
from app.db import fetch_full_conversation, finalize_session

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def run_summary_job(session_id: str):
    conversation = await fetch_full_conversation(session_id)

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize this conversation briefly."},
            {"role": "user", "content": conversation}
        ]
    )

    summary = response.choices[0].message.content
    await finalize_session(session_id, summary)
