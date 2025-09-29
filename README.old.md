# Google Dorks Toolkit

A comprehensive Django-based web application for managing, categorizing, and executing Google dorking queries. This tool is designed for security researchers, penetration testers, and cybersecurity professionals to systematically organize and use Google dorks for legitimate security research.

## 🚀 Features

### Core Functionality
- **Dork Management**: Create, edit, and organize Google dork queries
- **Categorization**: Organize dorks by type (File Discovery, Login Pages, Database Files, etc.)
- **Risk Assessment**: Classify dorks by difficulty and risk level
- **Search & Filter**: Advanced filtering by category, difficulty, risk level, and tags
- **Bookmarks**: Save favorite dorks for quick access

### Search & Results
- **Execute Dorks**: Run Google dork queries directly from the interface
- **Result Storage**: Save and organize search results
- **Result Analysis**: Mark interesting results and add notes
- **Session Management**: Create search sessions for organized campaigns

### User Interface
- **Responsive Design**: Bootstrap-based UI that works on all devices
- **Dashboard**: Overview of statistics and recent activity
- **Admin Interface**: Full Django admin for data management
- **Safety Warnings**: Risk level indicators and safety reminders

## 📋 Prerequisites

- Python 3.8+
- Django 5.2+
- Virtual environment (recommended)

## 🛠️ Installation & Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd d:\MP@
   ```

2. **Activate the virtual environment**
   ```bash
   # Windows
   env\Scripts\activate
   ```

3. **Install dependencies** (already installed)
   ```bash
   pip install django requests beautifulsoup4 googlesearch-python
   ```

4. **Run migrations** (already completed)
   ```bash
   python manage.py migrate
   ```

5. **Load sample data** (already loaded)
   ```bash
   python manage.py load_sample_dorks
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main Application: http://127.0.0.1:8000/
   - Admin Interface: http://127.0.0.1:8000/admin/
   - Login: admin / admin123

## 📊 Sample Data

The application comes pre-loaded with:
- **8 Categories**: File Discovery, Login Pages, Directory Listing, Error Pages, Database Files, Configuration Files, Sensitive Information, Web Application
- **20 Google Dorks**: Covering various security research scenarios
- **Admin User**: username: `admin`, password: `admin123`

## 🗂️ Project Structure

```
googledorks/
├── models.py              # Database models (DorkCategory, GoogleDork, SearchResult, etc.)
├── views.py               # Application views and logic
├── admin.py               # Django admin configuration
├── urls.py                # URL routing
├── templates/googledorks/ # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Dashboard
│   ├── dork_list.html    # Dork listing with filters
│   └── dork_detail.html  # Individual dork details
├── management/commands/
│   └── load_sample_dorks.py # Sample data loader
└── migrations/           # Database migration files
```

## 🔍 Google Dork Categories

1. **File Discovery** - Find exposed files and documents
2. **Login Pages** - Discover authentication interfaces
3. **Directory Listing** - Locate open directory listings
4. **Error Pages** - Find error pages revealing information
5. **Database Files** - Locate exposed database files
6. **Configuration Files** - Find config and settings files
7. **Sensitive Information** - Discover pages with sensitive data
8. **Web Application** - Target specific web applications

## 🎯 Usage Examples

### Basic Google Dorks Included:
- `filetype:pdf site:example.com` - Find PDF files on a domain
- `inurl:wp-admin/login.php` - WordPress admin login pages
- `intitle:"Index of /" +parent directory` - Open directory listings
- `filetype:sql "INSERT INTO"` - SQL database dump files
- `inurl:phpmyadmin` - phpMyAdmin interfaces

### Risk Levels:
- **Low**: Basic file discovery, public information
- **Medium**: Login pages, directory listings
- **High**: Configuration files, backup files
- **Critical**: Database files, password files, private keys

## 🛡️ Security & Ethics

### ⚠️ Important Disclaimer
This tool is intended for:
- ✅ Educational purposes
- ✅ Authorized security testing
- ✅ Legitimate security research
- ✅ Bug bounty programs with proper scope

### 🚫 Do NOT use for:
- ❌ Unauthorized access to systems
- ❌ Violating terms of service
- ❌ Illegal activities
- ❌ Accessing private information without permission

### Best Practices:
1. Always obtain proper authorization before testing
2. Respect robots.txt and website terms of service
3. Use rate limiting to avoid overwhelming servers
4. Report vulnerabilities responsibly
5. Follow applicable laws and regulations

## 🔧 Customization

### Adding New Dorks
1. Use the admin interface at `/admin/`
2. Navigate to "Google dorks" → "Add"
3. Fill in the dork details:
   - Title and description
   - Google dork query
   - Category and risk level
   - Tags for organization

### Creating New Categories
1. Go to admin → "Dork categories" → "Add"
2. Set name, description, and color code
3. Organize dorks by assigning categories

### Extending Functionality
The application is built with Django best practices and can be extended with:
- API endpoints for programmatic access
- Advanced search result analysis
- Integration with other security tools
- Custom reporting features
- User authentication and permissions

## 📱 Features Overview

### Dashboard
- Statistics overview (total dorks, categories, results)
- Recent dorks and search results
- Category breakdown with color coding
- Quick action buttons

### Dork Management
- Filter by category, difficulty, risk level
- Search through titles, descriptions, and tags
- Sort by various criteria
- Bookmark favorite dorks

### Search Results
- Store and organize found results
- Mark interesting results for review
- Add notes to results
- Filter by domain and other criteria

### Session Management
- Create organized search campaigns
- Group related dorks together
- Track session progress and results

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is for educational and legitimate security research purposes only. Users are responsible for ensuring their use complies with applicable laws and regulations.

## 🆘 Support

For issues or questions:
1. Check the Django admin interface for data management
2. Review the sample dorks for examples
3. Consult Django documentation for framework questions

---

**Remember**: Always use this tool responsibly and ethically. Unauthorized access to computer systems is illegal and unethical.