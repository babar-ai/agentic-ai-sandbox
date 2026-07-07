# 🔍 LangGraph Search Agent

A **ReAct-style agentic AI** built with [LangGraph](https://github.com/langchain-ai/langgraph) that uses the **Groq LLaMA-3.3-70b** model and **Tavily Search** to answer questions by intelligently searching the web in a loop until it has enough information to respond.

---

## 📁 File Structure

```
ai agents in langgraph by DL ai/
│
├── search_agent.py     ← Main agent code
└── README.md           ← This file

langgraph/
├── config.py           ← Pydantic settings (API keys)
├── .env                ← Environment variables (Groq + Tavily keys)
└── requirements.txt    ← Python dependencies
```

---

## ⚙️ How It Works — The Workflow

This agent follows the **ReAct (Reason + Act) pattern** — the LLM reasons about what to do and acts by calling tools, repeating in a loop until it has a final answer.

### High-Level Flow

```
User Question
     │
     ▼
┌──────────┐
│   LLM    │  ← call_Groq_model()
│  Node    │    Groq LLaMA-3.3-70b thinks and decides
└──────────┘
     │
     ▼
exists_action()  ──── Does AIMessage have tool_calls?
     │
  ┌──┴──┐
 YES    NO
  │      │
  ▼      ▼
Action   END
 Node    (Return final answer to user)
  │
  ▼
┌──────────┐
│  Action  │  ← take_action()
│  Node    │    Executes the requested tool (Tavily Search)
└──────────┘
     │
     ▼
 ToolMessage result appended to state["messages"]
     │
     └────────────────────► Back to LLM Node (loop)
```

---

## 🧩 Component Breakdown

### 1. `AgenticState` — Shared Memory

```python
class AgenticState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
```

- This is the **state** that flows through every node in the graph.
- `messages` is a list of all messages exchanged so far: `HumanMessage`, `AIMessage`, and `ToolMessage`.
- `operator.add` means LangGraph **appends** new messages rather than replacing the old ones — so the full conversation history is always preserved.

---

### 2. `Agent.__init__()` — Graph Construction

```python
graph.add_node("llm", self.call_Groq_model)
graph.add_node("action", self.take_action)

graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
graph.add_edge("action", "llm")
graph.set_entry_point("llm")
```

- Two nodes are registered: `"llm"` and `"action"`.
- After the `"llm"` node runs, `exists_action` decides the route:
  - **Tool call needed?** → go to `"action"`
  - **No tool call needed?** → go to `END` (done)
- After `"action"` runs, it always loops back to `"llm"`.
- Entry point is set to `"llm"`, so the LLM always thinks first.

---

### 3. `call_Groq_model()` — LLM Node

```python
def call_Groq_model(self, state: AgenticState) -> AgenticState:
    messages = state["messages"]
    if self.system:
        messages = [SystemMessage(content=self.system)] + messages
    message = self.model.invoke(messages)
    return {'messages': [message]}
```

- Reads all current messages from state.
- Prepends the **system prompt** (if any) on every call to guide LLM behavior.
- Calls the Groq LLaMA model with the full message history.
- The LLM returns an `AIMessage` that either:
  - Has **`tool_calls`** filled in → the LLM wants to search something.
  - Has **`content`** filled in and no tool calls → the LLM has a final answer.
- The new `AIMessage` is appended to `state["messages"]`.

---

### 4. `exists_action()` — Router / Conditional Edge

```python
def exists_action(self, state: AgenticState) -> bool:
    result = state['messages'][-1]
    return len(result.tool_calls) > 0
```

- Reads the **latest message** (the `AIMessage` the LLM just produced).
- Returns `True` if `tool_calls` list is non-empty → route to Action node.
- Returns `False` if `tool_calls` is empty → route to END.

---

### 5. `take_action()` — Action Node

```python
def take_action(self, state: AgenticState) -> AgenticState:
    tool_calls = state['messages'][-1].tool_calls
    tool_messages = []

    for tc in tool_calls:
        if not tc['name'] in self.tools:
            result = "bad tool name"
        else:
            result = self.tools[tc['name']].invoke(tc['args'])

        tool_messages.append(ToolMessage(
            tool_call_id=tc['id'],
            name=tc['name'],
            content=str(result)
        ))
    return {'messages': tool_messages}
```

- Reads the `tool_calls` from the last `AIMessage`.
- Loops over each requested tool call (the LLM can request multiple at once).
- Validates that the tool name exists in the registered tools.
- Invokes the tool (Tavily web search) with the LLM's provided arguments.
- Wraps each result in a `ToolMessage` (linked back to the tool call via `tool_call_id`).
- Appends all `ToolMessage`s to state and loops back to the LLM.

---

## 💬 Message State — What Lives in `state["messages"]`

At each step, a new message is appended to the list. Here's what it looks like for a typical weather query:

| Step | Message Type    | Content                                              |
|------|-----------------|------------------------------------------------------|
| 0    | `HumanMessage`  | "What is the weather in Mardan, Khyber Pakhtunkhwa?" |
| 1    | `AIMessage`     | `content=''`, `tool_calls=[{name: 'tavily_search_results_json', args: {query: '...'}}]` |
| 2    | `ToolMessage`   | Raw web search results from Tavily                    |
| 3    | `AIMessage`     | "The current weather in Mardan is 102.2°F..." (final answer) |

---

## 🔧 Setup & Configuration

### 1. Environment Variables

Create a `.env` file in the `langgraph/` root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Agent

```bash
cd "ai agents in langgraph by DL ai"
python search_agent.py
```

---

## 🛠️ Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Agent Framework | LangGraph                           |
| LLM             | Groq — `llama-3.3-70b-versatile`    |
| Search Tool     | Tavily Search API (max 4 results)   |
| Config Mgmt     | Pydantic Settings (`config.py`)     |
| Language        | Python 3.10+                        |

---

## 📝 System Prompt

The agent is initialized with this system prompt to guide its behavior:

> *"You are a smart research assistant. Use the search engine to look up information. You are allowed to make multiple calls (either together or in sequence). Only look up information when you are sure of what you want. If you need to look up some information before asking a follow up question, you are allowed to do that!"*

---

## 🔄 Example Run

**Input:**
```
What is the weather in Mardan, Khyber Pakhtunkhwa?
```

**Agent Thought Process:**
1. LLM receives the question → decides it needs to search.
2. `exists_action` detects a tool call → routes to Action node.
3. Tavily searches `"Mardan Khyber Pakhtunkwa weather"` → returns live data.
4. LLM receives search results → composes a natural language answer.
5. `exists_action` sees no more tool calls → routes to END.

**Output:**
```
AI Response: The current weather in Mardan, Khyber Pakhtunkhwa is overcast
with a temperature of 102.2°F and a wind speed of 5 mph. The humidity is 80%
and the cloud base is 3937 ft...
```
