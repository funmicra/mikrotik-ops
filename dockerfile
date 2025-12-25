# Use official Python image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port if needed (not mandatory for CLI)
# EXPOSE 22

# Default command
CMD ["python", "main.py"]
