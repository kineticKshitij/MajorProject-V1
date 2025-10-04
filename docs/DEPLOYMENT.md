# Deployment Guide

## 🚀 Quick Deployment Options

### 1. Docker Deployment (Recommended)

#### SQLite Version (Quick Start)
```bash
# Clone repository
git clone https://github.com/kineticKshitij/MajorProject-V1.git
cd MajorProject-V1

# Start with SQLite
docker-compose -f docker-compose.sqlite.yml up --build

# Access at http://localhost:8000
```

#### PostgreSQL Version (Production)
```bash
# Start with PostgreSQL
docker-compose -f docker-compose.production.yml up --build

# Access at http://localhost:8000
```

### 2. Local Development Setup

#### Prerequisites
- Python 3.13+
- Git
- Google Gemini API Key (optional for AI features)

#### Installation Steps
```bash
# 1. Clone repository
git clone https://github.com/kineticKshitij/MajorProject-V1.git
cd MajorProject-V1

# 2. Create virtual environment
python -m venv env

# 3. Activate virtual environment
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup database
python manage.py migrate

# 6. Load sample data
python manage.py load_sample_dorks

# 7. Create superuser
python manage.py createsuperuser

# 8. Run development server
python manage.py runserver
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Configuration
DEBUG=False
DJANGO_SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Configuration (SQLite - Default)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=/app/db.sqlite3

# Database Configuration (PostgreSQL - Production)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=googledorks
# DB_USER=postgres
# DB_PASSWORD=your-password
# DB_HOST=db
# DB_PORT=5432

# Google Gemini AI Configuration (Optional)
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp

# Additional Settings
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
```

### Google Gemini API Setup

1. **Get API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Create API Key**: Sign in and create a new API key
3. **Add to Environment**: Set `GEMINI_API_KEY` in your `.env` file
4. **Configure in App**: Users can also add personal API keys in their profiles

## 🛡️ Security Configuration

### Production Security Checklist

1. **Secret Key**: Generate a secure Django secret key
2. **Debug Mode**: Set `DEBUG=False` in production
3. **Allowed Hosts**: Configure proper allowed hosts
4. **HTTPS**: Enable HTTPS in production
5. **Database**: Use PostgreSQL in production
6. **API Keys**: Secure API key storage
7. **User Permissions**: Configure proper user permissions

### Generate Secret Key
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## 📊 Database Setup

### SQLite (Development)
- Default configuration
- No additional setup required
- Data stored in `db.sqlite3`

### PostgreSQL (Production)
```yaml
# docker-compose.yml example
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: googledorks
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    environment:
      DB_ENGINE: django.db.backends.postgresql
      DB_NAME: googledorks
      DB_USER: postgres
      DB_PASSWORD: your-password
      DB_HOST: db
      DB_PORT: 5432
```

## 🌐 Deployment Platforms

### Heroku Deployment
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set DJANGO_SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set GEMINI_API_KEY=your-api-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py load_sample_dorks
```

### DigitalOcean App Platform
1. Fork repository to your GitHub
2. Create new app in DigitalOcean
3. Connect GitHub repository
4. Set environment variables
5. Deploy

### AWS/Azure/GCP
- Use Docker containers
- Configure environment variables
- Set up database service
- Configure load balancer
- Enable HTTPS

## 🔍 Monitoring & Logging

### Django Logging
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Health Checks
- **Application**: `/admin/login/` endpoint
- **Database**: Connection tests
- **AI Service**: API key validation

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection**
   ```bash
   # Check database status
   python manage.py dbshell
   ```

2. **Static Files**
   ```bash
   # Collect static files
   python manage.py collectstatic --noinput
   ```

3. **Migration Issues**
   ```bash
   # Reset migrations (development only)
   python manage.py migrate --fake-initial
   ```

4. **Gemini API Issues**
   - Verify API key validity
   - Check quota limits
   - Ensure correct model name

### Docker Issues
```bash
# View logs
docker-compose logs -f

# Rebuild containers
docker-compose build --no-cache

# Reset volumes
docker-compose down -v
```

## 📈 Performance Optimization

### Production Settings
- Enable gzip compression
- Configure caching (Redis/Memcached)
- Use CDN for static files
- Database query optimization
- Enable database connection pooling

### Caching Configuration
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## 🔄 Backup & Recovery

### Database Backup
```bash
# SQLite
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3

# PostgreSQL
pg_dump googledorks > backup_$(date +%Y%m%d).sql
```

### Media Files Backup
```bash
# Backup user uploads
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

## 📱 Mobile Optimization

- Responsive design included
- Mobile-friendly navigation
- Touch-optimized interface
- Progressive Web App features

## 🤝 Support

For deployment support:
- Check [GitHub Issues](https://github.com/kineticKshitij/MajorProject-V1/issues)
- Review [Documentation](https://github.com/kineticKshitij/MajorProject-V1/wiki)
- Contact maintainers

---

**Remember**: This tool is for ethical security research only. Always comply with applicable laws and obtain proper authorization before testing systems.