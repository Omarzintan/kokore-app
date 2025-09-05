#!/usr/bin/env python
"""
Script to import data from JSON fixtures into the database.
Run this on PythonAnywhere after uploading the fixtures directory.
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictionary.settings_production')
django.setup()

from django.core.management import call_command

def import_data():
    """Import all app data from fixtures directory"""
    fixtures_dir = 'fixtures'
    
    if not os.path.exists(fixtures_dir):
        print(f"Error: {fixtures_dir} directory not found!")
        print("Please make sure you've uploaded the fixtures directory to PythonAnywhere.")
        return
    
    # Import data for each app
    fixtures = [f for f in os.listdir(fixtures_dir) if f.endswith('.json')]
    
    if not fixtures:
        print("No fixture files found in the fixtures directory.")
        return
    
    for fixture in fixtures:
        fixture_path = os.path.join(fixtures_dir, fixture)
        print(f"Loading data from {fixture_path}...")
        call_command('loaddata', fixture_path)
    
    print("Data import complete!")

if __name__ == '__main__':
    import_data()
