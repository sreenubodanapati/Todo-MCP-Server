@echo off
echo Starting Todo MCP Server...
echo.
echo The server will start and wait for MCP client connections.
echo To stop the server, press Ctrl+C
echo.
cd /d "%~dp0"
C:\MCP\Todo-mcp-server\.venv\Scripts\python.exe main.py
pause