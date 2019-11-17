from django.urls import path
from course.views import (
    course_list_view,
    detail_course_view,
)

app_name = 'course'

urlpatterns = [
    path('courses', course_list_view, name="courses"),
    path('<slug>', detail_course_view, name="detail"),
]
