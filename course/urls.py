from django.urls import path
from course.views import (
    course_list_view,
    detail_course_view,
    create_course_view,
    edit_course_view
)

app_name = 'course'

urlpatterns = [
    path('courses', course_list_view, name="courses"),
    path('create_course', create_course_view, name="create_course"),
    path('<slug>', detail_course_view, name="detail"),
    path('<slug>/edit_course', edit_course_view, name="edit_course"),
]
