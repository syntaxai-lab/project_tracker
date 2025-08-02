import os
import json
import logging
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from mcp_client import fetch_tasks
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


class AgentState(TypedDict):
    prompt: str
    filters: dict
    output: dict


# Load model name from env
model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model=model_name, temperature=0)
llm = ChatOpenAI(model=model_name, openai_api_key=api_key, temperature=0)


def interpret_with_llm(state):
    """Use LLM to extract query filters."""
    user_query = state["prompt"]
    instruction = (
        "Extract filters (assigned_to, status, due_date) from the following user query. "
        "Return JSON only, e.g. {\"assigned_to\":\"Bob\",\"status\":\"overdue\"}.\n"
        f"Query: {user_query}"
    )
    response = llm.invoke(instruction)
    try:
        filters = json.loads(response.content)
    except json.JSONDecodeError:
        logging.warning("[AGENT] Failed to parse filters from LLM response.")
        filters = {}
    return {"filters": filters, "prompt": user_query}


def call_api(state):
    """Call MCP client with filters."""
    logging.info(f"[AGENT] Calling API with filters: {state['filters']}")
    results = fetch_tasks(state["filters"])
    logging.info(f"[AGENT] API responded: {results}")
    return {"output": results}


# Build workflow
workflow = StateGraph(AgentState)
workflow.add_node("interpret_query", interpret_with_llm)
workflow.add_node("fetch_api", call_api)

workflow.add_edge("interpret_query", "fetch_api")
workflow.set_entry_point("interpret_query")
graph = workflow.compile()

if __name__ == "__main__":
    query = input("ask your questions here: ")
    output = graph.invoke({"prompt": query})
    print(output["output"])
