from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

from langchain_groq import ChatGroq
from config import settings


groq_api_key = settings.Groq_api_key


#workflow state
class AgenticState(TypedDict):
    messages: List[HumanMessage | AIMessage]


#language model
llm = ChatGroq(model_name="llama-3.3-70b-versatile",groq_api_key=groq_api_key)


#process node
def process(state: AgenticState) -> AgenticState:
    messages = state["messages"]
    response = llm.invoke(messages)
    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    return state

#compile the graph
graph = StateGraph(AgenticState)
graph.add_node("process",process)
graph.add_edge(START,'process')
graph.add_edge('process',END)
agent = graph.compile()

#invoke the agent
agent.invoke({"messages":[HumanMessage(content="hi how are you")]})


