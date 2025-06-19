from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from loguru import logger
from langgraph.graph import MessagesState, StateGraph
from app.util import llm
from app.tools import get_conversion_factor, convert


def call_llm(state: MessagesState):
    logger.debug("-->call llm<--")

    tools = [get_conversion_factor, convert]
    llm_with_tools = llm.bind_tools(tools)

    SYSTEM_PROMPT = """
    To convert 10 USD to INR, follow these steps:
    1. First, get the conversion factor between USD and INR
    2. Then, use that conversion factor to convert 10 USD
    3. Provide both the conversion rate and the final converted amount

    What is the conversion factor between USD and INR, and based on that can you convert 10 USD to INR?
    """
    resp = llm_with_tools.invoke([SYSTEM_PROMPT] + state["messages"])

    logger.debug(f"response from llm call: {resp}")
    return {"messages": [resp]}


def create_workflow() -> CompiledStateGraph:
    tools = [get_conversion_factor, convert]

    workflow = StateGraph(MessagesState)
    workflow.add_node("travel agent", call_llm)
    workflow.add_node("tools", ToolNode(tools))

    workflow.set_entry_point("travel agent")
    workflow.add_conditional_edges("travel agent", tools_condition)

    workflow.add_edge("tools", "travel agent")

    app = workflow.compile()
    return app


def create_graph_png(graph: CompiledStateGraph, file_name: str = "graph.png"):
    graph_png = graph.get_graph().draw_mermaid_png()
    with open(file_name, "wb") as f:
        f.write(graph_png)
