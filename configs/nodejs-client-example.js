import mcp from '@modelcontextprotocol/sdk/client/stdio.js';
import { spawn } from 'child_process';

// Configuration for Todo MCP Server
const todoServerConfig = {
  name: 'todo-server',
  command: 'python',
  args: ['main.py'],
  cwd: '/path/to/Todo-mcp-server',
  env: {
    TODO_FILE: 'todos.json',
    LOG_LEVEL: 'INFO',
    MAX_TODOS: '1000'
  }
};

// Initialize MCP client
const client = new mcp.Client({
  name: 'todo-client',
  version: '1.0.0'
});

// Connect to the server
async function connectToTodoServer() {
  try {
    const serverProcess = spawn(todoServerConfig.command, todoServerConfig.args, {
      cwd: todoServerConfig.cwd,
      env: { ...process.env, ...todoServerConfig.env },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    await client.connect({
      reader: serverProcess.stdout,
      writer: serverProcess.stdin
    });

    console.log('Connected to Todo MCP Server');
    
    // List available tools
    const tools = await client.listTools();
    console.log('Available tools:', tools.tools.map(t => t.name));

    return client;
  } catch (error) {
    console.error('Failed to connect to Todo MCP Server:', error);
    throw error;
  }
}

// Example usage
async function main() {
  const client = await connectToTodoServer();
  
  // Add a todo
  const result = await client.callTool({
    name: 'add_todo',
    arguments: {
      title: 'Test todo from Node.js client',
      description: 'This is a test todo created from a Node.js MCP client',
      priority: 'high'
    }
  });
  
  console.log('Todo added:', result);
  
  // List todos
  const todos = await client.callTool({
    name: 'list_todos',
    arguments: {}
  });
  
  console.log('Current todos:', todos);
}

// Run if this is the main module
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export { connectToTodoServer, todoServerConfig };