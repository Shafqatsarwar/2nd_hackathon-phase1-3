from typing import Dict, Any, List
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from .task_tools import MCPTaskTools
from .web_search import search_web
from ..database import get_session
from sqlmodel import Session

# Load environment variables (works locally, no-op on Vercel where env vars are injected)
load_dotenv(".env.backend", override=True)


class TodoOpenAIAgent:
    """
    OpenAI Agent that uses MCP tools to interact with the todo system
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please add it to your Vercel environment variables or .env.backend file."
            )
        self.client = OpenAI(api_key=api_key)
        self.task_tools = MCPTaskTools(get_session)

        # Define the tools that the agent can use
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web for general knowledge, news, weather, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The search query"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description (optional)"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority level (default: medium)"},
                            "is_recurring": {"type": "boolean", "description": "Is this a recurring task?"},
                            "recurrence_interval": {"type": "string", "description": "Interval e.g. 'daily', 'weekly'"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve tasks from the list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "task_id": {"type": "integer", "description": "The task ID to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task from the list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "task_id": {"type": "integer", "description": "The task ID to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modify task title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "task_id": {"type": "integer", "description": "The task ID to update"},
                            "title": {"type": "string", "description": "New title (optional)"},
                            "description": {"type": "string", "description": "New description (optional)"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "New priority"},
                            "is_recurring": {"type": "boolean", "description": "Update recurrence status"},
                            "recurrence_interval": {"type": "string", "description": "Update recurrence interval"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    def process_message(self, user_id: str, message: str, session: Session) -> str:
        """
        Process a user message using OpenAI agent with MCP tools
        """
        # Create a temporary task_tools instance with the current session
        temp_task_tools = MCPTaskTools(lambda: session)

        # Prepare the messages for the OpenAI API
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful todo management assistant. "
                    "Help users manage their tasks using the provided tools. "
                    "Always use the appropriate tool for the user's request. "
                    "Only use the tools provided, do not try to access the database directly. "
                    "When adding tasks, the tools now include automatic 'Analysis Skills' which identify priority and suggested tags. "
                    "Incorporate this analysis into your response to the user to showcase your intelligence. "
                    "For general knowledge questions (news, weather, etc.), use the 'web_search' tool. "
                    "IMPORTANT: When using 'web_search', extract only the essential keywords from the user's request. "
                    "Do NOT include filler words like 'what about', 'how to', 'next month', or conversational phrasing. "
                    "Example: for 'buy solar system in pakistan next month', search for 'solar system prices pakistan'. "
                    "Keep web search answers concise (approx 10-30 words). "
                    "\n\n"
                    "CONTEXT AWARENESS: If the user refers to 'it', 'that task', or uses follow-up commands like 'make it recurring' or 'repeat every month', "
                    "first use 'list_tasks' to see their recent tasks, then identify the most recently added task and update it accordingly. "
                    "For example, if they say 'repeat every month' right after adding a task, use 'update_task' on the most recent task with is_recurring=true and recurrence_interval='monthly'. "
                    f"The current user ID is: {user_id}"
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]

        # Call the OpenAI API with function calling
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        # Process the response
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Append the assistant message (the one that requested tools) to the history,
        # so that the following tool responses correctly follow a message with tool_calls.
        assistant_message = {
            "role": response_message.role,
            "content": response_message.content or "",
        }
        if response_message.tool_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": getattr(tool_call, "type", "function_call"),
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in response_message.tool_calls
            ]
        messages.append(assistant_message)

        if tool_calls:
            # Process tool calls
            tool_results = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Add the user_id to the function args if not present
                if "user_id" not in function_args:
                    function_args["user_id"] = user_id

                # Call the appropriate MCP tool function
                if function_name == "add_task":
                    result = temp_task_tools.add_task(
                        user_id=function_args["user_id"],
                        title=function_args["title"],
                        description=function_args.get("description"),
                        priority=function_args.get("priority", "medium"),
                        is_recurring=function_args.get("is_recurring", False),
                        recurrence_interval=function_args.get("recurrence_interval")
                    )
                elif function_name == "list_tasks":
                    result = temp_task_tools.list_tasks(
                        user_id=function_args["user_id"],
                        status=function_args.get("status", "all")
                    )
                elif function_name == "complete_task":
                    result = temp_task_tools.complete_task(
                        user_id=function_args["user_id"],
                        task_id=function_args["task_id"]
                    )
                elif function_name == "delete_task":
                    result = temp_task_tools.delete_task(
                        user_id=function_args["user_id"],
                        task_id=function_args["task_id"]
                    )
                elif function_name == "update_task":
                    result = temp_task_tools.update_task(
                        user_id=function_args["user_id"],
                        task_id=function_args["task_id"],
                        title=function_args.get("title"),
                        description=function_args.get("description"),
                        priority=function_args.get("priority"),
                        is_recurring=function_args.get("is_recurring"),
                        recurrence_interval=function_args.get("recurrence_interval")
                    )
                elif function_name == "web_search":
                    result = search_web(
                        query=function_args["query"]
                    )
                else:
                    result = {"error": f"Unknown tool: {function_name}"}

                tool_results.append({
                    "role": "tool",
                    "type": "tool_response",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(result)
                })

            # If there were tool calls, get the final response from the assistant
            if tool_results:
                # Add the tool results to the messages
                for tool_result in tool_results:
                    messages.append(tool_result)

                # Get the final response from the assistant
                final_response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )

                return final_response.choices[0].message.content

        # If no tool calls were made, return the assistant's response
        if response_message.content:
            return response_message.content

        return "I processed your request, but I don't have a specific response to share."
