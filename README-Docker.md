# Dream AI - Docker Setup

This project uses Docker and Docker Compose for easy deployment and development.

## Prerequisites

- Docker
- Docker Compose
- OpenAI API Key

## Quick Start

1. **Clone the repository and navigate to the project directory**

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key and other configuration.

3. **Run the application:**

   **Basic (FastAPI only):**
   ```bash
   docker-compose up --build
   ```

   **With Nginx reverse proxy:**
   ```bash
   docker-compose --profile nginx up --build
   ```

   **With Redis caching:**
   ```bash
   docker-compose --profile redis up --build
   ```

   **Full stack (FastAPI + Nginx + Redis):**
   ```bash
   docker-compose --profile nginx --profile redis up --build
   ```

   **Background mode:**
   ```bash
   docker-compose up -d --build
   ```

## Available Services

- **FastAPI Application**: Dream AI backend service
  - Direct access: http://localhost:8020
  - Via nginx (if enabled): http://localhost
  
- **Nginx**: Reverse proxy and load balancer (optional)
  - Enable with: `--profile nginx`
  - Port: 80 (HTTP)

- **Redis**: Caching service (optional)
  - Enable with: `--profile redis`
  - Port: 6379

## API Endpoints

- **Health Check**: `/health`
- **API Documentation**: `/docs`
- **ReDoc**: `/redoc`
- **Dream Analysis**: `POST /api/v1/dream-ai/analyze`
- **Image Generation**: `POST /api/v1/dream-ai/generate-image`
- **Complete Interpretation**: `POST /api/v1/dream-ai/complete-interpretation`

## Docker Commands

**Start FastAPI application only:**
```bash
docker-compose up --build
```

**Start with specific services:**
```bash
# With nginx
docker-compose --profile nginx up --build

# With redis
docker-compose --profile redis up --build

# Full stack
docker-compose --profile nginx --profile redis up --build
```

**Start services in background:**
```bash
docker-compose up -d
```

**Stop services:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f [service-name]
```

**Rebuild specific service:**
```bash
docker-compose build [service-name]
```

## Development and Deployment

**For simple development/testing:**
```bash
docker-compose up
```
Access your API at: http://localhost:8020

**For production-like setup with reverse proxy:**
```bash
docker-compose --profile nginx up -d
```
Access your API at: http://localhost (port 80)

**For full production setup with caching:**
```bash
docker-compose --profile nginx --profile redis up -d
```

## Configuration Options

The single `docker-compose.yml` file uses **profiles** to enable optional services:

- **Default**: Only FastAPI application runs
- **nginx profile**: Adds reverse proxy
- **redis profile**: Adds caching layer

This approach gives you flexibility without maintaining multiple files.

## Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional:
- `APP_NAME`: Application name (default: "Dream AI Interpreter")
- `DEBUG`: Debug mode (default: false)

## Health Checks

All services include health checks:
- FastAPI: Checks `/health` endpoint
- Nginx: Validates configuration
- Redis: Pings Redis server

## Volumes

- `redis_data`: Persistent storage for Redis data

## Networks

- `dream-ai-network`: Internal network for service communication

## Troubleshooting

1. **Port conflicts**: Ensure ports 80, 8020, and 6379 are available
2. **API Key**: Verify your OpenAI API key is set correctly in `.env`
3. **Logs**: Check service logs with `docker-compose logs [service-name]`
4. **Health**: Check service health with `docker-compose ps`
