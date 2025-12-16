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




#### 3. Instructions on How to Run and Test

### Running the Server

Execute the following command in your terminal to start the Uvicorn server:

```bash
uvicorn app.main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

### Testing the WebSocket

#### 1. Launch the Client

Open the provided `chat_client.html` file in any modern web browser.

#### 2. Verify Connection

The status indicator should turn **green**, confirming a successful WebSocket connection to the backend.

#### 3. Test Complex Interaction (Tool Calling)

To verify the **Advanced** requirement, send the following message in the chat UI:

```
Check the status for order ORD-123
```

**Expected Behavior:**
The AI should not respond with generic text. Instead, it should internally execute the `get_delivery_status` function and return accurate data, for example:

```
It is Shipped – Arriving Tomorrow
```

This confirms proper OpenAI Tool Calling integration and backend function execution.

#### 4. Test Session Summarization

1. Close the browser tab or refresh the page to disconnect the WebSocket.
2. Navigate to your **Supabase `sessions` table**.
3. After a few seconds, verify that the `summary` column has been automatically updated with a concise conversation summary.

---

## 4. Key Design Choices

### FastAPI & WebSockets

FastAPI with WebSockets was chosen over traditional REST APIs to enable **token-by-token streaming**. This significantly reduces perceived latency and makes the AI interaction feel faster and more conversational.

### Asynchronous Architecture

The backend is fully asynchronous using Python’s `asyncio` (`async def` throughout). This ensures that:

* Database operations (Supabase)
* External API calls (OpenAI)

Do not block the event loop, allowing the server to efficiently handle multiple concurrent chat sessions.

### Function Calling for Complex Interaction

Rather than using brittle regex-based routing, **OpenAI Tool Calling** is implemented. This allows the model to intelligently decide when to trigger internal functions (e.g., database lookups for order status) based on user intent, enabling interactions beyond simple Q&A.

### Upsert Strategy for Consistency

An **upsert (update-or-insert)** strategy is used for session management. This prevents errors when clients reconnect using an existing session ID and ensures consistent, robust session handling across reconnects.
