FROM python:3.11-slim

# Install system dependencies for tkinter and X11
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    xauth \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Create data directory
RUN mkdir -p /root/.aws_log_helper

# Set environment variables for GUI
ENV DISPLAY=:0
ENV PYTHONPATH=/app

# Create a non-root user (optional, but recommended)
RUN useradd -m -s /bin/bash appuser && \
    mkdir -p /home/appuser/.aws_log_helper && \
    chown -R appuser:appuser /home/appuser

# Switch to non-root user
USER appuser
WORKDIR /home/appuser/app
COPY --chown=appuser:appuser . .

# Expose the application
CMD ["python3", "main.py"]