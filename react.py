# Import necessary libraries for type hints, LangChain, and LangGraph
import os
from typing import Annotated, Sequence, TypedDict  # For type hints and state definition
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage # Message types
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini 2.5 Pro model
from langchain_core.tools import tool  # For defining tools
from langgraph.graph import StateGraph, END  # For building the workflow graph
from langgraph.prebuilt import ToolNode  # Prebuilt node for tools
from langgraph.graph.message import add_messages  # Helper for message accumulation
from dotenv import load_dotenv  # For environment variables

# Load environment variables
load_dotenv()

# Define the state structure for the ReAct agent
class AgentState(TypedDict):
    """
    A TypedDict defining the state for the ReAct agent.
    Stores conversation messages with accumulation.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]  # List of messages

# Initialize the Gemini 2.5 Pro model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Specify the Gemini model
    google_api_key=os.getenv("GEMINI_API_KEY"),  # Load API key from environment
    temperature=0.3,  # Control randomness (0 = deterministic, 1 = creative)
    max_tokens=1000  # Limit response length
)

# Define tools for calculations
@tool
def add(a: int, b: int) -> int:
    """
    Adds two numbers together.
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        The sum of a and b
    """
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """
    Subtracts the second number from the first.
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        The difference of a and b
    """
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiplies two numbers.
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        The product of a and b
    """
    return a * b

# Combine tools
tools = [add, subtract, multiply]
# Bind tools to the model
model = llm.bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    """
    Calls the LLM with a system prompt and current messages.
    
    Args:
        state: The current agent state
    
    Returns:
        Updated state with the LLM's response
    """
    system_prompt = SystemMessage(content="You are an AI assistant that performs calculations using tools.")
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    """
    Checks if the last message contains tool calls.
    
    Args:
        state: The current agent state
    
    Returns:
        "continue" if tool calls are present, "end" otherwise
    """
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    return "continue"

# Define the LangGraph workflow
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)
graph.add_node("tools", ToolNode(tools=tools))
graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {"continue": "tools", "end": END}
)
graph.add_edge("tools", "our_agent")
app = graph.compile()

def print_stream(stream):
    """
    Prints the output of the workflow stream.
    
    Args:
        stream: The stream of state updates from the workflow
    """
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

# Example usage
if __name__ == "__main__":
    print("\n=== REACT AGENT ===")
    inputs = {"messages": [HumanMessage(content="Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
    print_stream(app.stream(inputs, stream_mode="values"))