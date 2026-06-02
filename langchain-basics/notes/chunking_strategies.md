# Character text Splitter

A Character Text Splitter is a simple chunking method that:
👉 splits text purely by counting characters👉 without understanding sentences, paragraphs, or meaning.
Example:
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
chunk_size=500,
chunk_overlap=50
)
chunks = splitter.split_text(text)

# Recursive Text Splitter

A Recursive Text Splitter breaks text into chunks by trying larger semantic boundaries first, and only falling back to smaller ones if needed.
Instead of blindly cutting by size (like CharacterTextSplitter), it follows this logic:
Try to keep meaning together. Split only when you must.
It uses a priority list of separators, for example:
1. "\n\n"   → paragraphs
2. "\n"     → lines
3. "."      → sentences
4. " "      → words
5. ""       → characters (last resort)

It works recursively:
- Try splitting by paragraphs
- If chunk is still too large → split that chunk by sentences
- Still too large? → split by words
- Still too large? → split by characters
That’s why it’s called recursive.
Example in langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
chunk_size=500,
chunk_overlap=50
)

chunks = splitter.split_text(text)

# Semantic Splitter

A Semantic Splitter uses embeddings + similarity to detect topic boundaries and split text into conceptually coherent chunks.

# Where is Semantic Chunking used?

Advanced RAG frameworks support this:
LangChain
LlamaIndex
For example (LangChain style):

from langchain.text_splitter import SemanticChunker
from langchain.embeddings import OpenAIEmbeddings

chunker = SemanticChunker(OpenAIEmbeddings())

chunks = chunker.split_text(text)

Raw Docs
↓
Recursive Split (structure)
↓
Semantic Split (topic)
↓
Small chunks (~300 tokens)
↓
Parent chunks (~2000 tokens)
↓
Vector DB
