from django.db import models

class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Descriptor(models.Model):
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Word(models.Model):
    word = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    descriptors = models.ManyToManyField(Descriptor)
    phonetic_spelling = models.CharField(max_length=50,blank=True)
    plural = models.CharField(max_length=50,blank=True)
    second_plural = models.CharField(max_length=50,blank=True)
    audio = models.FileField(upload_to="word_audio/",blank=True)

    def __str__(self):
        return self.word


class Translation(models.Model):
    from_word = models.ForeignKey(Word, on_delete=models.CASCADE)
    to_language = models.ForeignKey(Language, on_delete=models.CASCADE)
    translation = models.TextField()

    def __str__(self):
        return self.translation


class Sentence(models.Model):
    sentence = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE,blank=True)
    translated_sentence = models.ManyToManyField('self')
    audio = models.FileField(upload_to="sentence_audio/",blank=True)

    def __str__(self):
        return self.sentence

