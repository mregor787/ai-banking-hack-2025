FROM python:3.10

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY main_service /app
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["/wait-for-it.sh", "mq", "5672", "--", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
