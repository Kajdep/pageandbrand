#!/usr/bin/env python3
"""
Website Generator Integration Module

This script integrates the WebsiteGenerator with the Flask application.
"""

import os
import sys
import json
from datetime import datetime

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from website_generator.website_generator import WebsiteGenerator

class WebsiteGeneratorIntegration:
    """Class for integrating WebsiteGenerator with Flask application."""
    
    def __init__(self):
        """Initialize the WebsiteGeneratorIntegration."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.generator = WebsiteGenerator(
            templates_dir=os.path.join(base_dir, 'website_generator', 'templates'),
            output_dir=os.path.join(base_dir, 'website_generator', 'output')
        )
        self.websites_db_path = os.path.join(base_dir, 'data', 'websites.json')
        
        # Create websites database if it doesn't exist
        if not os.path.exists(self.websites_db_path):
            with open(self.websites_db_path, 'w') as f:
                json.dump([], f)
    
    def get_templates(self):
        """Get available templates."""
        return self.generator.get_templates()
    
    def get_features(self):
        """Get available features."""
        return self.generator.get_features()
    
    def get_generated_websites(self):
        """Get list of generated websites."""
        if os.path.exists(self.websites_db_path):
            with open(self.websites_db_path, 'r') as f:
                return json.load(f)
        return []
    
    def generate_website(self, business_data, template_id, color_scheme, features):
        """Generate a website for a business and save to database."""
        # Generate website
        website_dir = self.generator.generate_website(
            business_data=business_data,
            template_id=template_id,
            color_scheme=color_scheme,
            features=features
        )
        
        # Create website record
        website_record = {
            'id': os.path.basename(website_dir),
            'business_id': business_data.get('id'),
            'business_name': business_data.get('name'),
            'template': template_id,
            'color_scheme': color_scheme,
            'features': features,
            'path': website_dir,
            'url': f"file://{os.path.join(website_dir, 'index.html')}",
            'generated_at': datetime.now().isoformat(),
            'status': 'generated'
        }
        
        # Add to database
        websites = self.get_generated_websites()
        websites.append(website_record)
        
        with open(self.websites_db_path, 'w') as f:
            json.dump(websites, f, indent=2)
        
        return website_record
    
    def update_website_status(self, website_id, status):
        """Update the status of a generated website."""
        websites = self.get_generated_websites()
        
        for website in websites:
            if website['id'] == website_id:
                website['status'] = status
                website['updated_at'] = datetime.now().isoformat()
                
                with open(self.websites_db_path, 'w') as f:
                    json.dump(websites, f, indent=2)
                
                return True
        
        return False
    
    def get_website_by_id(self, website_id):
        """Get a website record by ID."""
        websites = self.get_generated_websites()
        
        for website in websites:
            if website['id'] == website_id:
                return website
        
        return None
    
    def get_websites_by_business_id(self, business_id):
        """Get website records for a business."""
        websites = self.get_generated_websites()
        return [website for website in websites if website.get('business_id') == business_id]
    
    def delete_website(self, website_id):
        """Delete a generated website."""
        websites = self.get_generated_websites()
        
        for i, website in enumerate(websites):
            if website['id'] == website_id:
                # Remove from database
                del websites[i]
                
                with open(self.websites_db_path, 'w') as f:
                    json.dump(websites, f, indent=2)
                
                # Delete files
                website_dir = website.get('path')
                if website_dir and os.path.exists(website_dir):
                    import shutil
                    shutil.rmtree(website_dir)
                
                return True
        
        return False
    
    def deploy_website(self, website_id, domain=None):
        """Deploy a generated website to a production environment."""
        website = self.get_website_by_id(website_id)
        
        if not website:
            return None
        
        # In a real implementation, this would deploy the website to a hosting provider
        # For now, we'll just update the status and URL
        website['status'] = 'deployed'
        website['deployed_at'] = datetime.now().isoformat()
        
        if domain:
            website['domain'] = domain
            website['url'] = f"https://{domain}"
        
        # Update in database
        websites = self.get_generated_websites()
        
        for i, w in enumerate(websites):
            if w['id'] == website_id:
                websites[i] = website
                
                with open(self.websites_db_path, 'w') as f:
                    json.dump(websites, f, indent=2)
                
                break
        
        return website

def main():
    """Test the WebsiteGeneratorIntegration."""
    integration = WebsiteGeneratorIntegration()
    
    # Example business data
    business_data = {
        'id': '123',
        'name': 'Test Business',
        'category': 'Test Category',
        'description': 'This is a test business description.',
        'address': '123 Test St, Test City, Test Country',
        'phone': '+1 234 567 8901',
        'email': 'test@example.com'
    }
    
    # Generate website
    website = integration.generate_website(
        business_data=business_data,
        template_id='modern',
        color_scheme='blue',
        features={
            'booking': True,
            'menu': False,
            'gallery': True,
            'testimonials': True,
            'contact_form': True,
            'social_media': False,
            'calendly': False
        }
    )
    
    print(f"Website generated: {website['url']}")
    
    # Get all websites
    websites = integration.get_generated_websites()
    print(f"Total websites: {len(websites)}")
    
    # Deploy website
    deployed = integration.deploy_website(website['id'], 'example.com')
    if deployed:
        print(f"Website deployed: {deployed['url']}")

if __name__ == '__main__':
    main()
