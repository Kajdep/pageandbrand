#!/usr/bin/env python3
"""
Message Analytics Module

This script provides functionality to analyze the effectiveness of outreach messages.
"""

import os
import sys
import json
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import Counter

class MessageAnalytics:
    """Class for analyzing the effectiveness of outreach messages."""
    
    def __init__(self, db_path=None):
        """Initialize the MessageAnalytics with database path."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = db_path or os.path.join(base_dir, 'data', 'outreach.db')
        self.output_dir = os.path.join(base_dir, 'data', 'analytics')
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create database tables if they don't exist
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create message_analytics table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS message_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT,
            business_id TEXT,
            template_id TEXT,
            sent_at TEXT,
            opened_at TEXT,
            replied_at TEXT,
            clicked_at TEXT,
            booked_at TEXT,
            status TEXT,
            FOREIGN KEY (business_id) REFERENCES businesses(id),
            FOREIGN KEY (message_id) REFERENCES messages(id),
            FOREIGN KEY (template_id) REFERENCES message_templates(id)
        )
        ''')
        
        # Create message_templates table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS message_templates (
            id TEXT PRIMARY KEY,
            name TEXT,
            subject TEXT,
            body TEXT,
            category TEXT,
            tags TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_message(self, message_id, business_id, template_id, status='sent'):
        """Track a message event."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if message already exists
        cursor.execute('SELECT id FROM message_analytics WHERE message_id = ?', (message_id,))
        existing = cursor.fetchone()
        
        now = datetime.now().isoformat()
        
        if existing:
            # Update existing record
            if status == 'sent':
                cursor.execute('UPDATE message_analytics SET sent_at = ? WHERE message_id = ?', (now, message_id))
            elif status == 'opened':
                cursor.execute('UPDATE message_analytics SET opened_at = ? WHERE message_id = ?', (now, message_id))
            elif status == 'replied':
                cursor.execute('UPDATE message_analytics SET replied_at = ? WHERE message_id = ?', (now, message_id))
            elif status == 'clicked':
                cursor.execute('UPDATE message_analytics SET clicked_at = ? WHERE message_id = ?', (now, message_id))
            elif status == 'booked':
                cursor.execute('UPDATE message_analytics SET booked_at = ? WHERE message_id = ?', (now, message_id))
            
            cursor.execute('UPDATE message_analytics SET status = ? WHERE message_id = ?', (status, message_id))
        else:
            # Create new record
            sent_at = now if status == 'sent' else None
            opened_at = now if status == 'opened' else None
            replied_at = now if status == 'replied' else None
            clicked_at = now if status == 'clicked' else None
            booked_at = now if status == 'booked' else None
            
            cursor.execute('''
            INSERT INTO message_analytics (
                message_id, business_id, template_id, sent_at, opened_at, replied_at, clicked_at, booked_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                message_id, business_id, template_id, sent_at, opened_at, replied_at, clicked_at, booked_at, status
            ))
        
        conn.commit()
        conn.close()
        
        return {'success': True, 'message_id': message_id, 'status': status}
    
    def get_message_analytics(self, message_id):
        """Get analytics for a specific message."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM message_analytics WHERE message_id = ?', (message_id,))
        analytics = cursor.fetchone()
        
        conn.close()
        
        if analytics:
            return dict(analytics)
        
        return None
    
    def get_template_analytics(self, template_id):
        """Get analytics for a specific template."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT 
            COUNT(*) as sent_count,
            SUM(CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END) as opened_count,
            SUM(CASE WHEN replied_at IS NOT NULL THEN 1 ELSE 0 END) as replied_count,
            SUM(CASE WHEN clicked_at IS NOT NULL THEN 1 ELSE 0 END) as clicked_count,
            SUM(CASE WHEN booked_at IS NOT NULL THEN 1 ELSE 0 END) as booked_count
        FROM message_analytics 
        WHERE template_id = ?
        ''', (template_id,))
        
        analytics = cursor.fetchone()
        
        # Get template details
        cursor.execute('SELECT * FROM message_templates WHERE id = ?', (template_id,))
        template = cursor.fetchone()
        
        conn.close()
        
        if analytics and template:
            result = dict(analytics)
            result['template'] = dict(template)
            
            # Calculate rates
            sent_count = result['sent_count']
            if sent_count > 0:
                result['open_rate'] = (result['opened_count'] / sent_count) * 100
                result['reply_rate'] = (result['replied_count'] / sent_count) * 100
                result['click_rate'] = (result['clicked_count'] / sent_count) * 100
                result['booking_rate'] = (result['booked_count'] / sent_count) * 100
            else:
                result['open_rate'] = 0
                result['reply_rate'] = 0
                result['click_rate'] = 0
                result['booking_rate'] = 0
            
            return result
        
        return None
    
    def compare_templates(self, template_ids=None):
        """Compare the performance of different templates."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if template_ids:
            placeholders = ','.join(['?' for _ in template_ids])
            cursor.execute(f'''
            SELECT 
                template_id,
                COUNT(*) as sent_count,
                SUM(CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END) as opened_count,
                SUM(CASE WHEN replied_at IS NOT NULL THEN 1 ELSE 0 END) as replied_count,
                SUM(CASE WHEN clicked_at IS NOT NULL THEN 1 ELSE 0 END) as clicked_count,
                SUM(CASE WHEN booked_at IS NOT NULL THEN 1 ELSE 0 END) as booked_count
            FROM message_analytics 
            WHERE template_id IN ({placeholders})
            GROUP BY template_id
            ''', template_ids)
        else:
            cursor.execute('''
            SELECT 
                template_id,
                COUNT(*) as sent_count,
                SUM(CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END) as opened_count,
                SUM(CASE WHEN replied_at IS NOT NULL THEN 1 ELSE 0 END) as replied_count,
                SUM(CASE WHEN clicked_at IS NOT NULL THEN 1 ELSE 0 END) as clicked_count,
                SUM(CASE WHEN booked_at IS NOT NULL THEN 1 ELSE 0 END) as booked_count
            FROM message_analytics 
            GROUP BY template_id
            ''')
        
        analytics = cursor.fetchall()
        
        # Get template details
        template_data = {}
        for row in analytics:
            template_id = row['template_id']
            cursor.execute('SELECT name FROM message_templates WHERE id = ?', (template_id,))
            template = cursor.fetchone()
            if template:
                template_data[template_id] = template['name']
        
        conn.close()
        
        results = []
        for row in analytics:
            template_id = row['template_id']
            result = dict(row)
            
            # Add template name
            result['template_name'] = template_data.get(template_id, 'Unknown Template')
            
            # Calculate rates
            sent_count = result['sent_count']
            if sent_count > 0:
                result['open_rate'] = (result['opened_count'] / sent_count) * 100
                result['reply_rate'] = (result['replied_count'] / sent_count) * 100
                result['click_rate'] = (result['clicked_count'] / sent_count) * 100
                result['booking_rate'] = (result['booked_count'] / sent_count) * 100
            else:
                result['open_rate'] = 0
                result['reply_rate'] = 0
                result['click_rate'] = 0
                result['booking_rate'] = 0
            
            results.append(result)
        
        return results
    
    def generate_performance_report(self, days=30, output_format='html'):
        """Generate a performance report for outreach messages."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get overall metrics
        cursor.execute('''
        SELECT 
            COUNT(*) as sent_count,
            SUM(CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END) as opened_count,
            SUM(CASE WHEN replied_at IS NOT NULL THEN 1 ELSE 0 END) as replied_count,
            SUM(CASE WHEN clicked_at IS NOT NULL THEN 1 ELSE 0 END) as clicked_count,
            SUM(CASE WHEN booked_at IS NOT NULL THEN 1 ELSE 0 END) as booked_count
        FROM message_analytics 
        WHERE sent_at >= ? AND sent_at <= ?
        ''', (start_date.isoformat(), end_date.isoformat()))
        
        overall = cursor.fetchone()
        
        # Get template performance
        cursor.execute('''
        SELECT 
            mt.name as template_name,
            COUNT(*) as sent_count,
            SUM(CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END) as opened_count,
            SUM(CASE WHEN replied_at IS NOT NULL THEN 1 ELSE 0 END) as replied_count,
            SUM(CASE WHEN clicked_at IS NOT NULL THEN 1 ELSE 0 END) as clicked_count,
            SUM(CASE WHEN booked_at IS NOT NULL THEN 1 ELSE 0 END) as booked_count
        FROM message_analytics ma
        JOIN message_templates mt ON ma.template_id = mt.id
        WHERE sent_at >= ? AND sent_at <= ?
        GROUP BY mt.id
        ORDER BY sent_count DESC
        ''', (start_date.isoformat(), end_date.isoformat()))
        
        templates = cursor.fetchall()
        
        # Get daily metrics
        cursor.execute('''
        SELECT 
            date(sent_at) as date,
            COUNT(*) as sent_count,
            SUM(CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END) as opened_count,
            SUM(CASE WHEN replied_at IS NOT NULL THEN 1 ELSE 0 END) as replied_count,
            SUM(CASE WHEN clicked_at IS NOT NULL THEN 1 ELSE 0 END) as clicked_count,
            SUM(CASE WHEN booked_at IS NOT NULL THEN 1 ELSE 0 END) as booked_count
        FROM message_analytics 
        WHERE sent_at >= ? AND sent_at <= ?
        GROUP BY date(sent_at)
        ORDER BY date(sent_at)
        ''', (start_date.isoformat(), end_date.isoformat()))
        
        daily = cursor.fetchall()
        
        conn.close()
        
        # Generate report
        if output_format == 'html':
            return self._generate_html_report(overall, templates, daily, days)
        elif output_format == 'json':
            return self._generate_json_report(overall, templates, daily, days)
        else:
            return {'error': f'Unsupported output format: {output_format}'}
    
    def _generate_html_report(self, overall, templates, daily, days):
        """Generate HTML report."""
        # Convert to DataFrames
        overall_df = pd.DataFrame([dict(overall)])
        templates_df = pd.DataFrame([dict(t) for t in templates])
        daily_df = pd.DataFrame([dict(d) for d in daily])
        
        # Calculate rates for overall
        if overall['sent_count'] > 0:
            overall_df['open_rate'] = (overall_df['opened_count'] / overall_df['sent_count']) * 100
            overall_df['reply_rate'] = (overall_df['replied_count'] / overall_df['sent_count']) * 100
            overall_df['click_rate'] = (overall_df['clicked_count'] / overall_df['sent_count']) * 100
            overall_df['booking_rate'] = (overall_df['booked_count'] / overall_df['sent_count']) * 100
        else:
            overall_df['open_rate'] = 0
            overall_df['reply_rate'] = 0
            overall_df['click_rate'] = 0
            overall_df['booking_rate'] = 0
        
        # Calculate rates for templates
        if not templates_df.empty:
            templates_df['open_rate'] = (templates_df['opened_count'] / templates_df['sent_count']) * 100
            templates_df['reply_rate'] = (templates_df['replied_count'] / templates_df['sent_count']) * 100
            templates_df['click_rate'] = (templates_df['clicked_count'] / templates_df['sent_count']) * 100
            templates_df['booking_rate'] = (templates_df['booked_count'] / templates_df['sent_count']) * 100
        
        # Generate charts
        self._generate_charts(overall_df, templates_df, daily_df)
        
        # Generate HTML
        html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Outreach Message Performance Report</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ padding-top: 20px; }}
                .chart-container {{ margin-bottom: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="mb-4">Outreach Message Performance Report</h1>
                <p class="lead">Performance metrics for the last {days} days</p>
                
                <div class="row mb-4">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title">Overall Performance</h5>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-3">
                                        <div class="card text-center mb-3">
                                            <div class="card-body">
                                                <h3>{overall['sent_count']}</h3>
                                                <p class="text-muted">Messages Sent</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="card text-center mb-3">
                                            <div class="card-body">
                                                <h3>{overall['opened_count']}</h3>
                                                <p class="text-muted">Messages Opened</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="card text-center mb-3">
                                            <div class="card-body">
                                                <h3>{overall['replied_count']}</h3>
                                                <p class="text-muted">Replies Received</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="card text-center mb-3">
                                            <div class="card-body">
                                                <h3>{overall['booked_count']}</h3>
                                                <p class="text-muted">Appointments Booked</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3>{overall_df['open_rate'].values[0]:.1f}%</h3>
                                                <p class="text-muted">Open Rate</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3>{overall_df['reply_rate'].values[0]:.1f}%</h3>
                                                <p class="text-muted">Reply Rate</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3>{overall_df['click_rate'].values[0]:.1f}%</h3>
                                                <p class="text-muted">Click Rate</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="card text-center">
                                            <div class="card-body">
                                                <h3>{overall_df['booking_rate'].values[0]:.1f}%</h3>
                                                <p class="text-muted">Booking Rate</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-6">
                        <div class="card chart-container">
                            <div class="card-header">
                                <h5 class="card-title">Daily Message Activity</h5>
                            </div>
                            <div class="card-body">
                                <img src="daily_activity.png" class="img-fluid" alt="Daily Message Activity">
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card chart-container">
                            <div class="card-header">
                                <h5 class="card-title">Conversion Funnel</h5>
                            </div>
                            <div class="card-body">
                                <img src="conversion_funnel.png" class="img-fluid" alt="Conversion Funnel">
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title">Template Performance</h5>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped">
                                        <thead>
                                            <tr>
                                                <th>Template</th>
                                                <th>Sent</th>
                                                <th>Opened</th>
                                                <th>Open Rate</th>
                                                <th>Replied</th>
                                                <th>Reply Rate</th>
                                                <th>Booked</th>
                                                <th>Booking Rate</th>
                                            </tr>
                                        </thead>
                                        <tbody>
        '''
        
        # Add template rows
        for _, row in templates_df.iterrows():
            html += f'''
                                            <tr>
                                                <td>{row['template_name']}</td>
                                                <td>{row['sent_count']}</td>
                                                <td>{row['opened_count']}</td>
                                                <td>{row['open_rate']:.1f}%</td>
                                                <td>{row['replied_count']}</td>
                                                <td>{row['reply_rate']:.1f}%</td>
                                                <td>{row['booked_count']}</td>
                                                <td>{row['booking_rate']:.1f}%</td>
                                            </tr>
            '''
        
        html += f'''
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-12">
                        <div class="card chart-container">
                            <div class="card-header">
                                <h5 class="card-title">Template Comparison</h5>
                            </div>
                            <div class="card-body">
                                <img src="template_comparison.png" class="img-fluid" alt="Template Comparison">
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title">Daily Metrics</h5>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped">
                                        <thead>
                                            <tr>
                                                <th>Date</th>
                                                <th>Sent</th>
                                                <th>Opened</th>
                                                <th>Replied</th>
                                                <th>Clicked</th>
                                                <th>Booked</th>
                                            </tr>
                                        </thead>
                                        <tbody>
        '''
        
        # Add daily rows
        for _, row in daily_df.iterrows():
            html += f'''
                                            <tr>
                                                <td>{row['date']}</td>
                                                <td>{row['sent_count']}</td>
                                                <td>{row['opened_count']}</td>
                                                <td>{row['replied_count']}</td>
                                                <td>{row['clicked_count']}</td>
                                                <td>{row['booked_count']}</td>
                                            </tr>
            '''
        
        html += f'''
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <footer class="text-center text-muted mb-4">
                    <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </footer>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        '''
        
        # Save HTML report
        report_path = os.path.join(self.output_dir, 'performance_report.html')
        with open(report_path, 'w') as f:
            f.write(html)
        
        return {
            'success': True,
            'report_path': report_path,
            'charts': [
                os.path.join(self.output_dir, 'daily_activity.png'),
                os.path.join(self.output_dir, 'conversion_funnel.png'),
                os.path.join(self.output_dir, 'template_comparison.png')
            ]
        }
    
    def _generate_json_report(self, overall, templates, daily, days):
        """Generate JSON report."""
        # Convert to dictionaries
        overall_dict = dict(overall)
        templates_list = [dict(t) for t in templates]
        daily_list = [dict(d) for d in daily]
        
        # Calculate rates for overall
        if overall_dict['sent_count'] > 0:
            overall_dict['open_rate'] = (overall_dict['opened_count'] / overall_dict['sent_count']) * 100
            overall_dict['reply_rate'] = (overall_dict['replied_count'] / overall_dict['sent_count']) * 100
            overall_dict['click_rate'] = (overall_dict['clicked_count'] / overall_dict['sent_count']) * 100
            overall_dict['booking_rate'] = (overall_dict['booked_count'] / overall_dict['sent_count']) * 100
        else:
            overall_dict['open_rate'] = 0
            overall_dict['reply_rate'] = 0
            overall_dict['click_rate'] = 0
            overall_dict['booking_rate'] = 0
        
        # Calculate rates for templates
        for template in templates_list:
            if template['sent_count'] > 0:
                template['open_rate'] = (template['opened_count'] / template['sent_count']) * 100
                template['reply_rate'] = (template['replied_count'] / template['sent_count']) * 100
                template['click_rate'] = (template['clicked_count'] / template['sent_count']) * 100
                template['booking_rate'] = (template['booked_count'] / template['sent_count']) * 100
            else:
                template['open_rate'] = 0
                template['reply_rate'] = 0
                template['click_rate'] = 0
                template['booking_rate'] = 0
        
        # Create report data
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'period_days': days,
            'overall': overall_dict,
            'templates': templates_list,
            'daily': daily_list
        }
        
        # Save JSON report
        report_path = os.path.join(self.output_dir, 'performance_report.json')
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return {
            'success': True,
            'report_path': report_path
        }
    
    def _generate_charts(self, overall_df, templates_df, daily_df):
        """Generate charts for the report."""
        # Set style
        plt.style.use('ggplot')
        
        # 1. Daily Activity Chart
        if not daily_df.empty:
            plt.figure(figsize=(10, 6))
            plt.plot(daily_df['date'], daily_df['sent_count'], marker='o', label='Sent')
            plt.plot(daily_df['date'], daily_df['opened_count'], marker='o', label='Opened')
            plt.plot(daily_df['date'], daily_df['replied_count'], marker='o', label='Replied')
            plt.plot(daily_df['date'], daily_df['booked_count'], marker='o', label='Booked')
            plt.title('Daily Message Activity')
            plt.xlabel('Date')
            plt.ylabel('Count')
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'daily_activity.png'))
            plt.close()
        
        # 2. Conversion Funnel
        plt.figure(figsize=(10, 6))
        stages = ['Sent', 'Opened', 'Replied', 'Clicked', 'Booked']
        values = [
            overall_df['sent_count'].values[0],
            overall_df['opened_count'].values[0],
            overall_df['replied_count'].values[0],
            overall_df['clicked_count'].values[0],
            overall_df['booked_count'].values[0]
        ]
        
        plt.bar(stages, values, color='#4e57d4')
        plt.title('Conversion Funnel')
        plt.xlabel('Stage')
        plt.ylabel('Count')
        
        # Add percentage labels
        for i, v in enumerate(values):
            if i > 0 and values[0] > 0:
                percentage = (v / values[0]) * 100
                plt.text(i, v + 5, f'{percentage:.1f}%', ha='center')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'conversion_funnel.png'))
        plt.close()
        
        # 3. Template Comparison
        if not templates_df.empty:
            plt.figure(figsize=(12, 8))
            
            # Limit to top 5 templates by sent count if there are more
            if len(templates_df) > 5:
                templates_df = templates_df.sort_values('sent_count', ascending=False).head(5)
            
            x = np.arange(len(templates_df))
            width = 0.2
            
            plt.bar(x - width*1.5, templates_df['open_rate'], width, label='Open Rate')
            plt.bar(x - width/2, templates_df['reply_rate'], width, label='Reply Rate')
            plt.bar(x + width/2, templates_df['click_rate'], width, label='Click Rate')
            plt.bar(x + width*1.5, templates_df['booking_rate'], width, label='Booking Rate')
            
            plt.title('Template Performance Comparison')
            plt.xlabel('Template')
            plt.ylabel('Rate (%)')
            plt.xticks(x, templates_df['template_name'], rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'template_comparison.png'))
            plt.close()
    
    def analyze_message_content(self, template_ids=None):
        """Analyze message content to identify effective patterns."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get templates and their performance
        if template_ids:
            placeholders = ','.join(['?' for _ in template_ids])
            cursor.execute(f'''
            SELECT 
                mt.id, mt.name, mt.subject, mt.body, mt.category, mt.tags,
                COUNT(ma.id) as sent_count,
                SUM(CASE WHEN ma.replied_at IS NOT NULL THEN 1 ELSE 0 END) as replied_count,
                SUM(CASE WHEN ma.booked_at IS NOT NULL THEN 1 ELSE 0 END) as booked_count
            FROM message_templates mt
            LEFT JOIN message_analytics ma ON mt.id = ma.template_id
            WHERE mt.id IN ({placeholders})
            GROUP BY mt.id
            ''', template_ids)
        else:
            cursor.execute('''
            SELECT 
                mt.id, mt.name, mt.subject, mt.body, mt.category, mt.tags,
                COUNT(ma.id) as sent_count,
                SUM(CASE WHEN ma.replied_at IS NOT NULL THEN 1 ELSE 0 END) as replied_count,
                SUM(CASE WHEN ma.booked_at IS NOT NULL THEN 1 ELSE 0 END) as booked_count
            FROM message_templates mt
            LEFT JOIN message_analytics ma ON mt.id = ma.template_id
            GROUP BY mt.id
            ''')
        
        templates = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        templates = [dict(t) for t in templates]
        
        # Calculate rates
        for template in templates:
            if template['sent_count'] > 0:
                template['reply_rate'] = (template['replied_count'] / template['sent_count']) * 100
                template['booking_rate'] = (template['booked_count'] / template['sent_count']) * 100
            else:
                template['reply_rate'] = 0
                template['booking_rate'] = 0
        
        # Sort by reply rate (descending)
        templates.sort(key=lambda x: x['reply_rate'], reverse=True)
        
        # Analyze content patterns
        high_performing = [t for t in templates if t['reply_rate'] > 20]  # Templates with >20% reply rate
        low_performing = [t for t in templates if t['reply_rate'] <= 20 and t['sent_count'] > 10]  # Low performing with sufficient data
        
        # Extract common words and phrases
        high_words = self._extract_common_words([t['body'] for t in high_performing])
        low_words = self._extract_common_words([t['body'] for t in low_performing])
        
        # Find distinctive words in high-performing templates
        distinctive_words = []
        for word, count in high_words.items():
            if word in low_words:
                if count / len(high_performing) > low_words[word] / len(low_performing):
                    distinctive_words.append(word)
            else:
                distinctive_words.append(word)
        
        # Analyze subject lines
        high_subjects = [t['subject'] for t in high_performing]
        subject_patterns = self._analyze_subject_lines(high_subjects)
        
        # Generate recommendations
        recommendations = self._generate_content_recommendations(
            high_performing, low_performing, distinctive_words, subject_patterns
        )
        
        return {
            'templates': templates,
            'high_performing': high_performing,
            'low_performing': low_performing,
            'distinctive_words': distinctive_words[:20],  # Top 20 distinctive words
            'subject_patterns': subject_patterns,
            'recommendations': recommendations
        }
    
    def _extract_common_words(self, texts):
        """Extract common words from a list of texts."""
        # Combine all texts
        combined_text = ' '.join(texts).lower()
        
        # Remove punctuation and split into words
        words = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in combined_text).split()
        
        # Remove common stop words
        stop_words = {'the', 'and', 'a', 'to', 'of', 'in', 'is', 'that', 'it', 'for', 'you', 'with', 'on', 'as', 'are', 'be', 'this', 'was', 'have', 'or', 'at', 'by', 'not', 'we', 'your', 'our', 'from', 'an', 'will', 'can', 'but', 'they', 'their', 'has', 'if', 'which', 'when', 'what', 'all', 'been', 'would', 'there', 'who', 'so', 'no', 'do', 'my', 'out', 'up', 'about', 'me', 'just', 'more', 'some', 'like', 'time', 'very', 'now', 'only', 'his', 'her', 'them', 'its', 'than', 'he', 'she', 'him', 'i', 'am', 'were', 'had', 'how', 'any', 'could', 'should', 'did', 'one', 'each', 'other', 'these', 'those', 'then', 'into', 'over', 'such', 'here', 'why', 'way', 'even', 'well', 'also', 'us', 'because', 'too', 'own', 'through', 'same', 'while', 'where', 'after', 'before', 'again', 'under', 'both', 'during', 'few', 'between', 'above', 'never', 'always', 'however', 'although', 'whether', 'without', 'within', 'against', 'upon', 'toward', 'among', 'throughout', 'despite', 'except', 'beyond', 'along', 'since', 'until', 'per', 'regarding', 'via', 'according', 'besides', 'furthermore'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequencies
        word_counts = Counter(filtered_words)
        
        return word_counts
    
    def _analyze_subject_lines(self, subjects):
        """Analyze subject lines for patterns."""
        patterns = {
            'question': 0,
            'personalized': 0,
            'short': 0,
            'contains_number': 0,
            'contains_business_name': 0,
            'contains_benefit': 0
        }
        
        benefit_keywords = ['improve', 'boost', 'increase', 'grow', 'enhance', 'save', 'reduce', 'maximize', 'optimize', 'gain', 'profit', 'revenue', 'customer', 'client', 'lead', 'sale', 'traffic', 'visibility', 'exposure', 'presence']
        
        for subject in subjects:
            # Question
            if '?' in subject:
                patterns['question'] += 1
            
            # Personalized (contains placeholder or specific reference)
            if '{' in subject or '}' in subject or 'your' in subject.lower() or 'you' in subject.lower():
                patterns['personalized'] += 1
            
            # Short (less than 50 characters)
            if len(subject) < 50:
                patterns['short'] += 1
            
            # Contains number
            if any(c.isdigit() for c in subject):
                patterns['contains_number'] += 1
            
            # Contains business name placeholder
            if '{business' in subject.lower() or 'your business' in subject.lower():
                patterns['contains_business_name'] += 1
            
            # Contains benefit
            if any(keyword in subject.lower() for keyword in benefit_keywords):
                patterns['contains_benefit'] += 1
        
        # Convert to percentages
        total = len(subjects)
        if total > 0:
            for key in patterns:
                patterns[key] = (patterns[key] / total) * 100
        
        return patterns
    
    def _generate_content_recommendations(self, high_performing, low_performing, distinctive_words, subject_patterns):
        """Generate content recommendations based on analysis."""
        recommendations = []
        
        # Subject line recommendations
        subject_recs = []
        if subject_patterns.get('question', 0) > 50:
            subject_recs.append("Use questions in subject lines to increase engagement")
        if subject_patterns.get('personalized', 0) > 50:
            subject_recs.append("Personalize subject lines with business name or industry")
        if subject_patterns.get('short', 0) > 70:
            subject_recs.append("Keep subject lines concise (under 50 characters)")
        if subject_patterns.get('contains_benefit', 0) > 40:
            subject_recs.append("Highlight benefits in subject lines")
        
        if subject_recs:
            recommendations.append({
                'category': 'Subject Lines',
                'recommendations': subject_recs
            })
        
        # Message content recommendations
        content_recs = []
        
        # Check if high-performing templates exist
        if high_performing:
            # Check average length
            avg_high_length = sum(len(t['body']) for t in high_performing) / len(high_performing)
            avg_low_length = sum(len(t['body']) for t in low_performing) / len(low_performing) if low_performing else 0
            
            if avg_high_length < avg_low_length:
                content_recs.append("Keep messages concise and to the point")
            elif avg_high_length > avg_low_length:
                content_recs.append("Provide more detailed information in messages")
            
            # Check for distinctive words
            if distinctive_words:
                content_recs.append(f"Include key terms that resonate with your audience: {', '.join(distinctive_words[:5])}")
            
            # Check for personalization
            personalization_count = sum(1 for t in high_performing if '{' in t['body'] or '}' in t['body'])
            if personalization_count / len(high_performing) > 0.5:
                content_recs.append("Personalize messages with business-specific information")
            
            # Check for call to action
            cta_count = sum(1 for t in high_performing if 'schedule' in t['body'].lower() or 'book' in t['body'].lower() or 'appointment' in t['body'].lower() or 'call' in t['body'].lower() or 'contact' in t['body'].lower())
            if cta_count / len(high_performing) > 0.7:
                content_recs.append("Include clear calls to action")
        else:
            content_recs.append("Not enough high-performing templates to generate specific recommendations")
        
        if content_recs:
            recommendations.append({
                'category': 'Message Content',
                'recommendations': content_recs
            })
        
        # General recommendations
        general_recs = [
            "Test different message templates to identify what works best for your audience",
            "Follow up with businesses that don't respond to initial outreach",
            "Segment your audience and tailor messages to specific business categories",
            "Include social proof or testimonials from similar businesses"
        ]
        
        recommendations.append({
            'category': 'General Strategy',
            'recommendations': general_recs
        })
        
        return recommendations

def main():
    """Test the MessageAnalytics."""
    analytics = MessageAnalytics()
    
    # Generate a performance report
    report = analytics.generate_performance_report(days=30, output_format='html')
    
    if 'success' in report and report['success']:
        print(f"Report generated: {report['report_path']}")
    else:
        print("Failed to generate report:", report.get('error', 'Unknown error'))

if __name__ == '__main__':
    main()
