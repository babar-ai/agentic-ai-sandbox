
from langchain_core.messages.system import SystemMessage
import operator
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, END

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import TypedDict, Annotated
from config import settings



groq_api_key = settings.Groq_api_key
tavily_api_key = settings.TAVILY_API_KEY


tool = TavilySearchResults(tavily_api_key=tavily_api_key, max_results=4)
print(type(tool))
print(tool.name)



class AgenticState(TypedDict):

    messages: Annotated[list[AnyMessage], operator.add]


class Agent:

    def __init__(self, model, tools, system=""):

        self.system = system
        graph = StateGraph(AgenticState)
        graph.add_node("llm", self.call_Groq_model)
        graph.add_node("action", self.take_action)

        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )

        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")

        self.graph = graph.compile()
        self.tools = {tool.name: tool for tool in tools}
        self.model = model.bind_tools(tools)

    
    def exists_action(self, state: AgenticState) -> bool:
        result = state['messages'][-1]
        print(f"\nResult...{result}")
        print(f"\nTool_call_length...{len(result.tool_calls)}")
        return len(result.tool_calls) > 0

    
    def call_Groq_model(self, state: AgenticState) -> AgenticState:

        messages = state["messages"]

        if self.system:
            messages = [SystemMessage(content=self.system)] + messages

        message = self.model.invoke(messages)

        return {'messages': [message]}

    
    def take_action(self, state: AgenticState) -> AgenticState:

        tool_calls = state['messages'][-1].tool_calls
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
        
        return {'messages': tool_messages}


prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

#language model
model = ChatGroq(model_name="llama-3.3-70b-versatile",groq_api_key=groq_api_key)
abot = Agent(model, [tool], system=prompt)

messages = [HumanMessage(content="What is the weather in Mardan, Khyber Pakhtunkwa?")]
result = abot.graph.invoke({"messages": messages})

print(f"\nAI Response: {result['messages'][-1].content}")

