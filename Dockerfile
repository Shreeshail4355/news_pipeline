FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy main.py and config.yaml (root files)
COPY main.py .
COPY config.yml .

# Copy the app folder contents
COPY app/ ./app/

# Run main.py (at root of /app)
CMD ["python", "main.py"]
