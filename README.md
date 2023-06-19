# Fast Stock Market

A FastAPI Stock Market API

## Architecture

The architecture of the service is as follows:

- An `Auth` service that handles authentication/authorization
- A `Stock` service that handles stock market data
- An `API Gateway` that handles routing with rate limiting
  - `Grafana` for querying:
    - `Prometheus` for metrics - Scraped from `/metrics` endpoint
    - `Loki` for logs - Collected with Docker Loki plugin
    - `Tempo` for traces - Pushed with gRPC

All services are written in Python `3.10` using FastAPI and are containerized using Docker.

`Auth` service uses JWT for authentication/authorization, with a MongoDB database for storing user data.

`Market` doesn't use a database, but instead uses a third party API to get stock market data.

`API Gateway` uses Redis for rate limiting. It can be interchanged with a `Redis Cluster` set up.

![Architecture](/assets/service_architecture.svg)

## Running the service

### Prerequisites

- Docker
- Docker Compose
- Python 3.10

### Installation

1. Clone the repository

```bash
git clone https://github.com/tomasanchez/fast-stock-market.git
```

2. Install [Loki Docker Driver](https://grafana.com/docs/loki/latest/clients/docker-driver/)

```bash
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
```

3. Build application image and start all services with docker-compose

```bash
docker-compose build
docker-compose up -d
```

4. Open API Gateway at Swagger UI http://localhost:80/docs

5. Make some requests to the API

6. Check predefined dashboard `FastAPI Observability` on Grafana http://localhost:3000/