from typing import NamedTuple
from entries.helpers import tokens
import re


class Token(NamedTuple):
    type: str
    value: str
    column: int


def sanitize_value(tag, text):
    return text.replace(tag, "").replace("{", "").replace("}", "")

def create_entry(token_list):
    # Expect only one dagaare word token, phonetic spelling, and part of speech entry
    entry = {}
    entry["dagaare_word"] = token_list[0].value
    entry["phonetic_spelling"] = token_list[1].value
    entry["translations"] = []
    count = 2
    while count < len(token_list):
        if token_list[count].type == tokens.PART_OF_SPEECH:
            entry["descriptors"] = token_list[count].value
        if token_list[count].type == tokens.WORD_PLURAL:
            entry["plural"] = token_list[count].value
        if token_list[count].type == tokens.WORD_PLURAL_2:
            entry["second_plural"] = token_list[count].value
        if token_list[count].type == tokens.ENGLISH_MEANING:
            translation = {}
            translation["english_meaning"] = token_list[count].value
            translation["example_sentences"] = []
            sentence_follows = False
            if count + 1 < len(token_list):
                if token_list[count + 1].type == tokens.DAGAARE_SENTENCE:
                    sentence_follows = True
            while sentence_follows:
                dagaare_sentence = token_list[count+1].value
                english_sentence = token_list[count+2].value
                translation["example_sentences"].append(
                    (dagaare_sentence, english_sentence))
                if count + 3 < len(token_list):
                    if token_list[count + 3].type == tokens.DAGAARE_SENTENCE:
                        count += 2
                        continue
                    else:
                        count += 2
                        sentence_follows = False
                        continue
                else:
                    count += 2
                    sentence_follows = False
            entry["translations"].append(translation)
        count += 1
    return entry


def tokenize(text):
    token_specification = [
        (tokens.DAGAARE_WORD, r'bLX{(.*?)}'),
        (tokens.ENGLISH_MEANING, r'bGE{(.*?)}'),
        (tokens.PHONETIC_SPELLING, r"bPH{(.*?)}"),
        (tokens.PART_OF_SPEECH, r"bPS{(.*?)}"),
        (tokens.DAGAARE_SENTENCE, r"bXV{(.*?)}"),
        (tokens.ENGLISH_SENTENCE, r"bXE{(.*?)}"),
        (tokens.WORD_PLURAL, r"bOP{(.*?)}"),
        (tokens.WORD_PLURAL_2, r"bTP{(.*?)}"),
        (tokens.EMPTY_TAG, r'bHM{}'),
        (tokens.EMPTY_TAG_2, r'bSN'),
        (tokens.NEWLINE,  r'\n'),           # Line endings
        (tokens.SKIP,     r'[ \t]+'),       # Skip over spaces and tabs
        (tokens.MISMATCH, r'.')            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_start = 0
    for mo in re.finditer(tok_regex, text):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == tokens.DAGAARE_WORD:
            value = sanitize_value('bLX', value)
        elif kind == tokens.ENGLISH_MEANING:
            value = sanitize_value('bGE', value)
        elif kind == tokens.PHONETIC_SPELLING:
            value = sanitize_value('bPH', value)
        elif kind == tokens.PART_OF_SPEECH:
            value = sanitize_value('bPS', value)
        elif kind == tokens.DAGAARE_SENTENCE:
            value = sanitize_value('bXV', value)
        elif kind == tokens.ENGLISH_SENTENCE:
            value = sanitize_value('bXE', value)
        elif kind == tokens.WORD_PLURAL:
            value = sanitize_value('bOP', value)
        elif kind == tokens.WORD_PLURAL_2:
            value = sanitize_value('bTP', value)
        elif kind == tokens.EMPTY_TAG:
            continue
        elif kind == tokens.EMPTY_TAG_2:
            continue
        elif kind == tokens.NEWLINE:
            continue
        elif kind == tokens.SKIP:
            continue
        elif kind == tokens.MISMATCH:
            continue
        yield Token(kind, value, column)

"""
latex_statement = '''\tbLX{ãa}\tbHM{} \tbPH{ã̀ã́} \tbPS{adv.} \tbSN \tbGE{yes (answer to a call)}
        \tbXV{N boɔle la a bie ka o sage ka 'ãa.'} \tbXE{I called the child and he answered, 'Yes.'}
        \tbSN \tbGE{what? (exclamation of disbelief)} \tbXV{Ka Naa boɔle fo ka fo zagere, ãa.}
        \tbXE{You refuse to answere the chief's call, what?}'''

latex_statement_2 = '''\tbLX{a}\tbHM{} \tbPH{à} \tbPS{pron.} \tbGE{they, them (3rd person plural weak form nonhuman)} \tbXV{Vɛŋ ka a kpɛ a zage.} \tbXE{Let them go into the pen.} \tbXV{De a moɔ eŋ a.} \tbXE{Give them the grass.}'''
latex_statement_3 = '''\tbLX{berɛ}\tbHM{} \tbPH{bìrɛ́} \tbPS{v.} \tbSN \tbGE{to wish} \tbXV{O berɛ ŋa zie da koŋ nyaa.} \tbXE{S/he wished day would never come.} \tbXV{O berɛ ona la da na gaa a tigiri.} \tbXE{S/he wished s/he would be the one to attend the feast.} \tbSN \tbGE{take by surprise} \tbXV{O berɛ ka saana la wa kpɛ. } \tbXE{Before he realized it, a stranger arrived.} %\tbPD{-, -, -, -, -, -}'''
latex_statement_4 = '''\tbLX{leɛre}\tbHM{} \tbPH{lɪ́ɛ́rɪ̀} \tbPS{v.} \tbSN \tbGE{to wave one's hands or other objects in the air or in the face of another} \tbXV{A zɔɔzɔɔreba da leɛrɛ la nuuri ennɛ taa.} \tbXE{The fighters were throwing their hands in each other's face.} \tbXV{A lɔɔre naŋ da wa ire n ma da leɛre la o nu ko ma ka n poɔ zaa sãã.} \tbXE{As the lorry took off my mother waved me but I was very sad.} \tbSN \tbGE{wave hand vigorously in the face of another, usually in anger} \tbXV{Dɔbɔ mine bayi da toora la taa kyɛ leɛrɛ nuuri ennɛ taa.} \tbXE{Two men were waving their hands angrily in each other's face.} %\tbPD{-, -, -, -, -, -}'''
"""

# for token in tokenize(latex_statement_2):
# print(token)

# token_list = [x for x in tokenize(latex_statement_4)]
# print(create_entry(token_list))

