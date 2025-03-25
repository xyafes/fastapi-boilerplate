# FastAPI Boilerplate

A production-ready(Not yet :d) FastAPI boilerplate with PostgreSQL, Celery, RabbitMQ, and Docker integration.

## Features

- **FastAPI** framework for building high-performance APIs
- **PostgreSQL** database with **Tortoise ORM** for async database operations
- **Celery** distributed task queue with **RabbitMQ** as message broker
- **Docker** and **Docker Compose** for containerization and orchestration
- **WebSocket** support for real-time communication
- **Authentication** middleware for API endpoints
- **CORS** middleware configured for API access control
- **Exception handling** with custom handlers
- Configured logging with rotation
- Healthcheck endpoint
- Alpine-based Docker images for minimal footprint

## Project Structure

```
fastapi-boilerplate/
├── alpine.Dockerfile       # Docker configuration for Alpine-based image
├── docker-compose.yml      # Docker Compose configuration
├── example_app.env         # Example environment variables for the app
├── example_postgres.env    # Example environment variables for PostgreSQL
├── Makefile                # Utility commands for development
├── postgresql.conf         # PostgreSQL configuration
├── pyproject.toml          # Python project dependencies
├── README.md               # Project documentation
├── uv.lock                 # Uv package manager lock file
├── migrations/             # Database migrations
│   └── models/
│       └── 0_20250313100715_init.py
└── source/                 # Application source code
    ├── __init__.py
    ├── celery_app.py       # Celery configuration
    ├── database.py         # Database connection utilities
    ├── models.py           # Database models
    ├── settings.py         # Application settings
    ├── tasks.py            # Celery tasks
    ├── api/                # API endpoints
    │   ├── __init__.py
    │   ├── exception_handlers.py  # Custom exception handlers
    │   ├── main.py        # FastAPI application entry point
    │   └── schemas.py     # Pydantic schemas for API
    └── app/               # Application logic
        ├── __init__.py
        └── example_ws.py  # WebSocket example implementation
```

## Prerequisites

- Docker and Docker Compose
- Python 3.13+
- uv

## Getting Started

### Using Docker Compose

1. Clone the repository:

```bash
git clone <repository-url> fastapi-boilerplate
cd fastapi-boilerplate
```

2. Create environment files from examples:

```bash
cp example_app.env .env
cp example_postgres.env postgres.env
```

3. Customize the environment variables in the created `.env` and `postgres.env` files according to your needs.

4. Start the services using Docker Compose:

```bash
docker-compose up -d
```

or

```bash
make up
```

The API will be available at http://localhost:8000.

### Local Development Setup

1. Clone the repository and navigate to the project directory.

2. İnstall dependencies with uv, https://docs.astral.sh/uv/:

```bash
uv lock
```

```bash
uv sync
```

3. Create and configure environment files.

4. Install and configure PostgreSQL and RabbitMQ locally.

## API Documentation

Once the application is running, you can access:

- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Key Endpoints

- **GET /healthcheck**: Health check endpoint
- **POST /create_user**: Create a new user
- **GET /get_user**: Get user by ID
- **GET /get_user_messages**: Get messages for a specific user
- **POST /create_message**: Create a new message for a user
- **WebSocket /ws**: WebSocket endpoint for real-time communication

## Environment Variables

### Application Environment Variables

- `DEBUG`: Enable debug mode (1 for enabled, 0 for disabled)
- `TOKEN`: Authentication token for API access
- `URI`: URI for WebSocket connections
- `AUTH`: Authentication token for WebSocket connections
- `BROKER_URL`: URL for connecting to RabbitMQ

### PostgreSQL Environment Variables

- `DATABASE_HOST`: PostgreSQL host
- `DATABASE_PORT`: PostgreSQL port
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name

## Celery Tasks

The boilerplate includes a Celery setup with example tasks:

- Regular task that runs every 30 seconds
- WebSocket listener task that runs every 25 minutes

## Contributing

Contributions are welcome. Please feel free to submit a Pull Request.
