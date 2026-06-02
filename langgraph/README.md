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

## 🚀 How to Run

These experiments are built in Jupyter Notebooks. To interact with them, start your Jupyter server from the root directory or directly inside this folder:

```bash
jupyter notebook
```

Open the notebooks in order (starting with `Hello_world.ipynb`) and execute the cells step-by-step. Make sure your `.env` file is configured with the necessary API keys (like `OPENAI_API_KEY` and `LANGCHAIN_API_KEY` for LangSmith tracing).
