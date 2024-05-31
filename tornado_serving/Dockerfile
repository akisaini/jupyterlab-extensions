FROM python:3.10-slim

# Create dir in container
WORKDIR /app

# Copy content in container dir
COPY . /app

RUN pip install tornado

EXPOSE 8889

CMD ["python", "server.py"]
