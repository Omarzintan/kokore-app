from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from entries.models import Word, Translation, Sentence, Language, DailyWord

import json
from django.core.serializers.json import DjangoJSONEncoder

def entry_index(request):
    # Get daily word
    daily_word_obj = get_daily_word()
    
    # Get Dagaare words that have translations
    dagaare_language = Language.objects.get(name="Dagaare")
    dagaare_words = Word.objects.filter(language=dagaare_language, translation__isnull=False).distinct()
    
    # Get English translations for autocomplete
    english_language = Language.objects.get(name="English")
    english_translations = Translation.objects.filter(to_language=english_language, from_word__isnull=False).values_list('translation', flat=True).distinct()
    
    # Prepare data for json_script template tag
    dagaare_words_list = [word.word for word in dagaare_words]
    english_translations_list = list(english_translations)
    
    query = request.GET.get("q")
    trd = request.GET.get("trd")
    words = None
    translations = None
    word_with_translations = []
    translation_with_source = []
    
    if query and trd == "dga-en":
        # First get exact matches with translations
        exact_matches = Word.objects.filter(word__iexact=query, translation__isnull=False).distinct()
        
        # Then get partial matches with translations (excluding exact matches)
        partial_matches = Word.objects.filter(
            Q(word__iregex=r'\b{0}\b'.format(query)) & 
            ~Q(word__iexact=query) &
            Q(translation__isnull=False)
        ).distinct()
        
        # Combine the results with exact matches first
        words = list(exact_matches) + list(partial_matches)
        
        # Get translations for each word
        for word in words:
            word_translations = word.translation_set.all()[:3]  # Limit to 3 translations for brevity
            word_with_translations.append({
                'word': word,
                'translations': word_translations,
                'is_exact_match': word.word.lower() == query.lower()  # Flag for highlighting in template
            })
            
    elif query and trd == "en-dga":
        # First get exact matches
        exact_matches = Translation.objects.filter(translation__iexact=query, from_word__isnull=False)
        
        # Then get partial matches (excluding exact matches)
        partial_matches = Translation.objects.filter(
            Q(translation__iregex=r'\b{0}\b'.format(query)) & 
            ~Q(translation__iexact=query) &
            Q(from_word__isnull=False)
        )
        
        # Combine the results with exact matches first
        translations = list(exact_matches) + list(partial_matches)
        
        # Get source word for each translation
        for translation in translations:
            translation_with_source.append({
                'translation': translation,
                'source_word': translation.from_word,
                'is_exact_match': translation.translation.lower() == query.lower()  # Flag for highlighting in template
            })
   
    context = {
            "dagaare_words": dagaare_words,
            "english_translations": english_translations,
            "dagaare_words_list": dagaare_words_list,
            "english_translations_list": english_translations_list,
            "words": words,
            "translations": translations,
            "word_with_translations": word_with_translations,
            "translation_with_source": translation_with_source,
            "daily_word": daily_word_obj
            }
    return render(request, "entries/entry_index.html", context)

def get_daily_word():
    """Helper function to get the daily word"""
    today = timezone.now().date()
    
    # Try to get today's word
    daily_word = DailyWord.objects.filter(featured_date=today).first()
    
    # If no word for today, get the most recent one
    if not daily_word:
        daily_word = DailyWord.objects.order_by('-featured_date').first()
    
    # If still no word, return None
    if not daily_word:
        return None
        
    return daily_word


def daily_word(request):
    """View to display the daily word"""
    daily_word_obj = get_daily_word()
    
    if not daily_word_obj:
        # No daily word found
        context = {
            "no_daily_word": True
        }
        return render(request, "entries/daily_word.html", context)
    
    # Get the word and its details
    word = daily_word_obj.word
    dagaare_language = Language.objects.get(name="Dagaare")
    english_language = Language.objects.get(name="English")
    
    # Get translations
    translations = word.translation_set.all()
    
    # Get example sentences
    translation_entries = []
    for translation in translations:
        sentence_pairs = []
        if translation.sentence_set.exists():
            dagaare_sentences = translation.sentence_set.filter(language=dagaare_language.id)
            for sentence in dagaare_sentences:
                sentence_pair = {
                    "dagaare_sentence": sentence,
                    "english_sentence": sentence.translated_sentence.filter(language=english_language.id).first()
                }
                sentence_pairs.append(sentence_pair)
        
        entry = {
            "translation": translation,
            "sentence_pairs": sentence_pairs
        }
        translation_entries.append(entry)
    
    context = {
        "daily_word": daily_word_obj,
        "word": word,
        "descriptors": word.descriptors.all(),
        "translations": translation_entries,
        "featured_date": daily_word_obj.featured_date
    }
    
    return render(request, "entries/daily_word.html", context)


def entry_detail(request, pk):
    # Get Dagaare words that have translations
    dagaare_language = Language.objects.get(name="Dagaare")
    dagaare_words = Word.objects.filter(language=dagaare_language, translation__isnull=False).distinct()
    
    # Get English translations for autocomplete
    english_language = Language.objects.get(name="English")
    english_translations = Translation.objects.filter(to_language=english_language, from_word__isnull=False).values_list('translation', flat=True).distinct()
    
    # Prepare data for json_script template tag
    dagaare_words_list = [word.word for word in dagaare_words]
    english_translations_list = list(english_translations)
    
    word = Word.objects.get(pk=pk)
    translation_entries = []
    translations = word.translation_set.all()
    for translation in translations:
        sentence_pairs = []
        if translation.sentence_set.exists():
            dagaare_sentences = translation.sentence_set.filter(language=dagaare_language.id)
            for sentence in dagaare_sentences:
                sentence_pair = {
                        "dagaare_sentence": sentence,
                        "english_sentence": sentence.translated_sentence.filter(language=english_language.id).first()}
                sentence_pairs.append(sentence_pair)

        entry = {"translation": translation,
                 "sentence_pairs": sentence_pairs
                 }
        translation_entries.append(entry)
    context = {
               "dagaare_words": dagaare_words,
               "english_translations": english_translations,
               "dagaare_words_list": dagaare_words_list,
               "english_translations_list": english_translations_list,
               "word": word,
               "descriptors": word.descriptors.all(),
               "translations": translation_entries
              }
    return render(request, "entries/entry_detail.html", context)
