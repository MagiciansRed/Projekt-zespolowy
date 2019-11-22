from django.shortcuts import render, get_object_or_404, redirect
from course.models import Course, Subscription
from course.forms import CourseCreateForm

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

        if request.POST.get('subscribe'):
            sub.course = course
            sub.user = current_user
            sub.save()
            context['subscription_state'] = True
    else:
        context['subscription_state'] = False
        if request.POST.get('subscribe'):
            sub.course = course
            sub.user = current_user
            sub.save()
            context['subscription_state'] = True

    return render(request, 'course/detail_course.html', context)


def create_course_view(request):
    if request.method == 'POST':
        course_form = CourseCreateForm(request.POST, instance=request.user)

        course = Course()
        if course_form.is_valid():
            data = course_form.cleaned_data
            course.name = data['name']
            course.description = data['description']
            course.author = request.user
            course.save()
            return redirect('course:courses')
    else:
        course_form = CourseCreateForm(instance=request.user)

    context = {
        'course_form': course_form,
    }
    return render(request, 'course/create_course.html', context)
