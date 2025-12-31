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

### 1. Clone the Repository

```bash
git clone https://github.com/yehudafreiman/contact_manager_2.git
cd contact_manager_2
```

### 2. Build and Push Docker Image

```bash
cd app
docker build -t yehudafreiman/contacts-api:v1 .
docker login
docker push yehudafreiman/contacts-api:v1
cd ..
```

### 3. Start Kubernetes Cluster

```bash
minikube start
```

### 4. Deploy All Resources

```bash
kubectl apply -f k8s/mongodb-pod.yaml
kubectl apply -f k8s/mongodb-service.yaml
kubectl apply -f k8s/api-pod.yaml
kubectl apply -f k8s/api-service.yaml
```

### 5. Wait for Pods to be Ready

Wait 30-60 seconds, then verify both pods show "Running" status:

```bash
kubectl get pods
```

Expected output:
```
NAME      READY   STATUS    RESTARTS   AGE
api       1/1     Running   0          30s
mongodb   1/1     Running   0          45s
```

### 6. Get the API URL

```bash
minikube service api-service --url
```

## Testing Instructions

Replace `<API_URL>` with the URL from the previous command.

### Test 1: GET - Get all contacts (should return empty list initially)

```bash
curl <API_URL>/contacts
```

### Test 2: POST - Create a new contact

```bash
curl -X POST <API_URL>/contacts \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "phone_number": "+1-555-0101"}'
```

### Test 3: GET - Get all contacts again (should show the created contact)

```bash
curl <API_URL>/contacts
```

### Test 4: PUT - Update the contact

```bash
curl -X PUT <API_URL>/contacts/<CONTACT_ID> \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1-555-9999"}'
```

### Test 5: DELETE - Delete the contact

```bash
curl -X DELETE <API_URL>/contacts/<CONTACT_ID>
```

### Test 6: Verify Error Handling

Update a non-existent contact (should return 404):
```bash
curl -X PUT <API_URL>/contacts/000000000000000000000000 \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1-555-0000"}'
```

Delete a non-existent contact (should return 404):
```bash
curl -X DELETE <API_URL>/contacts/000000000000000000000000
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
