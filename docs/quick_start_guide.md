# Quick Start Guide

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
