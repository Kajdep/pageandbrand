#!/usr/bin/env python3
"""
Outreach CLI Interface

This script provides a command-line interface for the OutreachGenerator tool.
"""

import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from outreach.outreach_generator import OutreachGenerator

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate personalized outreach emails for businesses without websites.')
    
    parser.add_argument('--input-file', '-i', type=str, required=True,
                        help='Path to CSV or JSON file containing business data')
    
    parser.add_argument('--template', '-t', type=str, default='initial_contact.txt',
                        choices=['initial_contact.txt', 'follow_up.txt', 'value_proposition.txt'],
                        help='Email template to use (default: initial_contact.txt)')
    
    parser.add_argument('--campaign', '-c', type=str, default=None,
                        help='Campaign name for organizing emails')
    
    parser.add_argument('--list-templates', '-l', action='store_true',
                        help='List available email templates')
    
    return parser.parse_args()

def main():
    """Main function to run the CLI interface."""
    args = parse_arguments()
    
    # Initialize the OutreachGenerator
    generator = OutreachGenerator()
    
    # List templates if requested
    if args.list_templates:
        print("Available email templates:")
        for template_name in generator.templates.keys():
            print(f"  - {template_name}")
        return
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        return
    
    # Load business data from input file
    print(f"Loading business data from {args.input_file}...")
    if args.input_file.endswith('.csv'):
        businesses = generator.load_businesses_from_csv(args.input_file)
    elif args.input_file.endswith('.json'):
        businesses = generator.load_businesses_from_json(args.input_file)
    else:
        print("Error: Input file must be CSV or JSON format.")
        return
    
    if not businesses:
        print("No business data found in the input file.")
        return
    
    print(f"Loaded {len(businesses)} businesses.")
    
    # Generate emails
    print(f"Generating personalized emails using template '{args.template}'...")
    emails = generator.generate_batch_emails(businesses, args.template)
    
    # Save the generated emails
    campaign_name = args.campaign or f"campaign_{os.path.basename(args.input_file).split('.')[0]}"
    saved_files = generator.save_batch_emails(emails, campaign_name=campaign_name)
    
    print(f"Generated and saved {len(saved_files)} emails:")
    for filepath in saved_files[:5]:  # Show first 5 files
        print(f"  - {filepath}")
    
    if len(saved_files) > 5:
        print(f"  ... and {len(saved_files) - 5} more.")
    
    print(f"\nAll emails saved to: {os.path.dirname(saved_files[0])}")
    print("Done!")

if __name__ == "__main__":
    main()
