FROM python:3.11-slim

WORKDIR /app

COPY bip39_thing.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "bip39_thing.py"]
