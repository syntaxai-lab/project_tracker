import os
import json
import logging
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from mcp_client import fetch_tasks, fetch_projects
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
llm = ChatOpenAI(model=model_name, openai_api_key=api_key, temperature=0)


def interpret_with_llm(state):
    """Use LLM to extract query filters and entity type."""
    user_query = state["prompt"]

    system_prompt = (
        "You are an intelligent API query parser. "
        "Analyze the user query and return ONLY a flat JSON object with:\n"
        "entity: 'projects' or 'tasks'\n"
        "any filters: status, assigned_to, due_date\n\n"
        "Example output:\n"
        "{\"entity\": \"tasks\", \"status\": \"overdue\"}"
    )

    # Send combined system + user prompt
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ])

    try:
        filters = json.loads(response.content)
    except json.JSONDecodeError:
        logging.warning("[AGENT] Failed to parse filters from LLM response. Defaulting to empty filters.")
        filters = {}

    if "entity" not in filters:
        filters["entity"] = "tasks"  # default fallback

    return {"filters": filters, "prompt": user_query}


def call_api(state):
    """Call MCP client with filters and route to correct endpoint."""
    filters = state["filters"]
    entity = filters.pop("entity", "tasks")
    logging.info(f"[AGENT] Calling API for entity={entity} with filters: {filters}")

    if entity == "projects":
        results = fetch_projects(filters)
    else:
        results = fetch_tasks(filters)

    logging.info(f"[AGENT] API responded: {results}")
    return {"output": results}


def run_agent():
    print("Ask your questions (press 0 to exit):")
    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() in ["0", "exit", "quit"]:
                print("Exiting agent.")
                break

            # Run the LLM → API pipeline
            result = graph.invoke({"prompt": user_input, "filters": {}, "output": {}})
            print(result["output"])

        except EOFError:
            print("\nEOF detected, exiting agent.")
            break
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt, exiting agent.")
            break


# Build workflow
workflow = StateGraph(AgentState)
workflow.add_node("interpret_query", interpret_with_llm)
workflow.add_node("fetch_api", call_api)

workflow.add_edge("interpret_query", "fetch_api")
workflow.set_entry_point("interpret_query")
graph = workflow.compile()

if __name__ == "__main__":
    run_agent()
