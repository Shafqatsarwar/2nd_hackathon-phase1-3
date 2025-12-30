from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
from sqlmodel import Session
from openai import OpenAI
from src.backend.database import get_session
from src.backend.auth_utils import verify_jwt
from src.backend.models import Conversation, Message
from src.backend.mcp_server.mcp_server import mcp_server
from src.backend.mcp_server.task_tools import MCPTaskTools


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]] = []


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    token_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint for the AI-powered todo chatbot
    """
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's chat")

    # Get or create conversation
    conversation_id = request.conversation_id
    if not conversation_id:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        conversation_id = conversation.id
    else:
        # Verify conversation belongs to user
        existing_conv = session.get(Conversation, conversation_id)
        if not existing_conv or existing_conv.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")

    # Store user message
    user_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=request.message
    )
    session.add(user_message)
    session.commit()

    # Prepare for AI interaction
    # For now, we'll simulate the AI agent behavior using a simple approach
    # In a real implementation, you would use OpenAI's agent system with MCP tools

    # For now, implement a simple rule-based response to demonstrate the concept
    response_text = await process_natural_language_command(
        user_id, request.message, session
    )

    # Store assistant response
    assistant_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="assistant",
        content=response_text
    )
    session.add(assistant_message)
    session.commit()

    return ChatResponse(
        conversation_id=conversation_id,
        response=response_text,
        tool_calls=[]  # In a real implementation, this would contain actual tool calls
    )


async def process_natural_language_command(user_id: str, message: str, session: Session):
    """
    Process natural language command and execute appropriate task operations
    This is a simplified version - in production, this would use OpenAI agents with MCP tools
    """
    task_tools = MCPTaskTools(lambda: session)
    message_lower = message.lower()

    # Simple pattern matching for demonstration
    if any(word in message_lower for word in ["add", "create", "remember", "need to"]):
        # Extract task title (simplified)
        title = message.replace("add", "").replace("create", "").replace("remember", "").replace("need to", "").strip()
        if title:
            result = task_tools.add_task(user_id, title)
            return f"I've added the task '{result['title']}' to your list."
        else:
            return "What task would you like me to add?"

    elif any(word in message_lower for word in ["show", "list", "display", "what"]):
        if "completed" in message_lower:
            tasks = task_tools.list_tasks(user_id, "completed")
        elif "pending" in message_lower:
            tasks = task_tools.list_tasks(user_id, "pending")
        else:
            tasks = task_tools.list_tasks(user_id, "all")

        if tasks:
            task_list = "\n".join([f"- {task['title']}" for task in tasks])
            return f"Here are your tasks:\n{task_list}"
        else:
            return "You don't have any tasks."

    elif any(word in message_lower for word in ["complete", "done", "finish"]):
        # This would need to identify which task to complete
        # For now, return a helpful message
        return "Please specify which task you'd like to mark as complete."

    elif any(word in message_lower for word in ["delete", "remove"]):
        # This would need to identify which task to delete
        # For now, return a helpful message
        return "Please specify which task you'd like to delete."

    else:
        return f"I understand you said: '{message}'. You can ask me to add, list, complete, or delete tasks."