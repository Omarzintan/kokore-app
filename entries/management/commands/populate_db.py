from django.core.management.base import BaseCommand
from entries import regex_strings
from entries.models import Word, Translation, Language, Descriptor, Sentence
from entries.helpers.mytokenizer import create_entry, tokenize
import re
import sqlite3

class Command(BaseCommand):
    help = 'Command to populate the descriptor table in the database'

    def _read_txt_file(self, filepath: str):
        with open(filepath, 'r') as fp:
            content = fp.readlines()
            return content

    def _sanitize_line(self, textline: str):
        textline = textline.replace("{``}", "'")
        textline = textline.replace('"', "'")
        return textline

    def _get_entry_data(self, textline: str):
        dagaare_words = re.findall(regex_strings.DAGARE_WORD_REGEX, textline)
        english_translations = re.findall(
            regex_strings.ENGLISH_MEANING_REGEX, textline)
        dagaare_sentences = re.findall(
            regex_strings.DAGARE_SENTENCE_REGEX, textline)
        english_sentences = re.findall(
            regex_strings.ENGLISH_SENTENCE_REGEX, textline)
        phonetic_spelling = re.findall(
            regex_strings.PHONETIC_SPELLING_REGEX, textline)
        descriptors = re.findall(regex_strings.DESCRIPTORS, textline)
        plural = re.findall(regex_strings.WORD_PLURAL_REGEX, textline)
        second_plural = re.findall(regex_strings.WORD_PLURAL_2_REGEX, textline)

        return {
                "dagaare_word": dagaare_words,
                "english_translations": english_translations,
                "dagaare_sentences": dagaare_sentences,
                "english_sentences": english_sentences,
                "phonetic_spelling": phonetic_spelling,
                "descriptors": descriptors,
                "plural": plural,
                "second_plural": second_plural
                }

    def _populate_db(self, entry_details: dict):
        dagaare_word = entry_details.get("dagaare_word")
        phonetic_spelling = entry_details.get("phonetic_spelling")
        descriptors = entry_details.get("descriptors")

        # language
        dagaare_language = Language.objects.get(name="Dagaare")
        english_language = Language.objects.get(name="English")
        # create word and save
        word = Word(word=dagaare_word,language=dagaare_language)
        word.save()
        # phonetic spelling
        word.phonetic_spelling = phonetic_spelling
        word.save()
        # plural
        if "plural" in entry_details:
            word.plural = entry_details.get("plural")
            word.save()
        # second plural
        if "second_plural" in entry_details:
            word.second_plural = entry_details.get("second_plural")
            word.save()
        # descriptors
        if descriptors == "interrogative pronoun":
            descriptors = "interr. pron."
        descriptor_list = descriptors.split(" ")
        for desc in descriptor_list:
            if desc:
                descriptor = Descriptor.objects.get(abbreviation=desc)
                word.descriptors.add(descriptor)
                word.save()
        # create translation and save
        translations = entry_details.get("translations")
        for translation_dict in translations:
            translation = Translation(
                    from_word=word,
                    to_language=english_language,
                    translation=translation_dict["english_meaning"])
            translation.save()
            if "example_sentences" in translation_dict:
                for example_sentence_pair in translation_dict.get("example_sentences"):
                    dagaare_sentence = Sentence(
                            sentence=example_sentence_pair[0],
                            language=dagaare_language,
                            translation=translation)
                    dagaare_sentence.save()

                    english_sentence = Sentence(
                            sentence=example_sentence_pair[1],
                            language=english_language,
                            translation=translation)
                    english_sentence.save()

                    dagaare_sentence.translated_sentence.add(english_sentence)
                    dagaare_sentence.save()

    def _create_dictionary_chapter(self, textlines: list[str]):
        try:
            for textline in textlines:
                if textline.startswith('%'):
                    continue
                sanitized_textline = self._sanitize_line(textline)
                token_list = [x for x in tokenize(sanitized_textline)]
                if len(token_list) == 0 or len(token_list) < 3:
                    continue
                entry_details = create_entry(token_list)
                self._populate_db(entry_details)

        except Exception as e:
            print(entry_details)
            print(f"Could not update dagare dictionary due to {e}.")

    def handle(self, *args, **options):
        chapters = ['a', 'b', 'd', 'E', 'f', 'g', 'gb', 'gy', 'h', 'i', 'k', 'kp',
                        'ky', 'l', 'm', 'n', 'ng', 'ngm', 'ny', 'O', 'p', 's', 't',
                        'u', 'v', 'w', 'y', 'z']
        #one_chapter = 'b'
        excluded_chapters = []
        for chapter in chapters:
            if chapter in excluded_chapters:
                continue
            try:
                self._create_dictionary_chapter(
                    self._read_txt_file("dictionary/data/chapters/"+chapter+".tex"))
                print(f"Created dictionary successfully for {chapter}")
            except Exception as e:
                print(f"Could not create dictionary for {chapter} due to {e}")

