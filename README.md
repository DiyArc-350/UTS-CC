# Minimarket CRUD API

A simple Flask REST API for managing minimarket inventory items with MongoDB, containerized with Docker.

## Prerequisites

- Docker
- Docker Compose

## Project Structure

```
project/
├── app.py
├── requirements.txt
├── docker-compose.yaml
├── Dockerfile.app
└── Dockerfile.db
```

## Quick Start

### 1. Clone/Setup the Project

Create a project folder and add all the files listed above.

### 2. Build and Run

```bash
docker-compose -p minimarket_app up --build
```

This will:
- Build the Flask app container
- Build the MongoDB container
- Create a network bridge between them
- Start both services

The Flask app will be available at `http://localhost:5000`

### 3. Verify It's Running

Check the health endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "ok"}
```

## API Endpoints

### Create Item
```bash
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Coca Cola 500ml",
    "price": 15000,
    "quantity": 50,
    "category": "Beverages"
  }'
```

**Required fields:** `name`, `price`  
**Optional fields:** `quantity` (default: 0), `category`

### Get All Items
```bash
curl http://localhost:5000/api/items
```

### Get Single Item
```bash
curl http://localhost:5000/api/items/<item_id>
```

### Update Item
```bash
curl -X PUT http://localhost:5000/api/items/<item_id> \
  -H "Content-Type: application/json" \
  -d '{
    "price": 16000,
    "quantity": 45
  }'
```

Any field can be updated: `name`, `price`, `quantity`, `category`

### Delete Item
```bash
curl -X DELETE http://localhost:5000/api/items/<item_id>
```

## Data Schema

Each item in the database contains:

```json
{
  "_id": "mongodb_object_id",
  "name": "Item Name",
  "price": 15000,
  "quantity": 50,
  "category": "Beverages",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
}
```

## Docker Commands

### Start containers
```bash
docker-compose -p minimarket_app up --build
```

### Stop containers
```bash
docker-compose -p minimarket_app down
```

### View logs
```bash
docker-compose -p minimarket_app logs -f
```

### View running containers
```bash
docker ps
```

### Access MongoDB shell
```bash
docker exec -it minimarket_app-mongodb-1 mongosh
```

## Volumes

- **mongodb_data** - Persists MongoDB database files
- **mongodb_config** - Persists MongoDB configuration
- **./app.py** - Hot-reloads Flask app code (development)
- **./logs** - Application logs (optional)

Data persists even after containers are stopped!

## Environment Variables

- `MONGO_URI` - MongoDB connection string (default: `mongodb://mongodb:27017/`)
- `FLASK_ENV` - Flask environment (default: `development`)

## Troubleshooting

### Containers won't start
```bash
docker-compose -p minimarket_app down -v
docker-compose -p minimarket_app up --build
```

### MongoDB connection refused
Make sure MongoDB container is running:
```bash
docker ps | grep mongodb
```

### Port already in use
Change ports in `docker-compose.yaml`:
- Flask: `5000:5000` → `5001:5000`
- MongoDB: `27017:27017` → `27018:27017`

### Check container logs
```bash
docker-compose -p minimarket_app logs flask-app
docker-compose -p minimarket_app logs mongodb
```

## Development

To modify the Flask app, edit `app.py` and the changes will hot-reload automatically (due to volume mount).

For production, remove the `volumes` section from `docker-compose.yaml` and rebuild.

## License

MIT