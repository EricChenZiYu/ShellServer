# Use Python 3.11 alpine image as base
FROM python:3.11.12-alpine

# Set working directory
WORKDIR /app

# Install system dependencies using Alpine package manager
RUN apk add --no-cache \
    curl \
    ca-certificates \
    bash \
    shadow

# Copy uv configuration files first
COPY pyproject.toml uv.lock* ./

# Install uv and dependencies in one step with correct path
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    export PATH="/root/.local/bin:$PATH" && \
    /root/.local/bin/uv sync --frozen --no-cache && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv

# Set environment variables for uv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy the rest of the application
COPY . .

# Create a non-root user for security (Alpine style) and fix permissions
RUN adduser -D -s /bin/bash app \
    && chown -R app:app /app \
    && mkdir -p /home/app/.local/bin \
    && cp /root/.local/bin/uv /home/app/.local/bin/ \
    && cp /root/.local/bin/uvx /home/app/.local/bin/ \
    && chown -R app:app /home/app/.local

USER app

# Add uv to PATH for the app user
ENV PATH="/home/app/.local/bin:$PATH"

# Expose port (if needed for debugging or other purposes)
EXPOSE 8000

# Set the default command to run the MCP server using uv in the project directory
CMD ["uv", "run", "--project", "/app", "python", "main.py"] 