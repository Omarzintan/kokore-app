# Kokore Dictionary App

A bilingual dictionary application built with Django that focuses on the Dagaare language and English translations.

## Overview

This application serves as a digital dictionary that allows users to:
- Search for words in Dagaare and find their English translations
- Search for English words and find their Dagaare translations
- View detailed information about words including phonetic spellings, grammatical descriptors, and example sentences

## Features

- **Bidirectional Search**: Search in both Dagaare-to-English and English-to-Dagaare directions
- **Autocomplete**: Suggestions appear as you type to help find words quickly
- **Detailed Word Entries**: View comprehensive information for each word:
  - Phonetic spelling
  - Grammatical information (parts of speech)
  - Translations
  - Example sentences in both languages
- **Audio Support**: Infrastructure for pronunciation examples (audio files)

## Technical Details

- Built with Django web framework
- Uses SQLite database for data storage
- Bootstrap for frontend styling
- jQuery UI for autocomplete functionality

## Data Models

- **Word**: Stores words with their language, phonetic spelling, and grammatical information
- **Translation**: Links words between languages
- **Sentence**: Stores example sentences with translations
- **Language**: Defines languages in the system (primarily Dagaare and English)
- **Descriptor**: Stores grammatical descriptors (like parts of speech)

## Getting Started

### Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Start the development server:
   ```
   python manage.py runserver
   ```
5. Access the application at http://localhost:8000

### Deployment to PythonAnywhere

1. Sign up for a [PythonAnywhere account](https://www.pythonanywhere.com/)

2. Upload your code to PythonAnywhere:
   ```
   # From your PythonAnywhere bash console
   git clone https://github.com/yourusername/kokore-app.git
   ```

3. Set up a virtual environment:
   ```
   mkvirtualenv --python=/usr/bin/python3.9 kokore-env
   pip install -r kokore-app/requirements.txt
   ```

4. Create a MySQL database from the PythonAnywhere dashboard

5. Configure environment variables:
   ```
   # In PythonAnywhere bash console
   echo 'export DJANGO_SECRET_KEY="your-secure-secret-key"' >> ~/.virtualenvs/kokore-env/bin/postactivate
   echo 'export DJANGO_DEBUG="False"' >> ~/.virtualenvs/kokore-env/bin/postactivate
   echo 'export DATABASE_PASSWORD="your-database-password"' >> ~/.virtualenvs/kokore-env/bin/postactivate
   ```

6. Configure your web app:
   - Go to the Web tab in PythonAnywhere
   - Add a new web app, select Manual Configuration, then Python 3.9
   - Set the virtual environment path to `/home/yourusername/.virtualenvs/kokore-env`
   - Edit the WSGI configuration file to use the production settings:
     ```python
     import os
     import sys
     
     # Add your project directory to the sys.path
     path = '/home/yourusername/kokore-app'
     if path not in sys.path:
         sys.path.insert(0, path)
     
     # Set environment variable to use production settings
     os.environ['DJANGO_SETTINGS_MODULE'] = 'dictionary.settings_production'
     
     # Import Django WSGI application
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```

7. Set up static files:
   - First, create the staticfiles directory:
     ```
     mkdir -p ~/kokore-app/staticfiles
     ```
   - In the web app configuration, add a static files mapping:
     - URL: `/static/`
     - Directory: `/home/yourusername/kokore-app/staticfiles`

8. Run migrations and collect static files:
   ```
   cd ~/kokore-app
   python manage.py migrate
   python manage.py collectstatic
   ```

9. Reload your web app from the PythonAnywhere dashboard

10. Your site should now be live at `yourusername.pythonanywhere.com`

## Purpose

This application is designed for language learning, documentation, and preservation purposes, specifically focused on the Dagaare language (spoken in parts of Ghana and Burkina Faso).

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/) - see the [LICENSE](LICENSE) file for details.

This means you are free to:
- Share and adapt the material for non-commercial purposes
- Use the dictionary and language data for educational, research, and personal use

With the requirement that you:
- Give appropriate credit to the project
- Indicate if changes were made
- Do not use the material for commercial purposes without permission
