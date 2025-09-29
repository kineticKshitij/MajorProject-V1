#!/bin/bash
# Docker Setup Script for Google Dorks Toolkit

echo "🔍 Google Dorks Toolkit - Docker Setup"
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "📖 Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "📖 Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker daemon is running"

# Build the application
echo "🔨 Building Google Dorks Toolkit..."
docker-compose -f docker-compose.sqlite.yml build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "🚀 To start the application:"
    echo "   docker-compose -f docker-compose.sqlite.yml up"
    echo ""
    echo "🌐 Access the application at:"
    echo "   http://localhost:8000"
    echo ""
    echo "🛑 To stop the application:"
    echo "   docker-compose -f docker-compose.sqlite.yml down"
else
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi