from django import forms
from course.models import Course, Word


class CourseCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=60)
    source_language = forms.CharField(max_length=60)
    target_language = forms.CharField(max_length=60)
    description = forms.CharField(max_length=600)
    image = forms.ImageField(required=False)

    class Meta:
        model = Course
        fields = ("name", "source_language", "target_language", "description", "image")


class EditCourseForm(forms.ModelForm):
    name = forms.CharField(max_length=60)
    source_language = forms.CharField(max_length=60)
    target_language = forms.CharField(max_length=60)
    description = forms.CharField(max_length=600)
    image = forms.ImageField(required=False)

    class Meta:
        model = Course
        fields = ("name", "source_language", "target_language", "description", "image")


class AddWordForm(forms.ModelForm):
    target_word = forms.CharField(max_length=60)
    source_word = forms.CharField(max_length=60)

    class Meta:
        model = Word
        fields = ("target_word", "source_word")


class RemoveWordForm(forms.ModelForm):
    source_word = forms.ModelChoiceField(queryset=Word.objects.all())

    class Meta:
        model = Word
        fields = ('source_word',)


class LearnWordForm(forms.ModelForm):
    source_word = forms.CharField(max_length=60)
    has_seen_translation = forms.BooleanField(required=False)

    class Meta:
        model = Word
        fields = ('source_word', 'has_seen_translation',)
