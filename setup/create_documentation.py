#!/usr/bin/env python3
"""
Setup Guide - Technical Documentation

This script provides technical setup instructions for the Business Finder & Website Generator system.
"""

import os
import sys
import json
import sqlite3
from datetime import datetime

def create_setup_guide():
    """Create a technical setup guide for the system."""
    
    guide = """# Business Finder & Website Generator System
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
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
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
"""
    
    # Create the docs directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    # Write the guide to a file
    with open('docs/technical_setup_guide.md', 'w') as f:
        f.write(guide)
    
    print(f"Technical setup guide created at docs/technical_setup_guide.md")
    
    return 'docs/technical_setup_guide.md'

def create_api_key_reference():
    """Create a reference guide for required API keys."""
    
    reference = """# API Key Reference Guide

## Required API Keys and Services

This document provides detailed information about the API keys and external services required for the Business Finder & Website Generator system.

## 1. Google Maps API

### Purpose
The Google Maps API is used by the Business Finder tool to search for local businesses, retrieve their information, and determine which ones don't have websites.

### Required APIs
- **Places API**: Search for businesses by location and category
- **Geocoding API**: Convert addresses to coordinates
- **Maps JavaScript API**: Display maps in the web interface

### Setup Instructions
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Navigate to "APIs & Services" > "Library"
4. Enable the following APIs:
   - Places API
   - Geocoding API
   - Maps JavaScript API
5. Go to "APIs & Services" > "Credentials"
6. Click "Create Credentials" > "API Key"
7. Restrict the API key:
   - Application restrictions: HTTP referrers
   - API restrictions: Select the enabled APIs

### Usage in the System
- Business search functionality
- Address validation
- Location-based filtering

### Pricing
- $200 free monthly credit
- Places API: $17 per 1,000 requests after free credit
- Geocoding API: $5 per 1,000 requests after free credit
- [Full pricing details](https://cloud.google.com/maps-platform/pricing)

### Environment Variable
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

## 2. SendGrid API

### Purpose
SendGrid is used for sending personalized outreach emails to businesses and tracking their engagement.

### Required Features
- **Mail Send API**: Send emails programmatically
- **Email Templates**: Store and use email templates
- **Event Webhook**: Track email opens, clicks, and replies

### Setup Instructions
1. Sign up at [SendGrid](https://sendgrid.com/)
2. Verify your sender identity:
   - Go to "Settings" > "Sender Authentication"
   - Follow the steps to verify your domain or email
3. Create an API key:
   - Go to "Settings" > "API Keys"
   - Click "Create API Key"
   - Select "Full Access" or customize with at least "Mail Send" permissions
4. Set up event tracking (optional but recommended):
   - Go to "Settings" > "Mail Settings" > "Event Webhook"
   - Enter your webhook URL (your server endpoint that will receive events)
   - Select events to track (opens, clicks, etc.)

### Usage in the System
- Sending initial outreach emails
- Sending follow-up emails
- Tracking email engagement
- Analyzing message effectiveness

### Pricing
- Free tier: 100 emails per day
- Essentials plan: $14.95/month for 50,000 emails
- Pro plan: $89.95/month for 100,000 emails
- [Full pricing details](https://sendgrid.com/pricing/)

### Environment Variable
```
SENDGRID_API_KEY=your_api_key_here
FROM_EMAIL=your_verified_email@example.com
FROM_NAME=Your Name
```

## 3. Calendly API

### Purpose
Calendly is used for appointment scheduling, allowing businesses to book consultations directly through their websites.

### Required Plan
- Professional plan or higher (required for API access)

### Setup Instructions
1. Sign up at [Calendly](https://calendly.com/)
2. Upgrade to the Professional plan
3. Set up your event types:
   - Go to "Event Types" > "Create"
   - Configure your consultation event(s)
4. Generate an API key:
   - Go to "Integrations" > "API"
   - Click "Generate New Token"
   - Give it a name and select appropriate permissions
5. Get your User URI:
   - This is in the format `https://api.calendly.com/users/XXXXXXXXXXXXXXXXXXXX`
   - You can get this by making a request to the Calendly API with your token

### Usage in the System
- Embedding booking widgets in generated websites
- Tracking scheduled appointments
- Integrating appointments with the lead management system

### Pricing
- Free: Basic scheduling
- Premium: $8/month (no API access)
- Professional: $12/month (includes API access)
- Teams: $16/user/month
- [Full pricing details](https://calendly.com/pricing)

### Environment Variables
```
CALENDLY_API_KEY=your_api_key_here
CALENDLY_USER_URI=your_user_uri_here
```

## 4. Domain and Hosting (Optional)

### Purpose
For hosting the PageAndBrand website and client websites.

### Recommended Providers
- **Domain Registration**: Namecheap, GoDaddy, Google Domains
- **Web Hosting**: DigitalOcean, AWS, Netlify, Vercel

### Setup Instructions
1. Register your domain(s):
   - pageandbrand.co.uk
   - pageandbrand.com
2. Set up hosting:
   - Create an account with your chosen provider
   - Set up a server or hosting plan
   - Configure DNS to point your domains to your hosting
3. Set up SSL certificates:
   - Use Let's Encrypt for free SSL
   - Or use SSL provided by your hosting company

### Usage in the System
- Hosting the PageAndBrand website
- Hosting client websites
- Deploying generated websites

### Pricing
- Domain registration: ~$10-15/year per domain
- Basic hosting: ~$5-10/month
- SSL certificates: Free with Let's Encrypt

## API Key Security Best Practices

1. **Never commit API keys to version control**
   - Use environment variables or a .env file (excluded from git)
   - Use a secrets manager for production environments

2. **Apply the principle of least privilege**
   - Only grant the permissions each API key needs
   - Use restricted API keys when possible

3. **Implement API key rotation**
   - Change keys periodically (every 3-6 months)
   - Have a process for updating keys across all systems

4. **Monitor API usage**
   - Watch for unusual patterns that might indicate compromise
   - Set up alerts for unexpected usage spikes

5. **Use API key restrictions**
   - Restrict by IP address when possible
   - Restrict by HTTP referrer for browser-based APIs
   - Set usage quotas to limit potential abuse

6. **Secure your environment variables**
   - Protect access to your .env file
   - Use encrypted environment variables in production

7. **Have a response plan for compromised keys**
   - Know how to quickly revoke and replace each type of key
   - Document the process for key replacement
"""
    
    # Create the docs directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    # Write the reference to a file
    with open('docs/api_key_reference.md', 'w') as f:
        f.write(reference)
    
    print(f"API key reference created at docs/api_key_reference.md")
    
    return 'docs/api_key_reference.md'

