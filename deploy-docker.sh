#!/bin/bash

echo "Building and starting Todo MCP Server with Docker..."
echo

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker."
    exit 1
fi

# Build the Docker image
echo "Building Docker image..."
if ! docker-compose build; then
    echo "Error: Failed to build Docker image"
    exit 1
fi

# Start the services
echo "Starting Todo MCP Server..."
if ! docker-compose up -d; then
    echo "Error: Failed to start services"
    exit 1
fi

echo
echo "Todo MCP Server is now running!"
echo
echo "To view logs: docker-compose logs -f todo-mcp-server"
echo "To stop: docker-compose down"
echo "To restart: docker-compose restart"
echo
echo "Container health status:"
docker-compose ps