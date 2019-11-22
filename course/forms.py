from django import forms
from course.models import Course


class CourseCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=60)
    description = forms.CharField(max_length=600)
    image = forms.ImageField(required=False)

    class Meta:
        model = Course
        fields = ("name", "description", "image")
