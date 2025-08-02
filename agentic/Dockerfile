FROM python:3.11-slim

WORKDIR /agentic

# Copy and install only agent dependencies
COPY requirements.txt /agentic/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy agentic code
COPY . /agentic

CMD ["python", "agent.py"]