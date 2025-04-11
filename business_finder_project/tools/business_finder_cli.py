#!/usr/bin/env python3
"""
Business Finder CLI Interface

This script provides a command-line interface for the BusinessFinder tool.
"""

import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.business_finder import BusinessFinder

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find businesses without websites in specified locations.')
    
    parser.add_argument('--query', '-q', type=str, required=True,
                        help='Type of business to search for (e.g., restaurants, plumbers)')
    
    parser.add_argument('--location', '-l', type=str, required=True,
                        help='Location to search in (e.g., "London, UK")')
    
    parser.add_argument('--max-results', '-m', type=int, default=20,
                        help='Maximum number of results to return (default: 20)')
    
    parser.add_argument('--min-rating', '-r', type=float, default=None,
                        help='Minimum rating to include in results')
    
    parser.add_argument('--categories', '-c', type=str, nargs='+', default=None,
                        help='Categories to include (space-separated)')
    
    parser.add_argument('--exclude-social', '-e', action='store_true',
                        help='Exclude businesses with social media presence')
    
    parser.add_argument('--output-format', '-o', type=str, choices=['csv', 'json', 'both'], default='both',
                        help='Output format (csv, json, or both)')
    
    parser.add_argument('--output-file', '-f', type=str, default=None,
                        help='Output filename (without extension)')
    
    parser.add_argument('--api-key', '-k', type=str, default=None,
                        help='Google Maps API key (if available)')
    
    return parser.parse_args()

def main():
    """Main function to run the CLI interface."""
    args = parse_arguments()
    
    # Initialize the BusinessFinder
    finder = BusinessFinder(api_key=args.api_key)
    
    print(f"Searching for {args.query} in {args.location}...")
    
    # Find businesses
    if args.api_key:
        businesses = finder.find_businesses_google_maps(args.query, args.location, args.max_results)
    else:
        businesses = finder.find_businesses_manual(args.query, args.location, args.max_results)
    
    print(f"Found {len(businesses)} businesses without websites.")
    
    # Apply filters if specified
    if args.min_rating or args.categories or args.exclude_social:
        filtered = finder.filter_results(
            min_rating=args.min_rating,
            categories=args.categories,
            exclude_social_media=args.exclude_social
        )
        print(f"Filtered to {len(filtered)} businesses.")
    
    # Export results
    if args.output_format in ['csv', 'both']:
        csv_file = finder.export_to_csv(
            filename=f"{args.output_file}.csv" if args.output_file else None
        )
        print(f"CSV exported to: {csv_file}")
    
    if args.output_format in ['json', 'both']:
        json_file = finder.export_to_json(
            filename=f"{args.output_file}.json" if args.output_file else None
        )
        print(f"JSON exported to: {json_file}")
    
    print("Done!")

if __name__ == "__main__":
    main()
