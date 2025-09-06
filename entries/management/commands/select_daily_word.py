import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from entries.models import Word, DailyWord, Language, Sentence


class Command(BaseCommand):
    help = 'Selects a new Dagaare word to be featured as the daily word'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force selection of a new word even if one is already selected for today',
        )

    def handle(self, *args, **options):
        today = timezone.now().date()
        force = options['force']

        # Check if we already have a word for today
        existing_word = DailyWord.objects.filter(featured_date=today).first()
        if existing_word and not force:
            self.stdout.write(
                self.style.WARNING(
                    f'A word is already selected for today: {existing_word.word.word}'
                )
            )
            return

        # Get Dagaare language
        try:
            dagaare_language = Language.objects.get(name="Dagaare")
        except Language.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Dagaare language not found in the database')
            )
            return

        # Get all previously featured words
        featured_word_ids = DailyWord.objects.values_list('word_id', flat=True)

        # Find words that have translations and example sentences
        # Prioritize words that haven't been featured before
        candidate_words = Word.objects.filter(
            language=dagaare_language,
            translation__isnull=False,
        ).exclude(
            id__in=featured_word_ids
        ).distinct()

        # If all words have been featured, allow repeats but prioritize oldest featured words
        if not candidate_words.exists():
            self.stdout.write(
                self.style.WARNING(
                    'All words have been featured before. Selecting from all words.'
                )
            )
            candidate_words = Word.objects.filter(
                language=dagaare_language,
                translation__isnull=False,
            ).distinct()

        # Further prioritize words with example sentences
        words_with_sentences = []
        for word in candidate_words:
            has_sentences = False
            for translation in word.translation_set.all():
                if Sentence.objects.filter(translation=translation).exists():
                    has_sentences = True
                    break
            
            if has_sentences:
                words_with_sentences.append(word)

        # If we have words with sentences, prioritize those
        if words_with_sentences:
            selected_word = random.choice(words_with_sentences)
        elif candidate_words:
            selected_word = random.choice(list(candidate_words))
        else:
            self.stdout.write(
                self.style.ERROR('No suitable words found in the database')
            )
            return

        # If forcing a new selection and there's an existing word for today, delete it
        if force and existing_word:
            existing_word.delete()

        # Create the daily word entry
        daily_word = DailyWord.objects.create(
            word=selected_word,
            featured_date=today,
            notes=f"Selected on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully selected word "{selected_word.word}" as the daily word for {today}'
            )
        )
