# Multi-Agent System with Gemini and LangGraph

## Project Overview

This project implements a **multi-agent system** using **LangChain**, **LangGraph**, and **Google's Gemini models** (Gemini 2.0 Flash for all agents). The system consists of five distinct Python scripts, each representing a specialized agent designed to handle specific tasks. These scripts are adapted from provided code (`Agent bot.py`, `Drafter.py`, `Memory_Agent.py`, `RAG_Agent.py`, `ReAct.py`), with the RAG agent to use Gemini 2.0 Flash and Chroma. Each agent is standalone and can be run independently to perform its designated function.

### Agents and Their Purposes

1. **Agent Bot (`agent_bot.py`)**

   - **Purpose**: A simple chat agent for general-purpose conversations.
   - **Functionality**: Processes user queries using Gemini 2.5 Pro and responds without additional tools or memory.
   - **Example**: "Tell me a joke" or "What is the capital of France?"
   - **Use Case**: Ideal for quick, stateless interactions.

2. **Drafter Agent (`drafter.py`)**

   - **Purpose**: A writing assistant for creating, editing, and saving text documents.
   - **Functionality**: Uses `update` and `save` tools to modify document content and save it to a file. The workflow ends after saving.
   - **Example**: "Write a note: Meeting at 3 PM" or "Save to note.txt".
   - **Use Case**: Useful for drafting notes or documents interactively.

3. **Memory Agent (`memory_agent.py`)**

   - **Purpose**: Maintains and logs conversation history.
   - **Functionality**: Stores all user and AI messages in memory and saves them to `logging.txt` when the user exits.
   - **Example**: Any query, with "exit" to save the conversation log.
   - **Use Case**: Tracks interactions for later review.

4. **RAG Agent (`rag_agent.py`)**

   - **Purpose**: Answers questions about stock market performance in 2024 using document retrieval.
   - **Functionality**: Loads a PDF (`Stock_Market_Performance_2024.pdf`), stores chunks in a Chroma vector database, and retrieves relevant information using a `retriever_tool`. Uses Gemini 2.0 Flash for both LLM and embeddings.
   - **Example**: "What was the S&P 500 performance in 2024?"
   - **Use Case**: Ideal for querying specific data from documents.

5. **ReAct Agent (`react.py`)**
   - **Purpose**: Performs calculations and handles general queries using a reasoning-and-acting approach.
   - **Functionality**: Uses `add`, `subtract`, and `multiply` tools to perform calculations and responds to non-tool queries using Gemini 2.5 Pro.
   - **Example**: "Add 40 + 12 and multiply by 6" or "Tell me a joke".
   - **Use Case**: Suitable for tasks requiring computation or external tool use.

### Technologies Used

- **LangChain**: A Python library for building applications with large language models, providing tools for prompts, memory, and tool integration.
- **LangGraph**: An extension of LangChain for creating stateful workflows as graphs, where nodes represent tasks (e.g., LLM calls, tool execution) and edges define flow.
- **Gemini 2.0 Flash**: Used in `agent_bot.py`, `drafter.py`, `memory_agent.py`, and `react.py` for natural language processing and tool-calling.Used in `rag_agent.py` for both LLM and embeddings, optimized for retrieval tasks.
- **Chroma**: A vector database for storing and searching document embeddings in the RAG agent.
- **PyPDFLoader**: A LangChain component for loading and extracting text from PDF files (used in `rag_agent.py`).
- **Python**: The programming language, requiring version 3.8 or higher.

## Project Structure

```
multi-agent-system/
│
├── agent_bot.py          # Simple chat agent
├── drafter.py           # Document editing and saving agent
├── memory_agent.py      # Conversation history logging agent
├── rag_agent.py         # RAG agent for document retrieval
├── react.py             # ReAct agent for calculations
├── .env                 # Environment file for API key
├── Stock_Market_Performance_2024.pdf  # Input PDF for RAG agent (required)
├── chroma_db_store/     # Directory for Chroma vector store
├── logging.txt          # Output file for memory agent logs
└── README.md            # This file
```

