@echo off
echo Building and starting Todo MCP Server with Docker...
echo.

REM Check if Docker is running
docker version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

REM Build the Docker image
echo Building Docker image...
docker-compose build

if %ERRORLEVEL% neq 0 (
    echo Error: Failed to build Docker image
    pause
    exit /b 1
)

REM Start the services
echo Starting Todo MCP Server...
docker-compose up -d

if %ERRORLEVEL% neq 0 (
    echo Error: Failed to start services
    pause
    exit /b 1
)

echo.
echo Todo MCP Server is now running!
echo.
echo To view logs: docker-compose logs -f todo-mcp-server
echo To stop: docker-compose down
echo To restart: docker-compose restart
echo.
echo Container health status:
docker-compose ps

pause