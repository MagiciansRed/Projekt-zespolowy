from django.shortcuts import render


# Create your views here.
def home_page_view(request):
    user = request.user
    if user.is_authenticated:
        return render(request, "dashboard.html")
    else: 
        return render(request, "home_page.html")


def register_view(request):
    return render(request, "account/register.html")
