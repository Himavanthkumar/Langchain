# Import necessary libraries for type hints and LangChain components
from typing import TypedDict, List  # For defining the state structure
from langchain_core.messages import HumanMessage, AIMessage  # Message types for user and AI
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini 2.5 Pro model
from langgraph.graph import StateGraph, START, END  # For building the workflow graph
from dotenv import load_dotenv  # For loading environment variables
import os  # For accessing environment variables

# Load environment variables from .env file (e.g., GEMINI_API_KEY)
load_dotenv()

# Define the state structure for the agent
class AgentState(TypedDict):
    """
    A TypedDict defining the state for the chat agent.
    This keeps track of the conversation messages.
    """
    messages: List[HumanMessage | AIMessage]  # List of human and AI messages

# Initialize the Gemini 2.5 Pro model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Specify the Gemini model
    google_api_key=os.getenv("GEMINI_API_KEY"),  # Load API key from environment
    temperature=0.3,  # Control randomness (0 = deterministic, 1 = creative)
    max_tokens=1000  # Limit response length
)

def process(state: AgentState) -> AgentState:
    """
    Processes the user input and generates a response using the LLM.
    
    Args:
        state: The current agent state containing the conversation messages
    
    Returns:
        Updated state with the AI's response appended
    """
    # Get the latest message from the state (user input)
    latest_message = state["messages"]
    # Invoke the LLM with the conversation history
    response = llm.invoke(latest_message)
    # Print the AI's response for user visibility
    print(f"\nAI: {response.content}")
    # Append the AI's response to the state
    state["messages"].append(AIMessage(content=response.content))
    return state

# Create a LangGraph workflow
graph = StateGraph(AgentState)
# Add a single node for processing user input
graph.add_node("process", process)
# Define the entry point (START) to the process node
graph.add_edge(START, "process")
# Define the exit point after processing
graph.add_edge("process", END)
# Compile the graph into an executable workflow
agent = graph.compile()

# Main loop to interact with the user
def run_chat_agent():
    """
    Runs the interactive chat agent.
    Users can input queries, and the agent responds until 'exit' is entered.
    """
    print("\n=== SIMPLE CHAT AGENT ===")
    # Initialize an empty conversation history
    conversation_history = []
    # Prompt for user input
    user_input = input("Enter: ")
    while user_input.lower() != "exit":
        # Append user input as a HumanMessage to the history
        conversation_history.append(HumanMessage(content=user_input))
        # Invoke the agent with the current history
        result = agent.invoke({"messages": conversation_history})
        # Update the conversation history with the result
        conversation_history = result["messages"]
        # Prompt for the next input
        user_input = input("Enter: ")

# Run the agent if the script is executed directly
if __name__ == "__main__":
    run_chat_agent()