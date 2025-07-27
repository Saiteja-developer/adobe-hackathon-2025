FROM python:3.10-slim

WORKDIR /app
COPY . .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uncomment if your summarizer uses nltk.tokenize
# RUN python3 -m nltk.downloader punkt

CMD ["python3", "main.py"]
