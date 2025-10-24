# Todo MCP Server - Deployment Guide

## Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Prerequisites:**
   - Docker Desktop installed and running
   - Git (to clone the repository)

2. **Deploy:**
   ```bash
   # Windows
   deploy-docker.bat
   
   # Linux/Mac
   chmod +x deploy-docker.sh && ./deploy-docker.sh
   ```

3. **Verify deployment:**
   ```bash
   docker-compose ps
   docker-compose logs todo-mcp-server
   ```

### Option 2: Local Python Installation

1. **Prerequisites:**
   - Python 3.12+
   - pip

2. **Setup:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Run:**
   ```bash
   python main.py
   ```

## Client Configuration

### Claude Desktop

1. **Find your configuration file:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add the server configuration:**
   - For local Python: Use `configs/claude-desktop.json`
   - For Docker: Use `configs/claude-desktop-docker.json`
   - Update paths to match your installation

3. **Restart Claude Desktop**

### VS Code with MCP Extension

1. **Install MCP extension** from VS Code marketplace
2. **Copy configuration** from `configs/vscode-mcp.json`
3. **Add to your VS Code settings** (User or Workspace)
4. **Restart VS Code**

### Other Clients

- **Cline:** Follow VS Code MCP setup
- **Continue:** Use provided configuration examples
- **Custom clients:** See `configs/nodejs-client-example.js`

## Production Checklist

### Security
- [ ] Use non-root user (automatic in Docker)
- [ ] Set appropriate resource limits
- [ ] Configure firewall rules if exposed
- [ ] Regular security updates
- [ ] Monitor access logs

### Performance
- [ ] Set appropriate `MAX_TODOS` limit
- [ ] Configure log rotation
- [ ] Monitor disk usage
- [ ] Set up monitoring/alerting

### Backup & Recovery
- [ ] Regular data backups (automatic backup on save)
- [ ] Test recovery procedures
- [ ] Document backup locations
- [ ] Set up monitoring for data integrity

### Monitoring
- [ ] Set up log aggregation
- [ ] Configure health check monitoring
- [ ] Set up alerts for failures
- [ ] Monitor resource usage

## Scaling Considerations

### Single Instance
- Good for: Personal use, small teams
- Limits: Single point of failure
- Data: Local file storage

### Multiple Instances
- Good for: Teams, high availability
- Setup: Load balancer + shared storage
- Data: Network storage or database

### Enterprise Deployment
- Consider: Kubernetes deployment
- Features: Auto-scaling, rolling updates
- Storage: Persistent volumes, database backend

## Troubleshooting

### Common Issues

1. **Server won't start:**
   ```bash
   # Check logs
   docker-compose logs todo-mcp-server
   
   # Check configuration
   docker-compose config
   
   # Verify permissions
   ls -la todos.json
   ```

2. **Client connection fails:**
   - Verify server is running
   - Check client configuration paths
   - Ensure proper permissions
   - Review client logs

3. **Data corruption:**
   ```bash
   # Check health
   docker-compose exec todo-mcp-server python -c "from main import health_check; print(health_check())"
   
   # Restore from backup
   cp todos.json.bak todos.json
   ```

4. **Performance issues:**
   - Check resource usage: `docker stats`
   - Review logs for errors
   - Consider increasing limits
   - Monitor disk space

### Log Locations

- **Docker:** `docker-compose logs todo-mcp-server`
- **Local:** `todo_server.log`
- **Client logs:** Varies by client application

### Support Resources

1. Check application health: Use `health_check` tool
2. Review documentation: README.md
3. Check configuration examples: `configs/` directory
4. Test with: `python test_todo.py`

## Advanced Configuration

### Custom Storage Backend
```python
# Override in main.py for database storage
# Example: SQLite, PostgreSQL, MongoDB
```

### Custom Authentication
```python
# Add authentication middleware
# Example: JWT tokens, API keys
```

### HTTP API (Future Extension)
```python
# Add FastAPI endpoints for REST access
# Enable in docker-compose.yml
```

### Monitoring Integration
```yaml
# Add to docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
  grafana:
    image: grafana/grafana
```

## Migration Guide

### From Development to Production

1. **Update environment variables:**
   ```bash
   cp .env.development .env.production
   # Edit .env.production with production values
   ```

2. **Use production Docker image:**
   ```bash
   docker-composer -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

3. **Configure monitoring and backups**

4. **Update client configurations**

### Data Migration

```bash
# Export data
docker-compose exec todo-mcp-server cat /data/todos.json > backup.json

# Import to new instance
docker cp backup.json todo-mcp-server:/data/todos.json
docker-compose restart todo-mcp-server
```

## Performance Tuning

### Resource Limits
```yaml
# In docker-compose.yml
services:
  todo-mcp-server:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

### Optimization Settings
```bash
# Environment variables
MAX_TODOS=10000
LOG_LEVEL=WARNING  # Reduce log verbosity
```

### Monitoring Commands
```bash
# Resource usage
docker stats todo-mcp-server

# Disk usage
docker-compose exec todo-mcp-server df -h

# Memory usage
docker-compose exec todo-mcp-server free -h
```