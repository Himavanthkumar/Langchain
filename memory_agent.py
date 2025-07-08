# Import necessary libraries for type hints and LangChain components
from typing import TypedDict, List, Union  # For type hints and state definition
from langchain_core.messages import HumanMessage, AIMessage  # Message types
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini 2.5 Pro model
from langgraph.graph import StateGraph, START, END  # For building the workflow graph
from dotenv import load_dotenv  # For loading environment variables
import os  # For file operations

# Load environment variables
load_dotenv()

# Define the state structure for the memory agent
class AgentState(TypedDict):
    """
    A TypedDict defining the state for the memory agent.
    Stores conversation messages for logging.
    """
    messages: List[Union[HumanMessage, AIMessage]]  # List of human and AI messages

# Initialize the Gemini 2.5 Pro model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Specify the Gemini model
    google_api_key=os.getenv("GEMINI_API_KEY"),  # Load API key from environment
    temperature=0.3,  # Control randomness (0 = deterministic, 1 = creative)
    max_tokens=1000  # Limit response length
)

def process(state: AgentState) -> AgentState:
    """
    Processes user input, generates a response, and updates the state.
    
    Args:
        state: The current agent state with messages
    
    Returns:
        Updated state with the AI's response
    """
    # Invoke the LLM with the current messages
    response = llm.invoke(state["messages"])
    # Append the AI's response to the state
    state["messages"].append(AIMessage(content=response.content))
    # Print the AI's response
    print(f"\nAI: {response.content}")
    # Print the current state for debugging
    print("CURRENT STATE: ", [msg.content for msg in state["messages"]])
    return state

# Define the LangGraph workflow
graph = StateGraph(AgentState)
# Add a single node for processing
graph.add_node("process", process)
# Define edges from START to process and process to END
graph.add_edge(START, "process")
graph.add_edge("process", END)
# Compile the graph
agent = graph.compile()

def run_memory_agent():
    """
    Runs the interactive memory agent.
    Maintains conversation history and saves it to a file when exiting.
    """
    print("\n=== MEMORY AGENT ===")
    conversation_history = []  # Initialize empty history
    user_input = input("Enter: ")
    while user_input.lower() != "exit":
        # Append user input as a HumanMessage
        conversation_history.append(HumanMessage(content=user_input))
        # Invoke the agent
        result = agent.invoke({"messages": conversation_history})
        # Update the history
        conversation_history = result["messages"]
        user_input = input("Enter: ")
    
    # Save conversation history to a file
    with open("logging.txt", "w") as file:
        file.write("Your Conversation Log:\n")
        for message in conversation_history:
            if isinstance(message, HumanMessage):
                file.write(f"You: {message.content}\n")
            elif isinstance(message, AIMessage):
                file.write(f"AI: {message.content}\n\n")
        file.write("End of Conversation")
    print("Conversation saved to logging.txt")

# Run the agent if the script is executed
if __name__ == "__main__":
    run_memory_agent()