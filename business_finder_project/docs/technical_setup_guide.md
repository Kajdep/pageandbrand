# Business Finder & Website Generator System
# Technical Setup Guide

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Dependencies](#dependencies)
3. [API Keys and External Services](#api-keys-and-external-services)
4. [Database Setup](#database-setup)
5. [Environment Configuration](#environment-configuration)
6. [Installation Steps](#installation-steps)
7. [Testing and Verification](#testing-and-verification)
8. [Deployment Options](#deployment-options)
9. [Security Considerations](#security-considerations)
10. [Backup and Recovery](#backup-and-recovery)

## System Architecture

The Business Finder & Website Generator system follows a modular architecture with the following components:

```
business_finder_project/
├── analytics/              # Message analytics modules
├── data/                   # Data storage directory
├── docs/                   # Documentation
├── integrations/           # Third-party integrations (Calendly, etc.)
├── outreach/               # Email outreach system
├── pageandbrand/           # PageAndBrand website files
├── tools/                  # Business finder tools
├── ui/                     # Web interface
├── website_generator/      # Website generator modules
└── setup/                  # Setup and initialization scripts
```

### Component Interactions

- **Business Finder** → Identifies businesses and stores data in the database
- **Outreach System** → Uses business data to send personalized messages
- **Website Generator** → Creates websites based on business information
- **Analytics** → Tracks message effectiveness and provides insights
- **UI** → Provides a web interface for all components
- **Integrations** → Connects with external services like Calendly

## Dependencies

### System Requirements
- Linux, macOS, or Windows operating system
- Python 3.8 or higher
- Node.js 14 or higher
- SQLite 3
- 2GB RAM minimum, 4GB recommended
- 10GB storage minimum

### Python Dependencies
```
# Core dependencies
flask==2.0.1
requests==2.26.0
pandas==1.3.3
numpy==1.21.2
matplotlib==3.4.3
google-api-python-client==2.23.0
sendgrid==6.8.0
python-dotenv==0.19.1
jinja2==3.0.1
werkzeug==2.0.1
sqlalchemy==1.4.25

# Development dependencies
pytest==6.2.5
black==21.9b0
flake8==3.9.2
```

### Node.js Dependencies
```
{
  "dependencies": {
    "bootstrap": "^5.1.3",
    "chart.js": "^3.5.1",
    "jquery": "^3.6.0",
    "popper.js": "^2.10.2"
  },
  "devDependencies": {
    "webpack": "^5.58.1",
    "webpack-cli": "^4.9.0"
  }
}
```

## API Keys and External Services

### Google Maps API
- **Purpose**: Used to find local businesses
- **Required Endpoints**: 
  - Places API
  - Geocoding API
  - Maps JavaScript API
- **Setup Process**:
  1. Create a Google Cloud Platform account
  2. Create a new project
  3. Enable the required APIs
  4. Create an API key with appropriate restrictions
  5. Set up billing (credit card required, but $200 monthly credit provided)
- **Environment Variable**: `GOOGLE_MAPS_API_KEY`
- **Documentation**: [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- **Pricing**: [Google Maps Platform Pricing](https://cloud.google.com/maps-platform/pricing)

### SendGrid (Email Service)
- **Purpose**: Sending outreach emails
- **Required Features**:
  - Mail Send API
  - Email Templates
  - Email Activity Tracking
- **Setup Process**:
  1. Create a SendGrid account
  2. Verify your domain
  3. Create an API key with Mail Send permissions
  4. Set up event webhooks for tracking (optional)
- **Environment Variable**: `SENDGRID_API_KEY`
- **Documentation**: [SendGrid API Documentation](https://docs.sendgrid.com/api-reference)
- **Pricing**: [SendGrid Pricing](https://sendgrid.com/pricing/)

### Calendly
- **Purpose**: Appointment scheduling
- **Required Plan**: Professional or higher (for API access)
- **Setup Process**:
  1. Create a Calendly account
  2. Upgrade to Professional plan
  3. Create event types for consultations
  4. Generate a Personal Access Token
  5. Get your Calendly user URI
- **Environment Variables**: 
  - `CALENDLY_API_KEY`
  - `CALENDLY_USER_URI`
- **Documentation**: [Calendly API Documentation](https://developer.calendly.com/)
- **Pricing**: [Calendly Pricing](https://calendly.com/pricing)

## Database Setup

The system uses SQLite for data storage, which requires minimal setup.

### Database Schema

The database includes the following tables:
- `businesses`: Stores information about businesses
- `messages`: Stores outreach messages
- `message_templates`: Stores email templates
- `message_analytics`: Tracks message performance
- `calendly_events`: Stores appointment information
- `calendly_event_types`: Stores available event types
- `websites`: Stores generated website information

### Initialization

The database is automatically created and initialized when the system is first run. You can also manually initialize it:

```bash
python3 setup/initialize_database.py
```

### Migration

If you need to migrate to a more robust database system (e.g., PostgreSQL), a migration script is provided:

```bash
python3 setup/migrate_database.py --target postgresql --connection-string "postgresql://user:password@localhost/dbname"
```

## Environment Configuration

The system uses environment variables for configuration. Create a `.env` file in the root directory with the following variables:

```
# API Keys
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
SENDGRID_API_KEY=your_sendgrid_api_key
CALENDLY_API_KEY=your_calendly_api_key
CALENDLY_USER_URI=your_calendly_user_uri

# Email Configuration
FROM_EMAIL=your@email.com
FROM_NAME=Your Name

# Application Settings
DEBUG=False
SECRET_KEY=generate_a_secure_random_key
DATABASE_PATH=data/outreach.db
PORT=5000
```

### Generating a Secure Secret Key

```python
import secrets
print(secrets.token_hex(16))
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/business_finder_project.git
cd business_finder_project
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Install Node.js Dependencies

```bash
cd ui
npm install
cd ..
```

### 5. Set Up Environment Variables

Create a `.env` file as described in the Environment Configuration section.

### 6. Initialize the Database

```bash
python3 setup/initialize_database.py
```

### 7. Run the Application

```bash
python3 ui/app.py
```

### 8. Access the Dashboard

Open your browser and navigate to `http://localhost:5000`

## Testing and Verification

### Running Tests

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_business_finder.py
pytest tests/test_outreach.py
pytest tests/test_website_generator.py
```

### Verification Checklist

1. **Business Finder**
   - [ ] Can search for businesses by location and category
   - [ ] Can filter businesses without websites
   - [ ] Can export results to CSV/JSON

2. **Outreach System**
   - [ ] Can create and edit email templates
   - [ ] Can send test emails
   - [ ] Can track email opens and replies

3. **Website Generator**
   - [ ] Can generate websites with different templates
   - [ ] Can enable/disable optional features
   - [ ] Can preview and download generated websites

4. **Analytics**
   - [ ] Can view message performance metrics
   - [ ] Can generate performance reports
   - [ ] Can analyze template effectiveness

5. **UI**
   - [ ] All pages load correctly
   - [ ] Forms submit and validate properly
   - [ ] Data is displayed correctly

## Deployment Options

### Local Deployment

The simplest deployment option is to run the application on your local machine:

```bash
python3 ui/app.py
```

### Server Deployment

For production use, deploy the application to a server:

1. **Set up a server** (e.g., DigitalOcean Droplet, AWS EC2)
2. **Install dependencies** (Python, Node.js, etc.)
3. **Clone the repository and install requirements**
4. **Set up environment variables**
5. **Use a production WSGI server**:

```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 ui.app:app
```

6. **Set up a reverse proxy** (Nginx or Apache)
7. **Configure SSL** (Let's Encrypt)

### Docker Deployment

A Dockerfile is provided for containerized deployment:

```bash
# Build the Docker image
docker build -t business-finder .

# Run the container
docker run -p 5000:5000 --env-file .env business-finder
```

## Security Considerations

### API Key Protection
- Store API keys in environment variables, never in code
- Use API key restrictions (IP, referrer, etc.) when possible
- Rotate API keys periodically

### Database Security
- Use parameterized queries to prevent SQL injection
- Backup the database regularly
- Encrypt sensitive data

### Web Security
- Use HTTPS for all connections
- Implement CSRF protection
- Sanitize user inputs
- Keep dependencies updated

### Email Security
- Verify sending domain with SPF and DKIM
- Avoid spam trigger words in templates
- Comply with anti-spam regulations (CAN-SPAM, GDPR)

## Backup and Recovery

### Database Backup

```bash
# Backup the SQLite database
python3 setup/backup_database.py

# Restore from backup
python3 setup/restore_database.py --backup-file backups/outreach_2025-04-10.db
```

### Configuration Backup

Keep a secure backup of your `.env` file and API keys.

### Automated Backups

Set up a cron job for automated backups:

```
# Daily database backup at 2 AM
0 2 * * * cd /path/to/business_finder_project && python3 setup/backup_database.py
```

### Recovery Plan

1. **Minor Issues**: Restore from the latest backup
2. **Major Issues**: Reinstall the application and restore data
3. **API Key Compromise**: Revoke and replace affected keys
4. **Server Failure**: Deploy to a new server and restore data
