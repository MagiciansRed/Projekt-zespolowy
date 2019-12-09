import random

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from course.models import Course, Subscription, Word, WordDetails
from course.forms import CourseCreateForm, EditCourseForm, AddWordForm, RemoveWordForm, LearnWordForm
from django.utils.text import slugify
from django.core.paginator import Paginator


# Create your views here.

@login_required
def course_list_view(request):
    context = {}
    courses = Course.objects.all()
    paginator = Paginator(courses, 3)

    page = request.GET.get('page')
    courses = paginator.get_page(page)
    context['courses'] = courses
    return render(request, 'course/courses.html', context)


@login_required
def detail_course_view(request, slug):
    context = {}
    course = get_object_or_404(Course, slug=slug)
    context['course_detail'] = course

    words = Word.objects.all().filter(course=course)
    context['words'] = words
    context['words_length'] = len(words)

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
                    remove_word_detail(words, current_user)
                    context['subscription_state'] = False
                break

        if request.POST.get('subscribe'):
            sub.course = course
            sub.user = current_user
            create_word_detail(words, current_user)
            sub.save()
            context['subscription_state'] = True
    else:
        context['subscription_state'] = False
        if request.POST.get('subscribe'):
            sub.course = course
            sub.user = current_user
            create_word_detail(words, current_user)
            sub.save()
            context['subscription_state'] = True

    return render(request, 'course/detail_course.html', context)


def create_word_detail(words, user):
    if isinstance(words, Word):
        detail = WordDetails()
        detail.word = words
        detail.user = user
        detail.value = 0
        detail.is_learnt = False
        detail.save()
    else:
        for word in words:
            detail = WordDetails()
            detail.word = word
            detail.user = user
            detail.value = 0
            detail.is_learnt = False
            detail.save()


def remove_word_detail(words, user):
    word_details = WordDetails.objects.all()
    for word in word_details:
        for w in words:
            if word.word == w and word.user == user:
                word.delete()


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
            if (data['image']):
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
            if data['source_language']:
                course.source_language = data['source_language']
            if data['target_language']:
                course.target_language = data['target_language']
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
        subscribers = Subscription.objects.all().filter(course=course)
        if word_form.is_valid():
            data = word_form.cleaned_data
            word.source_word = data['source_word']
            word.target_word = data['target_word']
            word.course = course
            try:
                print(word.source_word)
                print(word.target_word)
                word.save()
                for sub in subscribers:
                    create_word_detail(word, sub.user)
                context['word_success'] = "Word added successfully."
                #return HttpResponseRedirect("/course/" + course.slug + "/edit_course")
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


@login_required
def learn_course_view(request, slug):
    context = {}
    course = get_object_or_404(Course, slug=slug)
    context['course_detail'] = course
    all_words = Word.objects.all().filter(course=course)
    is_word_to_learn = False
    context['learn_all'] = ""

    current_user = request.user

    for w in all_words:
        if not checkIfLearnedWord(w, current_user):
            is_word_to_learn = True

    if is_word_to_learn:
        words = get_all_unlearned_words(all_words, current_user)
        word = random.choice(words)
        context['word'] = word
        word_details_query = WordDetails.objects.filter(word=word, user=current_user)
        word_details = word_details_query[0]

        if request.POST.get('next'):
            learn_word_form = LearnWordForm(request.POST)
            context['learn_form'] = learn_word_form

            has_seen_translation_checkbox = request.POST.get('has_seen_translation')
            if has_seen_translation_checkbox is None:
                word_details.value = word_details.value + 1

            if word_details.value >= 5:
                word_details.is_learnt = True
            else:
                word_details.is_learnt = False
            word_details.save()

        else:
            learn_word_form = LearnWordForm()
            context['learn_form'] = learn_word_form
    else:
        context['learn_all'] = "You have learned all the words."
        render(request, 'course/learn_course.html', context)

    return render(request, 'course/learn_course.html', context)


def checkIfLearnedWord(word, user):
    query = WordDetails.objects.filter(word=word, user=user)
    if len(query) > 0:
        word = query[0]
        return word.is_learnt
    else:
        return True


def get_all_unlearned_words(all_words, current_user):
    result = []
    for word in all_words:
        if not checkIfLearnedWord(word, current_user):
            result.append(word)

    return result
