from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import os

from app.db import create_session, log_event
from app.llm import stream_llm_response
from app.summarizer import run_summary_job

app = FastAPI()

# Serve frontend folder
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("frontend/index.html")

@app.websocket("/ws/session/{session_id}")
async def websocket_session(ws: WebSocket, session_id: str):
    await ws.accept()
    await create_session(session_id)

    try:
        while True:
            user_msg = await ws.receive_text()
            await log_event(session_id, "user", user_msg)

            async for token in stream_llm_response(session_id):
                await ws.send_text(token)

    except WebSocketDisconnect:
        asyncio.create_task(run_summary_job(session_id))
