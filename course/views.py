from django.shortcuts import render, get_object_or_404
from course.models import Course, Subscription


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

    current_user = request.user
    sub = Subscription()
    entry = Subscription.objects.filter(course=course)

    if entry.exists():
        for e in entry:
            if e.user.username == current_user.username:
                context['subscription_state'] = True
                if request.POST.get('unsubscribe'):
                    e.delete()
                    context['subscription_state'] = False
                break

    else:
        context['subscription_state'] = False
        if request.POST.get('subscribe'):
            sub.course = course
            sub.user = current_user
            sub.save()
            context['subscription_state'] = True

    return render(request, 'course/detail_course.html', context)
