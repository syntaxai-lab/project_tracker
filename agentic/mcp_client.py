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


def fetch_tasks(filters):
    """Return structured response for the agent with smart prompt-based filter fallback."""
    logging.info(f"[MCP] Fetching tasks with filters: {filters}")
    data = get_tasks(filters)
    return {"filters": filters, "results": data}


def fetch_projects(filters):
    """Return structured response for project-related queries."""
    logging.info(f"[MCP] Fetching projects with filters: {filters}")
    data = get_projects(filters)
    return {"filters": filters, "results": data}


def route_fetch(entity, filters):
    """Route to the appropriate fetch function based on entity."""
    if entity == "tasks":
        return fetch_tasks(filters)
    elif entity == "projects":
        return fetch_projects(filters)

    # Default fallback: return empty results when entity is unknown
    logging.warning("[MCP] route_fetch called with unknown entity. Returning empty results.")
    return {"filters": filters, "results": []}