## Prerequisites

To run this project, you need:

1. **Python 3.8+**: Ensure Python is installed on your system.
2. **Google API Key**: Obtain an API key for Gemini models from Google Cloud.
3. **Input PDF for RAG Agent**: Provide a `Stock_Market_Performance_2024.pdf` file for `rag_agent.py`.
4. **Required Python Packages**:
   - Install the necessary libraries using pip:
     ```bash
     pip install langchain langchain-google-genai langgraph chromadb pypdf python-dotenv
     ```

## Setup Instructions

1. **Create the Project Directory**

   - Create a directory named `multi-agent-system`.
   - Save the five Python scripts (`agent_bot.py`, `drafter.py`, `memory_agent.py`, `rag_agent.py`, `react.py`) in this directory.

2. **Add the PDF File**

   - Place the `Stock_Market_Performance_2024.pdf` file in the project directory for `rag_agent.py`.
   - Ensure the `pdf_path` variable in `rag_agent.py` (`pdf_path = "Stock_Market_Performance_2024.pdf"`) matches the file location.

3. **Set Up the Environment File**

   - Create a `.env` file in the project directory.
   - Add your Google API key:
     ```bash
     GEMINI_API_KEY=your-api-key
     ```
   - Replace `your-api-key` with your actual Gemini API key. Note that `rag_agent.py` uses `GEMINI_API_KEY`, while others use `GOOGLE_API_KEY` for compatibility with earlier scripts. You can use the same key for both.

4. **Install Dependencies**

   - Run the following command in your terminal to install required packages:
     ```bash
     pip install -r requirements.txt
     ```

5. **Create the Chroma Store Directory**

   - The RAG agent creates a `chroma_db_store` directory at `C:\Users\himav\Desktop\Code\Code\python\Langgraph\chroma_db_store`.
   - Update the `persist_directory` path in `rag_agent.py` if you’re on a different system or prefer a different location (e.g., `./chroma_db_store` for the project directory).
   - Ensure you have write permissions for the directory.

