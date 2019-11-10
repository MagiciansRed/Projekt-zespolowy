from django.shortcuts import render
from course.models import Course


# Create your views here.
context = {}
courses = Course.objects.all()
context['courses'] = courses

def course_list_view(request):
    return render(request, 'course/courses.html', context)
