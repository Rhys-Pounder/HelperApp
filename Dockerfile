# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /home/appuser/app

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /home/appuser

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Flask for web interface
RUN pip install --no-cache-dir flask

# Copy application files
COPY *.py ./
COPY templates/ ./templates/

# Create data directory for database
RUN mkdir -p data && chown -R appuser:appuser data

# Switch to non-root user
USER appuser

# Expose port 8080
EXPOSE 8080

# Run the web application
CMD ["python", "web_app.py"]