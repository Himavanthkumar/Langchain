# Multi-Agent System with Gemini 2.5 Pro and LangGraph

## Project Overview

This project implements a multi-agent system using **LangChain**, **LangGraph**, and **Gemini 2.5 Pro** (Google's large language model). The system consists of five distinct Python scripts, each representing a specialized agent designed to handle specific tasks. These agents are adapted from provided scripts (`Agent bot.py`, `Drafter.py`, `Memory_Agent.py`, `RAG_Agent.py`, `ReAct.py`) and converted to use Gemini 2.5 Pro instead of OpenAI's GPT-4o. Each script is standalone and can be run independently to perform its designated function.

### Agents and Their Purposes

1. **Agent Bot (`agent_bot.py`)**
   - A simple chat agent that processes general user queries and responds using Gemini 2.5 Pro.
   - Ideal for basic conversational tasks, such as answering questions or providing information.
   - Example: "Tell me a joke" or "What is the capital of France?"

2. **Drafter Agent (`drafter.py`)**
   - A writing assistant that allows users to create, update, and save text documents.
   - Uses tools (`update` and `save`) to modify document content and save it to a file.
   - Example: "Write a note: Meeting at 3 PM" or "Save to note.txt".

3. **Memory Agent (`memory_agent.py`)**
   - Maintains a conversation history and saves it to a file (`logging.txt`) when the user exits.
   - Useful for tracking interactions over time.
   - Example: Any query, with "exit" to save the log.

4. **RAG Agent (`rag_agent.py`)**
   - A Retrieval-Augmented Generation (RAG) agent that retrieves information from a document store (using FAISS) and answers questions about stock market performance in 2024.
   - Uses a tool (`retriever_tool`) to search a vector store for relevant document chunks.
   - Example: "What was the S&P 500 performance in 2024?"

5. **ReAct Agent (`react.py`)**
   - A Reasoning-and-Acting (ReAct) agent that performs calculations using tools (`add`, `subtract`, `multiply`) and handles general queries.
   - Follows a "reason, act, observe" loop to call tools when needed.
   - Example: "Add 40 + 12 and multiply by 6" or "Tell me a joke".

### Technologies Used

- **LangChain**: A Python library for building applications with large language models, providing tools for prompts, memory, and tool integration.
- **LangGraph**: An extension of LangChain for creating stateful, multi-agent workflows as graphs, where nodes represent tasks and edges define flow.
- **Gemini 2.5 Pro**: Google's advanced language model used for natural language processing and tool-calling.
- **FAISS**: A library for efficient similarity search, used in the RAG agent for document retrieval.
- **Python**: The programming language for all scripts, requiring version 3.8 or higher.

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
├── logging.txt          # Output file for memory agent logs
└── README.md            # This file
```

## Prerequisites

To run this project, you need:

1. **Python 3.8+**: Ensure Python is installed on your system.
2. **Google API Key**: Obtain an API key for Gemini 2.5 Pro from Google Cloud.
3. **Required Python Packages**:
   - Install the necessary libraries using pip:
     ```bash
     pip install langchain langchain-google-genai langgraph faiss-cpu python-dotenv
     ```

## Setup Instructions

1. **Clone or Create the Project Directory**
   - Create a directory named `multi-agent-system`.
   - Save the five Python scripts (`agent_bot.py`, `drafter.py`, `memory_agent.py`, `rag_agent.py`, `react.py`) in this directory.

2. **Set Up the Environment File**
   - Create a `.env` file in the project directory.
   - Add your Google API key:
     ```bash
     GOOGLE_API_KEY=your-api-key
     ```
   - Replace `your-api-key` with your actual Gemini API key.

3. **Install Dependencies**
   - Run the following command in your terminal to install required packages:
     ```bash
     pip install langchain langchain-google-genai langgraph faiss-cpu python-dotenv
     ```

4. **Verify Setup**
   - Ensure all scripts are in the project directory.
   - Confirm the `.env` file contains a valid `GOOGLE_API_KEY`.
   - Check that Python and pip are correctly installed:
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
  - The agent responds with an answer from Gemini 2.5 Pro.
  - Type `exit` to quit.
- **Example**:
  ```
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
  Enter: What's the weather like?
  AI: I don't have real-time weather data, but it's probably sunny somewhere!
  CURRENT STATE: ['What's the weather like?', 'I don't have real-time weather data, but it's probably sunny somewhere!']
  Enter: exit
  Conversation saved to logging.txt
  ```

### 4. Running the RAG Agent
- **Purpose**: Answer questions about stock market performance.
- **Command**:
  ```bash
  python rag_agent.py
  ```
- **Interaction**:
  - Enter questions about the stock market (e.g., "What was the S&P 500 performance in 2024?").
  - The agent retrieves relevant document chunks and responds.
  - Type `exit` or `quit` to stop.
- **Example**:
  ```
  What is your question: What was the S&P 500 performance in 2024?
  === ANSWER ===
  The S&P 500 saw a 10% rise in 2024.
  What is your question: exit
  ```

### 5. Running the ReAct Agent
- **Purpose**: Perform calculations and handle general queries.
- **Command**:
  ```bash
  python react.py
  ```
- **Interaction**:
  - Enter calculation queries (e.g., "Add 40 + 12 and multiply by 6") or general questions.
  - The agent uses tools for calculations and responds to other queries.
  - The script runs once with the example input; modify the `inputs` variable for different queries.
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

- **Document Store**: The RAG agent uses a FAISS vector store with sample documents about the stock market. To use real documents, replace the `sample_docs` list in `rag_agent.py` with your own data (e.g., load a PDF using `PyPDFLoader`).
- **Tools**: The ReAct and Drafter agents use placeholder tools. You can extend them with real APIs (e.g., a weather API for ReAct).
- **Gemini 2.5 Pro**: Ensure your Google API key is valid. If you encounter rate limits, check your API quota.
- **Logging**: The Memory Agent saves logs to `logging.txt`, and the Drafter Agent saves documents to user-specified files (e.g., `note.txt`).
- **Extensibility**: Add more agents, tools, or documents to enhance functionality.

## Troubleshooting

- **API Key Errors**: Verify that `GOOGLE_API_KEY` is correctly set in the `.env` file.
- **Module Not Found**: Ensure all dependencies are installed (`pip install -r requirements.txt` if you create a requirements file).
- **File Not Found**: For the Drafter Agent, ensure write permissions in the project directory.
- **FAISS Issues**: If the RAG agent fails, check that `faiss-cpu` is installed and the vector store is properly initialized.

## Contributing

Feel free to extend this project by:
- Adding new agents for specific tasks (e.g., a code generator).
- Integrating real data sources for the RAG agent.
- Enhancing tool functionality with external APIs.
- Improving the user interface (e.g., adding a web frontend).

For questions or contributions, contact the project maintainer or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details (not included in this repository but can be added).