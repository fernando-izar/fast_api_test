# FastAPI Interview Application 🚀

A professional FastAPI application with PostgreSQL and MongoDB integration, containerized with Docker for easy deployment.

## 🌟 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Database Integration**: PostgreSQL for relational data, MongoDB for logs
- **Authentication**: JWT-based authentication system
- **Database Migration**: Alembic for PostgreSQL schema management
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Containerized**: Docker and Docker Compose for easy deployment
- **Development Tools**: Database admin interfaces included

## 🏗️ Architecture

```
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/v1/              # API routes
│   ├── core/                # Configuration and settings
│   ├── db/                  # Database connections
│   ├── models/              # SQLAlchemy models
│   └── schemas/             # Pydantic schemas
├── alembic/                 # Database migrations
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yml       # Development environment
└── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### Option 1: Using the Start Script (Recommended)

```bash
# Make the script executable
chmod +x start.sh

# Run the start script
./start.sh
```

### Option 2: Manual Docker Compose

```bash
# Copy environment configuration
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app
```

### Option 3: Docker Only

```bash
# Build the image
docker build -t fastapi-interview-app .

# Run the container
docker run -p 8000:8000 fastapi-interview-app
```

## 🔗 Access Points

Once running, you can access:

- **🎯 API Documentation**: http://localhost:8000/docs
- **📚 Alternative Docs**: http://localhost:8000/redoc
- **🗄️ PostgreSQL Admin**: http://localhost:8080 (admin@example.com / admin)
- **📊 MongoDB Admin**: http://localhost:8081 (admin / admin)

## 🛠️ Development

### Local Development with Hot Reload

```bash
# Start in development mode
docker-compose up

# The application will automatically reload when you make changes
```

### Running Database Migrations

```bash
# Generate a new migration
docker-compose exec app alembic revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec app alembic upgrade head
```

### Installing New Dependencies

```bash
# Add to requirements.txt, then rebuild
docker-compose build app
docker-compose up -d
```

## 🔧 Configuration

Environment variables can be configured in `.env` file:

```bash
# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=fastapi_password
POSTGRES_DB=fastapi_db

# MongoDB
MONGODB_HOST=mongodb
MONGODB_PORT=27017
MONGODB_DB=fastapi_logs
MONGODB_USERNAME=fastapi_user
MONGODB_PASSWORD=fastapi_password

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🔒 Production Considerations

This Docker setup includes several production-ready features:

- **Multi-stage builds** for optimized image size
- **Non-root user** for security
- **Health checks** for container monitoring
- **Volume persistence** for database data
- **Network isolation** between services
- **Environment variable configuration**

For production deployment:

1. Update all passwords and secret keys
2. Use a reverse proxy like Nginx
3. Enable HTTPS/TLS
4. Set up proper logging and monitoring
5. Use external managed databases for scalability

## 📊 API Endpoints

The application includes the following API routes:

- `/api/v1/auth/*` - Authentication endpoints
- `/api/v1/users/*` - User management
- `/api/v1/jobs/*` - Job management
- `/api/v1/agents/*` - Agent management
- `/api/v1/job_logs/*` - Job logging

## 🛑 Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ this will delete database data)
docker-compose down -v
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Change ports in `docker-compose.yml`
2. **Database connection issues**: Ensure services are healthy with `docker-compose ps`
3. **Permission issues**: Check file permissions and Docker user settings

### Viewing Logs

```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs app
docker-compose logs postgres
docker-compose logs mongodb

# Follow logs in real-time
docker-compose logs -f app
```

### Accessing Database Directly

```bash
# PostgreSQL
docker-compose exec postgres psql -U fastapi_user -d fastapi_db

# MongoDB
docker-compose exec mongodb mongosh -u fastapi_user -p fastapi_password
```

## 🏆 Interview Highlights

This setup demonstrates:

- **Professional Docker practices** with multi-stage builds
- **Full-stack application** with multiple databases
- **Development environment** that's identical to production
- **Security best practices** (non-root user, environment variables)
- **Documentation and ease of use** for quick evaluation
- **Scalable architecture** ready for production deployment

---

*Built with ❤️ for the interview process*