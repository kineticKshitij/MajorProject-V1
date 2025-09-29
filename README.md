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
- **🤖 AI Assistant**: Google Gemini-powered chatbot for security research guidance

### User Authentication & Profiles
- **🔐 Custom User Registration**: Enhanced signup with ethical usage agreement
- **👤 User Profiles**: Comprehensive profile management with social links
- **🔑 Personal API Keys**: Individual Gemini API key management per user
- **🛡️ Secure Sessions**: User-specific chat sessions and data isolation
- **📈 Activity Tracking**: Personal usage statistics and analytics

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

# Create superuser account
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Getting Started Guide

1. **Visit the Application**: Navigate to `http://localhost:8000`
2. **Register Account**: Click "Register" to create your personal account
3. **Setup API Key**: 
   - Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Add it during registration or in Profile Settings
4. **Explore Features**: Browse dorks, use AI assistant, bookmark favorites
5. **Start Research**: Execute dorks responsibly and ethically

## 📋 Prerequisites

- **Python 3.13+**
- **Docker** (for containerized deployment)
- **Git** (for version control)
- **Google Gemini API Key** (for AI chatbot functionality)

## 🏗️ Project Architecture

```
MajorProject-V1/
├── InformationExtractor/     # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── accounts/                # User authentication system
│   ├── models.py            # Custom User and Profile models
│   ├── views.py             # Authentication views
│   ├── forms.py             # Registration and profile forms
│   ├── templates/           # Auth templates
│   └── admin.py             # User admin interface
├── googledorks/             # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Business logic
│   ├── admin.py             # Admin interface
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, images
│   └── management/commands/ # Custom Django commands
├── chatbot/                 # AI Assistant application
│   ├── models.py            # Chat models
│   ├── views.py             # Chat API endpoints
│   ├── services.py          # Gemini AI integration
│   ├── templates/           # Chat interface
│   └── admin.py             # Chat admin interface
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

### 4. User Account Management
- Register for personalized experience
- Set up personal Gemini API key for AI chatbot
- Manage profile settings and preferences
- Track personal usage statistics

### 5. AI Assistant
- Intelligent chatbot powered by Google Gemini
- Security research guidance and explanations
- Google dork suggestions and recommendations
- Chat session management and history
- Ethical hacking best practices advice

### 6. Admin Features
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

# Google Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp
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
- **AI Integration**: Google Gemini API (google-genai)
- **Containerization**: Docker, Docker Compose
- **Web Server**: Gunicorn, Nginx (production)

## � Database Models

### Core Models
- **GoogleDork**: Individual dork queries with metadata
- **DorkCategory**: Organizational categories
- **SearchResult**: Tracked search outcomes
- **SearchSession**: Grouped research sessions
- **DorkBookmark**: User-saved favorites
- **User**: Custom user model with API key storage
- **UserProfile**: Extended user information and preferences
- **ChatSession**: AI conversation sessions
- **ChatMessage**: Individual chat messages
- **ChatFeedback**: User feedback on AI responses
- **ChatMetrics**: Chat usage analytics

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