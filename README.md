# Google Dorks Toolkit 🔍

A comprehensive web application for managing and executing Google dorks (advanced search queries) for security research and information gathering.

![Python](https://img.shields.io/badge/python-v3.13+-blue.svg)
![Django](https://img.shields.io/badge/django-v5.2.6-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)

## 🚀 Features

### Core Functionality
- **📚 Dork Library**: Pre-loaded with 20+ Google dorks across 8 categories
- **🔍 Advanced Search**: Filter dorks by category, difficulty, risk level, and keywords
- **⚡ Execute Dorks**: Direct integration to execute searches on Google
- **📊 Dashboard**: Overview with statistics and recent activity
- **🔖 Bookmarks**: Save and organize your favorite dorks
- **📝 Session Tracking**: Track your search history and sessions

### Categories
- **Information Disclosure**: Find exposed sensitive files and data
- **Login Pages**: Discover authentication portals
- **Vulnerable Files**: Locate potentially vulnerable file types
- **Directory Listings**: Find open directory indexes
- **Error Messages**: Discover application error pages
- **Database Files**: Locate exposed database files
- **Configuration Files**: Find exposed config files
- **Network Infrastructure**: Discover network-related information

### Security Features
- **Risk Assessment**: Each dork is rated by risk level (Low, Medium, High, Critical)
- **Difficulty Levels**: Categorized by complexity (Beginner, Intermediate, Advanced)
- **Usage Tracking**: Monitor which dorks are most popular
- **Responsible Disclosure**: Guidelines for ethical use

## 🛠️ Installation

### Method 1: Docker (Recommended)

#### Prerequisites
- Docker
- Docker Compose

#### Quick Start with SQLite
```bash
# Clone the repository
git clone <repository-url>
cd google-dorks-toolkit

# Build and run with SQLite
docker-compose -f docker-compose.sqlite.yml up --build

# Access the application
# http://localhost:8000
```

#### Production Setup with PostgreSQL
```bash
# Build and run with PostgreSQL
docker-compose up --build

# Access the application
# http://localhost:8000
```

### Method 2: Manual Installation

#### Prerequisites
- Python 3.13+
- pip

#### Setup Steps
```bash
# Clone the repository
git clone <repository-url>
cd google-dorks-toolkit

# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load sample data
python manage.py load_sample_dorks

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access the application
# http://localhost:8000
```

## 🏗️ Project Structure

```
google-dorks-toolkit/
├── InformationExtractor/          # Django project settings
│   ├── settings.py               # Main settings
│   ├── urls.py                   # URL routing
│   └── wsgi.py                   # WSGI config
├── googledorks/                  # Main application
│   ├── models.py                 # Database models
│   ├── views.py                  # View controllers
│   ├── urls.py                   # App URL patterns
│   ├── admin.py                  # Admin interface
│   ├── management/               # Django commands
│   │   └── commands/
│   │       └── load_sample_dorks.py
│   ├── templates/                # HTML templates
│   │   └── googledorks/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── dork_list.html
│   │       └── ...
│   └── static/                   # Static files
│       ├── css/
│       ├── js/
│       └── favicon.svg
├── docker-compose.yml            # Docker Compose (PostgreSQL)
├── docker-compose.sqlite.yml     # Docker Compose (SQLite)
├── Dockerfile                    # Docker configuration
├── requirements.txt              # Python dependencies
├── manage.py                     # Django management script
└── README.md                     # This file
```

## 📱 Usage

### Browsing Dorks
1. Navigate to **Browse Dorks** to see all available dorks
2. Use filters to narrow down by:
   - Category (Information Disclosure, Login Pages, etc.)
   - Difficulty Level (Beginner, Intermediate, Advanced)
   - Risk Level (Low, Medium, High, Critical)
   - Keywords in title or description

### Executing Dorks
1. Click on any dork to view details
2. Click **Execute Dork** to open Google search in a new tab
3. Review results responsibly

### Managing Bookmarks
1. Click the bookmark icon on any dork to save it
2. Access your bookmarks from the **My Bookmarks** section
3. Organize and manage your saved dorks

### Search Sessions
1. Create search sessions to track your research
2. Group related searches together
3. Review session history and results

### Admin Interface
Access the Django admin at `/admin/` to:
- Add new dorks and categories
- Manage user accounts
- View usage statistics
- Moderate content

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/googledorks

# Security (for production)
SECURE_SSL_REDIRECT=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

### Database Configuration
The application supports both SQLite (development) and PostgreSQL (production):

#### SQLite (Default)
- No additional configuration needed
- Database file: `db.sqlite3`

#### PostgreSQL
Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'googledorks',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🛡️ Ethical Usage

### ⚠️ Important Disclaimer
This tool is designed for **educational and legitimate security research purposes only**. Users must:

1. **Respect Others' Privacy**: Never access unauthorized systems
2. **Follow Laws**: Comply with local and international laws
3. **Get Permission**: Only test systems you own or have explicit permission to test
4. **Be Responsible**: Use findings for constructive security improvements
5. **Report Responsibly**: Follow responsible disclosure practices

### Guidelines
- Use only for authorized penetration testing
- Don't exploit discovered vulnerabilities
- Respect website terms of service
- Consider the impact of your searches
- Document findings professionally

## 🤝 Contributing

### Development Setup
```bash
# Fork the repository
# Clone your fork
git clone <your-fork-url>
cd google-dorks-toolkit

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python manage.py test

# Commit and push
git commit -m "Add your feature"
git push origin feature/your-feature-name

# Create pull request
```

### Adding New Dorks
1. Use the admin interface (`/admin/`)
2. Create new categories if needed
3. Add dork with proper categorization
4. Set appropriate risk and difficulty levels
5. Test the dork for accuracy

### Code Standards
- Follow PEP 8 style guidelines
- Write descriptive commit messages
- Add tests for new features
- Update documentation

## 📊 Database Models

### GoogleDork
- **title**: Descriptive name
- **query**: The actual Google dork query
- **description**: Detailed explanation
- **category**: Related category
- **difficulty**: Beginner/Intermediate/Advanced
- **risk_level**: Low/Medium/High/Critical
- **tags**: Comma-separated keywords
- **usage_count**: Tracking popularity

### DorkCategory
- **name**: Category name
- **description**: Category description
- **color**: UI color coding

### SearchResult
- **dork**: Related dork
- **url**: Found URL
- **title**: Page title
- **snippet**: Search snippet
- **created_at**: Discovery timestamp

### SearchSession
- **name**: Session name
- **description**: Session notes
- **user**: Associated user
- **created_at**: Session start time

### DorkBookmark
- **user**: User who bookmarked
- **dork**: Bookmarked dork
- **notes**: Personal notes
- **created_at**: Bookmark timestamp

## 🚀 Deployment

### Docker Production Deployment
```bash
# Production build
docker-compose -f docker-compose.yml up -d --build

# SSL setup (recommended)
# Use nginx reverse proxy with Let's Encrypt
```

### Traditional Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic

# Run with gunicorn
pip install gunicorn
gunicorn InformationExtractor.wsgi:application
```

## 🐛 Troubleshooting

### Common Issues

#### Docker Build Fails
```bash
# Clear Docker cache
docker system prune -a
docker-compose build --no-cache
```

#### Template Errors
```bash
# Clear Django cache
python manage.py collectstatic --clear
# Restart development server
```

#### Database Migration Issues
```bash
# Reset migrations (development only)
python manage.py migrate --fake googledorks zero
python manage.py makemigrations googledorks
python manage.py migrate
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django framework and community
- Bootstrap for UI components
- Google for search capabilities
- Security research community
- Open source contributors

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: Check the wiki for detailed guides
- **Security**: Report security issues privately
- **Features**: Suggest improvements via GitHub Discussions

---

**Remember**: Use this tool responsibly and ethically. Always respect others' privacy and follow applicable laws and regulations.