FROM python:3.11-slim

WORKDIR /app

# copier et installer dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copier code
COPY app/ app
COPY .env .env
COPY fake_device_publisher.py fake_device_publisher.py

EXPOSE 8000

CMD ["uvicorn", "app.main:socket_app", "--host", "0.0.0.0", "--port", "8000"]
