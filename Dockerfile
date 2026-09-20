# Use lightweight official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependencies list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Create directory for persistent SQLite database
RUN mkdir -p /app/data

# Declare volume for data persistence across container deployments
VOLUME ["/app/data"]

# Expose port 5000 for Flask/Gunicorn
EXPOSE 5000

# Run production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
