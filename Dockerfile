# Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./backend /app/backend

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
