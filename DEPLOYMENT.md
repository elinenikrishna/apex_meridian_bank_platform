# Deployment

## Local API and Frontend

```bash
PYTHONPATH=src:. uvicorn apps.backend.app.main:app --host 0.0.0.0 --port 8080
python -m http.server 8088 --directory frontend
```

## Docker Compose

```bash
docker compose up --build backend frontend postgres kafka zookeeper minio
```

Services:

- `backend`: FastAPI platform APIs
- `frontend`: Nginx-hosted dashboard app
- `postgres`: warehouse and governance metadata
- `mysql`: operational customer/account source simulation
- `mongo`: digital session source simulation
- `cassandra`: payment event source simulation
- `kafka` and `zookeeper`: streaming event mesh
- `minio`: S3-compatible lakehouse object storage
- `airflow`: optional orchestration profile

## Kubernetes

```bash
docker build -f apps/backend/Dockerfile -t apex-meridian-api:local .
docker build -f frontend/Dockerfile -t apex-meridian-frontend:local .
kubectl apply -k infrastructure/kubernetes/overlays/local
```

## CI/CD

GitHub Actions and Jenkins both validate Python tests, generate smoke data, and build service images. Production deployments should add image signing, vulnerability scanning, environment-specific secrets, and approval gates.

