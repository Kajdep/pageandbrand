#!/usr/bin/env python3
"""
Business Finder Tool

This script helps find local businesses without websites in specified locations.
It uses Google Maps data and provides filtering options to identify potential clients.
"""

import os
import json
import time
import pandas as pd
import requests
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class BusinessFinder:
    """Tool to find businesses without websites in specified locations."""
    
    def __init__(self, api_key=None):
        """Initialize the BusinessFinder with optional API key."""
        self.api_key = api_key
        self.results = []
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def find_businesses_google_maps(self, query, location, max_results=20):
        """
        Find businesses using Google Maps API.
        
        Args:
            query (str): Type of business (e.g., 'restaurants', 'plumbers')
            location (str): Location to search in (e.g., 'London, UK')
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of business data dictionaries
        """
        if not self.api_key:
            print("Warning: No API key provided. Using manual search method instead.")
            return self.find_businesses_manual(query, location, max_results)
            
        try:
            # Build the Places API service
            places_service = build('places', 'v1', developerKey=self.api_key)
            
            # Perform the search
            search_request = places_service.places().searchNearby(
                location=location,
                keyword=query,
                radius=5000,  # 5km radius
                maxResults=max_results
            )
            search_response = search_request.execute()
            
            # Process results
            businesses = []
            for place in search_response.get('places', []):
                # Get detailed information for each place
                detail_request = places_service.places().get(name=place['name'])
                detail_response = detail_request.execute()
                
                # Check if the business has a website
                has_website = 'websiteUri' in detail_response
                
                business_data = {
                    'name': detail_response.get('displayName', {}).get('text', ''),
                    'address': detail_response.get('formattedAddress', ''),
                    'phone': detail_response.get('internationalPhoneNumber', ''),
                    'has_website': has_website,
                    'website': detail_response.get('websiteUri', ''),
                    'category': ', '.join([c.get('displayName', {}).get('text', '') for c in detail_response.get('primaryTypeDisplayName', [])]),
                    'rating': detail_response.get('rating', 0),
                    'location': location,
                    'source': 'Google Maps API'
                }
                
                if not has_website:
                    businesses.append(business_data)
            
            self.results.extend(businesses)
            return businesses
            
        except HttpError as e:
            print(f"Error accessing Google Places API: {e}")
            return self.find_businesses_manual(query, location, max_results)
    
    def find_businesses_manual(self, query, location, max_results=20):
        """
        Simulate finding businesses without using API (for demo or when API key is unavailable).
        
        Args:
            query (str): Type of business (e.g., 'restaurants', 'plumbers')
            location (str): Location to search in (e.g., 'London, UK')
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of simulated business data dictionaries
        """
        print(f"Searching for {query} in {location} without website...")
        
        # This is a simulation - in a real scenario, you would use web scraping or other methods
        # to gather this data from Google Maps or other sources
        
        # Generate some sample data for demonstration
        sample_businesses = []
        business_types = {
            'restaurants': ['Italian', 'Indian', 'Chinese', 'Pub', 'Cafe', 'Bistro'],
            'plumbers': ['Emergency Plumbing', 'Plumbing & Heating', 'Bathroom Specialist'],
            'electricians': ['Electrical Services', 'Emergency Electrician', 'Lighting Specialist'],
            'hairdressers': ['Hair Salon', 'Barber Shop', 'Beauty Salon'],
            'dentists': ['Dental Practice', 'Dental Clinic', 'Orthodontist'],
            'mechanics': ['Auto Repair', 'Garage', 'Car Service'],
            'cleaners': ['Cleaning Service', 'Home Cleaning', 'Office Cleaning'],
        }
        
        # Default to restaurants if query not in our sample data
        category_options = business_types.get(query.lower(), business_types['restaurants'])
        
        # London areas for sample data
        london_areas = [
            'Camden', 'Greenwich', 'Hackney', 'Hammersmith', 'Islington', 
            'Kensington', 'Lambeth', 'Lewisham', 'Southwark', 'Tower Hamlets',
            'Wandsworth', 'Westminster', 'Croydon', 'Barnet', 'Enfield'
        ]
        
        # Generate sample businesses
        for i in range(min(max_results, 20)):
            area = london_areas[i % len(london_areas)]
            business_type = category_options[i % len(category_options)]
            
            business_data = {
                'name': f"{business_type} {i+1} - {area}",
                'address': f"{10+i} High Street, {area}, {location}",
                'phone': f"+44 20 7946 {1000+i}",
                'has_website': False,
                'website': '',
                'category': query,
                'rating': round(3 + (i % 20) / 10, 1),  # Ratings between 3.0 and 4.9
                'location': location,
                'source': 'Manual Search Simulation'
            }
            sample_businesses.append(business_data)
        
        self.results.extend(sample_businesses)
        return sample_businesses
    
    def filter_results(self, min_rating=None, categories=None, exclude_social_media=False):
        """
        Filter the results based on criteria.
        
        Args:
            min_rating (float): Minimum rating to include
            categories (list): List of categories to include
            exclude_social_media (bool): Whether to exclude businesses with social media
            
        Returns:
            list: Filtered list of business data dictionaries
        """
        filtered_results = self.results.copy()
        
        if min_rating is not None:
            filtered_results = [b for b in filtered_results if b.get('rating', 0) >= min_rating]
            
        if categories:
            filtered_results = [b for b in filtered_results if any(cat.lower() in b.get('category', '').lower() for cat in categories)]
            
        # In a real implementation, you would check for social media presence
        # This is just a placeholder for the concept
        if exclude_social_media:
            filtered_results = [b for b in filtered_results if not b.get('has_social_media', False)]
            
        return filtered_results
    
    def export_to_csv(self, filename=None):
        """
        Export results to CSV file.
        
        Args:
            filename (str): Optional filename, defaults to timestamped file
            
        Returns:
            str: Path to the exported CSV file
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"business_leads_{timestamp}.csv"
            
        filepath = os.path.join(self.output_dir, filename)
        
        if self.results:
            df = pd.DataFrame(self.results)
            df.to_csv(filepath, index=False)
            print(f"Exported {len(self.results)} businesses to {filepath}")
            return filepath
        else:
            print("No results to export")
            return None
    
    def export_to_json(self, filename=None):
        """
        Export results to JSON file.
        
        Args:
            filename (str): Optional filename, defaults to timestamped file
            
        Returns:
            str: Path to the exported JSON file
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"business_leads_{timestamp}.json"
            
        filepath = os.path.join(self.output_dir, filename)
        
        if self.results:
            with open(filepath, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"Exported {len(self.results)} businesses to {filepath}")
            return filepath
        else:
            print("No results to export")
            return None

def main():
    """Main function to demonstrate the BusinessFinder class."""
    finder = BusinessFinder()
    
    # Example usage
    print("Business Finder Tool")
    print("-------------------")
    print("Finding restaurants in London without websites...")
    finder.find_businesses_manual("restaurants", "London, UK", 10)
    
    print("\nFinding plumbers in Manchester without websites...")
    finder.find_businesses_manual("plumbers", "Manchester, UK", 5)
    
    # Filter results
    filtered = finder.filter_results(min_rating=3.5)
    print(f"\nFiltered to {len(filtered)} businesses with rating >= 3.5")
    
    # Export results
    finder.export_to_csv()
    finder.export_to_json()
    
    print("\nDone! Check the data directory for exported files.")

if __name__ == "__main__":
    main()
