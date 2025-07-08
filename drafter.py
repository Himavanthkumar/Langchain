# Import necessary libraries for type hints, LangChain, and LangGraph
from typing import Annotated, Sequence, TypedDict  # For type hints and state definition
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage  # Message types
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini 2.5 Pro model
from langchain_core.tools import tool  # For defining tools
from langgraph.graph import StateGraph, END  # For building the workflow graph
from langgraph.prebuilt import ToolNode  # Prebuilt node for tool execution
from langgraph.graph.message import add_messages  # Helper for adding messages to state
from dotenv import load_dotenv  # For loading environment variables
import os  # For file operations and environment variables

# Load environment variables from .env file
load_dotenv()

# Define the state structure for the drafter agent
class AgentState(TypedDict):
    """
    A TypedDict defining the state for the drafter agent.
    Stores conversation messages and supports message accumulation.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]  # List of messages with automatic accumulation

# Initialize global variable to store document content
document_content = ""

# Initialize the Gemini 2.5 Pro model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Specify the Gemini model
    google_api_key=os.getenv("GEMINI_API_KEY"),  # Load API key from environment
    temperature=0.3,  # Control randomness (0 = deterministic, 1 = creative)
    max_tokens=1000  # Limit response length
)


# Define tools for document editing
@tool
def update(content: str) -> str:
    """
    Updates the document with the provided content.
    
    Args:
        content: The new content for the document
    
    Returns:
        A confirmation message with the updated content
    """
    global document_content  # Access the global document content
    document_content = content  # Update the content
    return f"Document has been updated successfully! The current content is:\n{document_content}"

@tool
def save(filename: str) -> str:
    """
    Saves the current document to a text file.
    
    Args:
        filename: Name for the text file (appends .txt if not present)
    
    Returns:
        A confirmation message or error message
    """
    global document_content  # Access the global document content
    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"  # Ensure .txt extension
    try:
        with open(filename, 'w') as file:
            file.write(document_content)  # Write content to file
        print(f"\n💾 Document has been saved to: {filename}")
        return f"Document has been saved successfully to '{filename}'."
    except Exception as e:
        return f"Error saving document: {str(e)}"

# Combine tools for the agent
tools = [update, save]
# Bind tools to the model for tool-calling
model = llm.bind_tools(tools)

def our_agent(state: AgentState) -> AgentState:
    """
    Processes user input and generates a response, potentially calling tools.
    
    Args:
        state: The current agent state with messages
    
    Returns:
        Updated state with new messages
    """
    # Define a system prompt to guide the agent
    system_prompt = SystemMessage(content=f"""
    You are Drafter, a helpful writing assistant. You help users update and modify documents.
    - Use the 'update' tool to modify document content.
    - Use the 'save' tool to save the document and finish.
    - Always show the current document state after modifications.
    Current document content: {document_content}
    """)

    # Get or prompt for user input
    if not state["messages"]:
        user_input = "I'm ready to help you update a document. What would you like to create?"
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("\nWhat would you like to do with the document? ")
        print(f"\n👤 USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    # Combine system prompt, existing messages, and new user message
    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    # Invoke the model with the messages
    response = model.invoke(all_messages)
    
    # Print the AI's response
    print(f"\n🤖 AI: {response.content}")
    # Check for tool calls and print them
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")
    
    # Return updated state with new messages
    return {"messages": list(state["messages"]) + [user_message, response]}

def should_continue(state: AgentState) -> str:
    """
    Determines if the workflow should continue or end based on tool calls.
    
    Args:
        state: The current agent state
    
    Returns:
        "continue" to call tools, "end" to finish
    """
    messages = state["messages"]
    if not messages:
        return "continue"
    # Check the most recent message for tool calls
    for message in reversed(messages):
        if isinstance(message, ToolMessage) and "saved" in message.content.lower():
            return "end"  # End if document was saved
    return "continue"

# Define the LangGraph workflow
graph = StateGraph(AgentState)
# Add nodes for the agent and tools
graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))
# Set the entry point
graph.set_entry_point("agent")
# Connect agent to tools
graph.add_edge("agent", "tools")
# Conditional edge after tools
graph.add_conditional_edges(
    "tools",
    should_continue,
    {"continue": "agent", "end": END}
)
# Compile the graph
app = graph.compile()

def run_document_agent():
    """
    Runs the interactive drafter agent.
    Users can edit and save documents until the save tool is used.
    """
    print("\n=== DRAFTER AGENT ===")
    state = {"messages": []}  # Initialize empty state
    # Stream the workflow and print messages
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            for message in step["messages"][-3:]:  # Show last 3 messages
                if isinstance(message, ToolMessage):
                    print(f"\n🛠️ TOOL RESULT: {message.content}")
    print("\n=== DRAFTER FINISHED ===")

# Run the agent if the script is executed
if __name__ == "__main__":
    run_document_agent()