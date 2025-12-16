# Realtime AI Backend (WebSockets + Supabase)

This project is a high-performance, asynchronous Python backend simulating a real-time conversational agent. It is designed to demonstrate WebSocket streaming, complex LLM interaction (Tool Calling), and asynchronous database persistence.

## 1. Detailed Setup Steps and Required Dependencies

### Prerequisites
* **Python 3.9+** installed on your machine.
* A **Supabase** account (for the PostgreSQL database).
* An **OpenAI API Key** (for the LLM).

### Step-by-Step Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/vinitsonawane45/tecnvirons-realtime-backend.git](https://github.com/vinitsonawane45/tecnvirons-realtime-backend.git)
    cd tecnvirons-realtime-backend
    ```

2.  **Create a Virtual Environment**
    It is recommended to use a virtual environment to manage dependencies.
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    Install the required Python packages using `pip`.
    ```bash
    pip install -r requirements.txt
    ```
    *Required Dependencies (`requirements.txt`):*
    * `fastapi`: For the web framework and WebSocket support.
    * `uvicorn`: An ASGI server to run the application.
    * `supabase`: For asynchronous interaction with the Supabase database.
    * `openai`: For accessing GPT-4o-mini and handling streams.
    * `python-dotenv`: For managing environment variables securely.

4.  **Configure Environment Variables**
    Create a file named `.env` in the root directory and add your keys (do not share this file):
    ```env
    OPENAI_API_KEY=sk-proj-...
    SUPABASE_URL=[https://your-project-id.supabase.co](https://your-project-id.supabase.co)
    SUPABASE_KEY=your-anon-public-key
    ```

---

## 2. Complete Supabase Database Schema

[cite_start]Run the following SQL commands in your Supabase project's **SQL Editor** to create the necessary tables for session tracking and event logging[cite: 39, 40, 41].

### Table 1: Sessions
Stores high-level metadata about the conversation.
```sql
-- Sessions table
create table if not exists sessions (
  session_id text primary key,
  user_id text,
  start_time timestamptz default now(),
  end_time timestamptz,
  duration_seconds integer,
  summary text
);

-- Event logs
create table if not exists session_events (
  id bigserial primary key,
  session_id text references sessions(session_id) on delete cascade,
  role text,
  content text,
  created_at timestamptz default now()
);
