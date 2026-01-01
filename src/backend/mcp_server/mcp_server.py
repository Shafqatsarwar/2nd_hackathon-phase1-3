from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: Dict[str, Any]


class TodoMCPServer:
    """
    Lightweight placeholder for the Phase III MCP server.
    It exposes the tool signatures that the AI agent is expected to call,
    but the actual server implementation lives outside this repo for now.
    """

    def __init__(self) -> None:
        self.tools = self._build_tool_definitions()

    def _build_tool_definitions(self) -> List[ToolDefinition]:
        """Return a list of MCP tool definitions for the todo agent."""
        return [
            self._tool(
                name="add_task",
                description="Create a new task",
                parameters={
                    "user_id": {"type": "string", "description": "The user ID"},
                    "title": {"type": "string", "description": "Task title"},
                    "description": {
                        "type": "string",
                        "description": "Task description (optional)"
                    }
                },
                required=["user_id", "title"]
            ),
            self._tool(
                name="list_tasks",
                description="Retrieve tasks for a user",
                parameters={
                    "user_id": {"type": "string", "description": "The user ID"},
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "default": "all"
                    }
                },
                required=["user_id"]
            ),
            self._tool(
                name="complete_task",
                description="Mark a task as complete",
                parameters={
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "integer", "description": "The task ID to complete"}
                },
                required=["user_id", "task_id"]
            ),
            self._tool(
                name="delete_task",
                description="Remove a task from the list",
                parameters={
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "integer", "description": "The task ID to delete"}
                },
                required=["user_id", "task_id"]
            ),
            self._tool(
                name="update_task",
                description="Modify task title or description",
                parameters={
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "integer", "description": "The task ID to update"},
                    "title": {"type": "string", "description": "New title (optional)"},
                    "description": {"type": "string", "description": "New description (optional)"}
                },
                required=["user_id", "task_id"]
            ),
        ]

    @staticmethod
    def _tool(name: str, description: str, parameters: Dict[str, Any], required: List[str]) -> ToolDefinition:
        return ToolDefinition(
            name=name,
            description=description,
            input_schema={
                "type": "object",
                "properties": parameters,
                "required": required
            }
        )


mcp_server = TodoMCPServer()
MCP_AVAILABLE = True
