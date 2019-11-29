from django import forms
from course.models import Course, Word


class CourseCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=60)
    description = forms.CharField(max_length=600)
    image = forms.ImageField(required=False)

    class Meta:
        model = Course
        fields = ("name", "description", "image")


class EditCourseForm(forms.ModelForm):
    name = forms.CharField(max_length=60)
    description = forms.CharField(max_length=600)
    image = forms.ImageField(required=False)

    class Meta:
        model = Course
        fields = ("name", "description", "image")


class AddWordForm(forms.ModelForm):
    target_word = forms.CharField(max_length=60)
    source_word = forms.CharField(max_length=60)

    class Meta:
        model = Word
        fields = ("target_word", "source_word")
