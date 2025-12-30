import asyncio
from typing import Dict, Any, List
from modelcontextprotocol import Server, Tool, ToolResult
from modelcontextprotocol.models import CallTool
from src.backend.database import get_session


class TodoMCPServer:
    """
    MCP Server implementation for the Todo AI Chatbot
    Provides tools for AI agents to interact with the todo system
    """

    def __init__(self):
        self.server = Server("todo-mcp-server", "1.0.0")
        self._setup_tools()

    def _setup_tools(self):
        """Setup MCP tools for task operations"""
        from src.backend.mcp_server.task_tools import MCPTaskTools

        # Add task tool
        add_task_tool = Tool(
            name="add_task",
            description="Create a new task",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description (optional)"}
                },
                "required": ["user_id", "title"]
            }
        )

        # List tasks tool
        list_tasks_tool = Tool(
            name="list_tasks",
            description="Retrieve tasks from the list",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}
                },
                "required": ["user_id"]
            }
        )

        # Complete task tool
        complete_task_tool = Tool(
            name="complete_task",
            description="Mark a task as complete",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "integer", "description": "The task ID to complete"}
                },
                "required": ["user_id", "task_id"]
            }
        )

        # Delete task tool
        delete_task_tool = Tool(
            name="delete_task",
            description="Remove a task from the list",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "integer", "description": "The task ID to delete"}
                },
                "required": ["user_id", "task_id"]
            }
        )

        # Update task tool
        update_task_tool = Tool(
            name="update_task",
            description="Modify task title or description",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "integer", "description": "The task ID to update"},
                    "title": {"type": "string", "description": "New title (optional)"},
                    "description": {"type": "string", "description": "New description (optional)"}
                },
                "required": ["user_id", "task_id"]
            }
        )

        # Add all tools to server
        self.server.add_tool(add_task_tool, self._handle_add_task)
        self.server.add_tool(list_tasks_tool, self._handle_list_tasks)
        self.server.add_tool(complete_task_tool, self._handle_complete_task)
        self.server.add_tool(delete_task_tool, self._handle_delete_task)
        self.server.add_tool(update_task_tool, self._handle_update_task)

    async def _handle_add_task(self, call: CallTool) -> ToolResult:
        """Handle add_task tool call"""
        try:
            from src.backend.mcp_server.task_tools import MCPTaskTools
            args = call.arguments
            task_tools = MCPTaskTools(get_session)
            result = task_tools.add_task(
                user_id=args["user_id"],
                title=args["title"],
                description=args.get("description")
            )
            return ToolResult(content=str(result), is_error=False)
        except Exception as e:
            return ToolResult(content=str({"error": str(e)}), is_error=True)

    async def _handle_list_tasks(self, call: CallTool) -> ToolResult:
        """Handle list_tasks tool call"""
        try:
            from src.backend.mcp_server.task_tools import MCPTaskTools
            args = call.arguments
            task_tools = MCPTaskTools(get_session)
            result = task_tools.list_tasks(
                user_id=args["user_id"],
                status=args.get("status", "all")
            )
            return ToolResult(content=str(result), is_error=False)
        except Exception as e:
            return ToolResult(content=str({"error": str(e)}), is_error=True)

    async def _handle_complete_task(self, call: CallTool) -> ToolResult:
        """Handle complete_task tool call"""
        try:
            from src.backend.mcp_server.task_tools import MCPTaskTools
            args = call.arguments
            task_tools = MCPTaskTools(get_session)
            result = task_tools.complete_task(
                user_id=args["user_id"],
                task_id=args["task_id"]
            )
            return ToolResult(content=str(result), is_error=False)
        except Exception as e:
            return ToolResult(content=str({"error": str(e)}), is_error=True)

    async def _handle_delete_task(self, call: CallTool) -> ToolResult:
        """Handle delete_task tool call"""
        try:
            from src.backend.mcp_server.task_tools import MCPTaskTools
            args = call.arguments
            task_tools = MCPTaskTools(get_session)
            result = task_tools.delete_task(
                user_id=args["user_id"],
                task_id=args["task_id"]
            )
            return ToolResult(content=str(result), is_error=False)
        except Exception as e:
            return ToolResult(content=str({"error": str(e)}), is_error=True)

    async def _handle_update_task(self, call: CallTool) -> ToolResult:
        """Handle update_task tool call"""
        try:
            from src.backend.mcp_server.task_tools import MCPTaskTools
            args = call.arguments
            task_tools = MCPTaskTools(get_session)
            result = task_tools.update_task(
                user_id=args["user_id"],
                task_id=args["task_id"],
                title=args.get("title"),
                description=args.get("description")
            )
            return ToolResult(content=str(result), is_error=False)
        except Exception as e:
            return ToolResult(content=str({"error": str(e)}), is_error=True)

    async def start(self):
        """Start the MCP server"""
        await self.server.start()

    async def stop(self):
        """Stop the MCP server"""
        await self.server.shutdown()


# Global instance for use in the application
mcp_server = TodoMCPServer()