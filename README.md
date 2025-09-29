# Google Dorks Toolkit 🔍

A comprehensive Django web application for managing and executing Google dorks (advanced search queries) for security research and penetration testing. This tool helps security professionals systematically organize and utilize Google dorking techniques for legitimate security assessments.

![Python](https://img.shields.io/badge/python-v3.13+-blue.svg)
![Django](https://img.shields.io/badge/django-v5.2.6-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)

## 🚀 Features

### Core Functionality
- **📚 Comprehensive Dork Library**: Pre-loaded with 20+ Google dorks across 8 categories
- **🔍 Advanced Search & Filtering**: Filter by category, difficulty, risk level, and keywords
- **⚡ Direct Execution**: One-click Google search execution
- **📊 Analytics Dashboard**: Statistics and usage tracking
- **🔖 Bookmark System**: Save and organize favorite dorks
- **📝 Session Management**: Track search sessions and history

### Security Categories
- **Information Disclosure**: Exposed sensitive files and data
- **Login Pages**: Authentication portals and admin interfaces
- **Vulnerable Files**: Potentially exploitable file types
- **Directory Listings**: Open directory indexes
- **Error Messages**: Application error pages revealing information
- **Database Files**: Exposed database dumps and files
- **Configuration Files**: Exposed config and settings files
- **Network Infrastructure**: Network-related information gathering

### Risk Assessment
- **Risk Levels**: Low, Medium, High, Critical classification
- **Difficulty Ratings**: Beginner, Intermediate, Advanced
- **Usage Analytics**: Track popularity and effectiveness
- **Ethical Guidelines**: Built-in responsible use guidelines

## 🛠️ Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/kineticKshitij/MajorProject-V1.git
cd MajorProject-V1

# Quick start with SQLite
docker-compose -f docker-compose.sqlite.yml up --build

# Access the application at http://localhost:8000
```

### Option 2: Local Development

```bash
# Clone and setup
git clone https://github.com/kineticKshitij/MajorProject-V1.git
cd MajorProject-V1

# Create virtual environment
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py load_sample_dorks

# Run development server
python manage.py runserver
```

## 📋 Prerequisites

- **Python 3.13+**
- **Docker** (for containerized deployment)
- **Git** (for version control)

## 🏗️ Project Architecture

```
MajorProject-V1/
├── InformationExtractor/     # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── googledorks/             # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Business logic
│   ├── admin.py             # Admin interface
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, images
│   └── management/commands/ # Custom Django commands
├── docker-compose*.yml      # Docker configurations
├── Dockerfile*              # Docker build files
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## 📱 Usage Guide

### 1. Browse Dorks
- Navigate through categorized Google dorks
- Use advanced filters for targeted searching
- View detailed information for each dork

### 2. Execute Searches
- Click "Execute Dork" to open Google search
- Results open in new tab for safety
- Track usage and effectiveness

### 3. Manage Collections
- Bookmark useful dorks for quick access
- Create search sessions for organized research
- Export results for documentation

### 4. Admin Features
- Access admin panel at `/admin/`
- Add custom dorks and categories
- Monitor usage statistics
- Manage user accounts

## 🔧 Configuration

### Environment Variables
Create `.env` file for production:

```env
# Django Configuration
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=/app/db.sqlite3

# For PostgreSQL
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=googledorks
# DB_USER=postgres
# DB_PASSWORD=your-password
# DB_HOST=db
# DB_PORT=5432
```

### Deployment Options

| Configuration | Use Case | Command |
|---------------|----------|---------|
| **SQLite Development** | Quick testing | `docker-compose -f docker-compose.sqlite.yml up` |
| **PostgreSQL Development** | Full dev environment | `docker-compose -f docker-compose.yml up` |
| **Production** | Live deployment | `docker-compose -f docker-compose.production.yml up` |

## 🛡️ Ethical Usage & Legal Disclaimer

### ⚠️ Important Notice
This tool is designed for **legitimate security research and educational purposes only**. Users must:

- ✅ **Only test systems you own** or have explicit written permission to test
- ✅ **Comply with local and international laws**
- ✅ **Follow responsible disclosure** for any findings
- ✅ **Respect privacy and data protection** regulations
- ✅ **Use for constructive security improvement**

### Prohibited Uses
- ❌ Unauthorized access to systems
- ❌ Data theft or privacy violations
- ❌ Malicious activities or exploitation
- ❌ Commercial espionage
- ❌ Any illegal activities

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit with descriptive messages: `git commit -m "Add amazing feature"`
5. Push to your fork: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages

## 📊 Technology Stack

- **Backend**: Django 5.2.6, Python 3.13+
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Containerization**: Docker, Docker Compose
- **Web Server**: Gunicorn, Nginx (production)

## � Database Models

### Core Models
- **GoogleDork**: Individual dork queries with metadata
- **DorkCategory**: Organizational categories
- **SearchResult**: Tracked search outcomes
- **SearchSession**: Grouped research sessions
- **DorkBookmark**: User-saved favorites

### Key Features
- **Relationship mapping** between models
- **Usage tracking** and analytics
- **User-specific** bookmarks and sessions
- **Categorization** and tagging system

## 🚀 Deployment

### Docker Production Setup
```bash
# Production deployment with PostgreSQL + Nginx
docker-compose -f docker-compose.production.yml up -d

# Monitor logs
docker-compose logs -f

# Scale if needed
docker-compose up --scale web=3
```

### Traditional Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn InformationExtractor.wsgi:application --bind 0.0.0.0:8000
```

## 🐛 Troubleshooting

### Common Issues

**Docker Build Fails**
```bash
# Clear cache and rebuild
docker system prune -a
docker-compose build --no-cache
```

**Database Migration Issues**
```bash
# Reset migrations (development only)
python manage.py migrate --fake googledorks zero
python manage.py makemigrations
python manage.py migrate
```

**Permission Errors**
```bash
# Fix file permissions (Linux/Mac)
sudo chown -R $USER:$USER .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django framework and community
- Bootstrap for responsive UI
- Google for search capabilities
- Security research community
- Open source contributors

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/kineticKshitij/MajorProject-V1/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kineticKshitij/MajorProject-V1/discussions)
- **Security**: Report security issues privately
- **Documentation**: Check the [Wiki](https://github.com/kineticKshitij/MajorProject-V1/wiki)

---

**⚡ Remember**: This tool is a powerful asset for security professionals. Use it responsibly, ethically, and always within the bounds of the law. Happy ethical hacking! 🎯