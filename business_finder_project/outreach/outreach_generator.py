#!/usr/bin/env python3
"""
Outreach Email Generator

This script generates personalized outreach emails for businesses without websites.
It uses templates and customization based on business data.
"""

import os
import json
import random
import pandas as pd
from datetime import datetime
from string import Template

class OutreachGenerator:
    """Tool to generate personalized outreach emails for businesses without websites."""
    
    def __init__(self):
        """Initialize the OutreachGenerator."""
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.templates_dir = os.path.join(self.base_dir, 'outreach', 'templates')
        self.output_dir = os.path.join(self.base_dir, 'outreach', 'generated')
        
        # Create directories if they don't exist
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize with default templates
        self.create_default_templates()
        
        # Load templates
        self.templates = self.load_templates()
        
    def create_default_templates(self):
        """Create default email templates if they don't exist."""
        default_templates = {
            'initial_contact.txt': """Subject: Boost Your Online Presence for ${business_name}

Dear ${contact_name},

I hope this email finds you well. I recently discovered ${business_name} while researching outstanding ${business_category} in ${location}, and I was impressed by your reputation.

However, I noticed that ${business_name} doesn't currently have a website, which means you might be missing out on potential customers who are searching online for services like yours.

As a web developer specializing in creating effective websites for ${business_category} businesses, I'd love to help you establish a strong online presence. A professional website can:

1. Make your business discoverable to new customers searching online
2. Showcase your services and unique selling points
3. Allow customers to find your location, hours, and contact information 24/7
4. ${custom_benefit}

I've helped several ${business_category} businesses in ${location} increase their customer base through effective websites. I'd be happy to discuss how we could create a website tailored specifically to your needs.

Would you be available for a quick 15-minute call to discuss how a website could benefit ${business_name}? You can book a time that works for you here: [Your Calendly Link]

Looking forward to potentially working together,

[Your Name]
[Your Contact Information]
""",
            'follow_up.txt': """Subject: Following Up: Website for ${business_name}

Dear ${contact_name},

I recently reached out regarding creating a website for ${business_name}. I understand you're busy running your business, so I wanted to follow up.

Having a website is increasingly important for ${business_category} businesses in ${location}. Your competitors are likely already online, and a professional website would help you:

1. Appear in Google searches when potential customers look for ${business_category} services
2. Build credibility and trust with new customers
3. ${custom_benefit}
4. Provide information and services to customers even outside business hours

I specialize in creating affordable, effective websites for businesses like yours. I'd be happy to show you some examples of my work for other ${business_category} businesses.

If you're interested, please book a quick 15-minute call at your convenience: [Your Calendly Link]

Best regards,

[Your Name]
[Your Contact Information]
""",
            'value_proposition.txt': """Subject: How ${business_name} Can Benefit from a Professional Website

Dear ${contact_name},

I hope you're having a great week. I'm reaching out because I believe ${business_name} could significantly benefit from having a professional website.

In today's digital world, over 80% of consumers search online before making purchasing decisions. Without a website, your business is potentially missing out on these customers.

For ${business_category} businesses in ${location}, a website can:

1. Increase visibility to potential customers searching online
2. Provide a platform to showcase your services and expertise
3. Allow for ${custom_feature} functionality
4. Build credibility and trust with new customers
5. ${custom_benefit}

I've helped several businesses similar to yours achieve significant growth through effective websites. For example, one ${business_category} business saw a 40% increase in new customer inquiries within three months of launching their website.

I offer affordable website packages specifically designed for ${business_category} businesses, including:

- Professional design tailored to your brand
- Mobile-friendly layout
- Search engine optimization
- ${custom_feature} integration
- Ongoing support and maintenance

I'd love to discuss how we could create a website that meets your specific needs and budget. Please book a convenient time for a quick call: [Your Calendly Link]

Best regards,

[Your Name]
[Your Contact Information]
"""
        }
        
        for filename, content in default_templates.items():
            filepath = os.path.join(self.templates_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Created default template: {filepath}")
    
    def load_templates(self):
        """Load all email templates from the templates directory."""
        templates = {}
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.templates_dir, filename)
                with open(filepath, 'r') as f:
                    templates[filename] = Template(f.read())
        return templates
    
    def generate_custom_benefit(self, business_category):
        """Generate a custom benefit based on business category."""
        benefits = {
            'restaurant': [
                "Allow customers to view your menu and make reservations online",
                "Showcase your signature dishes with high-quality photos",
                "Highlight special events and promotions to drive more bookings",
                "Enable online ordering for takeaway or delivery services"
            ],
            'plumber': [
                "Let customers request emergency services with a simple online form",
                "Display testimonials from satisfied customers to build trust",
                "Showcase your range of services with detailed descriptions",
                "Allow customers to book appointments online at their convenience"
            ],
            'electrician': [
                "Enable customers to request quotes through an online form",
                "Showcase your certifications and qualifications prominently",
                "Display before-and-after photos of your electrical work",
                "Allow customers to schedule routine maintenance online"
            ],
            'hairdresser': [
                "Let clients book appointments online 24/7",
                "Showcase your portfolio of styles and transformations",
                "Promote special offers and loyalty programs",
                "Allow clients to select their preferred stylist when booking"
            ],
            'dentist': [
                "Enable patients to book appointments and fill forms online",
                "Showcase before-and-after photos of successful treatments",
                "Provide educational content about dental health",
                "Allow patients to request emergency appointments online"
            ],
            'mechanic': [
                "Let customers book service appointments online",
                "Display testimonials from satisfied customers",
                "Showcase your specializations and certifications",
                "Allow customers to request quotes for specific repairs"
            ],
            'cleaner': [
                "Enable customers to book cleaning services online",
                "Showcase your range of cleaning packages",
                "Display testimonials from satisfied customers",
                "Allow customers to specify special cleaning requirements"
            ],
            # Default category for any other business type
            'default': [
                "Showcase testimonials from satisfied customers",
                "Display your portfolio of work and achievements",
                "Highlight your unique selling points and specializations",
                "Allow customers to contact you easily through online forms"
            ]
        }
        
        # Find the most relevant category
        for key in benefits.keys():
            if key in business_category.lower():
                return random.choice(benefits[key])
        
        # If no specific category matches, use default
        return random.choice(benefits['default'])
    
    def generate_custom_feature(self, business_category):
        """Generate a custom feature based on business category."""
        features = {
            'restaurant': [
                "online reservation",
                "menu display",
                "food ordering",
                "table booking"
            ],
            'plumber': [
                "emergency service request",
                "appointment scheduling",
                "quote request",
                "service area map"
            ],
            'electrician': [
                "emergency callout",
                "service booking",
                "quote request",
                "project gallery"
            ],
            'hairdresser': [
                "appointment booking",
                "stylist selection",
                "service pricing",
                "style gallery"
            ],
            'dentist': [
                "appointment scheduling",
                "patient form submission",
                "treatment information",
                "emergency contact"
            ],
            'mechanic': [
                "service booking",
                "repair quote request",
                "service history tracking",
                "vehicle information storage"
            ],
            'cleaner': [
                "service scheduling",
                "package selection",
                "special request submission",
                "recurring booking"
            ],
            # Default category for any other business type
            'default': [
                "contact form",
                "service showcase",
                "customer testimonial",
                "appointment booking"
            ]
        }
        
        # Find the most relevant category
        for key in features.keys():
            if key in business_category.lower():
                return random.choice(features[key])
        
        # If no specific category matches, use default
        return random.choice(features['default'])
    
    def generate_email(self, business_data, template_name='initial_contact.txt'):
        """
        Generate a personalized email for a business.
        
        Args:
            business_data (dict): Dictionary containing business information
            template_name (str): Name of the template file to use
            
        Returns:
            str: Personalized email content
        """
        if template_name not in self.templates:
            print(f"Template {template_name} not found. Using initial_contact.txt instead.")
            template_name = 'initial_contact.txt'
        
        template = self.templates[template_name]
        
        # Extract business information
        business_name = business_data.get('name', 'your business')
        business_category = business_data.get('category', 'local business')
        location = business_data.get('location', 'your area')
        
        # Generate contact name if not available
        contact_name = business_data.get('contact_name', 'Business Owner')
        
        # Generate custom elements
        custom_benefit = business_data.get('custom_benefit', 
                                          self.generate_custom_benefit(business_category))
        custom_feature = business_data.get('custom_feature',
                                          self.generate_custom_feature(business_category))
        
        # Prepare substitution dictionary
        substitutions = {
            'business_name': business_name,
            'contact_name': contact_name,
            'business_category': business_category,
            'location': location,
            'custom_benefit': custom_benefit,
            'custom_feature': custom_feature
        }
        
        # Generate personalized email
        email_content = template.safe_substitute(substitutions)
        return email_content
    
    def generate_batch_emails(self, businesses_data, template_name='initial_contact.txt'):
        """
        Generate personalized emails for multiple businesses.
        
        Args:
            businesses_data (list): List of dictionaries containing business information
            template_name (str): Name of the template file to use
            
        Returns:
            dict: Dictionary mapping business names to their personalized emails
        """
        emails = {}
        for business_data in businesses_data:
            business_name = business_data.get('name', f"Business_{len(emails)}")
            email_content = self.generate_email(business_data, template_name)
            emails[business_name] = email_content
        return emails
    
    def save_email(self, business_name, email_content, campaign_name=None):
        """
        Save a generated email to a file.
        
        Args:
            business_name (str): Name of the business
            email_content (str): Content of the email
            campaign_name (str): Optional campaign name for organizing emails
            
        Returns:
            str: Path to the saved email file
        """
        # Create campaign directory if specified
        if campaign_name:
            campaign_dir = os.path.join(self.output_dir, campaign_name)
            os.makedirs(campaign_dir, exist_ok=True)
            output_dir = campaign_dir
        else:
            output_dir = self.output_dir
        
        # Sanitize business name for filename
        safe_name = "".join([c if c.isalnum() else "_" for c in business_name])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{safe_name}_{timestamp}.txt"
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(email_content)
        
        return filepath
    
    def save_batch_emails(self, emails, campaign_name=None):
        """
        Save multiple generated emails to files.
        
        Args:
            emails (dict): Dictionary mapping business names to their personalized emails
            campaign_name (str): Optional campaign name for organizing emails
            
        Returns:
            list: List of paths to the saved email files
        """
        saved_files = []
        for business_name, email_content in emails.items():
            filepath = self.save_email(business_name, email_content, campaign_name)
            saved_files.append(filepath)
        return saved_files
    
    def load_businesses_from_csv(self, csv_file):
        """
        Load business data from a CSV file.
        
        Args:
            csv_file (str): Path to the CSV file
            
        Returns:
            list: List of dictionaries containing business information
        """
        try:
            df = pd.read_csv(csv_file)
            businesses = df.to_dict('records')
            return businesses
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return []
    
    def load_businesses_from_json(self, json_file):
        """
        Load business data from a JSON file.
        
        Args:
            json_file (str): Path to the JSON file
            
        Returns:
            list: List of dictionaries containing business information
        """
        try:
            with open(json_file, 'r') as f:
                businesses = json.load(f)
            return businesses
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return []

