FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src:/app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/backend apps/backend
COPY src src
COPY data/sample data/sample
COPY data/reference data/reference

EXPOSE 8080
CMD ["uvicorn", "apps.backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]

