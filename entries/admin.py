from django.contrib import admin
from entries.models import Language, Descriptor, Word, Translation, Sentence, DailyWord

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

class DailyWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'featured_date', 'get_translations')
    list_filter = ('featured_date',)
    search_fields = ('word__word', 'notes')
    date_hierarchy = 'featured_date'
    ordering = ('-featured_date',)
    
    def get_translations(self, obj):
        translations = obj.word.translation_set.all()
        return ", ".join([t.translation for t in translations[:3]])
    
    get_translations.short_description = 'Translations'

admin.site.register(Language, LanguageAdmin)
admin.site.register(Descriptor, DescriptorAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(DailyWord, DailyWordAdmin)

