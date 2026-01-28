
FROM python:3.14-slim
WORKDIR /app
RUN useradd -m userapp
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/logs && chown -R userapp:userapp /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
USER userapp
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
