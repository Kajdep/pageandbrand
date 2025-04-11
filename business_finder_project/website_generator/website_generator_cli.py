#!/usr/bin/env python3
"""
Website Generator CLI

This script provides a command-line interface for the WebsiteGenerator class.
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from website_generator.website_generator import WebsiteGenerator

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Generate a website for a business')
    
    parser.add_argument('--business-name', required=True, help='Business name')
    parser.add_argument('--business-category', required=True, help='Business category')
    parser.add_argument('--business-description', required=True, help='Business description')
    parser.add_argument('--business-address', required=True, help='Business address')
    parser.add_argument('--business-phone', required=True, help='Business phone number')
    parser.add_argument('--business-email', required=True, help='Business email address')
    
    parser.add_argument('--template', choices=['modern', 'classic', 'minimal'], default='modern', help='Website template')
    parser.add_argument('--color-scheme', choices=['blue', 'green', 'red', 'purple'], default='blue', help='Color scheme')
    
    parser.add_argument('--enable-booking', action='store_true', help='Enable booking system')
    parser.add_argument('--enable-menu', action='store_true', help='Enable menu display')
    parser.add_argument('--enable-gallery', action='store_true', help='Enable photo gallery')
    parser.add_argument('--enable-testimonials', action='store_true', help='Enable testimonials')
    parser.add_argument('--enable-contact-form', action='store_true', help='Enable contact form')
    parser.add_argument('--enable-social-media', action='store_true', help='Enable social media integration')
    parser.add_argument('--enable-calendly', action='store_true', help='Enable Calendly integration')
    parser.add_argument('--calendly-link', help='Calendly link (required if --enable-calendly is set)')
    
    parser.add_argument('--output-dir', help='Output directory for generated website')
    
    return parser.parse_args()

def main():
    """Run the website generator CLI."""
    args = parse_args()
    
    # Check if Calendly link is provided when Calendly integration is enabled
    if args.enable_calendly and not args.calendly_link:
        print('Error: --calendly-link is required when --enable-calendly is set')
        sys.exit(1)
    
    # Create business data dictionary
    business_data = {
        'name': args.business_name,
        'category': args.business_category,
        'description': args.business_description,
        'address': args.business_address,
        'phone': args.business_phone,
        'email': args.business_email,
        'services': [
            {
                'name': 'Service 1',
                'description': 'Description of service 1 and its benefits.'
            },
            {
                'name': 'Service 2',
                'description': 'Description of service 2 and its benefits.'
            },
            {
                'name': 'Service 3',
                'description': 'Description of service 3 and its benefits.'
            }
        ],
        'social': {
            'facebook': 'https://facebook.com/',
            'instagram': 'https://instagram.com/',
            'twitter': 'https://twitter.com/',
            'linkedin': 'https://linkedin.com/'
        }
    }
    
    # Add Calendly data if enabled
    if args.enable_calendly:
        business_data['calendly'] = {
            'link': args.calendly_link
        }
    
    # Create features dictionary
    features = {
        'booking': args.enable_booking,
        'menu': args.enable_menu,
        'gallery': args.enable_gallery,
        'testimonials': args.enable_testimonials,
        'contact_form': args.enable_contact_form,
        'social_media': args.enable_social_media,
        'calendly': args.enable_calendly
    }
    
    # Initialize WebsiteGenerator
    generator = WebsiteGenerator()
    
    # Generate website
    website_dir = generator.generate_website(
        business_data=business_data,
        template_id=args.template,
        color_scheme=args.color_scheme,
        features=features,
        output_dir=args.output_dir
    )
    
    print(f"Website generated at: {website_dir}")
    print(f"To view the website, open: file://{os.path.join(website_dir, 'index.html')}")

if __name__ == '__main__':
    main()
