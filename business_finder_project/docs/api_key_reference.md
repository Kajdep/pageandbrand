# API Key Reference Guide

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
