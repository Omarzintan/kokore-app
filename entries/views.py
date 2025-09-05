from django.db.models import Q
from django.shortcuts import render
from entries.models import Word, Translation, Sentence, Language

def entry_index(request):
    all_words = Word.objects.all()
    query = request.GET.get("q")
    trd = request.GET.get("trd")
    words = None
    translations = None
    word_with_translations = []
    translation_with_source = []
    
    if query and trd == "dga-en":
        # First get exact matches
        exact_matches = Word.objects.filter(word__iexact=query)
        
        # Then get partial matches (excluding exact matches)
        partial_matches = Word.objects.filter(
            Q(word__iregex=r'\b{0}\b'.format(query)) & 
            ~Q(word__iexact=query)
        )
        
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
        exact_matches = Translation.objects.filter(translation__iexact=query)
        
        # Then get partial matches (excluding exact matches)
        partial_matches = Translation.objects.filter(
            Q(translation__iregex=r'\b{0}\b'.format(query)) & 
            ~Q(translation__iexact=query)
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
            "all_words": all_words,
            "words": words,
            "translations": translations,
            "word_with_translations": word_with_translations,
            "translation_with_source": translation_with_source
            }
    return render(request, "entries/entry_index.html", context)

def entry_detail(request, pk):
    all_words = Word.objects.all()
    dagaare_language = Language.objects.get(name="Dagaare")
    english_language = Language.objects.get(name="English")
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
    context = {"all_words": all_words,
               "word": word,
               "descriptors": word.descriptors.all(),
               "translations": translation_entries}
    return render(request, "entries/entry_detail.html", context)
