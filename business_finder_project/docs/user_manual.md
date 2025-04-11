# Business Finder & Website Generator System
# User Manual and Setup Guide

## Table of Contents
1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Required API Keys and Setup](#required-api-keys-and-setup)
4. [Installation Guide](#installation-guide)
5. [Business Finder Tool](#business-finder-tool)
6. [Outreach System](#outreach-system)
7. [Website Generator](#website-generator)
8. [Analytics Dashboard](#analytics-dashboard)
9. [PageAndBrand Website](#pageandBrand-website)
10. [Maintenance and Updates](#maintenance-and-updates)
11. [Troubleshooting](#troubleshooting)
12. [Support](#support)

## Introduction

This manual provides comprehensive instructions for setting up and using the Business Finder & Website Generator system. This integrated solution helps you identify local businesses without websites, conduct personalized outreach, and generate professional websites for these businesses.

The system is designed for use in London and across England, targeting businesses that don't have an online presence but could benefit from professional website services.

## System Overview

The Business Finder & Website Generator system consists of several integrated components:

1. **Business Finder Tool**: Identifies local businesses without websites using various data sources and filtering methods.

2. **Personalized Outreach System**: Creates customized email templates and manages outreach campaigns.

3. **Outreach Automation**: Schedules emails, tracks responses, and provides analytics on message effectiveness.

4. **Lead Management Dashboard**: Provides an overview of potential clients and their status.

5. **Website Generator**: Creates customized websites with optional features like booking systems, menu displays, and more.

6. **Calendly Integration**: Allows clients to book appointments directly through their websites.

7. **Analytics System**: Tracks the effectiveness of outreach messages and provides insights for improvement.

8. **PageAndBrand Website**: Your own business website showcasing your services to potential clients.

## Required API Keys and Setup

To fully utilize this system, you'll need to obtain the following API keys and credentials:

### 1. Google Maps API Key
- **Purpose**: Used by the Business Finder tool to search for local businesses
- **How to obtain**: 
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Create a new project
  3. Enable the Google Maps Platform and Places API
  4. Generate an API key
  5. Restrict the API key to the Places API for security
- **Cost**: Google provides $200 monthly credit, which is sufficient for moderate usage

### 2. Email Service Provider API
- **Purpose**: Used for sending automated outreach emails
- **Recommended providers**: SendGrid, Mailchimp, or Amazon SES
- **How to obtain SendGrid API key**:
  1. Sign up at [SendGrid](https://sendgrid.com/)
  2. Navigate to Settings > API Keys
  3. Create a new API key with appropriate permissions
- **Cost**: SendGrid offers a free tier with 100 emails/day

### 3. Calendly API Key
- **Purpose**: Used for appointment booking integration
- **How to obtain**:
  1. Sign up for a Calendly account at [Calendly](https://calendly.com/)
  2. Go to Integrations > API
  3. Generate a Personal Access Token
- **Cost**: Requires Calendly Professional plan ($12/month) for API access

### 4. Domain and Hosting
- **Purpose**: For hosting the PageAndBrand website and client websites
- **Recommended providers**: Namecheap for domains, DigitalOcean for hosting
- **Cost**: 
  - Domains: ~$10-15/year per domain
  - Hosting: Starting at $5/month (can host multiple websites)

## Installation Guide

### System Requirements
- Python 3.8 or higher
- Node.js 14 or higher
- SQLite database
- 2GB RAM minimum, 4GB recommended
- 10GB storage minimum

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/business_finder_project.git
   cd business_finder_project
   ```

2. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Install Node.js dependencies**
   ```bash
   cd ui
   npm install
   cd ..
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   SENDGRID_API_KEY=your_sendgrid_api_key
   CALENDLY_API_KEY=your_calendly_api_key
   CALENDLY_USER_URI=your_calendly_user_uri
   ```

5. **Initialize the database**
   ```bash
   python3 setup/initialize_database.py
   ```

6. **Start the application**
   ```bash
   python3 ui/app.py
   ```

7. **Access the dashboard**
   Open your browser and navigate to `http://localhost:5000`

## Business Finder Tool

The Business Finder tool helps you identify local businesses without websites that could benefit from your services.

### Using the Command Line Interface

1. **Basic search**
   ```bash
   python3 tools/business_finder_cli.py --location "London" --category "restaurants" --radius 5000
   ```

2. **Advanced search with filters**
   ```bash
   python3 tools/business_finder_cli.py --location "Manchester" --category "hair salon" --radius 10000 --no-website-only --output-format csv --output-file salons.csv
   ```

3. **Available parameters**
   - `--location`: City or area to search (required)
   - `--category`: Business category (required)
   - `--radius`: Search radius in meters (default: 5000)
   - `--no-website-only`: Only return businesses without websites
   - `--limit`: Maximum number of results (default: 50)
   - `--output-format`: Output format (json or csv, default: json)
   - `--output-file`: File to save results (default: prints to console)

### Using the Web Interface

1. Navigate to the "Business Finder" tab in the dashboard
2. Enter location, category, and radius
3. Toggle "Only businesses without websites" if desired
4. Click "Search" to find businesses
5. View results in the table
6. Export results as CSV or JSON
7. Add promising businesses to your leads list

### Best Practices

- Start with specific neighborhoods rather than entire cities
- Focus on business categories that benefit most from websites (restaurants, salons, etc.)
- Use the "no-website-only" filter to find the most promising leads
- Export and save your results regularly
- Add notes about each business as you research them

## Outreach System

The Outreach System helps you create personalized email templates and manage outreach campaigns.

### Creating Email Templates

1. Navigate to the "Templates" tab in the dashboard
2. Click "New Template"
3. Fill in the template details:
   - Name: Internal name for the template
   - Subject: Email subject line
   - Body: Email content
   - Category: Type of template (initial contact, follow-up, etc.)
   - Tags: Keywords for organizing templates
4. Use placeholders for personalization:
   - `{business_name}`: Name of the business
   - `{owner_name}`: Name of the business owner
   - `{category}`: Business category
   - `{location}`: Business location
   - `{calendly_link}`: Your Calendly booking link
5. Click "Save Template"

### Managing Outreach Campaigns

1. Navigate to the "Campaigns" tab in the dashboard
2. Click "New Campaign"
3. Fill in the campaign details:
   - Name: Campaign name
   - Description: Campaign purpose
   - Start Date: When to begin sending emails
   - End Date: When to stop sending emails
   - Target Audience: Which businesses to target
4. Select templates for:
   - Initial Contact
   - Follow-up #1 (sent if no response after X days)
   - Follow-up #2 (sent if no response after Y days)
5. Set the follow-up schedule
6. Click "Create Campaign"

### Tracking Responses

1. Navigate to the "Responses" tab in the dashboard
2. View all responses organized by campaign
3. Click on a response to see the full conversation
4. Add notes or change the lead status
5. Schedule follow-up actions

### Best Practices

- Personalize templates with specific details about each business
- Keep initial emails concise and focused on value proposition
- Include a clear call-to-action (book a call, reply with questions, etc.)
- Follow up 2-3 times with different angles if there's no response
- Test different templates and analyze which ones perform best
- Adjust your approach based on analytics data

## Website Generator

The Website Generator creates professional websites for businesses with various customizable features.

### Using the Command Line Interface

1. **Basic website generation**
   ```bash
   python3 website_generator/website_generator_cli.py --business-name "Delicious Corner Cafe" --business-category "Restaurant" --business-description "A cozy cafe serving delicious food and coffee." --business-address "123 High Street, London" --business-phone "+44 20 1234 5678" --business-email "info@example.com" --template modern --color-scheme blue
   ```

2. **Website with optional features**
   ```bash
   python3 website_generator/website_generator_cli.py --business-name "Elite Hair Salon" --business-category "Hair Salon" --business-description "Premium hair styling and treatments." --business-address "456 Main Road, Manchester" --business-phone "+44 20 9876 5432" --business-email "info@example.com" --template classic --color-scheme purple --enable-booking --enable-gallery --enable-testimonials --enable-contact-form --enable-calendly --calendly-link "https://calendly.com/yourusername/consultation"
   ```

3. **Available parameters**
   - Basic information (all required):
     - `--business-name`: Name of the business
     - `--business-category`: Category of the business
     - `--business-description`: Description of the business
     - `--business-address`: Address of the business
     - `--business-phone`: Phone number of the business
     - `--business-email`: Email address of the business
   
   - Design options:
     - `--template`: Website template (modern, classic, or minimal, default: modern)
     - `--color-scheme`: Color scheme (blue, green, red, or purple, default: blue)
   
   - Optional features (all disabled by default):
     - `--enable-booking`: Enable booking system
     - `--enable-menu`: Enable menu display
     - `--enable-gallery`: Enable photo gallery
     - `--enable-testimonials`: Enable testimonials
     - `--enable-contact-form`: Enable contact form
     - `--enable-social-media`: Enable social media integration
     - `--enable-calendly`: Enable Calendly integration
     - `--calendly-link`: Calendly link (required if --enable-calendly is set)
   
   - Output options:
     - `--output-dir`: Output directory for generated website

### Using the Web Interface

1. Navigate to the "Website Generator" tab in the dashboard
2. Select a business from your leads or enter new business details
3. Choose a template and color scheme
4. Select optional features
5. Preview the website
6. Generate and download the website files
7. Deploy the website to hosting

### Available Templates

1. **Modern**
   - Clean, minimalist design
   - Large hero image
   - Smooth animations
   - Mobile-first approach

2. **Classic**
   - Traditional business layout
   - Multiple content sections
   - Sidebar navigation
   - Emphasis on information

3. **Minimal**
   - Ultra-simple design
   - Focus on essential information
   - Fast loading
   - Limited graphics

### Optional Features

1. **Booking System**
   - Allows customers to book appointments
   - Integrates with business calendar
   - Sends confirmation emails
   - Prevents double-bookings

2. **Menu Display**
   - Attractive menu layout
   - Categories and items
   - Prices and descriptions
   - Optional images

3. **Photo Gallery**
   - Responsive image grid
   - Lightbox functionality
   - Caption support
   - Lazy loading for performance

4. **Testimonials**
   - Customer reviews section
   - Star ratings
   - Customer photos (optional)
   - Carousel display

5. **Contact Form**
   - User-friendly form
   - Form validation
   - Anti-spam protection
   - Email notifications

6. **Social Media Integration**
   - Social media links
   - Share buttons
   - Social feed display (optional)
   - Follow counters (optional)

7. **Calendly Integration**
   - Embedded Calendly widget
   - Appointment scheduling
   - Automatic confirmations
   - Calendar syncing

### Best Practices

- Choose templates that match the business style and industry
- Enable only features that the business will actually use
- Use high-quality images for the best visual impact
- Keep content concise and focused on customer needs
- Test the website on multiple devices before delivery
- Provide the business with instructions for updating content

## Analytics Dashboard

The Analytics Dashboard provides insights into the effectiveness of your outreach efforts and helps you optimize your approach.

### Accessing Analytics

1. Navigate to the "Analytics" tab in the dashboard
2. View the main dashboard for an overview of key metrics
3. Use the date range selector to analyze specific periods
4. Export reports as needed

### Key Metrics

1. **Outreach Performance**
   - Emails sent
   - Open rate
   - Reply rate
   - Booking rate
   - Conversion rate (leads to clients)

2. **Template Effectiveness**
   - Performance comparison between templates
   - Subject line analysis
   - Content pattern analysis
   - Recommendations for improvement

3. **Campaign Analysis**
   - Campaign comparison
   - Timeline of results
   - Target audience response rates
   - ROI calculation

4. **Lead Funnel**
   - Visualization of lead progression
   - Conversion rates between stages
   - Bottleneck identification
   - Opportunity forecasting

### Generating Reports

1. Navigate to the "Reports" section
2. Select report type:
   - Performance Summary
   - Template Analysis
   - Campaign Comparison
   - Lead Funnel Analysis
3. Choose date range
4. Select output format (HTML or JSON)
5. Generate and download the report

### Using Analytics to Improve Results

1. **Identify top-performing templates**
   - Note common elements in successful templates
   - Adapt other templates to include these elements
   - A/B test variations to further optimize

2. **Optimize outreach timing**
   - Analyze when responses are most likely
   - Schedule campaigns accordingly
   - Adjust follow-up timing based on data

3. **Refine target audience**
   - Identify business categories with highest response rates
   - Focus efforts on most promising segments
   - Develop specialized templates for high-value segments

4. **Improve conversion funnel**
   - Identify where leads are dropping off
   - Strengthen weak points in the process
   - Implement automated nurturing for stalled leads

## PageAndBrand Website

The PageAndBrand website showcases your services to potential clients who are looking for website development services.

### Website Structure

1. **Home Page**
   - Hero section with value proposition
   - Key features and benefits
   - Call-to-action for consultation

2. **Services Section**
   - Website Design
   - Booking Systems
   - Local SEO
   - Menu & Product Displays
   - Photo Galleries
   - Testimonials & Reviews

3. **How It Works Section**
   - Step-by-step process explanation
   - Consultation to launch timeline
   - Client involvement details

4. **Portfolio Section**
   - Showcase of client websites
   - Before/after examples
   - Industry-specific samples

5. **Testimonials Section**
   - Client success stories
   - Results and benefits achieved
   - Social proof elements

6. **Pricing Section**
   - Package options and pricing
   - Feature comparison
   - Upsell opportunities

7. **Contact Section**
   - Contact form
   - Business information
   - Social media links

8. **Calendly Integration**
   - Appointment scheduling
   - Consultation booking
   - Automatic confirmations

### Customizing Your Website

1. **Update Content**
   - Edit the HTML files in the `pageandbrand` directory
   - Modify text, images, and links as needed
   - Update pricing and package information

2. **Change Design Elements**
   - Modify the CSS in `styles.css`
   - Update color scheme and typography
   - Adjust layout and spacing

3. **Add Portfolio Items**
   - Create new portfolio entries in the HTML
   - Add images to the `images` directory
   - Write compelling descriptions

4. **Update Testimonials**
   - Add real client testimonials as you acquire them
   - Include photos and business names (with permission)
   - Highlight specific results and benefits

### Deploying to Your Domain

1. **Set up hosting**
   - Sign up with a web hosting provider
   - Set up a hosting account for your domain

2. **Configure domain**
   - Point your domain (pageandbrand.co.uk and .com) to your hosting
   - Set up SSL certificates for security

3. **Upload website files**
   - Upload all files from the `pageandbrand` directory to your hosting
   - Maintain the directory structure

4. **Test the website**
   - Check all pages and links
   - Test on multiple devices and browsers
   - Verify contact form and Calendly integration

## Maintenance and Updates

### Regular Maintenance Tasks

1. **Database Backup**
   - Back up the SQLite database weekly
   - Store backups in a secure location
   - Test restoration periodically

2. **API Key Rotation**
   - Update API keys every 3-6 months
   - Revoke unused or compromised keys
   - Update environment variables with new keys

3. **Software Updates**
   - Check for Python and Node.js updates monthly
   - Update dependencies using pip and npm
   - Test system after updates

4. **Content Refresh**
   - Update templates with fresh content
   - Revise outreach strategies based on analytics
   - Add new portfolio items to your website

### System Expansion

1. **Adding New Features**
   - The system is modular and can be extended
   - New modules can be added to the existing structure
   - Follow the established coding patterns

2. **Scaling Considerations**
   - The SQLite database can be migrated to PostgreSQL for larger scale
   - The web interface can be deployed to a production server
   - Email sending can be scaled with enterprise ESP plans

## Troubleshooting

### Common Issues and Solutions

1. **Business Finder Not Returning Results**
   - Check Google Maps API key validity
   - Verify API key has correct permissions
   - Ensure location format is correct
   - Try reducing search radius

2. **Email Sending Failures**
   - Verify SendGrid API key
   - Check daily sending limits
   - Ensure email templates have valid syntax
   - Check for spam trigger words in content

3. **Website Generator Errors**
   - Ensure all required parameters are provided
   - Check for valid template and color scheme values
   - Verify Calendly link format if enabled
   - Check output directory permissions

4. **Dashboard Access Issues**
   - Verify Flask server is running
   - Check port availability
   - Ensure database file is not corrupted
   - Clear browser cache and cookies

### Error Logs

- Application logs are stored in the `logs` directory
- Each component has its own log file
- Check these logs for detailed error information
- Include relevant log excerpts when seeking support

## Support

For additional assistance:

- Email: support@pageandbrand.co.uk
- Phone: +44 20 1234 5678
- Hours: Monday-Friday, 9am-5pm GMT

When contacting support, please include:
- Detailed description of the issue
- Steps to reproduce the problem
- Error messages or screenshots
- System information (OS, Python version, etc.)
