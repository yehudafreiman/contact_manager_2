# Contact Manager API

A REST API for managing contacts, built with FastAPI and MongoDB, orchestrated with Kubernetes.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/contacts` | Get all contacts |
| POST | `/contacts` | Create a new contact |
| PUT | `/contacts/{id}` | Update an existing contact |
| DELETE | `/contacts/{id}` | Delete a contact |

## Prerequisites

- Docker
- minikube (or other local Kubernetes)
- kubectl

## Setup Instructions

### 1. Start minikube

```bash
minikube start
```

### 2. Build Docker Image

```bash
cd app
docker build -t yehudafreiman/contacts-api:v1 .
```

### 3. Push to Docker Hub

```bash
docker login
docker push yehudafreiman/contacts-api:v1
```

### 4. Deploy MongoDB

```bash
kubectl apply -f k8s/mongodb-pod.yaml
kubectl apply -f k8s/mongodb-service.yaml
```

### 5. Deploy the API

```bash
kubectl apply -f k8s/api-pod.yaml
kubectl apply -f k8s/api-service.yaml
```

### 6. Verify Pods are Running

```bash
kubectl get pods
```

Wait until both Pods show `Running` status.

### 7. Get the API URL

```bash
minikube service api-service --url
```

## Testing Instructions

Replace `<API_URL>` with the URL from the previous command.

### GET - Get all contacts

```bash
curl <API_URL>/contacts
```

### POST - Create a new contact

```bash
curl -X POST <API_URL>/contacts \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "phone_number": "+1-555-0101"}'
```

### PUT - Update a contact

```bash
curl -X PUT <API_URL>/contacts/<CONTACT_ID> \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1-555-9999"}'
```

### DELETE - Delete a contact

```bash
curl -X DELETE <API_URL>/contacts/<CONTACT_ID>
```

## Project Structure

```
week11_k8s_contacts/
├── README.md
├── .gitignore
├── app/
│   ├── Dockerfile
│   ├── main.py
│   ├── data_interactor.py
│   ├── models.py
│   └── requirements.txt
└── k8s/
    ├── mongodb-pod.yaml
    ├── mongodb-service.yaml
    ├── api-pod.yaml
    └── api-service.yaml
```

## Cleanup

```bash
kubectl delete -f k8s/
minikube stop
```
