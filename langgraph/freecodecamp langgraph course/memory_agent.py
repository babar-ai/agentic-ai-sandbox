from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Union
from langgraph.graph import StateGraph, START, END

from langchain_groq import ChatGroq
from config import settings



groq_api_key = settings.Groq_api_key

#agentic state
class AgentState(TypedDict):

    messages:List[HumanMessage | AIMessage]


#language model
llm = ChatGroq(model_name="llama-3.3-70b-versatile",groq_api_key=groq_api_key)


#process node
def process(state:AgentState) -> AgentState:

    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"current state {state['messages']}")
    print(f"\nAI: {response.content}")
    
    return state
     

#compile the graph
graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,'process')
graph.add_edge('process',END)
agent = graph.compile() 

conversation_history = []

user_input = input("User: ")

while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))

    result = agent.invoke({"messages": conversation_history})

    conversation_history = result["messages"]

    user_input = input("User: ")

    