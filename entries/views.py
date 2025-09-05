from django.db.models import Q
from django.shortcuts import render
from entries.models import Word, Translation, Sentence, Language

def entry_index(request):
    all_words = Word.objects.all()
    query = request.GET.get("q")
    trd = request.GET.get("trd")
    words = None
    translations = None
    if query and trd == "dga-en":
        words = Word.objects.filter(
                Q(word__iexact=query) |
                Q(word__iregex=r'\b{0}\b'.format(query)))
    elif query and trd == "en-dga":
        # for postgres, use \y for the regex
        translations = Translation.objects.filter(Q(translation__iexact=query) |
                Q(translation__iregex=r'\b{0}\b'.format(query)))
   
    context = {
            "all_words": all_words,
            "words": words,
            "translations": translations
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
