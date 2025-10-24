#!/usr/bin/env python3
"""
Todo MCP Server using FastMCP

A production-ready Model Context Protocol server that provides todo list management functionality.
"""

import json
import os
import logging
import sys
from datetime import datetime
from typing import List, Dict, Optional, Any, TypedDict, cast
from pathlib import Path

from fastmcp import FastMCP

# Configuration
TODO_FILE = Path(os.getenv("TODO_FILE", "todos.json"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_TODOS = int(os.getenv("MAX_TODOS", "1000"))
MAX_TITLE_LENGTH = int(os.getenv("MAX_TITLE_LENGTH", "200"))
MAX_DESCRIPTION_LENGTH = int(os.getenv("MAX_DESCRIPTION_LENGTH", "1000"))

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('todo_server.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Todo Server")

# Todo data structure with proper typing
class TodoDict(TypedDict):
    id: int
    title: str
    description: str
    priority: str
    status: str
    created_at: str
    updated_at: str
    completed_at: Optional[str]

todos: List[TodoDict] = []

def validate_input(value: str, max_length: int, field_name: str) -> str:
    """Validate and sanitize input"""
    value = value.strip()
    if len(value) > max_length:
        raise ValueError(f"{field_name} exceeds maximum length of {max_length} characters")
    
    return value

def load_todos():
    """Load todos from file with error handling"""
    global todos
    try:
        if TODO_FILE.exists():
            with open(TODO_FILE, 'r', encoding='utf-8') as f:
                data: Any = json.load(f)
                if isinstance(data, list):
                    # Validate and convert loaded data to TodoDict format
                    loaded_todos: List[TodoDict] = []
                    for item in data:  # type: ignore
                        if isinstance(item, dict) and 'id' in item and 'title' in item:
                            # Cast to TodoDict since we've validated the required fields
                            todo_item: TodoDict = cast(TodoDict, item)
                            loaded_todos.append(todo_item)
                        else:
                            logger.warning(f"Skipping invalid todo item: {item}")
                    todos = loaded_todos
                    logger.info(f"Loaded {len(todos)} todos from {TODO_FILE}")
                else:
                    logger.warning("Invalid data format in todos file, starting fresh")
                    todos = []
        else:
            todos = []
            logger.info("No existing todos file, starting fresh")
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading todos: {e}")
        todos = []

def save_todos():
    """Save todos to file with error handling"""
    try:
        # Create backup if file exists
        if TODO_FILE.exists():
            backup_file = TODO_FILE.with_suffix('.bak')
            TODO_FILE.rename(backup_file)
        
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(todos, f, indent=2, ensure_ascii=False)
        logger.debug(f"Saved {len(todos)} todos to {TODO_FILE}")
        
        # Remove backup on successful save
        backup_file = TODO_FILE.with_suffix('.bak')
        if backup_file.exists():
            backup_file.unlink()
            
    except IOError as e:
        logger.error(f"Failed to save todos: {e}")
        # Restore backup if save failed
        backup_file = TODO_FILE.with_suffix('.bak')
        if backup_file.exists():
            backup_file.rename(TODO_FILE)
        raise Exception(f"Failed to save todos: {e}")

def get_next_id() -> int:
    """Get the next available todo ID"""
    if not todos:
        return 1
    return max([todo.get('id', 0) for todo in todos], default=0) + 1

def check_max_todos():
    """Check if we've reached the maximum number of todos"""
    if len(todos) >= MAX_TODOS:
        raise ValueError(f"Maximum number of todos ({MAX_TODOS}) reached")

# Load todos on startup
load_todos()

@mcp.tool()
def add_todo(title: str, description: str = "", priority: str = "medium") -> str:
    """
    Add a new todo item.
    
    Args:
        title: The title of the todo item
        description: Optional description of the todo item
        priority: Priority level (low, medium, high)
    
    Returns:
        Success message with the todo ID
    """
    try:
        check_max_todos()
        
        # Validate and sanitize inputs
        title = validate_input(title, MAX_TITLE_LENGTH, "Title")
        if not title:
            raise ValueError("Title cannot be empty")
        
        description = validate_input(description, MAX_DESCRIPTION_LENGTH, "Description")
        
        if priority not in ["low", "medium", "high"]:
            logger.warning(f"Invalid priority '{priority}', defaulting to 'medium'")
            priority = "medium"
        
        todo: TodoDict = {
            "id": get_next_id(),
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        todos.append(todo)
        save_todos()
        
        logger.info(f"Added todo with ID {todo['id']}: {title}")
        return f"Todo added successfully with ID: {todo['id']}"
        
    except Exception as e:
        logger.error(f"Error adding todo: {e}")
        raise

@mcp.tool()
def list_todos(status: str = "all", priority: str = "all") -> str:
    """
    List todo items with optional filtering.
    
    Args:
        status: Filter by status (all, pending, completed)
        priority: Filter by priority (all, low, medium, high)
    
    Returns:
        Formatted list of todos
    """
    filtered_todos = todos.copy()
    
    # Filter by status
    if status != "all":
        filtered_todos = [t for t in filtered_todos if t["status"] == status]
    
    # Filter by priority
    if priority != "all":
        filtered_todos = [t for t in filtered_todos if t["priority"] == priority]
    
    if not filtered_todos:
        return "No todos found matching the criteria."
    
    # Sort by priority (high -> medium -> low) and then by creation date
    priority_order = {"high": 3, "medium": 2, "low": 1}
    filtered_todos.sort(key=lambda x: (priority_order.get(x["priority"], 2), x["created_at"]))
    
    result = f"Found {len(filtered_todos)} todo(s):\n\n"
    
    for todo in filtered_todos:
        status_icon = "✅" if todo["status"] == "completed" else "⏳"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(todo["priority"], "🟡")
        
        result += f"{status_icon} {priority_icon} [{todo['id']}] {todo['title']}\n"
        if todo["description"]:
            result += f"   Description: {todo['description']}\n"
        result += f"   Status: {todo['status']} | Priority: {todo['priority']}\n"
        result += f"   Created: {todo['created_at'][:19].replace('T', ' ')}\n"
        if todo["completed_at"]:
            result += f"   Completed: {todo['completed_at'][:19].replace('T', ' ')}\n"
        result += "\n"
    
    return result

@mcp.tool()
def get_todo(todo_id: int) -> str:
    """
    Get details of a specific todo item.
    
    Args:
        todo_id: The ID of the todo item
    
    Returns:
        Detailed information about the todo item
    """
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        return f"Todo with ID {todo_id} not found."
    
    status_icon = "✅" if todo["status"] == "completed" else "⏳"
    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(todo["priority"], "🟡")
    
    result = f"{status_icon} {priority_icon} Todo #{todo['id']}: {todo['title']}\n\n"
    
    if todo["description"]:
        result += f"Description: {todo['description']}\n"
    
    result += f"Status: {todo['status']}\n"
    result += f"Priority: {todo['priority']}\n"
    result += f"Created: {todo['created_at'][:19].replace('T', ' ')}\n"
    result += f"Updated: {todo['updated_at'][:19].replace('T', ' ')}\n"
    
    if todo["completed_at"]:
        result += f"Completed: {todo['completed_at'][:19].replace('T', ' ')}\n"
    
    return result

@mcp.tool()
def update_todo(todo_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None) -> str:
    """
    Update an existing todo item.
    
    Args:
        todo_id: The ID of the todo item to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority level (low, medium, high) (optional)
    
    Returns:
        Success message
    """
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        return f"Todo with ID {todo_id} not found."
    
    updated = False
    
    if title is not None:
        if not title.strip():
            raise ValueError("Title cannot be empty")
        todo["title"] = title.strip()
        updated = True
    
    if description is not None:
        todo["description"] = description.strip()
        updated = True
    
    if priority is not None:
        if priority in ["low", "medium", "high"]:
            todo["priority"] = priority
            updated = True
        else:
            raise ValueError("Priority must be one of: low, medium, high")
    
    if updated:
        todo["updated_at"] = datetime.now().isoformat()
        save_todos()
        return f"Todo {todo_id} updated successfully."
    else:
        return "No changes were made."

@mcp.tool()
def complete_todo(todo_id: int) -> str:
    """
    Mark a todo item as completed.
    
    Args:
        todo_id: The ID of the todo item to complete
    
    Returns:
        Success message
    """
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        return f"Todo with ID {todo_id} not found."
    
    if todo["status"] == "completed":
        return f"Todo {todo_id} is already completed."
    
    todo["status"] = "completed"
    todo["completed_at"] = datetime.now().isoformat()
    todo["updated_at"] = datetime.now().isoformat()
    
    save_todos()
    
    return f"Todo {todo_id} marked as completed! ✅"

@mcp.tool()
def reopen_todo(todo_id: int) -> str:
    """
    Reopen a completed todo item.
    
    Args:
        todo_id: The ID of the todo item to reopen
    
    Returns:
        Success message
    """
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        return f"Todo with ID {todo_id} not found."
    
    if todo["status"] == "pending":
        return f"Todo {todo_id} is already pending."
    
    todo["status"] = "pending"
    todo["completed_at"] = None
    todo["updated_at"] = datetime.now().isoformat()
    
    save_todos()
    
    return f"Todo {todo_id} reopened successfully! ⏳"

@mcp.tool()
def delete_todo(todo_id: int) -> str:
    """
    Delete a todo item.
    
    Args:
        todo_id: The ID of the todo item to delete
    
    Returns:
        Success message
    """
    global todos
    
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        return f"Todo with ID {todo_id} not found."
    
    todos = [t for t in todos if t["id"] != todo_id]
    save_todos()
    
    return f"Todo {todo_id} deleted successfully."

@mcp.tool()
def clear_completed_todos() -> str:
    """
    Delete all completed todo items.
    
    Returns:
        Success message with count of deleted items
    """
    global todos
    
    completed_count = len([t for t in todos if t["status"] == "completed"])
    
    if completed_count == 0:
        return "No completed todos to clear."
    
    todos = [t for t in todos if t["status"] != "completed"]
    save_todos()
    
    return f"Cleared {completed_count} completed todo(s)."

@mcp.tool()
def get_todo_stats() -> str:
    """
    Get statistics about todos.
    
    Returns:
        Todo statistics summary
    """
    if not todos:
        return "No todos found."
    
    total = len(todos)
    pending = len([t for t in todos if t["status"] == "pending"])
    completed = len([t for t in todos if t["status"] == "completed"])
    
    high_priority = len([t for t in todos if t["priority"] == "high" and t["status"] == "pending"])
    medium_priority = len([t for t in todos if t["priority"] == "medium" and t["status"] == "pending"])
    low_priority = len([t for t in todos if t["priority"] == "low" and t["status"] == "pending"])
    
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    result = f"📊 Todo Statistics\n\n"
    result += f"Total todos: {total}\n"
    result += f"Pending: {pending} ⏳\n"
    result += f"Completed: {completed} ✅\n"
    result += f"Completion rate: {completion_rate:.1f}%\n\n"
    
    if pending > 0:
        result += f"Pending by priority:\n"
        result += f"  🔴 High: {high_priority}\n"
        result += f"  🟡 Medium: {medium_priority}\n"
        result += f"  🟢 Low: {low_priority}\n"
    
    return result

@mcp.tool()
def health_check() -> str:
    """
    Check the health status of the todo server.
    
    Returns:
        Health status information
    """
    try:
        # Check file system access
        TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Check data integrity
        todo_count = len(todos)
        
        # Check for data corruption
        valid_todos = 0
        for todo in todos:
            if 'id' in todo and 'title' in todo:
                valid_todos += 1
        
        status: Dict[str, Any] = {
            "status": "healthy",
            "version": "1.0.0",
            "total_todos": todo_count,
            "valid_todos": valid_todos,
            "data_file": str(TODO_FILE),
            "timestamp": datetime.now().isoformat()
        }
        
        if valid_todos != todo_count:
            status["status"] = "warning"
            status["issues"] = f"{todo_count - valid_todos} corrupted todos found"
        
        logger.info(f"Health check completed: {status['status']}")
        return json.dumps(status, indent=2)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        error_status = {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(error_status, indent=2)

def setup_server():
    """Initialize server configuration and data"""
    logger.info("Starting Todo MCP Server...")
    logger.info(f"Configuration - Max todos: {MAX_TODOS}, Log level: {LOG_LEVEL}")
    logger.info(f"Data file: {TODO_FILE}")
    
    # Ensure data directory exists
    TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing todos
    load_todos()
    
    logger.info(f"Server initialized with {len(todos)} existing todos")

if __name__ == "__main__":
    try:
        setup_server()
        logger.info("Starting MCP server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        sys.exit(1)
