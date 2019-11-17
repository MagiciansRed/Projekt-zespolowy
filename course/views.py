from django.shortcuts import render, get_object_or_404
from course.models import Course

# Create your views here.



def course_list_view(request):
    context = {}
    courses = Course.objects.all()
    context['courses'] = courses

    return render(request, 'course/courses.html', context)


def detail_course_view(request, slug):
    context = {}
    course = get_object_or_404(Course, slug=slug)
    context['course_detail'] = course

    return render(request, 'course/detail_course.html', context)
