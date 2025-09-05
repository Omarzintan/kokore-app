from django.core.management.base import BaseCommand
from entries.models import Language

class Command(BaseCommand):
    help = 'Command to populate the language table in the database'

    def _create_language_entries(self):
        languages = {1:{"name": "Dagaare", "code": "dga"}, 2:{"name": "English", "code": "en"}}

        for language_entry in languages:
            language_entry_dict = languages.get(language_entry)
            language = Language(code=language_entry_dict.get("code"), name=language_entry_dict.get("name"))
            language.save()

    def handle(self, *args, **options):
        self._create_language_entries()
