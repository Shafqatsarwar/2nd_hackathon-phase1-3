from typing import List, Dict, Any
from sqlmodel import Session, select
from ..models import Task, TaskCreate, TaskUpdate


class MCPTaskTools:
    """
    MCP Tools for task operations that can be called by AI agents
    """

    def __init__(self, session_getter):
        self.get_session = session_getter

    def add_task(self, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """
        MCP Tool: Create a new task
        """
        with self.get_session() as session:
            task_data = TaskCreate(title=title, description=description or "")
            db_task = Task.model_validate(task_data, update={"user_id": user_id})
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return {
                "task_id": db_task.id,
                "status": "created",
                "title": db_task.title,
                "description": db_task.description,
                "completed": db_task.completed
            }

    def list_tasks(self, user_id: str, status: str = "all") -> List[Dict[str, Any]]:
        """
        MCP Tool: Retrieve tasks from the list
        """
        with self.get_session() as session:
            query = select(Task).where(Task.user_id == user_id)

            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)

            tasks = session.exec(query).all()

            return [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
                for task in tasks
            ]

    def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: Mark a task as complete
        """
        with self.get_session() as session:
            db_task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()

            if not db_task:
                return {
                    "error": f"Task {task_id} not found for user {user_id}",
                    "status": "error"
                }

            db_task.completed = True
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return {
                "task_id": db_task.id,
                "status": "completed",
                "title": db_task.title
            }

    def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: Remove a task from the list
        """
        with self.get_session() as session:
            db_task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()

            if not db_task:
                return {
                    "error": f"Task {task_id} not found for user {user_id}",
                    "status": "error"
                }

            session.delete(db_task)
            session.commit()

            return {
                "task_id": task_id,
                "status": "deleted",
                "title": db_task.title
            }

    def update_task(self, user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """
        MCP Tool: Modify task title or description
        """
        with self.get_session() as session:
            db_task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()

            if not db_task:
                return {
                    "error": f"Task {task_id} not found for user {user_id}",
                    "status": "error"
                }

            if title is not None:
                db_task.title = title
            if description is not None:
                db_task.description = description

            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return {
                "task_id": db_task.id,
                "status": "updated",
                "title": db_task.title
            }