def create_quick_start_guide():
    """Create a quick start guide for the system."""
    
    guide = """# Quick Start Guide

## Business Finder & Website Generator System

This guide will help you quickly set up and start using the Business Finder & Website Generator system.

## 1. Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- Git

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/business_finder_project.git
cd business_finder_project

# Install Python dependencies
pip3 install -r requirements.txt

# Install Node.js dependencies
cd ui
npm install
cd ..

# Create environment file
cp .env.example .env
# Edit .env with your API keys

# Initialize the database
python3 setup/initialize_database.py

# Start the application
python3 ui/app.py
```

## 2. Finding Businesses Without Websites

### Using the Command Line

```bash
# Basic search
python3 tools/business_finder_cli.py --location "London" --category "restaurants" --radius 5000 --no-website-only

# Save results to CSV
python3 tools/business_finder_cli.py --location "Manchester" --category "hair salon" --radius 10000 --no-website-only --output-format csv --output-file salons.csv
```

### Using the Web Interface

1. Open your browser and go to `http://localhost:5000`
2. Navigate to the "Business Finder" tab
3. Enter location, category, and search radius
4. Check "Only businesses without websites"
5. Click "Search"
6. Export or add promising leads to your database

## 3. Creating Outreach Campaigns

### Setting Up Email Templates

1. Go to the "Templates" tab
2. Click "New Template"
3. Create templates for:
   - Initial contact
   - Follow-up #1
   - Follow-up #2
4. Use placeholders like `{business_name}` for personalization

### Creating a Campaign

1. Go to the "Campaigns" tab
2. Click "New Campaign"
3. Select your target businesses
4. Choose your templates
5. Set follow-up schedule
6. Start the campaign

## 4. Generating Websites

### Using the Command Line

```bash
# Basic website
python3 website_generator/website_generator_cli.py --business-name "Test Business" --business-category "Restaurant" --business-description "A test business description." --business-address "123 Test St, London" --business-phone "+44 20 1234 5678" --business-email "info@example.com" --template modern --color-scheme blue

# Website with features
python3 website_generator/website_generator_cli.py --business-name "Test Business" --business-category "Restaurant" --business-description "A test business description." --business-address "123 Test St, London" --business-phone "+44 20 1234 5678" --business-email "info@example.com" --template modern --color-scheme blue --enable-booking --enable-menu --enable-gallery
```

### Using the Web Interface

1. Go to the "Website Generator" tab
2. Select a business from your leads
3. Choose template and color scheme
4. Select optional features
5. Click "Generate Website"
6. Preview and download the website

## 5. Analyzing Results

1. Go to the "Analytics" tab
2. View key metrics:
   - Open rates
   - Reply rates
   - Booking rates
3. Compare template performance
4. Generate reports for specific date ranges

## 6. Managing Your PageAndBrand Website

1. Customize the website in the `pageandbrand` directory
2. Update content, images, and pricing
3. Deploy to your domain (pageandbrand.co.uk and .com)

## 7. Next Steps

- Read the full [User Manual](user_manual.md) for detailed instructions
- Check the [Technical Setup Guide](technical_setup_guide.md) for advanced configuration
- Review the [API Key Reference](api_key_reference.md) for external service setup

## 8. Getting Help

If you encounter any issues:
- Check the Troubleshooting section in the User Manual
- Review error logs in the `logs` directory
- Contact support at support@pageandbrand.co.uk
"""
    
    # Create the docs directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    # Write the guide to a file
    with open('docs/quick_start_guide.md', 'w') as f:
        f.write(guide)
    
    print(f"Quick start guide created at docs/quick_start_guide.md")
    
    return 'docs/quick_start_guide.md'