6. **Verify Setup**
   - Confirm that all scripts, `.env`, and `Stock_Market_Performance_2024.pdf` are in the project directory.
   - Verify that `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) is set in `.env`.
   - Check that Python and pip are installed:
     ```bash
     python --version
     pip --version
     ```

## How to Run the Project

Each script is standalone and can be run independently. Follow these steps to run each agent:

### 1. Running the Agent Bot

- **Purpose**: General-purpose chat.
- **Command**:
  ```bash
  python agent_bot.py
  ```
- **Interaction**:
  - Enter a query (e.g., "Tell me a joke").
  - The agent responds using Gemini 2.5 Pro.
  - Type `exit` to quit.
- **Example**:
  ```
  === SIMPLE CHAT AGENT ===
  Enter: Tell me a joke
  AI: Why did the scarecrow become a motivational speaker? Because he was outstanding in his field!
  Enter: exit
  ```

### 2. Running the Drafter Agent

- **Purpose**: Edit and save documents.
- **Command**:
  ```bash
  python drafter.py
  ```
- **Interaction**:
  - Enter commands to update or save a document (e.g., "Write a note: Meeting at 3 PM", "Save to note.txt").
  - The agent updates the document content or saves it to a file.
  - The workflow ends after saving.
- **Example**:
  ```
  === DRAFTER AGENT ===
  What would you like to do with the document? Write a note: Meeting at 3 PM
  🤖 AI: Updating document with the note.
  🔧 USING TOOLS: ['update']
  🛠️ TOOL RESULT: Document has been updated successfully! The current content is:
  Meeting at 3 PM
  What would you like to do with the document? Save to note.txt
  🤖 AI: Saving document...
  💾 Document has been saved to: note.txt
  🛠️ TOOL RESULT: Document has been saved successfully to 'note.txt'.
  === DRAFTER FINISHED ===
  ```

### 3. Running the Memory Agent

- **Purpose**: Log conversation history.
- **Command**:
  ```bash
  python memory_agent.py
  ```
- **Interaction**:
  - Enter any query (e.g., "What's the weather like?").
  - The agent responds and logs the conversation.
  - Type `exit` to save the log to `logging.txt`.
- **Example**:
  ```
  === MEMORY AGENT ===
  Enter: What's the weather like?
  AI: I don't have real-time weather data, but it's probably sunny somewhere!
  CURRENT STATE: ['What's the weather like?', 'I don't have real-time weather data, but it's probably sunny somewhere!']
  Enter: exit
  Conversation saved to logging.txt
  ```

### 4. Running the RAG Agent

- **Purpose**: Answer questions about stock market performance in 2024.
- **Command**:
  ```bash
  python rag_agent.py
  ```
- **Interaction**:
  - Ensure `Stock_Market_Performance_2024.pdf` is in the project directory.
  - Enter questions about the stock market (e.g., "What was the S&P 500 performance in 2024?").
  - The agent retrieves relevant document chunks and responds.
  - Type `exit` or `quit` to stop.
- **Example**:
  ```
  === RAG AGENT ===
  PDF has been loaded and has 10 pages
  Created ChromaDB vector store!
  What is your question: What was the S&P 500 performance in 2024?
  Calling Tool: retriever_tool with query: What was the S&P 500 performance in 2024?
  Result length: 123
  Tools Execution Complete. Back to the model!
  === ANSWER ===
  The S&P 500 saw a 10% rise in 2024, according to Document 1.
  What is your question: exit
  ```
  _Note_: The actual output depends on the content of `Stock_Market_Performance_2024.pdf`.

### 5. Running the ReAct Agent

- **Purpose**: Perform calculations and handle general queries.
- **Command**:
  ```bash
  python react.py
  ```
- **Interaction**:
  - The script runs with a predefined input ("Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.").
  - To test different queries, modify the `inputs` variable in `react.py` (e.g., `inputs = {"messages": [HumanMessage(content="Your query here")]}`).
  - The agent uses tools for calculations and responds to general queries.
- **Example**:

  ```
  === REACT AGENT ===
  ============================== [HumanMessage] ==============================
  content='Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.'
  ============================== [AIMessage] ==============================
  To solve the query, I will first add 40 and 12, which gives 52. Then, I will multiply 52 by 6, resulting in 312.

  Here's a joke for you: Why did the math book look sad? Because it had too many problems!
  Final Answer: 312
  ```

## Notes

- **PDF Requirement for RAG Agent**: The `rag_agent.py` script requires a `Stock_Market_Performance_2024.pdf` file. If unavailable, modify the script to use sample documents (e.g., add a `sample_docs` list as in previous versions).
- **Chroma Vector Store**: The RAG agent stores embeddings in `chroma_db_store`. Update the `persist_directory` in `rag_agent.py` if the default path (`C:\Users\himav\Desktop\Code\Code\python\Langgraph\chroma_db_store`) is unsuitable.
- **Gemini Models**: Most agents use Gemini 2.0 Flash. Ensure your API key supports both models.
- **Environment Variables**: Use `GEMINI_API_KEY` in .env.
- **Logging**: The Memory Agent saves logs to `logging.txt`, and the Drafter Agent saves documents to user-specified files (e.g., `note.txt`).
- **Extensibility**: Each script is modular, allowing you to test or extend individual agents.

## Extending the Project

You can enhance the system by:

- **Adding More Documents**: Load additional PDFs or text files into the RAG agent’s vector store.
- **Expanding Tools**: Add new tools (e.g., a web search tool) to the ReAct or Drafter agents.
- **Integrating Agents**: Combine agents into a single system with a supervisor to route queries (e.g., based on keywords).
- **Improving Retrieval**: Adjust `chunk_size`, `chunk_overlap`, or `search_kwargs` in `rag_agent.py` for better accuracy.
- **Adding a UI**: Create a web or command-line interface for a user-friendly experience.

## Contributing

Contributions are welcome! To contribute:

- Add new agents or tools.
- Fix bugs or improve error handling.
- Submit pull requests or contact the project maintainer with suggestions.
