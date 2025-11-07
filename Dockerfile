FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./


ENV FLASK_RUN_RELOAD=true

CMD ["flask", "--app", "server", "run", "-h",  "0.0.0.0", "-p", "8080"]