def main():
    """Create all documentation files."""
    technical_guide = create_setup_guide()
    api_reference = create_api_key_reference()
    quick_start = create_quick_start_guide()
    
    print("\nDocumentation created successfully:")
    print(f"- Technical Setup Guide: {technical_guide}")
    print(f"- API Key Reference: {api_reference}")
    print(f"- Quick Start Guide: {quick_start}")
    print(f"- User Manual: docs/user_manual.md (already created)")
    
    # Create a README file that links to all documentation
    readme = f"""# Business Finder & Website Generator System

A comprehensive system for finding local businesses without websites, conducting personalized outreach, and generating professional websites.

## Documentation

- [Quick Start Guide](docs/quick_start_guide.md) - Get up and running quickly
- [User Manual](docs/user_manual.md) - Complete user instructions
- [Technical Setup Guide](docs/technical_setup_guide.md) - Detailed technical setup
- [API Key Reference](docs/api_key_reference.md) - Guide to required external services

## Features

- Business finder tool
- Personalized outreach system
- Outreach automation
- Lead management dashboard
- Website generator with optional features
- Calendly integration
- Analytics system
- PageAndBrand website

## Installation

See the [Quick Start Guide](docs/quick_start_guide.md) for installation instructions.

## License

This project is proprietary and confidential.
"""
    
    with open('README.md', 'w') as f:
        f.write(readme)
    
    print(f"- README: README.md")

if __name__ == "__main__":
    main()
