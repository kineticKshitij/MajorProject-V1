@echo off
REM Docker Setup Script for Google Dorks Toolkit (Windows)

echo 🔍 Google Dorks Toolkit - Docker Setup
echo ======================================

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not in PATH.
    echo 📖 Visit: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed or not in PATH.
    echo 📖 Visit: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are available

REM Check if Docker daemon is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker daemon is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker daemon is running

REM Build the application
echo 🔨 Building Google Dorks Toolkit...
docker-compose -f docker-compose.sqlite.yml build

if %errorlevel% equ 0 (
    echo ✅ Build successful!
    echo.
    echo 🚀 To start the application:
    echo    docker-compose -f docker-compose.sqlite.yml up
    echo.
    echo 🌐 Access the application at:
    echo    http://localhost:8000
    echo.
    echo 🛑 To stop the application:
    echo    docker-compose -f docker-compose.sqlite.yml down
) else (
    echo ❌ Build failed. Please check the error messages above.
    pause
    exit /b 1
)

pause