#!/bin/bash

# Production deployment script
set -e

echo "🚀 Starting FastAPI Interview Application Deployment"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your actual configuration values!"
fi

# Build the application
echo "🔨 Building FastAPI application..."
docker build -t fastapi-interview-app .

# Start the services
echo "🌟 Starting all services with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if application is running
if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo ""
    echo "🎉 Interview Application is ready!"
    echo "📊 API Documentation: http://localhost:8000/docs"
    echo "🔍 Alternative Docs: http://localhost:8000/redoc"
    echo "🗄️  PostgreSQL Admin: http://localhost:8080 (admin@example.com / admin)"
    echo "📊 MongoDB Admin: http://localhost:8081 (admin / admin)"
    echo ""
    echo "To stop the application: docker-compose down"
    echo "To view logs: docker-compose logs -f app"
else
    echo "❌ Application failed to start properly"
    echo "📋 Checking logs..."
    docker-compose logs app
    exit 1
fi