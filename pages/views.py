from django.shortcuts import render
from course.models import Course, Subscription, WordDetails


# Create your views here.
def home_page_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        subscribed_courses = Subscription.objects.filter(user=user)
        words = WordDetails.objects.all().filter(user=user, is_learnt=True)
        number_words_learned = len(words)
        context['subscriptions'] = subscribed_courses
        context['profile'] = user
        context['words_learned'] = number_words_learned
        return render(request, "dashboard.html", context)
    else:
        return render(request, "home_page.html")


def register_view(request):
    return render(request, "account/register.html")
