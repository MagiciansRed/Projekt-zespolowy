from django.shortcuts import render


# Create your views here.
def home_page_view(request):
    return render(request, "home_page.html")


def register_view(request):
    return render(request, "account/register.html")
