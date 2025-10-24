# Todo MCP Server

A Model Context Protocol (MCP) server built with FastMCP that provides comprehensive todo list management functionality.

## Features

- ✅ Add, update, and delete todo items
- 🏷️ Priority levels (low, medium, high)
- 📊 Status tracking (pending, completed)
- 🔍 Filter todos by status and priority
- 📈 Todo statistics and analytics
- 💾 Persistent storage in JSON format
- 🕒 Automatic timestamps for creation, updates, and completion

## Installation

### Option 1: Using the provided setup
1. Clone or download this repository
2. Run the project (this will automatically set up a virtual environment):
   ```bash
   # On Windows
   start_server.bat
   
   # On Linux/Mac
   python main.py
   ```

### Option 2: Manual setup
1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   
   # Activate on Windows
   .venv\Scripts\activate
   
   # Activate on Linux/Mac
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # OR
   pip install fastmcp>=2.12.5
   ```

## Usage

### Running the Server

```bash
python main.py
```

The server will start and listen for MCP connections. It stores todos in a `todos.json` file in the current directory.

### Available Tools

#### `add_todo(title, description="", priority="medium")`
Add a new todo item.
- `title`: The title of the todo (required)
- `description`: Optional description
- `priority`: Priority level - "low", "medium", or "high" (default: "medium")

**Example:**
```
add_todo("Buy groceries", "Milk, bread, eggs", "high")
```

#### `list_todos(status="all", priority="all")`
List todo items with optional filtering.
- `status`: Filter by status - "all", "pending", or "completed" (default: "all")
- `priority`: Filter by priority - "all", "low", "medium", or "high" (default: "all")

**Examples:**
```
list_todos()                          # List all todos
list_todos(status="pending")          # List only pending todos
list_todos(priority="high")           # List only high priority todos
list_todos(status="pending", priority="high")  # List pending high priority todos
```

#### `get_todo(todo_id)`
Get detailed information about a specific todo item.
- `todo_id`: The ID of the todo item

**Example:**
```
get_todo(1)
```

#### `update_todo(todo_id, title=None, description=None, priority=None)`
Update an existing todo item.
- `todo_id`: The ID of the todo to update (required)
- `title`: New title (optional)
- `description`: New description (optional)
- `priority`: New priority level (optional)

**Example:**
```
update_todo(1, title="Buy groceries and cook dinner", priority="high")
```

#### `complete_todo(todo_id)`
Mark a todo item as completed.
- `todo_id`: The ID of the todo to complete

**Example:**
```
complete_todo(1)
```

#### `reopen_todo(todo_id)`
Reopen a completed todo item.
- `todo_id`: The ID of the todo to reopen

**Example:**
```
reopen_todo(1)
```

#### `delete_todo(todo_id)`
Delete a todo item permanently.
- `todo_id`: The ID of the todo to delete

**Example:**
```
delete_todo(1)
```

#### `clear_completed_todos()`
Delete all completed todo items.

**Example:**
```
clear_completed_todos()
```

#### `get_todo_stats()`
Get statistics about your todos including total count, completion rate, and priority breakdown.

**Example:**
```
get_todo_stats()
```

## Data Structure

Each todo item contains:
- `id`: Unique identifier
- `title`: Todo title
- `description`: Optional description
- `priority`: Priority level (low/medium/high)
- `status`: Current status (pending/completed)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `completed_at`: Completion timestamp (null if not completed)

## Data Storage

Todos are stored in a `todos.json` file in the server's working directory. The file is automatically created on first use and updated whenever todos are modified.

## MCP Configuration

To use this server with an MCP client, add it to your client's configuration. For example, with Claude Desktop:

```json
{
  "mcpServers": {
    "todo": {
      "command": "python",
      "args": ["path/to/main.py"],
      "cwd": "path/to/todo-mcp-server"
    }
  }
}
```

## Testing

To test the functionality without running the MCP server:

```bash
python test_todo.py
```

This will demonstrate all the todo management features with sample data.

## Project Structure

```
Todo-mcp-server/
├── main.py                    # Main MCP server implementation
├── test_todo.py              # Test script demonstrating functionality
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Project configuration
├── README.md                # This documentation
├── DEPLOYMENT.md            # Comprehensive deployment guide
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose setup
├── .dockerignore           # Docker build exclusions
├── .env.example            # Environment configuration template
├── .env.development        # Development environment settings
├── .env.production         # Production environment settings
├── start_server.bat        # Windows startup script (local)
├── deploy-docker.bat       # Windows Docker deployment script
├── deploy-docker.sh        # Unix Docker deployment script
├── stop-docker.bat         # Windows Docker stop script
├── todos.json              # Data storage (created automatically)
├── todo_server.log         # Application logs (created automatically)
└── configs/                # Client configuration examples
    ├── claude-desktop.json           # Claude Desktop (local Python)
    ├── claude-desktop-docker.json    # Claude Desktop (Docker)
    ├── claude-desktop-unix.json      # Claude Desktop (Unix systems)
    ├── vscode-mcp.json              # VS Code MCP extension
    ├── vscode-mcp-docker.json       # VS Code MCP extension (Docker)
    └── nodejs-client-example.js     # Node.js client example
