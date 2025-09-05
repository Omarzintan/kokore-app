from django.contrib import admin
from entries.models import Language, Descriptor, Word, Translation, Sentence

# Register your models here.
class LanguageAdmin(admin.ModelAdmin):
    pass

class DescriptorAdmin(admin.ModelAdmin):
    pass

class WordAdmin(admin.ModelAdmin):
    pass

class TranslationAdmin(admin.ModelAdmin):
    pass

class SentenceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Language, LanguageAdmin)
admin.site.register(Descriptor, DescriptorAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(Sentence, SentenceAdmin)

