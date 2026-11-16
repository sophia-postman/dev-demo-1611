# 🚗 Vehicle Service API

A lightweight Python/Flask implementation of the Vehicle Service API — a RESTful service for managing a registry of vehicles.

## Endpoints

| Method   | Path               | Description          |
|----------|--------------------|----------------------|
| `GET`    | `/vehicles`        | List all vehicles    |
| `POST`   | `/vehicles`        | Create a vehicle     |
| `GET`    | `/vehicles/{id}`   | Retrieve a vehicle   |
| `PATCH`  | `/vehicles/{id}`   | Update a vehicle     |
| `DELETE` | `/vehicles/{id}`   | Delete a vehicle     |

## Authentication

Every request must include a valid API key in the `X-API-Key` header.

```
X-API-Key: dev-api-key
```

Set the `API_KEY` environment variable to change the key (defaults to `dev-api-key` for local development).

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
python app.py
```

The server starts on `http://localhost:3000` by default.

### Environment variables

| Variable      | Default       | Description                        |
|---------------|---------------|------------------------------------|
| `API_KEY`     | `dev-api-key` | API key required in `X-API-Key` header |
| `PORT`        | `3000`        | Port the server listens on         |
| `FLASK_DEBUG` | `false`       | Set to `true` to enable debug mode |

### 3. Point Postman at the local server

Update the `baseUrl` variable in the **local** environment to:

```
http://localhost:3000
```

## Example requests

### Create a vehicle
```bash
curl -X POST http://localhost:3000/vehicles \
  -H "X-API-Key: dev-api-key" \
  -H "Content-Type: application/json" \
  -d '{"vin":"4M2DV11W4RDJ53329","make":"Mercury","model":"Villager","year":"1994","miles":159864,"nickName":"The Lisa Marie"}'
```

### Get all vehicles
```bash
curl http://localhost:3000/vehicles \
  -H "X-API-Key: dev-api-key"
```

### Retrieve a vehicle
```bash
curl http://localhost:3000/vehicles/1 \
  -H "X-API-Key: dev-api-key"
```

### Update a vehicle
```bash
curl -X PATCH http://localhost:3000/vehicles/1 \
  -H "X-API-Key: dev-api-key" \
  -H "Content-Type: application/json" \
  -d '{"miles":162000}'
```

### Delete a vehicle
```bash
curl -X DELETE http://localhost:3000/vehicles/1 \
  -H "X-API-Key: dev-api-key"
```

## Notes

- Data is stored **in-memory** — it resets when the server restarts. Swap `_vehicles` for a database-backed store for persistence.
- VINs are unique — attempting to create a duplicate VIN returns `409 Conflict`.
