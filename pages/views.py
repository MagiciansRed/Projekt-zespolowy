from django.shortcuts import render
from course.models import Course, Subscription


# Create your views here.
def home_page_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        subscribed_courses = Subscription.objects.filter(user=user)
        context['subscriptions'] = subscribed_courses
        context['profile'] = user
        return render(request, "dashboard.html", context)
    else:
        return render(request, "home_page.html")


def register_view(request):
    return render(request, "account/register.html")
