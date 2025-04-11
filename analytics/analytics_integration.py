#!/usr/bin/env python3
"""
Analytics Integration Module

This script integrates the MessageAnalytics with the Flask application.
"""

import os
import sys
import json
from datetime import datetime

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analytics.message_analytics import MessageAnalytics

class AnalyticsIntegration:
    """Class for integrating MessageAnalytics with Flask application."""
    
    def __init__(self, db_path=None):
        """Initialize the AnalyticsIntegration."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.analytics = MessageAnalytics(db_path=db_path)
        self.output_dir = os.path.join(base_dir, 'data', 'analytics')
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def track_message_event(self, message_id, business_id, template_id, status):
        """Track a message event."""
        return self.analytics.track_message(
            message_id=message_id,
            business_id=business_id,
            template_id=template_id,
            status=status
        )
    
    def get_message_analytics(self, message_id):
        """Get analytics for a specific message."""
        return self.analytics.get_message_analytics(message_id)
    
    def get_template_analytics(self, template_id):
        """Get analytics for a specific template."""
        return self.analytics.get_template_analytics(template_id)
    
    def compare_templates(self, template_ids=None):
        """Compare the performance of different templates."""
        return self.analytics.compare_templates(template_ids)
    
    def generate_performance_report(self, days=30, output_format='html'):
        """Generate a performance report for outreach messages."""
        return self.analytics.generate_performance_report(days, output_format)
    
    def analyze_message_content(self, template_ids=None):
        """Analyze message content to identify effective patterns."""
        return self.analytics.analyze_message_content(template_ids)
    
    def get_dashboard_data(self):
        """Get data for the analytics dashboard."""
        # Get overall metrics
        templates_comparison = self.compare_templates()
        
        # Get content analysis
        content_analysis = self.analyze_message_content()
        
        # Generate recent report
        report_result = self.generate_performance_report(days=30, output_format='json')
        report_path = report_result.get('report_path')
        
        report_data = {}
        if report_path and os.path.exists(report_path):
            with open(report_path, 'r') as f:
                report_data = json.load(f)
        
        # Prepare dashboard data
        dashboard_data = {
            'generated_at': datetime.now().isoformat(),
            'overall_metrics': report_data.get('overall', {}),
            'templates_performance': templates_comparison,
            'content_recommendations': content_analysis.get('recommendations', []),
            'daily_metrics': report_data.get('daily', []),
            'report_url': f"/analytics/reports/performance_report.html"
        }
        
        return dashboard_data

def main():
    """Test the AnalyticsIntegration."""
    integration = AnalyticsIntegration()
    
    # Track a test message
    integration.track_message_event(
        message_id='test_message_1',
        business_id='test_business_1',
        template_id='test_template_1',
        status='sent'
    )
    
    # Generate a performance report
    report = integration.generate_performance_report(days=30, output_format='html')
    
    if 'success' in report and report['success']:
        print(f"Report generated: {report['report_path']}")
    else:
        print("Failed to generate report:", report.get('error', 'Unknown error'))
    
    # Get dashboard data
    dashboard_data = integration.get_dashboard_data()
    print("Dashboard data generated")

if __name__ == '__main__':
    main()
