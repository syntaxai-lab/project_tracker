FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies first (for caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . /app

# Expose Flask port
EXPOSE 5050

# Environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5050

# Run the Flask app
CMD ["flask", "run"]