
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage, AnyMessage
from langchain_community.tools import TavilySearchResults
from langchain_groq import ChatGroq
import operator

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import TypedDict, Annotated
from config import settings


groq_api_key = settings.Groq_api_key
tavily_api_key = settings.TAVILY_API_KEY

DB_PATH = Path(__file__).parent / "agent_memory.db"   # persistent SQLite file saved next to the script
conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
memory = SqliteSaver(conn)    # conversation history survives after the program closes

tool = TavilySearchResults(tavily_api_key=tavily_api_key, max_results=4)


class AgenticState(TypedDict):
    message: Annotated[list[AnyMessage], operator.add]


class Agent:

    def __init__(self, model, tools, checkpointer, system=""):

        self.system = system
        self.tools = {tool.name: tool for tool in tools}
        self.model = model.bind_tools(tools)                  # bind_tools sends the JSON schema of every tool to the LLM alongside the messages. So the model now knows:

        graph = StateGraph(AgenticState)
        graph.add_node("llm", self.call_groq_model)
        graph.add_node("action", self.take_action)

        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
    
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")

        self.graph = graph.compile(checkpointer=checkpointer)

    def exists_action(self, state: AgenticState) -> bool:
        result = state['message'][-1]
        print(f"\nResult...{result}")
        print(f"\nTool_call_length...{len(result.tool_calls)}")
        return len(result.tool_calls) > 0


    def call_groq_model(self, state:AgenticState) -> AgenticState:

        messages = state['message']

        if self.system:
            messages = [SystemMessage(content=self.system)] + messages

        message = self.model.invoke(messages)

        return {'message': [message]}


    def take_action(self, state: AgenticState) -> AgenticState:

        tool_calls = state['message'][-1].tool_calls
        tool_messages = []

        for tc in tool_calls:
            print(f"Calling: {tc}")

            if not tc['name'] in self.tools:
                print("\n...bad tool name....")
                result = "bad tool name"
            else:
                result = self.tools[tc['name']].invoke(tc['args'])

            tool_messages.append(ToolMessage(tool_call_id=tc['id'], name=tc['name'], content=str(result)))
            print("Back to the model!")
        
        return {'message': tool_messages}




        
prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

#language model
model = ChatGroq(model_name="llama-3.3-70b-versatile",groq_api_key=groq_api_key)

workflow = Agent(model, [tool], checkpointer=memory, system=prompt)

config1 = {"configurable": {"thread_id": "1"}}

messages = [HumanMessage(content="What is the weather in Mardan, Khyber Pakhtunkhwa?")]

# result = workflow.graph.invoke({"message": messages}, config1)

# print(f"\nAI Response: {result['message'][-1].content}")


# ── STREAMING ──────────────────────────────────────────────────────────────
# graph.stream() yields one dict per node execution as it completes.
# Each dict looks like: {"node_name": updated_state_slice}
# This lets you print intermediate results (tool calls, tool results, etc.)
# BEFORE the full graph finishes — useful for showing live progress.

print("\n--- Streaming Events ---\n")

for event in workflow.graph.stream({"message": messages}, config1):
    # event is a dict: { "node_name": { state_key: [new_messages] } }
    for node_name, state_update in event.items():
        print(f"[Node: {node_name}]")
        for msg in state_update.get("message", []):
            msg_type = type(msg).__name__
            content = msg.content if msg.content else f"(tool_calls: {getattr(msg, 'tool_calls', [])})"
            print(f"  [{msg_type}] {content}")
        print()

print("--- Streaming Complete ---")
