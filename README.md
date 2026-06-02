# Agentic AI Sandbox 🧪

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-v0.1+-green.svg?style=flat-square)](https://github.com/langchain-ai/langchain)
[![LangGraph](https://img.shields.io/badge/LangGraph-Active-orange.svg?style=flat-square)](https://github.com/langchain-ai/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg?style=flat-square&logo=streamlit)](https://streamlit.io/)

A hands-on engineering sandbox exploring stateful multi-agent systems, cognitive architectures, and advanced RAG workflows using LangGraph, LangChain, and emerging Agentic AI frameworks. This repository acts as a centralized playground for technical study notes, basic implementations, and continuous learning experiments.

---

## 📂 Repository Structure

```text
agentic-ai-sandbox/
├── .gitignore
├── README.md
├── requirements.txt
├── langchain-basics/                # Core LangChain foundations & notes
│   ├── basic_qa_chatbot.py         # Streamlit QA chatbot using OpenAI API
│   ├── retriever_chain.py           # Template for Retriever Chain implementation
│   └── notes/                       # Converted and formatted study notes
│       ├── chunking_strategies.md
│       ├── embedding_techniques.md
│       ├── langchain_components.md
│       ├── benefits_of_langchain.md
│       └── images/                  # Extracted inline figures and diagrams
└── langgraph/                       # Stateful, multi-actor Jupyter Notebooks
    ├── Hello_world.ipynb            # Foundational StateGraph setup
    ├── Graph_iii.ipynb              # Stateful nodes & edge routing
    ├── Graph_iv.ipynb               # Advanced branching logic
    └── multiple_inputs.ipynb        # StateGraph with parallel/multiple inputs
```

---

## 🚀 Explored Frameworks & Modules

### 🟢 1. [LangChain Basics](./langchain-basics)
This module covers the core building blocks of LLM applications, ranging from prompt templates to vector store retriever chains:
*   **Implementations:**
    *   [basic_qa_chatbot.py](./langchain-basics/basic_qa_chatbot.py) — A Streamlit chatbot interface powered by `ChatOpenAI` and `StrOutputParser` with tracing configured.
    *   [retriever_chain.py](./langchain-basics/retriever_chain.py) — Template structure for building custom retriever-based RAG chains.
*   **Detailed Study Notes (with diagrams):**
    *   [LangChain Core Components](./langchain-basics/notes/langchain_components.md): An in-depth overview of Models, Prompts, Memory, Indexes, Chains, Agents, and Runnables.
    *   [Chunking Strategies](./langchain-basics/notes/chunking_strategies.md): Analysis of Character-based, Recursive Character-based, and Semantic chunking.
    *   [Embedding Techniques](./langchain-basics/notes/embedding_techniques.md): Examination of vector spaces, dimensions, and popular models (OpenAI, SentenceTransformers, BGE).
    *   [Benefits of LangChain](./langchain-basics/notes/benefits_of_langchain.md): Key advantages of using a modular LLM framework.

### 🟢 2. [LangGraph Foundations](./langgraph)
This module focuses on building stateful, cyclic, multi-actor applications which are critical for agentic workflows:
*   **Notebooks:**
    *   [Hello_world.ipynb](./langgraph/Hello_world.ipynb) — Basic state representation using `TypedDict` and assembling a compiled `StateGraph`.
    *   [Graph_iii.ipynb](./langgraph/Graph_iii.ipynb) — Defining state nodes, mapping standard edges, and handling structured agent responses.
    *   [Graph_iv.ipynb](./langgraph/Graph_iv.ipynb) — Custom conditional edges, routing decisions, and state validation.
    *   [multiple_inputs.ipynb](./langgraph/multiple_inputs.ipynb) — Handling parallel workflows, multi-actor nodes, and parallel inputs.
*   **Core Concepts Covered:** State Management, Nodes & Edges, Conditional Routing, and Graph Compilation.

### 🟡 3. CrewAI *(Coming Soon)*
Future experiments orchestrating role-based, collaborative AI agent squads to automate multi-task workflows.

### 🟡 4. LlamaIndex *(Coming Soon)*
Future experiments with specialized data frameworks for advanced RAG architectures, query engines, and metadata indexing.

---

## 🛠️ Getting Started & Installation

### Prerequisites
*   Python 3.9+
*   Jupyter Notebook or JupyterLab (to run the LangGraph exercises)
*   An OpenAI API Key (configured in a local `.env` file)

### Setup Instructions
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_GITHUB_USERNAME/agentic-ai-sandbox.git
    cd agentic-ai-sandbox
    ```

2.  **Set up a virtual environment (Recommended):**
    ```bash
    python -m venv .venv
    # Activate on Windows:
    .venv\Scripts\activate
    # Activate on macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the root directory and add your keys:
    ```env
    OPENAI_API_KEY=your-openai-api-key-here
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_API_KEY=your-langsmith-key-here
    ```

5.  **Running the Streamlit Chatbot:**
    ```bash
    streamlit run langchain-basics/basic_qa_chatbot.py
    ```

6.  **Running the Jupyter Notebooks:**
    ```bash
    jupyter notebook
    ```
    Navigate to the `langgraph/` directory to open and explore the notebooks.
