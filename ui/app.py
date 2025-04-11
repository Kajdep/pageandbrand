#!/usr/bin/env python3
"""
Lead Management Dashboard

This script provides a web-based dashboard for managing leads, campaigns, and website generation.
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import sqlite3

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.business_finder import BusinessFinder
from outreach.outreach_generator import OutreachGenerator
from outreach.outreach_automation import OutreachAutomation

app = Flask(__name__)
app.secret_key = 'business_finder_secret_key'

# Initialize components
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'data', 'outreach.db')
automation = OutreachAutomation(db_path=db_path)
finder = BusinessFinder()
generator = OutreachGenerator()

@app.route('/')
def index():
    """Render the dashboard home page."""
    return render_template('index.html')

@app.route('/leads')
def leads():
    """Render the leads management page."""
    # Get leads from database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, name, category, location, phone, email, date_added
    FROM businesses
    ORDER BY date_added DESC
    ''')
    
    leads_data = cursor.fetchall()
    conn.close()
    
    return render_template('leads.html', leads=leads_data)

@app.route('/lead/<int:lead_id>')
def lead_detail(lead_id):
    """Render the lead detail page."""
    # Get lead details from database
    lead_details = automation.get_business_details(lead_id)
    
    if not lead_details:
        flash('Lead not found', 'error')
        return redirect(url_for('leads'))
    
    return render_template('lead_detail.html', lead=lead_details)

@app.route('/campaigns')
def campaigns():
    """Render the campaigns management page."""
    # Get campaigns from database
    campaigns_data = automation.get_all_campaigns()
    
    return render_template('campaigns.html', campaigns=campaigns_data)

@app.route('/campaign/<int:campaign_id>')
def campaign_detail(campaign_id):
    """Render the campaign detail page."""
    # Get campaign details from database
    campaign_stats = automation.get_campaign_stats(campaign_id)
    
    if not campaign_stats:
        flash('Campaign not found', 'error')
        return redirect(url_for('campaigns'))
    
    return render_template('campaign_detail.html', campaign=campaign_stats)

@app.route('/finder')
def finder_tool():
    """Render the business finder tool page."""
    return render_template('finder.html')

@app.route('/api/find-businesses', methods=['POST'])
def api_find_businesses():
    """API endpoint to find businesses without websites."""
    data = request.json
    query = data.get('query', '')
    location = data.get('location', '')
    max_results = int(data.get('max_results', 20))
    
    if not query or not location:
        return jsonify({'error': 'Query and location are required'}), 400
    
    # Find businesses
    businesses = finder.find_businesses_manual(query, location, max_results)
    
    # Apply filters if specified
    min_rating = data.get('min_rating')
    if min_rating:
        min_rating = float(min_rating)
        businesses = [b for b in businesses if b.get('rating', 0) >= min_rating]
    
    categories = data.get('categories')
    if categories:
        businesses = [b for b in businesses if any(cat.lower() in b.get('category', '').lower() for cat in categories)]
    
    return jsonify({'businesses': businesses})

@app.route('/api/import-businesses', methods=['POST'])
def api_import_businesses():
    """API endpoint to import businesses into the database."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not (file.filename.endswith('.csv') or file.filename.endswith('.json')):
        return jsonify({'error': 'File must be CSV or JSON'}), 400
    
    # Save file temporarily
    temp_path = os.path.join(base_dir, 'data', 'temp_' + file.filename)
    file.save(temp_path)
    
    # Import businesses
    count = automation.import_businesses(temp_path)
    
    # Clean up
    os.remove(temp_path)
    
    return jsonify({'success': True, 'count': count})

@app.route('/api/create-campaign', methods=['POST'])
def api_create_campaign():
    """API endpoint to create a new campaign."""
    data = request.json
    name = data.get('name', '')
    description = data.get('description', '')
    template_name = data.get('template_name', 'initial_contact.txt')
    
    if not name:
        return jsonify({'error': 'Campaign name is required'}), 400
    
    # Create campaign
    campaign_id = automation.create_campaign(name, description, template_name)
    
    # Add businesses if specified
    business_ids = data.get('business_ids')
    filters = data.get('filters')
    
    if business_ids or filters:
        count = automation.add_businesses_to_campaign(campaign_id, business_ids, filters)
        return jsonify({'success': True, 'campaign_id': campaign_id, 'businesses_added': count})
    
    return jsonify({'success': True, 'campaign_id': campaign_id})

