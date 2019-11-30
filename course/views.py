from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from course.models import Course, Subscription, Word
from course.forms import CourseCreateForm, EditCourseForm, AddWordForm, RemoveWordForm
from django.utils.text import slugify
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

    words = Word.objects.all().filter(course=course)
    context['words'] = words

    current_user = request.user
    sub = Subscription()
    entry = Subscription.objects.filter(course=course)

    context['subscription_state'] = False

    if request.POST.get('delete') and course.author == current_user:
        course.delete()
        return redirect('course:courses')

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


@login_required
def create_course_view(request):
    context = {}
    if request.method == 'POST':
        course_form = CourseCreateForm(request.POST, request.FILES, instance=request.user)

        course = Course()
        if course_form.is_valid():
            data = course_form.cleaned_data
            course.name = data['name']
            course.description = data['description']
            course.author = request.user
            if(data['image']):
                course.image = data['image']

            try:
                course.save()
                return redirect('course:detail', course.slug)
            except IntegrityError:
                print("error")
                context['course_error'] = "You have already created a course with this name. Choose a different one."
    else:
        course_form = CourseCreateForm(instance=request.user)

    context['course_form'] = course_form

    return render(request, 'course/create_course.html', context)


@login_required
def edit_course_view(request, slug):
    context = {}
    course = get_object_or_404(Course, slug=slug)
    context['course_detail'] = course
    context['course_error'] = ""
    context['course_unauthorized'] = ""
    context['word_success'] = ""
    context['word_error'] = ""
    context['word_success_delete'] = ""

    if course.author != request.user:
        context['course_unauthorized'] = "You cannot edit someone else's course."
        return render(request, 'course/edit_course.html', context)

    if request.POST.get('edit'):
        course_form = EditCourseForm(request.POST, request.FILES, instance=request.user,
                                     initial={'name': course.name, 'description': course.description})

        if course_form.is_valid():
            data = course_form.cleaned_data
            if data['name']:
                course.name = data['name']
            if data['description']:
                course.description = data['description']
            course.author = request.user
            if data['image']:
                course.image = data['image']
            course.slug = slugify(course.author.username + "-" + course.name)
            try:
                course.save()
                return redirect('course:detail', course.slug)
            except IntegrityError:
                print("error")
                context['course_error'] = "You have already created a course with this name. Choose a different one."
    else:
        course_form = EditCourseForm(instance=request.user, initial={'name': course.name,
                                                                     'description': course.description})

    if request.POST.get('add_word'):
        word_form = AddWordForm(request.POST, instance=request.user)
        word = Word()
        if word_form.is_valid():
            data = word_form.cleaned_data
            word.source_word = data['source_word']
            word.target_word = data['target_word']
            word.course = course
            try:
                word.save()
                context['word_success'] = "Word added successfully."
            except IntegrityError:
                context['word_error'] = "You have already such word. Choose a different one."

    else:
        word_form = AddWordForm(instance=request.user)

    if request.POST.get('remove_word'):
        word_remove_form = RemoveWordForm(request.POST)
        word_remove_form.fields['source_word'].queryset = Word.objects.filter(course=course)

        if word_remove_form.is_valid():
            data = word_remove_form.cleaned_data
            word = Word.objects.all().filter(course=course).filter(source_word=data['source_word'].source_word)
            word.delete()
            context['word_success_delete'] = "Word deleted successfully."

    else:
        word_remove_form = RemoveWordForm()
        word_remove_form.fields['source_word'].queryset = Word.objects.filter(course=course)

    context['course_form'] = course_form
    context['word_form'] = word_form
    context['word_remove_form'] = word_remove_form

    return render(request, 'course/edit_course.html', context)

