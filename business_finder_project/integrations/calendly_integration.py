#!/usr/bin/env python3
"""
Calendly Integration Module

This script provides functionality to integrate Calendly with the business finder and website generator tools.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
import sqlite3

class CalendlyIntegration:
    """Class for integrating Calendly with the business finder and website generator tools."""
    
    def __init__(self, api_key=None, user_uri=None, db_path=None):
        """Initialize the CalendlyIntegration with API key and user URI."""
        self.api_key = api_key or os.environ.get('CALENDLY_API_KEY')
        self.user_uri = user_uri or os.environ.get('CALENDLY_USER_URI')
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = db_path or os.path.join(base_dir, 'data', 'outreach.db')
        
        # Create database tables if they don't exist
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create calendly_events table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendly_events (
            id TEXT PRIMARY KEY,
            business_id TEXT,
            event_type TEXT,
            start_time TEXT,
            end_time TEXT,
            invitee_name TEXT,
            invitee_email TEXT,
            invitee_phone TEXT,
            status TEXT,
            created_at TEXT,
            updated_at TEXT,
            canceled_at TEXT,
            FOREIGN KEY (business_id) REFERENCES businesses(id)
        )
        ''')
        
        # Create calendly_event_types table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendly_event_types (
            id TEXT PRIMARY KEY,
            name TEXT,
            slug TEXT,
            duration INTEGER,
            description TEXT,
            uri TEXT,
            active BOOLEAN,
            created_at TEXT,
            updated_at TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_auth_headers(self):
        """Get authentication headers for Calendly API requests."""
        if not self.api_key:
            raise ValueError("Calendly API key is required")
        
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_event_types(self):
        """Get available event types from Calendly."""
        if not self.api_key or not self.user_uri:
            return {'error': 'Calendly API key and user URI are required'}
        
        try:
            url = f"https://api.calendly.com/event_types?user={self.user_uri}"
            response = requests.get(url, headers=self.get_auth_headers())
            response.raise_for_status()
            
            data = response.json()
            event_types = []
            
            for event_type in data.get('collection', []):
                event_type_data = {
                    'id': event_type.get('id'),
                    'name': event_type.get('name'),
                    'slug': event_type.get('slug'),
                    'duration': event_type.get('duration'),
                    'description': event_type.get('description'),
                    'uri': event_type.get('uri'),
                    'active': event_type.get('active'),
                    'created_at': event_type.get('created_at'),
                    'updated_at': event_type.get('updated_at')
                }
                
                event_types.append(event_type_data)
                
                # Save to database
                self._save_event_type(event_type_data)
            
            return {'event_types': event_types}
        
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def _save_event_type(self, event_type):
        """Save event type to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO calendly_event_types (
            id, name, slug, duration, description, uri, active, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_type.get('id'),
            event_type.get('name'),
            event_type.get('slug'),
            event_type.get('duration'),
            event_type.get('description'),
            event_type.get('uri'),
            event_type.get('active', True),
            event_type.get('created_at'),
            event_type.get('updated_at')
        ))
        
        conn.commit()
        conn.close()
    
    def get_scheduled_events(self, start_time=None, end_time=None):
        """Get scheduled events from Calendly."""
        if not self.api_key or not self.user_uri:
            return {'error': 'Calendly API key and user URI are required'}
        
        try:
            # Default to events in the next 30 days if not specified
            if not start_time:
                start_time = datetime.utcnow().isoformat() + 'Z'
            if not end_time:
                end_time = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
            
            url = f"https://api.calendly.com/scheduled_events?user={self.user_uri}&min_start_time={start_time}&max_start_time={end_time}"
            response = requests.get(url, headers=self.get_auth_headers())
            response.raise_for_status()
            
            data = response.json()
            events = []
            
            for event in data.get('collection', []):
                event_data = {
                    'id': event.get('id'),
                    'event_type': event.get('event_type'),
                    'start_time': event.get('start_time'),
                    'end_time': event.get('end_time'),
                    'status': event.get('status'),
                    'uri': event.get('uri'),
                    'created_at': event.get('created_at'),
                    'updated_at': event.get('updated_at')
                }
                
                # Get invitee details
                invitee_data = self.get_event_invitees(event.get('uri'))
                if 'invitees' in invitee_data and invitee_data['invitees']:
                    invitee = invitee_data['invitees'][0]
                    event_data['invitee_name'] = invitee.get('name')
                    event_data['invitee_email'] = invitee.get('email')
                    event_data['invitee_phone'] = invitee.get('text_reminder_number')
                
                events.append(event_data)
                
                # Save to database
                self._save_event(event_data)
            
            return {'events': events}
        
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def get_event_invitees(self, event_uri):
        """Get invitees for a specific event."""
        if not self.api_key:
            return {'error': 'Calendly API key is required'}
        
        try:
            url = f"https://api.calendly.com/scheduled_events/{event_uri.split('/')[-1]}/invitees"
            response = requests.get(url, headers=self.get_auth_headers())
            response.raise_for_status()
            
            data = response.json()
            invitees = []
            
            for invitee in data.get('collection', []):
                invitee_data = {
                    'id': invitee.get('id'),
                    'name': invitee.get('name'),
                    'email': invitee.get('email'),
                    'text_reminder_number': invitee.get('text_reminder_number'),
                    'status': invitee.get('status'),
                    'created_at': invitee.get('created_at'),
                    'updated_at': invitee.get('updated_at'),
                    'canceled_at': invitee.get('canceled_at')
                }
                
                invitees.append(invitee_data)
            
            return {'invitees': invitees}
        
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def _save_event(self, event):
        """Save event to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO calendly_events (
            id, event_type, start_time, end_time, invitee_name, invitee_email, invitee_phone,
            status, created_at, updated_at, canceled_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event.get('id'),
            event.get('event_type'),
            event.get('start_time'),
            event.get('end_time'),
            event.get('invitee_name'),
            event.get('invitee_email'),
            event.get('invitee_phone'),
            event.get('status'),
            event.get('created_at'),
            event.get('updated_at'),
            event.get('canceled_at')
        ))
        
        conn.commit()
        conn.close()
    
    def get_event_by_id(self, event_id):
        """Get event details by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM calendly_events WHERE id = ?', (event_id,))
        event = cursor.fetchone()
        
        conn.close()
        
        if event:
            return dict(event)
        
        return None
    
    def get_events_by_business_id(self, business_id):
        """Get events for a specific business."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM calendly_events WHERE business_id = ? ORDER BY start_time DESC', (business_id,))
        events = cursor.fetchall()
        
        conn.close()
        
        return [dict(event) for event in events]
    
    def update_event_business_id(self, event_id, business_id):
        """Update the business ID for an event."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE calendly_events SET business_id = ? WHERE id = ?', (business_id, event_id))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def generate_booking_widget(self, event_type_uri=None, business_id=None, widget_type='inline'):
        """Generate HTML code for Calendly booking widget."""
        if not event_type_uri:
            # Use default event type if not specified
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT uri FROM calendly_event_types WHERE active = 1 LIMIT 1')
            event_type = cursor.fetchone()
            
            conn.close()
            
            if event_type:
                event_type_uri = event_type['uri']
            else:
                return {'error': 'No active event types found'}
        
        # Generate widget code
        if widget_type == 'inline':
            widget_code = f'''
            <!-- Calendly inline widget begin -->
            <div class="calendly-inline-widget" data-url="{event_type_uri}" style="min-width:320px;height:630px;"></div>
            <script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>
            <!-- Calendly inline widget end -->
            '''
        else:  # popup
            widget_code = f'''
            <!-- Calendly badge widget begin -->
            <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
            <script src="https://assets.calendly.com/assets/external/widget.js" type="text/javascript" async></script>
            <script type="text/javascript">window.onload = function() {{ Calendly.initBadgeWidget({{ url: '{event_type_uri}', text: 'Schedule time with me', color: '#0069ff', textColor: '#ffffff', branding: true }}); }}</script>
            <!-- Calendly badge widget end -->
            '''
        
        return {
            'widget_code': widget_code,
            'event_type_uri': event_type_uri,
            'business_id': business_id,
            'widget_type': widget_type
        }
    
    def generate_website_integration_code(self, event_type_uri=None, widget_type='inline'):
        """Generate code for integrating Calendly with a website."""
        widget_data = self.generate_booking_widget(event_type_uri, None, widget_type)
        
        if 'error' in widget_data:
            return widget_data
        
        # Generate additional JavaScript for tracking
        tracking_code = '''
        <script type="text/javascript">
        // Calendly tracking code
        function isCalendlyEvent(e) {
            return e.data.event && e.data.event.indexOf('calendly') === 0;
        }
        
        window.addEventListener('message', function(e) {
            if (isCalendlyEvent(e)) {
                console.log('Calendly event:', e.data.event);
                
                if (e.data.event === 'calendly.event_scheduled') {
                    // Event scheduled
                    console.log('Event scheduled:', e.data);
                    
                    // You can add custom tracking code here
                    // For example, send data to Google Analytics
                    if (typeof ga !== 'undefined') {
                        ga('send', 'event', 'Calendly', 'Event Scheduled', 'Booking Completed');
                    }
                    
                    // Or show a custom thank you message
                    alert('Thank you for scheduling an appointment!');
                }
            }
        });
        </script>
        '''
        
        return {
            'widget_code': widget_data['widget_code'],
            'tracking_code': tracking_code,
            'event_type_uri': widget_data['event_type_uri'],
            'widget_type': widget_type,
            'full_code': widget_data['widget_code'] + tracking_code
        }
    
    def sync_events_with_businesses(self):
        """Sync Calendly events with businesses in the database."""
        # Get all events from Calendly
        events_data = self.get_scheduled_events()
        
        if 'error' in events_data:
            return events_data
        
        # Get all businesses from database
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, email FROM businesses')
        businesses = cursor.fetchall()
        
        # Match events with businesses based on email
        matched_count = 0
        
        for event in events_data.get('events', []):
            invitee_email = event.get('invitee_email')
            
            if invitee_email:
                for business in businesses:
                    if business['email'] and business['email'].lower() == invitee_email.lower():
                        # Update event with business ID
                        cursor.execute('UPDATE calendly_events SET business_id = ? WHERE id = ?', (business['id'], event.get('id')))
                        matched_count += 1
                        break
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'total_events': len(events_data.get('events', [])),
            'matched_events': matched_count
        }

def main():
    """Test the CalendlyIntegration."""
    # This would use real API keys in production
    integration = CalendlyIntegration(
        api_key='test_api_key',
        user_uri='https://calendly.com/test_user'
    )
    
    # Generate widget code
    widget_data = integration.generate_website_integration_code(
        widget_type='inline'
    )
    
    print("Calendly Widget Code:")
    print(widget_data['widget_code'])
    
    print("\nCalendly Tracking Code:")
    print(widget_data['tracking_code'])

if __name__ == '__main__':
    main()
