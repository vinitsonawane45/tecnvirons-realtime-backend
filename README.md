# Realtime AI Backend (WebSockets + Supabase)

This project is a high-performance, fully asynchronous Python backend that simulates a real-time conversational AI system. It demonstrates **WebSocket-based token streaming**, **LLM tool calling for complex interactions**, and **asynchronous persistence using Supabase (PostgreSQL)**.

The goal of this project is not just chat, but a realistic backend architecture suitable for production-grade, real-time AI applications.

---

## 1. Setup & Installation

### Prerequisites

You **must** have the following before running this project:

* **Python 3.9 or higher**
* A **Supabase account** (PostgreSQL database)
* An **OpenAI API key**

If any of these are missing, the backend will not work. There are no fallbacks.

---

### Step-by-Step Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/vinitsonawane45/tecnvirons-realtime-backend.git
cd tecnvirons-realtime-backend
```

---

#### 2. Create and Activate a Virtual Environment

Using a virtual environment is **not optional** if you want predictable dependency behavior.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

---

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Core Dependencies Explained:**

* `fastapi` – Web framework with native WebSocket support
* `uvicorn` – ASGI server for FastAPI
* `supabase` – Async client for Supabase/PostgreSQL
* `openai` – OpenAI API client (streaming + tool calling)
* `python-dotenv` – Secure environment variable management

If `pip install` fails here, fix it before proceeding. Everything else depends on this step.

---

#### 4. Configure Environment Variables

Create a `.env` file in the project root **(never commit this file)**:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
```

If any of these values are incorrect, the application will start but fail at runtime.

---

## 2. Supabase Database Schema

Run the following SQL in your **Supabase SQL Editor** to create the required tables.

These tables are mandatory. The backend logic assumes they exist.

```sql
-- Stores one row per chat session
create table if not exists sessions (
  session_id text primary key,
  user_id text,
  start_time timestamptz default now(),
  end_time timestamptz,
  duration_seconds integer,
  summary text
);

-- Stores all messages/events for a session
create table if not exists session_events (
  id bigserial primary key,
  session_id text references sessions(session_id) on delete cascade,
  role text,
  content text,
  created_at timestamptz default now()
);
```

If these tables are missing or modified incorrectly, session tracking and summarization will break.

---

## 3. Running and Testing the Application

### Running the Server

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The server will be available at:

```
http://127.0.0.1:8000
```

If this command fails, do **not** move forward until the error is fixed.

---

### Testing the WebSocket Client

#### 1. Launch the Client

Open the provided `chat_client.html` file in any modern browser (Chrome, Edge, Firefox).

---

#### 2. Verify Connection

A **green status indicator** confirms:

* WebSocket handshake succeeded
* Backend is accepting concurrent connections

If the indicator is not green, your WebSocket endpoint is broken.

---

#### 3. Test Tool Calling (Complex Interaction)

Send the following message in the chat UI:

```
Check the status for order ORD-123
```

**Expected Result:**

* The model detects intent
* Triggers the internal `get_delivery_status` tool
* Returns structured, non-generic data

Example response:

```
It is Shipped – Arriving Tomorrow
```

If this returns a generic LLM response, tool calling is **not** working.

---

#### 4. Test Automatic Session Summarization

1. Refresh or close the browser tab (this closes the WebSocket)
2. Open the `sessions` table in Supabase
3. Wait a few seconds

You should see the `summary` column populated automatically.

If it stays `NULL`, your disconnect handling or background task is broken.

---

## 4. Key Design Decisions (Why This Architecture Exists)

### FastAPI + WebSockets

WebSockets are used instead of REST to support **token-level streaming**. This drastically reduces perceived latency and enables real-time conversational UX.

REST would be simpler — and objectively worse — for this use case.

---

### Fully Asynchronous Backend

Every critical path uses `async def`:

* WebSocket handling
* Supabase writes
* OpenAI streaming

This prevents blocking the event loop and allows the server to scale across multiple concurrent chat sessions without collapsing.

---

### OpenAI Tool Calling (Not Regex Hacks)

Instead of brittle keyword matching, the system uses **OpenAI Tool Calling**.

This allows the model to:

* Interpret intent
* Decide when backend logic is required
* Call internal Python functions safely

This is the difference between a demo chatbot and a real AI system.

---

### Upsert-Based Session Management

Sessions are created using an **upsert strategy**:

* Reconnects do not cause duplicate rows
* Session IDs remain stable
* State consistency is maintained

Without upserts, reconnect behavior would be unreliable and error-prone.

---

## Final Notes

This backend is intentionally opinionated:

* Real-time first
* Async everywhere
* No fake logic or shortcuts

If something breaks, it breaks loudly — which is exactly what you want in a serious system.
