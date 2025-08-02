import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

API_URL = os.getenv("API_URL", "http://localhost:5050")


def get_tasks(filters: dict):
    """Call Flask API with filters."""
    try:
        response = requests.get(f"{API_URL}/tasks", params=filters, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"[MCP] Task fetch failed: {e}")
        return {"error": str(e), "results": []}


def get_projects(filters: dict):
    """Call Flask API to fetch projects."""
    try:
        response = requests.get(f"{API_URL}/projects", params=filters, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"[MCP] Project fetch failed: {e}")
        return {"error": str(e), "results": []}


def fetch_tasks(filters, user_prompt=None):
    """Return structured response for the agent with smart prompt-based filter fallback."""
    # Apply fallback extraction if filters are empty
    if not filters and user_prompt:
        lower_prompt = user_prompt.lower()
        if "overdue" in lower_prompt:
            filters["status"] = "overdue"
        if "assigned to" in lower_prompt:
            # crude extraction of name after 'assigned to'
            parts = lower_prompt.split("assigned to")
            if len(parts) > 1:
                filters["assigned_to"] = parts[1].strip().split(" ")[0]
        if "project" in lower_prompt:
            filters["entity"] = "projects"

    logging.info(f"[MCP] Fetching tasks with filters: {filters}")
    data = get_tasks(filters)
    return {"filters": filters, "results": data}
