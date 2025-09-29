from django.core.management.base import BaseCommand
from googledorks.models import DorkCategory, GoogleDork
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Load sample Google dork data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading sample Google dork data...'))

        # Create categories
        categories_data = [
            {
                'name': 'File Discovery',
                'description': 'Find exposed files and documents',
                'color': '#dc3545'
            },
            {
                'name': 'Login Pages',
                'description': 'Discover login and authentication pages',
                'color': '#fd7e14'
            },
            {
                'name': 'Directory Listing',
                'description': 'Find directory listings and exposed folders',
                'color': '#ffc107'
            },
            {
                'name': 'Error Pages',
                'description': 'Find error pages that may reveal information',
                'color': '#28a745'
            },
            {
                'name': 'Database Files',
                'description': 'Locate exposed database files',
                'color': '#6f42c1'
            },
            {
                'name': 'Configuration Files',
                'description': 'Find configuration and settings files',
                'color': '#20c997'
            },
            {
                'name': 'Sensitive Information',
                'description': 'Discover pages with sensitive data',
                'color': '#e83e8c'
            },
            {
                'name': 'Web Application',
                'description': 'Target specific web applications',
                'color': '#007bff'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = DorkCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'color': cat_data['color']
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample dorks
        dorks_data = [
            {
                'title': 'PDF Files Discovery',
                'query': 'filetype:pdf site:example.com',
                'description': 'Find PDF files on a specific domain that might contain sensitive information.',
                'category': 'File Discovery',
                'difficulty': 'beginner',
                'risk_level': 'low',
                'tags': 'pdf, documents, files'
            },
            {
                'title': 'Excel Spreadsheets',
                'query': 'filetype:xls OR filetype:xlsx site:*.com',
                'description': 'Locate Excel spreadsheets that might contain financial or personal data.',
                'category': 'File Discovery',
                'difficulty': 'beginner',
                'risk_level': 'medium',
                'tags': 'excel, spreadsheet, data'
            },
            {
                'title': 'WordPress Admin Login',
                'query': 'inurl:wp-admin/login.php',
                'description': 'Find WordPress admin login pages.',
                'category': 'Login Pages',
                'difficulty': 'beginner',
                'risk_level': 'low',
                'tags': 'wordpress, admin, login'
            },
            {
                'title': 'phpMyAdmin Interfaces',
                'query': 'inurl:phpmyadmin',
                'description': 'Discover phpMyAdmin database management interfaces.',
                'category': 'Database Files',
                'difficulty': 'intermediate',
                'risk_level': 'high',
                'tags': 'phpmyadmin, database, mysql'
            },
            {
                'title': 'Directory Listings',
                'query': 'intitle:"Index of /" +parent directory',
                'description': 'Find open directory listings that expose file structures.',
                'category': 'Directory Listing',
                'difficulty': 'beginner',
                'risk_level': 'medium',
                'tags': 'directory, listing, files'
            },
            {
                'title': 'SQL Database Files',
                'query': 'filetype:sql "INSERT INTO" site:*.com',
                'description': 'Find SQL dump files containing database data.',
                'category': 'Database Files',
                'difficulty': 'intermediate',
                'risk_level': 'critical',
                'tags': 'sql, database, dump'
            },
            {
                'title': 'Configuration Files',
                'query': 'filetype:ini OR filetype:cfg OR filetype:conf',
                'description': 'Locate configuration files that might contain sensitive settings.',
                'category': 'Configuration Files',
                'difficulty': 'intermediate',
                'risk_level': 'high',
                'tags': 'config, settings, ini'
            },
            {
                'title': 'Log Files',
                'query': 'filetype:log',
                'description': 'Find log files that might contain error messages or system information.',
                'category': 'File Discovery',
                'difficulty': 'beginner',
                'risk_level': 'medium',
                'tags': 'logs, errors, system'
            },
            {
                'title': 'Email Lists',
                'query': 'filetype:txt "email" OR "mail" "@" site:*.edu',
                'description': 'Find text files containing email addresses on educational sites.',
                'category': 'Sensitive Information',
                'difficulty': 'intermediate',
                'risk_level': 'medium',
                'tags': 'email, contacts, personal'
            },
            {
                'title': 'Server Info Pages',
                'query': 'intitle:"Apache Status" "Apache Server Status for"',
                'description': 'Find Apache server status pages that reveal server information.',
                'category': 'Sensitive Information',
                'difficulty': 'intermediate',
                'risk_level': 'medium',
                'tags': 'apache, server, status'
            },
            {
                'title': 'Password Files',
                'query': 'filetype:txt "password" OR "passwd" OR "pwd"',
                'description': 'Search for text files that might contain passwords.',
                'category': 'Sensitive Information',
                'difficulty': 'advanced',
                'risk_level': 'critical',
                'tags': 'password, credentials, security'
            },
            {
                'title': 'Backup Files',
                'query': 'filetype:bak OR filetype:backup OR filetype:old',
                'description': 'Find backup files that might contain sensitive data.',
                'category': 'File Discovery',
                'difficulty': 'intermediate',
                'risk_level': 'high',
                'tags': 'backup, old, archive'
            },
            {
                'title': 'FTP Files',
                'query': 'intitle:"index of" inurl:ftp',
                'description': 'Discover FTP directory listings.',
                'category': 'Directory Listing',
                'difficulty': 'beginner',
                'risk_level': 'medium',
                'tags': 'ftp, directory, files'
            },
            {
                'title': 'Git Repositories',
                'query': 'inurl:.git/config OR inurl:.git/HEAD',
                'description': 'Find exposed Git repositories that might contain source code.',
                'category': 'Configuration Files',
                'difficulty': 'advanced',
                'risk_level': 'high',
                'tags': 'git, repository, source'
            },
            {
                'title': 'Database Connection Strings',
                'query': 'filetype:php "mysql_connect" OR "mysql_pconnect"',
                'description': 'Find PHP files with database connection information.',
                'category': 'Database Files',
                'difficulty': 'advanced',
                'risk_level': 'critical',
                'tags': 'php, mysql, connection'
            },
            {
                'title': 'Error Messages',
                'query': 'intitle:"Error" OR intitle:"Warning" "SQL" OR "MySQL"',
                'description': 'Find pages with SQL error messages that might reveal database structure.',
                'category': 'Error Pages',
                'difficulty': 'intermediate',
                'risk_level': 'medium',
                'tags': 'error, sql, database'
            },
            {
                'title': 'WordPress Config Files',
                'query': 'filetype:txt "wp-config.php" OR filetype:php "wp-config"',
                'description': 'Find WordPress configuration files.',
                'category': 'Configuration Files',
                'difficulty': 'intermediate',
                'risk_level': 'critical',
                'tags': 'wordpress, config, php'
            },
            {
                'title': 'Drupal Sites',
                'query': 'inurl:"/user/login" "Drupal"',
                'description': 'Find Drupal CMS login pages.',
                'category': 'Web Application',
                'difficulty': 'beginner',
                'risk_level': 'low',
                'tags': 'drupal, cms, login'
            },
            {
                'title': 'Joomla Sites',
                'query': 'inurl:"/administrator/index.php" "Joomla"',
                'description': 'Discover Joomla CMS administrator interfaces.',
                'category': 'Web Application',
                'difficulty': 'beginner',
                'risk_level': 'medium',
                'tags': 'joomla, cms, admin'
            },
            {
                'title': 'SSH Private Keys',
                'query': 'filetype:key "BEGIN RSA PRIVATE KEY" OR "BEGIN DSA PRIVATE KEY"',
                'description': 'Find SSH private key files that could allow unauthorized access.',
                'category': 'Sensitive Information',
                'difficulty': 'advanced',
                'risk_level': 'critical',
                'tags': 'ssh, private key, security'
            }
        ]

        # Get or create a default user for the dorks
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(f'Created admin user with password: admin123')

        for dork_data in dorks_data:
            category = categories[dork_data['category']]
            dork, created = GoogleDork.objects.get_or_create(
                title=dork_data['title'],
                defaults={
                    'query': dork_data['query'],
                    'description': dork_data['description'],
                    'category': category,
                    'difficulty': dork_data['difficulty'],
                    'risk_level': dork_data['risk_level'],
                    'tags': dork_data['tags'],
                    'created_by': user
                }
            )
            if created:
                self.stdout.write(f'Created dork: {dork.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded sample data!\n'
                f'Categories: {DorkCategory.objects.count()}\n'
                f'Dorks: {GoogleDork.objects.count()}\n'
                f'Admin user: admin / admin123'
            )
        )