#!/usr/bin/env python
"""
Script to export data from the database to JSON fixtures.
Run this locally to create fixture files that can be loaded on PythonAnywhere.
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictionary.settings')
django.setup()

from django.core.management import call_command

def export_data():
    """Export all app data to fixtures directory"""
    # Create fixtures directory if it doesn't exist
    fixtures_dir = 'fixtures'
    if not os.path.exists(fixtures_dir):
        os.makedirs(fixtures_dir)
    
    # Export data from each app
    apps = ['entries', 'pages']
    for app in apps:
        output_file = os.path.join(fixtures_dir, f'{app}_data.json')
        print(f"Exporting {app} data to {output_file}...")
        call_command('dumpdata', app, '--indent=4', output=output_file)
    
    print("Data export complete. Upload the fixtures directory to PythonAnywhere.")

if __name__ == '__main__':
    export_data()