```

## Production Deployment

### Docker Deployment (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   # Windows
   deploy-docker.bat
   
   # Linux/Mac
   chmod +x deploy-docker.sh
   ./deploy-docker.sh
   ```

2. **Manual Docker commands:**
   ```bash
   # Build the image
   docker-compose build
   
   # Start the server
   docker-compose up -d
   
   # View logs
   docker-compose logs -f todo-mcp-server
   
   # Stop the server
   docker-compose down
   ```

3. **Environment Configuration:**
   - Copy `.env.example` to `.env` and modify as needed
   - Use `.env.production` for production settings
   - Use `.env.development` for development settings

### Environment Variables

- `TODO_FILE`: Path to the todos data file (default: `todos.json`)
- `LOG_LEVEL`: Logging level - DEBUG, INFO, WARNING, ERROR (default: `INFO`)
- `MAX_TODOS`: Maximum number of todos allowed (default: `1000`)
- `MAX_TITLE_LENGTH`: Maximum length for todo titles (default: `200`)
- `MAX_DESCRIPTION_LENGTH`: Maximum length for descriptions (default: `1000`)

## Client Integration

### Claude Desktop

1. **Local Python Installation:**
   Add to your Claude Desktop configuration file:
   ```json
   {
     "mcpServers": {
       "todo-server": {
         "command": "python",
         "args": ["main.py"],
         "cwd": "C:\\path\\to\\Todo-mcp-server",
         "env": {
           "TODO_FILE": "todos.json",
           "LOG_LEVEL": "INFO"
         }
       }
     }
   }
   ```

2. **Docker Installation:**
   ```json
   {
     "mcpServers": {
       "todo-server": {
         "command": "docker",
         "args": [
           "run", "--rm", "-i",
           "-v", "todo_data:/data",
           "-v", "todo_logs:/app/logs",
           "todo-mcp-server"
         ]
       }
     }
   }
   ```

3. **Configuration File Locations:**
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

### VS Code MCP Extension

1. **Install the MCP extension** for VS Code
2. **Add server configuration** to your workspace settings or user settings:
   ```json
   {
     "mcp.servers": [
       {
         "name": "todo-server",
         "command": {
           "type": "stdio",
           "program": "python",
           "args": ["main.py"],
           "cwd": "${workspaceFolder}/Todo-mcp-server"
         }
       }
     ]
   }
   ```

### Other MCP Clients

#### Cline (VS Code Extension)
Add to your Cline settings:
```json
{
  "cline.mcp.servers": {
    "todo-server": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/Todo-mcp-server"
    }
  }
}
```

#### Continue (VS Code Extension)
Add to your Continue configuration:
```json
{
  "mcpServers": {
    "todo-server": {
      "transport": {
        "type": "stdio"
      },
      "command": ["python", "main.py"],
      "cwd": "/path/to/Todo-mcp-server"
    }
  }
}
```

#### Node.js Applications
See `configs/nodejs-client-example.js` for a complete example of integrating with Node.js applications.

## Health Monitoring

The server includes a built-in health check system:

1. **Health Check Tool:** Use the `health_check()` tool to verify server status
2. **Docker Health Checks:** Automatic health monitoring in Docker deployments
3. **Logging:** Comprehensive logging to file and console
4. **Error Handling:** Graceful error handling with detailed error messages

## Security Features

- **Input validation** and sanitization
- **File system security** with proper permissions
- **Non-root Docker user** for container security
- **Resource limits** to prevent abuse
- **Backup and recovery** for data integrity

## Monitoring and Logs

- **Application logs:** Available in `todo_server.log`
- **Docker logs:** `docker-compose logs -f todo-mcp-server`
- **Health status:** Regular health checks and status reporting
- **Performance metrics:** Built-in statistics and monitoring

## Troubleshooting

### Common Issues

1. **Permission Errors:**
   - Ensure proper file permissions for the data directory
   - For Docker: volumes are properly mounted

2. **Connection Issues:**
   - Verify the server is running: `docker-compose ps`
   - Check logs: `docker-compose logs todo-mcp-server`

3. **Data Corruption:**
   - The server automatically creates backups before saving
   - Use the health check tool to verify data integrity

4. **Resource Limits:**
   - Adjust environment variables for your use case
   - Monitor resource usage with Docker stats

### Getting Help

1. Check the application logs
2. Run the health check tool
3. Verify your client configuration
4. Ensure Docker/Python dependencies are installed

## Development

### Local Development Setup
```bash
# Clone and setup
git clone <repository>
cd Todo-mcp-server

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env

# Run in development mode
python main.py
```

### Testing
```bash
# Run functionality tests
python test_todo.py

# Test Docker build
docker-compose build

# Test health check
docker-compose exec todo-mcp-server python -c "from main import health_check; print(health_check())"
```

## Architecture

The server is built with production-ready features:

- **FastMCP Framework:** Modern Python MCP server framework
- **Async Operations:** Non-blocking I/O for better performance
- **Data Persistence:** JSON-based storage with backup/recovery
- **Containerization:** Docker support for easy deployment
- **Monitoring:** Health checks, logging, and error tracking
- **Security:** Input validation, resource limits, secure defaults

## Requirements

- **Python 3.12+** (for local installation)
- **Docker & Docker Compose** (for containerized deployment)
- **FastMCP 2.12.5+**

## License

This project is open source and available under the MIT License.