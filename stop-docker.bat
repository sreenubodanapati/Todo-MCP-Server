@echo off
echo Stopping Todo MCP Server Docker containers...
echo.

docker-compose down

if %ERRORLEVEL% neq 0 (
    echo Error: Failed to stop containers
    pause
    exit /b 1
)

echo.
echo Todo MCP Server stopped successfully!
echo.
echo To remove data volumes as well, run: docker-compose down -v
echo To remove images as well, run: docker-compose down --rmi all

pause