def main():
    """Main function to demonstrate the OutreachGenerator class."""
    generator = OutreachGenerator()
    
    # Example business data
    example_businesses = [
        {
            'name': 'Delicious Corner Cafe',
            'category': 'restaurant',
            'location': 'London, UK',
            'contact_name': 'Mr. Smith'
        },
        {
            'name': 'Quick Fix Plumbing',
            'category': 'plumber',
            'location': 'Manchester, UK',
            'contact_name': 'Ms. Johnson'
        },
        {
            'name': 'Elite Hair Salon',
            'category': 'hairdresser',
            'location': 'Birmingham, UK',
            'contact_name': 'Mrs. Williams'
        }
    ]
    
    # Generate emails for example businesses
    print("Generating example emails...")
    emails = generator.generate_batch_emails(example_businesses)
    
    # Save the generated emails
    saved_files = generator.save_batch_emails(emails, campaign_name='example_campaign')
    
    print(f"Generated and saved {len(saved_files)} emails:")
    for filepath in saved_files:
        print(f"  - {filepath}")
    
    # Example of loading from CSV (if available)
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if csv_files:
        print(f"\nFound CSV files in data directory: {csv_files}")
        print(f"You can load business data from these files using:")
        print(f"  generator.load_businesses_from_csv('{os.path.join(data_dir, csv_files[0])}')")
    
    print("\nDone! Check the outreach/generated directory for the example emails.")

if __name__ == "__main__":
    main()
