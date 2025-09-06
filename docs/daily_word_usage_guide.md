# Daily Dagaare Word Feature - Usage Guide

This guide explains how to use and manage the Daily Dagaare Word feature in the Kokore Dictionary App.

## For Users

### Viewing the Daily Word

1. **Home Page**: When you visit the home page, you'll see the Daily Dagaare Word featured in a card below the search bar (if no search is active).

2. **Daily Word Page**: Click on the "Daily Word" link in the navigation menu to visit the dedicated daily word page, which includes:
   - The Dagaare word with phonetic spelling
   - Grammatical information
   - English translations
   - Example sentences in both Dagaare and English
   - Social sharing options

3. **Previous Daily Words**: Currently, the system only displays the most recent daily word. Future enhancements may include a calendar view or archive of previous daily words.

### Sharing Daily Words

On the daily word page, you can share the featured word via:
- Twitter
- Facebook
- Email

Simply click on the respective sharing button at the bottom of the daily word card.

## For Administrators

### Managing Daily Words

1. **Admin Interface**: Log in to the Django admin interface and navigate to the "Daily Words" section under the "Entries" app.

2. **Viewing Daily Words**: The admin list displays:
   - The featured Dagaare word
   - The date it was/will be featured
   - The first few translations

3. **Adding a Daily Word Manually**: Click "Add Daily Word" and:
   - Select a word from the dropdown (or search by typing)
   - Set the featured date (defaults to today)
   - Add optional notes about why this word was selected

4. **Editing Daily Words**: Click on an existing daily word to:
   - Change the featured date
   - Update notes
   - Select a different word

### Automatic Word Selection

The system automatically selects a new daily word at midnight using a scheduled task. The selection process:

1. Prioritizes words that have never been featured before
2. Prefers words that have example sentences
3. Ensures variety by not repeating words until all have been featured

### Manual Word Selection

To manually select a daily word using the management command:

```bash
# Select a word for today
python manage.py select_daily_word

# Force selection of a new word even if one exists for today
python manage.py select_daily_word --force
```

### Setting Up the Scheduled Task

The scheduled task uses django-crontab to automatically select a new word each day at midnight. To manage this:

1. **Install the scheduled tasks**:
   ```bash
   python manage.py crontab add
   ```

2. **Show currently configured jobs**:
   ```bash
   python manage.py crontab show
   ```

3. **Remove the scheduled tasks**:
   ```bash
   python manage.py crontab remove
   ```

## Deployment Instructions

### Deploying to PythonAnywhere

When deploying the application to PythonAnywhere, you'll need to set up the daily word feature as follows:

1. **Run migrations** to create the DailyWord table:
   ```bash
   cd ~/kokore-app
   workon kokore-env  # Activate your virtual environment
   python manage.py migrate --settings=dictionary.settings_production
   ```

2. **Select the first daily word**:
   ```bash
   python manage.py select_daily_word --settings=dictionary.settings_production
   ```

3. **Set up scheduled task** using PythonAnywhere's task scheduler:
   - Go to the PythonAnywhere dashboard and click on "Tasks"
   - Add a new scheduled task that runs at 00:00 (midnight)
   - Enter the command:
     ```bash
     cd ~/kokore-app && workon kokore-env && python manage.py select_daily_word --settings=dictionary.settings_production
     ```
   - This will run daily and select a new word each day

4. **Alternative: Using django-crontab**:
   - If you prefer to use django-crontab instead of PythonAnywhere's task scheduler:
     ```bash
     cd ~/kokore-app
     workon kokore-env
     python manage.py crontab add --settings=dictionary.settings_production
     ```
   - Note: You'll need to re-run this command after each deployment

### Verifying Deployment

1. **Check the daily word page** at `yourusername.pythonanywhere.com/daily-word/`
2. **Verify scheduled tasks** in the PythonAnywhere dashboard
3. **Monitor logs** for any errors in the task execution

## Troubleshooting

### No Daily Word Appears

If no daily word appears on the home page or daily word page:

1. Check if any daily words exist in the database:
   ```bash
   python manage.py shell -c "from entries.models import DailyWord; print(DailyWord.objects.all())"
   ```

2. Manually select a daily word:
   ```bash
   python manage.py select_daily_word
   ```

3. Verify the cron job is properly installed:
   ```bash
   python manage.py crontab show
   ```

### Word Selection Issues

If inappropriate words are being selected:

1. Review the selection algorithm in `entries/management/commands/select_daily_word.py`
2. Consider adding filters to exclude certain words or prioritize others
3. Use the admin interface to manually schedule specific words for future dates