@app.route('/api/schedule-campaign', methods=['POST'])
def api_schedule_campaign():
    """API endpoint to schedule a campaign."""
    data = request.json
    campaign_id = data.get('campaign_id')
    
    if not campaign_id:
        return jsonify({'error': 'Campaign ID is required'}), 400
    
    # Generate email content first
    automation.generate_campaign_emails(campaign_id)
    
    # Schedule campaign
    start_date = data.get('start_date')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    emails_per_day = int(data.get('emails_per_day', 10))
    follow_up_days = int(data.get('follow_up_days', 7))
    
    count = automation.schedule_campaign(campaign_id, start_date, emails_per_day, follow_up_days)
    
    return jsonify({'success': True, 'emails_scheduled': count})

@app.route('/api/campaign-stats/<int:campaign_id>')
def api_campaign_stats(campaign_id):
    """API endpoint to get campaign statistics."""
    stats = automation.get_campaign_stats(campaign_id)
    
    if not stats:
        return jsonify({'error': 'Campaign not found'}), 404
    
    return jsonify(stats)

@app.route('/website-generator')
def website_generator():
    """Render the website generator page."""
    return render_template('website_generator.html')

@app.route('/api/generate-website', methods=['POST'])
def api_generate_website():
    """API endpoint to generate a website for a business."""
    # This would be implemented in the website generator module
    # For now, return a placeholder response
    return jsonify({'success': True, 'message': 'Website generation will be implemented in the next phase'})

@app.route('/templates')
def templates():
    """Render the email templates management page."""
    # Get templates from the OutreachGenerator
    template_names = list(generator.templates.keys())
    templates_data = []
    
    for name in template_names:
        template_path = os.path.join(generator.templates_dir, name)
        with open(template_path, 'r') as f:
            content = f.read()
        
        templates_data.append({
            'name': name,
            'content': content
        })
    
    return render_template('templates.html', templates=templates_data)

@app.route('/api/save-template', methods=['POST'])
def api_save_template():
    """API endpoint to save an email template."""
    data = request.json
    name = data.get('name', '')
    content = data.get('content', '')
    
    if not name or not content:
        return jsonify({'error': 'Name and content are required'}), 400
    
    # Ensure template has .txt extension
    if not name.endswith('.txt'):
        name += '.txt'
    
    # Save template
    template_path = os.path.join(generator.templates_dir, name)
    with open(template_path, 'w') as f:
        f.write(content)
    
    # Reload templates
    generator.templates = generator.load_templates()
    
    return jsonify({'success': True})

@app.route('/analytics')
def analytics():
    """Render the analytics page."""
    # Get analytics data from database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT a.campaign_id, c.name, a.sent_count, a.open_count, a.click_count, 
           a.reply_count, a.appointment_count, a.date
    FROM analytics a
    JOIN campaigns c ON a.campaign_id = c.id
    ORDER BY a.date DESC
    ''')
    
    analytics_data = cursor.fetchall()
    conn.close()
    
    return render_template('analytics.html', analytics=analytics_data)

@app.route('/settings')
def settings():
    """Render the settings page."""
    return render_template('settings.html')

@app.route('/api/save-settings', methods=['POST'])
def api_save_settings():
    """API endpoint to save settings."""
    data = request.json
    
    # Save settings to a JSON file
    settings_path = os.path.join(base_dir, 'data', 'settings.json')
    with open(settings_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return jsonify({'success': True})

@app.route('/api/get-settings')
def api_get_settings():
    """API endpoint to get settings."""
    settings_path = os.path.join(base_dir, 'data', 'settings.json')
    
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    else:
        settings = {}
    
    return jsonify(settings)

def main():
    """Run the Flask application."""
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
