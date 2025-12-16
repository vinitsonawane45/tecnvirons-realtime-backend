import os
import json
from openai import AsyncOpenAI
from app.db import fetch_history, log_event

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- 1. DEFINE THE TOOL ---
# This simulates a database lookup. In a real job, this would query SQL.
async def get_delivery_status(order_id: str):
    """Mock function to check delivery status."""
    # Simulating data for specific IDs
    mock_db = {
        "ORD-123": "Shipped - Arriving Tomorrow",
        "ORD-456": "Processing - Warehouse",
        "ORD-999": "Delivered - Front Porch"
    }
    return mock_db.get(order_id, "Order not found.")

# Tool definition for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_delivery_status",
            "description": "Get the delivery status of a customer order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, e.g., ORD-123",
                    }
                },
                "required": ["order_id"],
            },
        }
    }
]

async def stream_llm_response(session_id: str):
    messages = await fetch_history(session_id)
    
    # System prompt establishes the AI's role
    messages.insert(0, {
        "role": "system",
        "content": "You are a helpful customer support agent. You can check order statuses using the available tools."
    })

    # Step 1: Call the model with tools enabled
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        stream=True
    )

    full_content = ""
    tool_calls = []
    
    # We need to handle the stream carefully to detect if the AI wants to talk OR run a tool
    async for chunk in response:
        delta = chunk.choices[0].delta
        
        # Case A: AI is just talking
        if delta.content:
            await log_event(session_id, "assistant", delta.content)
            yield delta.content
            full_content += delta.content

        # Case B: AI wants to run a tool (it builds the function call piece by piece)
        if delta.tool_calls:
            for tc in delta.tool_calls:
                if len(tool_calls) <= tc.index:
                    tool_calls.append({"id": "", "function": {"name": "", "arguments": ""}})
                
                if tc.id: tool_calls[tc.index]["id"] += tc.id
                if tc.function.name: tool_calls[tc.index]["function"]["name"] += tc.function.name
                if tc.function.arguments: tool_calls[tc.index]["function"]["arguments"] += tc.function.arguments

    # Step 2: If the AI decided to call a tool
    if tool_calls:
        # 1. Log the tool call request
        available_functions = {"get_delivery_status": get_delivery_status}
        
        # Add the assistant's "thought process" (the tool call) to history
        messages.append({
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": tc["function"]
                } for tc in tool_calls
            ]
        })

        # 2. Execute the function(s)
        for tc in tool_calls:
            function_name = tc["function"]["name"]
            function_args = json.loads(tc["function"]["arguments"])
            
            if function_name in available_functions:
                # Run the Python function
                function_response = await available_functions[function_name](**function_args)
                
                # Add the tool output to history
                messages.append({
                    "tool_call_id": tc["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
                
                # Send a system note to user (Optional UI touch)
                yield f"\n[System: Checked Order {function_args.get('order_id')}]\n"

        # 3. Get the final answer from the AI based on the tool output
        final_stream = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )

        async for chunk in final_stream:
            delta = chunk.choices[0].delta
            if delta.content:
                await log_event(session_id, "assistant", delta.content)
                yield delta.content