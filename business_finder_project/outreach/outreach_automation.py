#!/usr/bin/env python3
"""
Outreach Automation System

This script automates the process of sending personalized emails to businesses without websites.
It includes scheduling, tracking, and analytics features.
"""

import os
import json
import time
import smtplib
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import schedule
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("outreach_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("OutreachAutomation")

class OutreachAutomation:
    """System to automate sending personalized emails to businesses without websites."""
    
    def __init__(self, email_config=None, db_path=None):
        """
        Initialize the OutreachAutomation system.
        
        Args:
            email_config (dict): Email configuration with SMTP settings
            db_path (str): Path to SQLite database file
        """
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Set up database
        if db_path is None:
            db_path = os.path.join(self.base_dir, 'data', 'outreach.db')
        self.db_path = db_path
        self._setup_database()
        
        # Set up email configuration
        self.email_config = email_config or {}
        
        # Initialize scheduler
        self.scheduler_running = False
        self.scheduler_thread = None
    
    def _setup_database(self):
        """Set up the SQLite database for tracking outreach."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            contact_name TEXT,
            location TEXT,
            source TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            template_name TEXT,
            status TEXT DEFAULT 'draft',
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_started TIMESTAMP,
            date_completed TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER,
            campaign_id INTEGER,
            email_type TEXT,
            subject TEXT,
            content TEXT,
            status TEXT DEFAULT 'pending',
            scheduled_time TIMESTAMP,
            sent_time TIMESTAMP,
            opened_time TIMESTAMP,
            clicked_time TIMESTAMP,
            replied_time TIMESTAMP,
            tracking_id TEXT,
            FOREIGN KEY (business_id) REFERENCES businesses (id),
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER,
            campaign_id INTEGER,
            status TEXT DEFAULT 'scheduled',
            scheduled_time TIMESTAMP,
            notes TEXT,
            calendly_link TEXT,
            FOREIGN KEY (business_id) REFERENCES businesses (id),
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            email_type TEXT,
            sent_count INTEGER DEFAULT 0,
            open_count INTEGER DEFAULT 0,
            click_count INTEGER DEFAULT 0,
            reply_count INTEGER DEFAULT 0,
            appointment_count INTEGER DEFAULT 0,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"Database setup complete at {self.db_path}")
    
    def import_businesses(self, data_file):
        """
        Import businesses from CSV or JSON file into the database.
        
        Args:
            data_file (str): Path to CSV or JSON file with business data
            
        Returns:
            int: Number of businesses imported
        """
        if not os.path.exists(data_file):
            logger.error(f"Data file not found: {data_file}")
            return 0
        
        # Load data from file
        if data_file.endswith('.csv'):
            df = pd.read_csv(data_file)
            businesses = df.to_dict('records')
        elif data_file.endswith('.json'):
            with open(data_file, 'r') as f:
                businesses = json.load(f)
        else:
            logger.error(f"Unsupported file format: {data_file}")
            return 0
        
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Import businesses
        count = 0
        for business in businesses:
            # Skip businesses with websites
            if business.get('has_website', False):
                continue
                
            # Prepare data
            name = business.get('name', '')
            category = business.get('category', '')
            address = business.get('address', '')
            phone = business.get('phone', '')
            email = business.get('email', '')
            contact_name = business.get('contact_name', '')
            location = business.get('location', '')
            source = business.get('source', 'import')
            
            # Check if business already exists
            cursor.execute(
                "SELECT id FROM businesses WHERE name = ? AND phone = ?",
                (name, phone)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing business
                cursor.execute('''
                UPDATE businesses 
                SET category = ?, address = ?, email = ?, contact_name = ?, 
                    location = ?, source = ?
                WHERE id = ?
                ''', (category, address, email, contact_name, location, source, existing[0]))
                logger.info(f"Updated existing business: {name}")
            else:
                # Insert new business
                cursor.execute('''
                INSERT INTO businesses 
                (name, category, address, phone, email, contact_name, location, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, category, address, phone, email, contact_name, location, source))
                count += 1
                logger.info(f"Imported new business: {name}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Imported {count} new businesses from {data_file}")
        return count
    
    def create_campaign(self, name, description, template_name):
        """
        Create a new email campaign.
        
        Args:
            name (str): Campaign name
            description (str): Campaign description
            template_name (str): Email template to use
            
        Returns:
            int: Campaign ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO campaigns (name, description, template_name, status)
        VALUES (?, ?, ?, 'draft')
        ''', (name, description, template_name))
        
        campaign_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Created campaign: {name} (ID: {campaign_id})")
        return campaign_id
    
    def add_businesses_to_campaign(self, campaign_id, business_ids=None, filters=None):
        """
        Add businesses to a campaign based on IDs or filters.
        
        Args:
            campaign_id (int): Campaign ID
            business_ids (list): List of business IDs to add
            filters (dict): Filters to select businesses
            
        Returns:
            int: Number of businesses added
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verify campaign exists
        cursor.execute("SELECT id FROM campaigns WHERE id = ?", (campaign_id,))
        if not cursor.fetchone():
            logger.error(f"Campaign not found: {campaign_id}")
            conn.close()
            return 0
        
        # Get businesses to add
        if business_ids:
            # Add specific businesses
            placeholders = ','.join(['?'] * len(business_ids))
            cursor.execute(
                f"SELECT id, name FROM businesses WHERE id IN ({placeholders})",
                business_ids
            )
        elif filters:
            # Add businesses based on filters
            query = "SELECT id, name FROM businesses WHERE 1=1"
            params = []
            
            if 'category' in filters:
                query += " AND category LIKE ?"
                params.append(f"%{filters['category']}%")
            
            if 'location' in filters:
                query += " AND location LIKE ?"
                params.append(f"%{filters['location']}%")
            
            cursor.execute(query, params)
        else:
            # Add all businesses
            cursor.execute("SELECT id, name FROM businesses")
        
        businesses = cursor.fetchall()
        
        # Generate emails for each business
        count = 0
        for business_id, business_name in businesses:
            # Check if business already has an email in this campaign
            cursor.execute(
                "SELECT id FROM emails WHERE business_id = ? AND campaign_id = ?",
                (business_id, campaign_id)
            )
            if cursor.fetchone():
                logger.info(f"Business already in campaign: {business_name}")
                continue
            
            # Add initial email
            cursor.execute('''
            INSERT INTO emails 
            (business_id, campaign_id, email_type, status)
            VALUES (?, ?, 'initial', 'pending')
            ''', (business_id, campaign_id))
            
            count += 1
            logger.info(f"Added business to campaign: {business_name}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Added {count} businesses to campaign {campaign_id}")
        return count
    
    def generate_campaign_emails(self, campaign_id, from_outreach_generator=True):
        """
        Generate email content for all businesses in a campaign.
        
        Args:
            campaign_id (int): Campaign ID
            from_outreach_generator (bool): Whether to use OutreachGenerator
            
        Returns:
            int: Number of emails generated
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get campaign details
        cursor.execute(
            "SELECT name, template_name FROM campaigns WHERE id = ?",
            (campaign_id,)
        )
        campaign = cursor.fetchone()
        if not campaign:
            logger.error(f"Campaign not found: {campaign_id}")
            conn.close()
            return 0
        
        campaign_name, template_name = campaign
        
        # Get emails that need content
        cursor.execute('''
        SELECT e.id, e.business_id, e.email_type, b.name, b.category, b.location, b.contact_name
        FROM emails e
        JOIN businesses b ON e.business_id = b.id
        WHERE e.campaign_id = ? AND e.content IS NULL AND e.status = 'pending'
        ''', (campaign_id,))
        
        emails = cursor.fetchall()
        if not emails:
            logger.info(f"No pending emails found for campaign {campaign_id}")
            conn.close()
            return 0
        
        count = 0
        
        if from_outreach_generator:
            # Use OutreachGenerator to generate email content
            try:
                # Import here to avoid circular imports
                sys.path.append(self.base_dir)
                from outreach.outreach_generator import OutreachGenerator
                
                generator = OutreachGenerator()
                
                for email_id, business_id, email_type, name, category, location, contact_name in emails:
                    # Prepare business data
                    business_data = {
                        'name': name,
                        'category': category,
                        'location': location,
                        'contact_name': contact_name or 'Business Owner'
                    }
                    
                    # Determine template based on email type
                    if email_type == 'initial':
                        template = 'initial_contact.txt'
                    elif email_type == 'follow_up':
                        template = 'follow_up.txt'
                    else:
                        template = 'value_proposition.txt'
                    
                    # Generate email content
                    email_content = generator.generate_email(business_data, template)
                    
                    # Extract subject from content
                    subject = ""
                    for line in email_content.split('\n'):
                        if line.startswith('Subject:'):
                            subject = line.replace('Subject:', '').strip()
                            break
                    
                    # Update email in database
                    cursor.execute('''
                    UPDATE emails
                    SET subject = ?, content = ?
                    WHERE id = ?
                    ''', (subject, email_content, email_id))
                    
                    count += 1
                    logger.info(f"Generated email for {name} in campaign {campaign_name}")
                
            except ImportError as e:
                logger.error(f"Failed to import OutreachGenerator: {e}")
                # Fall back to simple templates
                for email_id, business_id, email_type, name, category, location, contact_name in emails:
                    subject = f"Website for {name}"
                    content = f"Dear {contact_name or 'Business Owner'},\n\nThis is a placeholder email for {name}.\n\nBest regards,\nYour Name"
                    
                    cursor.execute('''
                    UPDATE emails
                    SET subject = ?, content = ?
                    WHERE id = ?
                    ''', (subject, content, email_id))
                    
                    count += 1
        else:
            # Use simple templates
            for email_id, business_id, email_type, name, category, location, contact_name in emails:
                subject = f"Website for {name}"
                content = f"Dear {contact_name or 'Business Owner'},\n\nThis is a placeholder email for {name}.\n\nBest regards,\nYour Name"
                
                cursor.execute('''
                UPDATE emails
                SET subject = ?, content = ?
                WHERE id = ?
                ''', (subject, content, email_id))
                
                count += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"Generated {count} emails for campaign {campaign_id}")
        return count
    
    def schedule_campaign(self, campaign_id, start_date=None, emails_per_day=10, follow_up_days=7):
        """
        Schedule emails for a campaign.
        
        Args:
            campaign_id (int): Campaign ID
            start_date (datetime): Start date for the campaign
            emails_per_day (int): Maximum emails to send per day
            follow_up_days (int): Days to wait before follow-up
            
        Returns:
            int: Number of emails scheduled
        """
        if start_date is None:
            start_date = datetime.now()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update campaign status
        cursor.execute('''
        UPDATE campaigns
        SET status = 'scheduled', date_started = ?
        WHERE id = ?
        ''', (start_date, campaign_id))
        
        # Get all pending emails for this campaign
        cursor.execute('''
        SELECT id FROM emails
        WHERE campaign_id = ? AND status = 'pending' AND scheduled_time IS NULL
        ''', (campaign_id,))
        
        emails = cursor.fetchall()
        if not emails:
            logger.info(f"No pending emails found for campaign {campaign_id}")
            conn.close()
            return 0
        
        # Schedule emails
        current_date = start_date
        count = 0
        
        for i, (email_id,) in enumerate(emails):
            # Calculate scheduled time
            day_offset = i // emails_per_day
            scheduled_time = current_date + timedelta(days=day_offset)
            
            # Update email with scheduled time
            cursor.execute('''
            UPDATE emails
            SET scheduled_time = ?, status = 'scheduled'
            WHERE id = ?
            ''', (scheduled_time, email_id))
            
            count += 1
        
        # Schedule follow-up emails
        cursor.execute('''
        SELECT e.id, e.business_id
        FROM emails e
        WHERE e.campaign_id = ? AND e.email_type = 'initial' AND e.status = 'scheduled'
        ''', (campaign_id,))
        
        initial_emails = cursor.fetchall()
        
        for email_id, business_id in initial_emails:
            # Schedule follow-up email
            follow_up_time = start_date + timedelta(days=follow_up_days)
            
            cursor.execute('''
            INSERT INTO emails 
            (business_id, campaign_id, email_type, status, scheduled_time)
            VALUES (?, ?, 'follow_up', 'scheduled', ?)
            ''', (business_id, campaign_id, follow_up_time))
            
            count += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"Scheduled {count} emails for campaign {campaign_id}")
        return count
    
    def send_scheduled_emails(self):
        """
        Send all scheduled emails that are due.
        
        Returns:
            int: Number of emails sent
        """
        if not self.email_config:
            logger.error("Email configuration not set")
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get scheduled emails that are due
        now = datetime.now()
        cursor.execute('''
        SELECT e.id, e.subject, e.content, b.name, b.email
        FROM emails e
        JOIN businesses b ON e.business_id = b.id
        WHERE e.status = 'scheduled' AND e.scheduled_time <= ? AND e.content IS NOT NULL
        ''', (now,))
        
        emails = cursor.fetchall()
        if not emails:
            logger.info("No scheduled emails due")
            conn.close()
            return 0
        
        # Send emails
        count = 0
        
        for email_id, subject, content, business_name, business_email in emails:
            # Skip if no email address
            if not business_email:
                logger.warning(f"No email address for {business_name}, skipping")
                continue
            
            # Send email
            try:
                self._send_email(business_email, subject, content)
                
                # Update email status
                cursor.execute('''
                UPDATE emails
                SET status = 'sent', sent_time = ?
                WHERE id = ?
                ''', (now, email_id))
                
                count += 1
                logger.info(f"Sent email to {business_name} <{business_email}>")
                
            except Exception as e:
                logger.error(f"Failed to send email to {business_name}: {e}")
                
                # Update email status
                cursor.execute('''
                UPDATE emails
                SET status = 'failed'
                WHERE id = ?
                ''', (email_id,))
        
        # Update campaign analytics
        cursor.execute('''
        UPDATE analytics
        SET sent_count = sent_count + ?
        WHERE campaign_id IN (
            SELECT DISTINCT campaign_id FROM emails WHERE id IN (?)
        )
        ''', (count, ','.join([str(e[0]) for e in emails])))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Sent {count} scheduled emails")
        return count
    
    def _send_email(self, to_email, subject, content):
        """
        Send an email using SMTP.
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            content (str): Email content
            
        Returns:
            bool: Whether the email was sent successfully
        """
        # Check if email configuration is set
        if not self.email_config:
            logger.error("Email configuration not set")
            return False
        
        # Extract SMTP settings
        smtp_server = self.email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = self.email_config.get('smtp_port', 587)
        smtp_username = self.email_config.get('smtp_username', '')
        smtp_password = self.email_config.get('smtp_password', '')
        from_email = self.email_config.get('from_email', smtp_username)
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach content
        msg.attach(MIMEText(content, 'plain'))
        
        # Send email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def start_scheduler(self):
        """Start the scheduler to send emails automatically."""
        if self.scheduler_running:
            logger.warning("Scheduler already running")
            return
        
        # Schedule tasks
        schedule.every().hour.do(self.send_scheduled_emails)
        schedule.every().day.at("09:00").do(self.update_analytics)
        
        # Start scheduler in a separate thread
        def run_scheduler():
            self.scheduler_running = True
            logger.info("Scheduler started")
            
            while self.scheduler_running:
                schedule.run_pending()
                time.sleep(60)
        
        self.scheduler_thread = threading.Thread(target=run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the scheduler."""
        if not self.scheduler_running:
            logger.warning("Scheduler not running")
            return
        
        self.scheduler_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=2)
        
        logger.info("Scheduler stopped")
    
    def update_analytics(self):
        """Update analytics for all campaigns."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all active campaigns
        cursor.execute('''
        SELECT id, name FROM campaigns
        WHERE status IN ('scheduled', 'active', 'running')
        ''')
        
        campaigns = cursor.fetchall()
        if not campaigns:
            logger.info("No active campaigns for analytics update")
            conn.close()
            return
        
        for campaign_id, campaign_name in campaigns:
            # Count emails by status
            cursor.execute('''
            SELECT 
                COUNT(CASE WHEN status = 'sent' THEN 1 END) as sent,
                COUNT(CASE WHEN opened_time IS NOT NULL THEN 1 END) as opened,
                COUNT(CASE WHEN clicked_time IS NOT NULL THEN 1 END) as clicked,
                COUNT(CASE WHEN replied_time IS NOT NULL THEN 1 END) as replied
            FROM emails
            WHERE campaign_id = ?
            ''', (campaign_id,))
            
            counts = cursor.fetchone()
            if not counts:
                continue
            
            sent, opened, clicked, replied = counts
            
            # Count appointments
            cursor.execute('''
            SELECT COUNT(*) FROM appointments
            WHERE campaign_id = ?
            ''', (campaign_id,))
            
            appointments = cursor.fetchone()[0]
            
            # Check if analytics entry exists
            cursor.execute('''
            SELECT id FROM analytics
            WHERE campaign_id = ? AND date >= date('now', 'start of day')
            ''', (campaign_id,))
            
            analytics_id = cursor.fetchone()
            
            if analytics_id:
                # Update existing entry
                cursor.execute('''
                UPDATE analytics
                SET sent_count = ?, open_count = ?, click_count = ?, 
                    reply_count = ?, appointment_count = ?
                WHERE id = ?
                ''', (sent, opened, clicked, replied, appointments, analytics_id[0]))
            else:
                # Create new entry
                cursor.execute('''
                INSERT INTO analytics
                (campaign_id, sent_count, open_count, click_count, reply_count, appointment_count)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (campaign_id, sent, opened, clicked, replied, appointments))
            
            logger.info(f"Updated analytics for campaign {campaign_name}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Analytics updated for {len(campaigns)} campaigns")
    
    def get_campaign_stats(self, campaign_id):
        """
        Get statistics for a campaign.
        
        Args:
            campaign_id (int): Campaign ID
            
        Returns:
            dict: Campaign statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get campaign details
        cursor.execute('''
        SELECT name, status, date_created, date_started, date_completed
        FROM campaigns
        WHERE id = ?
        ''', (campaign_id,))
        
        campaign = cursor.fetchone()
        if not campaign:
            logger.error(f"Campaign not found: {campaign_id}")
            conn.close()
            return {}
        
        name, status, date_created, date_started, date_completed = campaign
        
        # Get email counts
        cursor.execute('''
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
            COUNT(CASE WHEN status = 'scheduled' THEN 1 END) as scheduled,
            COUNT(CASE WHEN status = 'sent' THEN 1 END) as sent,
            COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed,
            COUNT(CASE WHEN opened_time IS NOT NULL THEN 1 END) as opened,
            COUNT(CASE WHEN clicked_time IS NOT NULL THEN 1 END) as clicked,
            COUNT(CASE WHEN replied_time IS NOT NULL THEN 1 END) as replied
        FROM emails
        WHERE campaign_id = ?
        ''', (campaign_id,))
        
        email_counts = cursor.fetchone()
        
        # Get appointment count
        cursor.execute('''
        SELECT COUNT(*) FROM appointments
        WHERE campaign_id = ?
        ''', (campaign_id,))
        
        appointment_count = cursor.fetchone()[0]
        
        # Calculate rates
        total = email_counts[0] or 1  # Avoid division by zero
        sent = email_counts[3] or 1   # Avoid division by zero
        
        open_rate = (email_counts[5] / sent) * 100 if sent > 0 else 0
        click_rate = (email_counts[6] / sent) * 100 if sent > 0 else 0
        reply_rate = (email_counts[7] / sent) * 100 if sent > 0 else 0
        appointment_rate = (appointment_count / sent) * 100 if sent > 0 else 0
        
        # Compile statistics
        stats = {
            'campaign_id': campaign_id,
            'name': name,
            'status': status,
            'date_created': date_created,
            'date_started': date_started,
            'date_completed': date_completed,
            'emails': {
                'total': email_counts[0],
                'pending': email_counts[1],
                'scheduled': email_counts[2],
                'sent': email_counts[3],
                'failed': email_counts[4],
                'opened': email_counts[5],
                'clicked': email_counts[6],
                'replied': email_counts[7]
            },
            'appointments': appointment_count,
            'rates': {
                'open_rate': round(open_rate, 2),
                'click_rate': round(click_rate, 2),
                'reply_rate': round(reply_rate, 2),
                'appointment_rate': round(appointment_rate, 2)
            }
        }
        
        conn.close()
        return stats
    
    def get_all_campaigns(self):
        """
        Get a list of all campaigns with basic statistics.
        
        Returns:
            list: List of campaign dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, name, status, date_created, date_started, date_completed
        FROM campaigns
        ORDER BY date_created DESC
        ''')
        
        campaigns = []
        for campaign_id, name, status, date_created, date_started, date_completed in cursor.fetchall():
            # Get email counts
            cursor.execute('''
            SELECT COUNT(*) as total, COUNT(CASE WHEN status = 'sent' THEN 1 END) as sent
            FROM emails
            WHERE campaign_id = ?
            ''', (campaign_id,))
            
            total, sent = cursor.fetchone()
            
            campaigns.append({
                'id': campaign_id,
                'name': name,
                'status': status,
                'date_created': date_created,
                'date_started': date_started,
                'date_completed': date_completed,
                'total_emails': total,
                'sent_emails': sent
            })
        
        conn.close()
        return campaigns
    
    def get_business_details(self, business_id):
        """
        Get details for a specific business.
        
        Args:
            business_id (int): Business ID
            
        Returns:
            dict: Business details
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, name, category, address, phone, email, contact_name, location, source, date_added
        FROM businesses
        WHERE id = ?
        ''', (business_id,))
        
        business = cursor.fetchone()
        if not business:
            logger.error(f"Business not found: {business_id}")
            conn.close()
            return {}
        
        # Get email history
        cursor.execute('''
        SELECT e.id, e.campaign_id, c.name, e.email_type, e.status, e.sent_time, e.opened_time, e.replied_time
        FROM emails e
        JOIN campaigns c ON e.campaign_id = c.id
        WHERE e.business_id = ?
        ORDER BY e.sent_time DESC
        ''', (business_id,))
        
        emails = []
        for email_id, campaign_id, campaign_name, email_type, status, sent_time, opened_time, replied_time in cursor.fetchall():
            emails.append({
                'id': email_id,
                'campaign_id': campaign_id,
                'campaign_name': campaign_name,
                'type': email_type,
                'status': status,
                'sent_time': sent_time,
                'opened_time': opened_time,
                'replied_time': replied_time
            })
        
        # Get appointment history
        cursor.execute('''
        SELECT id, campaign_id, status, scheduled_time, notes
        FROM appointments
        WHERE business_id = ?
        ORDER BY scheduled_time DESC
        ''', (business_id,))
        
        appointments = []
        for appointment_id, campaign_id, status, scheduled_time, notes in cursor.fetchall():
            appointments.append({
                'id': appointment_id,
                'campaign_id': campaign_id,
                'status': status,
                'scheduled_time': scheduled_time,
                'notes': notes
            })
        
        # Compile business details
        details = {
            'id': business[0],
            'name': business[1],
            'category': business[2],
            'address': business[3],
            'phone': business[4],
            'email': business[5],
            'contact_name': business[6],
            'location': business[7],
            'source': business[8],
            'date_added': business[9],
            'emails': emails,
            'appointments': appointments
        }
        
        conn.close()
        return details
    
    def add_appointment(self, business_id, campaign_id, scheduled_time, notes=None, calendly_link=None):
        """
        Add an appointment for a business.
        
        Args:
            business_id (int): Business ID
            campaign_id (int): Campaign ID
            scheduled_time (datetime): Scheduled appointment time
            notes (str): Optional notes
            calendly_link (str): Optional Calendly link
            
        Returns:
            int: Appointment ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO appointments
        (business_id, campaign_id, status, scheduled_time, notes, calendly_link)
        VALUES (?, ?, 'scheduled', ?, ?, ?)
        ''', (business_id, campaign_id, scheduled_time, notes, calendly_link))
        
        appointment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Added appointment for business {business_id} in campaign {campaign_id}")
        return appointment_id

def main():
    """Main function to demonstrate the OutreachAutomation class."""
    import sys
    
    # Set up email configuration (for demonstration only)
    email_config = {
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'smtp_username': 'your_email@example.com',
        'smtp_password': 'your_password',
        'from_email': 'Your Name <your_email@example.com>'
    }
    
    # Initialize automation system
    automation = OutreachAutomation(email_config)
    
    print("Outreach Automation System")
    print("-------------------------")
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == 'import' and len(sys.argv) > 2:
            # Import businesses from file
            data_file = sys.argv[2]
            count = automation.import_businesses(data_file)
            print(f"Imported {count} businesses from {data_file}")
            return
        
        elif sys.argv[1] == 'create-campaign' and len(sys.argv) > 3:
            # Create a new campaign
            name = sys.argv[2]
            description = sys.argv[3]
            template = sys.argv[4] if len(sys.argv) > 4 else 'initial_contact.txt'
            
            campaign_id = automation.create_campaign(name, description, template)
            print(f"Created campaign: {name} (ID: {campaign_id})")
            return
        
        elif sys.argv[1] == 'stats' and len(sys.argv) > 2:
            # Show campaign statistics
            campaign_id = int(sys.argv[2])
            stats = automation.get_campaign_stats(campaign_id)
            
            print(f"Campaign: {stats.get('name')} (ID: {campaign_id})")
            print(f"Status: {stats.get('status')}")
            print(f"Created: {stats.get('date_created')}")
            print(f"Started: {stats.get('date_started')}")
            print(f"Completed: {stats.get('date_completed')}")
            print("\nEmails:")
            for key, value in stats.get('emails', {}).items():
                print(f"  {key}: {value}")
            print("\nRates:")
            for key, value in stats.get('rates', {}).items():
                print(f"  {key}: {value}%")
            print(f"\nAppointments: {stats.get('appointments')}")
            return
    
    # Show example usage
    print("\nExample usage:")
    print("  python outreach_automation.py import /path/to/businesses.csv")
    print("  python outreach_automation.py create-campaign 'Campaign Name' 'Campaign Description'")
    print("  python outreach_automation.py stats 1")
    
    print("\nFor programmatic usage, see the OutreachAutomation class documentation.")

if __name__ == "__main__":
    main()
