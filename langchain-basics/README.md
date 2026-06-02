# LangChain Basics 🦜🔗

This directory contains foundational code and study notes for understanding **LangChain**, a framework for developing applications powered by language models.

## 📁 Contents

### 1. Python Scripts
*   **[`basic_qa_chatbot.py`](./basic_qa_chatbot.py)**
    A simple Streamlit web application demonstrating how to build a Question-Answering (QA) chatbot. It utilizes `ChatOpenAI`, custom `ChatPromptTemplate`, and `StrOutputParser`.
*   **[`retriever_chain.py`](./retriever_chain.py)**
    A boilerplate/template script for implementing a Retriever-Augmented Generation (RAG) chain.

### 2. Study Notes (`/notes`)
Detailed markdown notes converted from original study documents. These cover essential RAG and LangChain theory:
*   **[LangChain Components](./notes/langchain_components.md):** An overview of Models, Prompts, Memory, Indexes, Chains, and Agents.
*   **[Chunking Strategies](./notes/chunking_strategies.md):** Exploring Character, Recursive, and Semantic text splitting.
*   **[Embedding Techniques](./notes/embedding_techniques.md):** Understanding vector spaces and comparing popular embedding models (OpenAI, BGE, SentenceTransformers).
*   **[Benefits of LangChain](./notes/benefits_of_langchain.md):** Why use a modular framework for LLMs.

*(All diagrams and figures referenced in the notes are stored in `notes/images/`)*

## 🚀 How to Run the Chatbot

Make sure you have your `.env` file set up in the root directory with your `OPENAI_API_KEY`. Then, run:

```bash
streamlit run basic_qa_chatbot.py
```
