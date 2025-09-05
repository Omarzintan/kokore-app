from django.core.management.base import BaseCommand
from entries.models import Descriptor

class Command(BaseCommand):
    help = 'Command to populate the descriptor table in the database'

    def _create_descriptor_entries(self):
        descriptors = [
                {"name": "Adjective", "abbreviation": "adj."},
                {"name": "Adverb", "abbreviation": "adv."},
                {"name": "Article", "abbreviation": "art."},
                {"name": "Assertive", "abbreviation": "assert."},
                {"name": "Complementizer", "abbreviation": "comp."},
                {"name": "Conjunction", "abbreviation": "conj."},
                {"name": "Definite", "abbreviation": "def."},
                {"name": "Determiner", "abbreviation": "det."},
                {"name": "Focus", "abbreviation": "foc."},
                {"name": "Human", "abbreviation": "human."},
                {"name": "Ideophone", "abbreviation": "idph."},
                {"name": "Imperfective", "abbreviation": "impf."},
                {"name": "Imperative", "abbreviation": "impv."},
                {"name": "Indefinite", "abbreviation": "indf."},
                {"name": "Intensifier", "abbreviation": "intens."},
                {"name": "Interjection", "abbreviation": "interj."},
                {"name": "Interrogative", "abbreviation": "interr."},
                {"name": "Intransitive", "abbreviation": "intr."},
                {"name": "Locative", "abbreviation": "loc."},
                {"name": "Noun", "abbreviation": "n."},
                {"name": "Negation", "abbreviation": "neg."},
                {"name": "Nominalizer", "abbreviation": "nmlz."},
                {"name": "Nonhuman", "abbreviation": "nonhuman."},
                {"name": "Particle", "abbreviation": "part."},
                {"name": "Perfect", "abbreviation": "perf."},
                {"name": "Past Tense", "abbreviation": "pst."},
                {"name": "Plural", "abbreviation": "pl."},
                {"name": "Postposition", "abbreviation": "post."},
                {"name": "Pronoun", "abbreviation": "pron."},
                {"name": "Relative", "abbreviation": "rel."},
                {"name": "Reciprocal", "abbreviation": "recp."},
                {"name": "Singulative", "abbreviation": "sg."},
                {"name": "Strong", "abbreviation": "str."},
                {"name": "Topic", "abbreviation": "top."},
                {"name": "Verb", "abbreviation": "v."},
                {"name": "Variant", "abbreviation": "var."},
                {"name": "Second Plural", "abbreviation": "2ndpl."}
        ]

        for descriptor_entry in descriptors:
            descriptor = Descriptor(name=descriptor_entry.get("name"), abbreviation=descriptor_entry.get("abbreviation"))
            descriptor.save()

    def handle(self, *args, **options):
        self._create_descriptor_entries()
