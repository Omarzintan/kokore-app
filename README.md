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
