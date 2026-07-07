# LangGraph Foundations 🕸️

This directory is dedicated to **LangGraph**, an extension of LangChain designed for building robust, stateful, multi-actor applications with LLMs. LangGraph treats application logic as a cyclic graph, allowing for loops, memory, and complex agent routing.

## 📓 Jupyter Notebooks

The experiments in this folder are structured sequentially to build an understanding of LangGraph from the ground up.

1.  **[`Hello_world.ipynb`](./Hello_world.ipynb)**
    *   *Focus:* The absolute basics of LangGraph.
    *   *Concepts:* Defining state using `TypedDict`, creating a simple node, and compiling a basic `StateGraph`.

2.  **[`Graph_iii.ipynb`](./Graph_iii.ipynb)**
    *   *Focus:* Expanding the graph with standard edges and multiple nodes.
    *   *Concepts:* Connecting nodes to dictate workflow, defining structured agent behavior, and executing the graph.

3.  **[`Graph_iv.ipynb`](./Graph_iv.ipynb)**
    *   *Focus:* Conditional routing and decision making.
    *   *Concepts:* Implementing conditional edges that dynamically choose the next node based on the current state (e.g., routing to a tool node vs. ending the conversation).

4.  **[`multiple_inputs.ipynb`](./multiple_inputs.ipynb)**
    *   *Focus:* Handling parallelism and multi-actor scenarios.
    *   *Concepts:* Processing parallel inputs, fanning out/fanning in, and state reducers.

5.  **[`Graph_v.ipynb`](./Graph_v.ipynb)**
    *   *Focus:* Looping graphs and stateful game logic.
    *   *Concepts:* Building a self-looping binary search guessing game. Covers `add_conditional_edges` for loop control, separating node responsibilities (`setup_node`, `guess_node`, `hint_node`), and using `state["list"][-1]` to track the latest value without a dedicated state key. Also includes graph visualization using `draw_mermaid_png()`.

## 🧠 Core Concepts Explained

### Setting the Entry Point
When defining a graph, you must specify where the execution begins. 
*   **Classic Syntax:** `workflow.set_entry_point("node_name")` tells the graph to always start at that specific node.
*   **Modern Syntax:** `workflow.add_edge(START, "node_name")` achieves the exact same thing by drawing a direct edge from the built-in `START` node.

### Compiling the Graph (`workflow.compile()`)
Calling `app = workflow.compile()` is the final step that transforms your graph blueprint into an executable application. It performs three critical functions:
1.  **Validation:** Checks the blueprint for missing nodes, disconnected edges, or invalid routing.
2.  **Freezing:** Locks the architecture so it can be executed efficiently.
3.  **Returning a Runnable:** Creates a standard LangChain Runnable (often saved as `app`) that can be executed via `app.invoke()` or `app.stream()`. This is also where you can inject memory (checkpointers) into your application (e.g., `workflow.compile(checkpointer=memory)`).

### Passing Arguments as Dictionaries (The State)
When you execute a graph, you must pass arguments as a dictionary (e.g., `app.invoke({"messages": ["Hello"]})`). This is because everything in LangGraph revolves around the **State** (defined as a `TypedDict` or Pydantic `BaseModel`).
*   **Initialization:** The dictionary you pass in is used to populate the initial State.
*   **Flexibility:** This allows you to inject multiple pieces of data (like `user_id` or `context`) at the start of the workflow, which are then passed into the entry node.

### Visualizing the Graph
Once a graph is compiled, you can visualize its structure. Inside a Jupyter Notebook, you can plot it as a Mermaid diagram using the following code:
```python
from IPython.display import Image, display

# Display as PNG
display(Image(app.get_graph().draw_mermaid_png()))
```
*Note: You can also use `app.get_graph().draw_ascii()` for a quick console-based text representation.*
## 🚀 How to Run

These experiments are built in Jupyter Notebooks. To interact with them, start your Jupyter server from the root directory or directly inside this folder:

```bash
jupyter notebook
```

Open the notebooks in order (starting with `Hello_world.ipynb`) and execute the cells step-by-step. Make sure your `.env` file is configured with the necessary API keys (like `OPENAI_API_KEY` and `LANGCHAIN_API_KEY` for LangSmith tracing).
