# Realtime AI Backend (WebSockets + Supabase)

A high-performance asynchronous backend simulating a real-time conversational agent.
This project demonstrates **WebSocket streaming**, **OpenAI Function Calling**, and **Supabase persistence**.

## 🚀 Features
- **Real-time Streaming:** Low latency token-by-token responses using FastAPI WebSockets.
- **Advanced AI Agents:** Implements OpenAI Tool Calling to simulate database lookups (e.g., checking order status).
- **Asynchronous Persistence:** Non-blocking logging of all events to Supabase.
- **Automated Summarization:** Triggers a background job to summarize the session upon disconnect.

## 🛠️ Tech Stack
- **Framework:** Python FastAPI (Async)
- **Database:** Supabase (PostgreSQL)
- **AI Model:** GPT-4o-Mini (via AsyncOpenAI)
- **Protocol:** WebSockets

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-folder>