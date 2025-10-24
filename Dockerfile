# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TODO_FILE=/data/todos.json
ENV LOG_LEVEL=INFO
ENV MAX_TODOS=10000
ENV MAX_TITLE_LENGTH=200
ENV MAX_DESCRIPTION_LENGTH=1000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r todouser && useradd -r -g todouser todouser

# Create data directory and set permissions
RUN mkdir -p /data /app/logs && \
    chown -R todouser:todouser /data /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY README.md .

# Create a health check script
RUN echo '#!/bin/bash\npython -c "import sys, os; sys.path.append(os.getcwd()); from main import health_check; print(health_check())" > /dev/null' > /app/healthcheck.sh && \
    chmod +x /app/healthcheck.sh

# Switch to non-root user
USER todouser

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /app/healthcheck.sh || exit 1

# Expose port for potential HTTP interface (future extension)
EXPOSE 8080

# Create volume for persistent data
VOLUME ["/data", "/app/logs"]

# Default command
CMD ["python", "main.py"]